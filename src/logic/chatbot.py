"""
AI Chatbot Integration with Multiple AI Providers

This module provides conversational AI capabilities using multiple free API options:
- Groq API (primary - fast LLM inference)
- Hugging Face (secondary - if Groq unavailable)
- Rule-based fallback (if all APIs unavailable)

Helps users discover local Richmond businesses through natural conversation.
FBLA 2026 Hidden Gems
"""
import os
import json
import urllib.request
import urllib.error
from src.database import queries

# ============================================
# API CONFIGURATION
# ============================================

def get_api_keys():
    """
    Retrieve API keys from environment variables or config file.
    
    Attempts to load from config module first, then falls back to environment variables.
    This allows flexible configuration for development and production.
    
    Returns:
        tuple: (groq_key, huggingface_key, cohere_key)
    """
    try:
        # Try to load from config module (development)
        import config
        groq_api_key = getattr(config, "GROQ_API_KEY", None) or os.environ.get("GROQ_API_KEY")
        huggingface_api_key = getattr(config, "HUGGINGFACE_API_KEY", None) or os.environ.get("HUGGINGFACE_API_KEY")
        cohere_api_key = getattr(config, "COHERE_API_KEY", None) or os.environ.get("COHERE_API_KEY")
    except ImportError:
        # Fallback to environment variables only
        groq_api_key = os.environ.get("GROQ_API_KEY")
        huggingface_api_key = os.environ.get("HUGGINGFACE_API_KEY")
        cohere_api_key = os.environ.get("COHERE_API_KEY")
    
    return groq_api_key, huggingface_api_key, cohere_api_key


def get_business_context():
    """
    Build system context for AI chatbot containing business knowledge.
    
    Creates a formatted string with:
    - Available business categories
    - Top 50 businesses with key details (name, category, rating, reviews)
    - Role description and response guidelines
    - Search capabilities and formatting instructions
    
    This context is passed to the AI model to help it provide relevant recommendations.
    
    Returns:
        str: System context prompt for AI model
    """
    # Fetch all businesses from database
    all_businesses = queries.get_all_businesses()
    available_categories = queries.get_categories()
    
    # Format business data concisely (limit to 10 for speed)
    formatted_businesses = []
    for business in all_businesses[:10]:
        formatted_businesses.append({
            "name": business.get("name"),
            "category": business.get("category"),
            "rating": business.get("average_rating"),
            "review_count": business.get("total_reviews")
        })
    
    # Build MINIMAL system prompt for speed
    system_context = f"""You are Hidden Gems AI for Richmond, VA businesses.
Categories: {', '.join(available_categories)}
Businesses: {formatted_businesses}
Be brief, friendly, and suggest 2-3 businesses per response. Keep it under 100 words."""
    
    return system_context


def detect_intent(user_message):
    """
    Determine the primary intent of the user's message.
    
    This helps tailor responses and search parameters for better recommendations.
    
    Args:
        user_message (str): The user's input message
    
    Returns:
        str: One of 'search', 'recommendation', 'deals', 'comparison', 'help', or 'general'
    """
    message_normalized = user_message.lower()
    
    # Detect search intent (user looking for specific business or category)
    search_keywords = ["find", "search", "looking for", "show me", "where can i", "need"]
    if any(keyword in message_normalized for keyword in search_keywords):
        return "search"
    
    # Detect recommendation intent (user wants suggestions)
    recommendation_keywords = ["recommend", "suggest", "best", "top", "popular", "favorite", "what should i"]
    if any(keyword in message_normalized for keyword in recommendation_keywords):
        return "recommendation"
    
    # Detect deals intent (user looking for discounts/offers)
    deals_keywords = ["deal", "discount", "coupon", "promo", "promotion", "special", "offer", "sale"]
    if any(keyword in message_normalized for keyword in deals_keywords):
        return "deals"
    
    # Detect comparison intent (user comparing businesses)
    comparison_keywords = ["compare", "vs", "versus", "difference", "which is better", "better than"]
    if any(keyword in message_normalized for keyword in comparison_keywords):
        return "comparison"
    
    # Detect help/info intent (user asking for guidance)
    help_keywords = ["help", "how", "what is", "guide", "tutorial", "how do i", "how can i"]
    if any(keyword in message_normalized for keyword in help_keywords):
        return "help"
    
    # Default to general conversation
    return "general"


def get_quick_actions(intent):
    """Get quick action buttons based on intent."""
    actions = {
        "greeting": ["Find Restaurants", "Show Deals", "Top Rated", "Help"],
        "search": ["Show More", "Filter by Rating", "View Deals", "Compare Options"],
        "recommendation": ["See More", "Different Category", "View Details"],
        "deals": ["All Deals", "By Category", "Expiring Soon"],
        "help": ["Search Businesses", "Save Favorites", "Write Reviews"],
        "general": ["Find Restaurants", "Browse Categories", "Show Deals"]
    }
    return actions.get(intent, actions["general"])


def search_businesses(query, category=None, min_rating=None):
    """Search businesses based on query parameters."""
    if category:
        businesses = queries.get_businesses_for_directory(category=category)
    else:
        businesses = queries.get_all_businesses()
    
    # Filter by rating if specified
    if min_rating:
        businesses = [b for b in businesses if b.get("average_rating", 0) >= min_rating]
    
    # Sort by rating
    businesses.sort(key=lambda x: x.get("average_rating", 0), reverse=True)
    
    return businesses[:10]  # Return top 10


def format_business_for_display(business):
    """Format a single business for chatbot display."""
    rating = business.get("average_rating", 0)
    reviews = business.get("total_reviews", 0)
    category = business.get("category", "Business")
    
    stars = "★" * int(rating) if rating > 0 else "☆☆☆☆☆"
    
    return f"{business.get('name')} - {stars} ({reviews} reviews)\n   {category}"


def call_cohere_api(messages, user_message, system_prompt, api_key):
    """Call Cohere API (MOST RELIABLE, FASTEST FREE OPTION)."""
    try:
        import cohere
        
        # Initialize Cohere client
        co = cohere.Client(api_key=api_key)
        
        # Build message history for context
        # Cohere expects roles: "User", "Chatbot", "System", "Tool"
        conversation_history = []
        for msg in messages[-3:]:  # Last 3 messages only for speed
            # Map common role names to Cohere format
            role = msg["role"]
            if role == "user":
                role = "User"
            elif role == "assistant":
                role = "Chatbot"
            elif role == "system":
                role = "System"
            
            conversation_history.append({
                "role": role,
                "message": msg["content"]
            })
        
        # Call Cohere chat API
        response = co.chat(
            message=user_message,
            model="command-r-08-2024",
            preamble=system_prompt,
            chat_history=conversation_history,
            temperature=0.5,  # Lower for speed
            max_tokens=300  # Reduced
        )
        
        return response.text
        
    except ImportError:
        raise Exception("cohere not installed. Run: pip install cohere")
    except Exception as e:
        raise Exception(f"Cohere API error: {str(e)}")


def call_groq_api(messages, user_message, system_prompt, api_key):
    """Call Groq API (FREE, FAST, BACKUP OPTION)."""
    try:
        from groq import Groq
        
        client = Groq(api_key=api_key)
        
        # Build conversation
        conversation = [{"role": "system", "content": system_prompt}]
        conversation.extend(messages[-3:])  # Only last 3 messages for speed
        conversation.append({"role": "user", "content": user_message})
        
        # Call Groq API with fastest model
        response = client.chat.completions.create(
            model="llama2-70b-4096",  # Faster than mixtral
            messages=conversation,
            temperature=0.5,  # Lower for faster inference
            max_tokens=300  # Further reduced
        )
        
        return response.choices[0].message.content
        
    except ImportError:
        raise Exception("groq not installed. Run: pip install groq")
    except Exception as e:
        raise Exception(f"Groq API error: {str(e)}")


def call_huggingface_api(messages, user_message, system_prompt, api_key):
    """Call Hugging Face Inference API (FREE backup option)."""
    try:
        from huggingface_hub import InferenceClient
        
        # Initialize HF client with the API key
        client = InferenceClient(api_key=api_key)
        
        # Prepare messages in OpenAI format
        formatted_messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history (last 3 messages for speed)
        for msg in messages[-3:]:
            formatted_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current user message
        formatted_messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Try multiple models in order of preference
        models = [
            "mistralai/Mistral-7B-Instruct-v0.2",
            "HuggingFaceH4/zephyr-7b-beta",
            "NousResearch/Nous-Hermes-2-Mistral-7B-DPO"
        ]
        
        for model in models:
            try:
                response = client.chat_completion(
                    model=model,
                    messages=formatted_messages,
                    max_tokens=300,  # Reduced for speed
                    temperature=0.5,  # Lower temp for faster inference
                    top_p=0.9
                )
                
                # Extract response text
                if response and hasattr(response, 'choices') and len(response.choices) > 0:
                    return response.choices[0].message.content
            except Exception as model_err:
                print(f"Model {model} failed: {str(model_err)[:100]}")
                continue
        
        return "I'm having trouble formulating a response. Please try again."
        
    except ImportError:
        raise Exception("huggingface_hub not installed. Run: pip install huggingface_hub")
    except Exception as e:
        raise Exception(f"Hugging Face API error: {str(e)}")


def rule_based_response(user_message):
    """Rule-based chatbot fallback (NO API NEEDED)."""
    normalized_message = user_message.lower()
    
    # Intent 1: Greeting
    if any(word in normalized_message for word in ["hi", "hello", "hey", "good morning", "good afternoon"]):
        return ("👋 Hi there! Welcome to Hidden Gems! I can help you:\n\n• Find local businesses in Richmond\n• Show current deals and promotions\n• Get recommendations based on ratings\n• Answer questions about businesses\n\nWhat would you like to explore?",
                ["Find Restaurants", "Show Deals", "Top Rated"])
    
    # Intent 2: Deals
    if any(word in normalized_message for word in ["deal", "discount", "coupon", "promo", "special", "offer"]):
        deals_businesses = [business for business in queries.get_all_businesses() if queries.get_deals_by_business(business.get("id"))]
        if deals_businesses:
            response = "🎁 Here are today's best deals:\n\n"
            for business in deals_businesses[:3]:
                deals = queries.get_deals_by_business(business.get("id"))
                response += f"• {business.get('name')} ({business.get('category')})\n"
                for deal in deals:
                    response += f"  {deal.get('description')}\n"
                response += "\n"
            return (response + "Want to see more details?", ["View All Deals", "Browse Directory"])
        else:
            return ("I don't have any deals listed right now, but check out our top-rated businesses!",
                   ["Top Rated", "Browse Directory"])
    
    # Intent 3: Search/Find
    if any(word in normalized_message for word in ["find", "search", "looking for", "show me", "where", "need"]):
        # Try to detect category
        categories = queries.get_categories()
        detected_cat = None
        for cat in categories:
            if cat.lower() in normalized_message:
                detected_cat = cat
                break
        
        if detected_cat:
            businesses = queries.get_businesses_for_directory(category=detected_cat, sort_by="rating_high")[:3]
            if businesses:
                response = f"I found {len(businesses)} great {detected_cat} businesses:\n\n"
                for business in businesses:
                    response += f"⭐ {business.get('name')} - {business.get('average_rating')}★ ({business.get('total_reviews')} reviews)\n"
                    response += f"   {business.get('category')}\n\n"
                return (response + "Would you like more details?", ["Show More", "View Deals", "Different Category"])
        
        # Ask for category
        return ("I can help you find businesses! What category interests you?",
               ["Food", "Retail", "Services", "Health & Wellness"])
    
    # Intent 4: Best/Top/Recommend
    if any(word in normalized_message for word in ["best", "top", "recommend", "popular", "favorite", "highest"]):
        businesses = sorted(queries.get_all_businesses(), key=lambda x: x.get("average_rating", 0), reverse=True)[:3]
        response = "🌟 Here are Richmond's top-rated businesses:\n\n"
        for business in businesses:
            response += f"⭐ {business.get('name')} - {business.get('average_rating')}★ ({business.get('total_reviews')} reviews)\n"
            response += f"   {business.get('category')}\n\n"
        return (response + "Want to know more about any of these?", ["View Details", "Show Deals", "Different Category"])
    
    # Intent 5: Help
    if any(word in normalized_message for word in ["help", "how", "what can you do", "commands"]):
        return ("I can help you with:\n\n🔍 Finding businesses by category\n⭐ Getting top-rated recommendations\n🎁 Showing current deals\n📍 Business details and information\n\nJust ask me what you're looking for!",
               ["Find Restaurants", "Show Deals", "Top Rated"])
    
    # Default fallback
    return ("I can help you discover local Richmond businesses! Try asking:\n\n• 'Find restaurants'\n• 'Show me deals'\n• 'What's the best rated?'\n• 'Help'\n\nWhat would you like to know?",
           ["Find Restaurants", "Show Deals", "Top Rated", "Help"])


def chat_with_ai(messages, user_message):
    """
    Send conversation to AI and get response. Tries multiple FREE options.
    
    Order of priority:
    1. Cohere API (most reliable, fastest, no cold starts)
    2. Groq API (very fast, free)
    3. Hugging Face (free, good quality)
    4. Rule-based fallback (always works)
    
    Args:
        messages: List of previous messages [{"role": "user"|"assistant", "content": "..."}]
        user_message: Current user message
        
    Returns:
        (response_text, intent, quick_actions) tuple
    """
    # Detect intent
    intent = detect_intent(user_message)
    
    # Get business context
    system_prompt = get_business_context()
    
    # Get API keys
    groq_key, hf_key, cohere_key = get_api_keys()
    
    # DEBUG: Log which keys are available
    print(f"[DEBUG] API Keys available - Cohere: {bool(cohere_key)}, Groq: {bool(groq_key)}, HF: {bool(hf_key)}")
    
    # Try Cohere first (MOST RELIABLE - fast, no cold starts)
    if cohere_key:
        try:
            response_text = call_cohere_api(messages, user_message, system_prompt, cohere_key)
            quick_actions = get_quick_actions(intent)
            print(f"[DEBUG] Successfully used Cohere API")
            return (response_text, intent, quick_actions)
        except Exception as e:
            print(f"[ERROR] Cohere API failed: {e}")
    
    # Try Groq second (fast and free)
    if groq_key:
        try:
            response_text = call_groq_api(messages, user_message, system_prompt, groq_key)
            quick_actions = get_quick_actions(intent)
            print(f"[DEBUG] Successfully used Groq API")
            return (response_text, intent, quick_actions)
        except Exception as e:
            print(f"[ERROR] Groq API failed: {e}")
    else:
        print(f"[DEBUG] GROQ_API_KEY is not set or empty!")
    
    # Try Hugging Face as backup
    if hf_key:
        try:
            response_text = call_huggingface_api(messages, user_message, system_prompt, hf_key)
            quick_actions = get_quick_actions(intent)
            print(f"[DEBUG] Successfully used HuggingFace API")
            return (response_text, intent, quick_actions)
        except Exception as e:
            print(f"[ERROR] HuggingFace API failed: {e}")
    
    # Fallback to rule-based (always works, no API needed)
    print(f"[DEBUG] Falling back to rule-based response")
    response_text, quick_actions = rule_based_response(user_message)
    return (response_text, intent, quick_actions)


def get_welcome_message():
    """Get the initial welcome message when chat opens."""
    return {
        "message": """👋 Hi! I'm the Hidden Gems Assistant!

I can help you:
• Find local businesses in Richmond, VA
• Get personalized recommendations
• Compare options and ratings
• Discover deals and promotions
• Answer questions about businesses

What would you like to explore today?""",
        "quick_actions": ["Find Restaurants", "Show Deals", "Top Rated Businesses", "Help Me"]
    }
