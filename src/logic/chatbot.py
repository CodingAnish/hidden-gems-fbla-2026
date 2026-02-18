"""
AI Chatbot using FREE APIs (Cohere, Groq, Hugging Face) with rule-based fallback.
FBLA 2026 Hidden Gems
"""
import os
import json
import urllib.request
import urllib.error
from src.database import queries

# Get API keys from config
def get_api_keys():
    """Get API keys from config or environment."""
    try:
        import config
        groq_key = getattr(config, "GROQ_API_KEY", None) or os.environ.get("GROQ_API_KEY")
        hf_key = getattr(config, "HUGGINGFACE_API_KEY", None) or os.environ.get("HUGGINGFACE_API_KEY")
        cohere_key = getattr(config, "COHERE_API_KEY", None) or os.environ.get("COHERE_API_KEY")
    except ImportError:
        groq_key = os.environ.get("GROQ_API_KEY")
        hf_key = os.environ.get("HUGGINGFACE_API_KEY")
        cohere_key = os.environ.get("COHERE_API_KEY")
    
    return groq_key, hf_key, cohere_key


def get_business_context():
    """Get formatted business data for Claude's context."""
    businesses = queries.get_all_businesses()
    categories = queries.get_categories()
    
    # Format business data concisely
    business_list = []
    for b in businesses[:50]:  # Limit to 50 to avoid token limits
        business_list.append({
            "name": b.get("name"),
            "category": b.get("category"),
            "rating": b.get("average_rating"),
            "reviews": b.get("total_reviews"),
            "address": b.get("address", "")[:50]  # Truncate long addresses
        })
    
    context = f"""You are an AI assistant for Hidden Gems, a local business directory in Richmond, Virginia.

AVAILABLE CATEGORIES: {', '.join(categories)}

BUSINESS DATA (Top 50):
{business_list}

YOUR ROLE:
- Help users discover and learn about local Richmond businesses
- Answer questions about businesses, categories, ratings, and deals
- Make personalized recommendations based on user preferences
- Be friendly, conversational, and concise
- Use emojis sparingly (1-2 per response)
- Always end with a question or call-to-action
- If you can't find specific information, suggest alternatives

RESPONSE FORMAT:
- Keep responses under 150 words
- Show maximum 3-5 businesses per response
- Use bullet points for lists
- Include ratings as stars (★)
- Be enthusiastic about local businesses

SEARCH CAPABILITIES:
When users search, filter by:
- Category (Food, Retail, Services, Entertainment, Health and Wellness)
- Rating (show highest rated first)
- Reviews (mention review counts)
- Deals (if they ask about discounts)

Remember: You're helping people support local Richmond businesses!"""
    
    return context


def detect_intent(message):
    """Detect user intent from message."""
    message_lower = message.lower()
    
    # Search intent
    if any(word in message_lower for word in ["find", "search", "looking for", "show me", "where", "need"]):
        return "search"
    
    # Recommendation intent
    if any(word in message_lower for word in ["recommend", "suggest", "best", "top", "popular", "favorite"]):
        return "recommendation"
    
    # Deal intent
    if any(word in message_lower for word in ["deal", "discount", "coupon", "promo", "special", "offer"]):
        return "deals"
    
    # Comparison intent
    if any(word in message_lower for word in ["compare", "vs", "versus", "difference", "which is better"]):
        return "comparison"
    
    # Help intent
    if any(word in message_lower for word in ["help", "how", "what is", "guide", "tutorial"]):
        return "help"
    
    # Greeting
    if any(word in message_lower for word in ["hi", "hello", "hey", "good morning", "good afternoon"]):
        return "greeting"
    
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
        for msg in messages[-10:]:  # Last 10 messages for context
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
            temperature=0.7,
            max_tokens=400
        )
        
        return response.text
        
    except ImportError:
        raise Exception("cohere not installed. Run: pip install cohere")
    except Exception as e:
        raise Exception(f"Cohere API error: {str(e)}")


def call_groq_api(messages, user_message, system_prompt, api_key):
    """Call Groq API (FREE, FAST, BACKUP OPTION)."""
    conversation = [{"role": "system", "content": system_prompt}]
    conversation.extend(messages[-10:])  # Last 5 exchanges
    conversation.append({"role": "user", "content": user_message})
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": conversation,
        "temperature": 0.7,
        "max_tokens": 400
    }
    
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(data).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    
    with urllib.request.urlopen(req, timeout=10) as response:
        result = json.loads(response.read().decode())
        return result["choices"][0]["message"]["content"]


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
        
        # Add conversation history (last 10 messages)
        for msg in messages[-10:]:
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
                    max_tokens=400,
                    temperature=0.7,
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
    message_lower = user_message.lower()
    
    # Intent 1: Greeting
    if any(word in message_lower for word in ["hi", "hello", "hey", "good morning", "good afternoon"]):
        return ("👋 Hi there! Welcome to Hidden Gems! I can help you:\n\n• Find local businesses in Richmond\n• Show current deals and promotions\n• Get recommendations based on ratings\n• Answer questions about businesses\n\nWhat would you like to explore?",
                ["Find Restaurants", "Show Deals", "Top Rated"])
    
    # Intent 2: Deals
    if any(word in message_lower for word in ["deal", "discount", "coupon", "promo", "special", "offer"]):
        deals_businesses = [b for b in queries.get_all_businesses() if queries.get_deals_by_business(b.get("id"))]
        if deals_businesses:
            response = "🎁 Here are today's best deals:\n\n"
            for b in deals_businesses[:3]:
                deals = queries.get_deals_by_business(b.get("id"))
                response += f"• {b.get('name')} ({b.get('category')})\n"
                for d in deals:
                    response += f"  {d.get('description')}\n"
                response += "\n"
            return (response + "Want to see more details?", ["View All Deals", "Browse Directory"])
        else:
            return ("I don't have any deals listed right now, but check out our top-rated businesses!",
                   ["Top Rated", "Browse Directory"])
    
    # Intent 3: Search/Find
    if any(word in message_lower for word in ["find", "search", "looking for", "show me", "where", "need"]):
        # Try to detect category
        categories = queries.get_categories()
        detected_cat = None
        for cat in categories:
            if cat.lower() in message_lower:
                detected_cat = cat
                break
        
        if detected_cat:
            businesses = queries.get_businesses_for_directory(category=detected_cat, sort_by="rating_high")[:3]
            if businesses:
                response = f"I found {len(businesses)} great {detected_cat} businesses:\n\n"
                for b in businesses:
                    response += f"⭐ {b.get('name')} - {b.get('average_rating')}★ ({b.get('total_reviews')} reviews)\n"
                    response += f"   {b.get('category')}\n\n"
                return (response + "Would you like more details?", ["Show More", "View Deals", "Different Category"])
        
        # Ask for category
        return ("I can help you find businesses! What category interests you?",
               ["Food", "Retail", "Services", "Health & Wellness"])
    
    # Intent 4: Best/Top/Recommend
    if any(word in message_lower for word in ["best", "top", "recommend", "popular", "favorite", "highest"]):
        businesses = sorted(queries.get_all_businesses(), key=lambda x: x.get("average_rating", 0), reverse=True)[:3]
        response = "🌟 Here are Richmond's top-rated businesses:\n\n"
        for b in businesses:
            response += f"⭐ {b.get('name')} - {b.get('average_rating')}★ ({b.get('total_reviews')} reviews)\n"
            response += f"   {b.get('category')}\n\n"
        return (response + "Want to know more about any of these?", ["View Details", "Show Deals", "Different Category"])
    
    # Intent 5: Help
    if any(word in message_lower for word in ["help", "how", "what can you do", "commands"]):
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
    
    # Try Cohere first (MOST RELIABLE - fast, no cold starts)
    if cohere_key:
        try:
            response_text = call_cohere_api(messages, user_message, system_prompt, cohere_key)
            quick_actions = get_quick_actions(intent)
            return (response_text, intent, quick_actions)
        except Exception as e:
            print(f"Cohere API error: {e}")
    
    # Try Groq second (fast and free)
    if groq_key:
        try:
            response_text = call_groq_api(messages, user_message, system_prompt, groq_key)
            quick_actions = get_quick_actions(intent)
            return (response_text, intent, quick_actions)
        except Exception as e:
            print(f"Groq API error: {e}")
    
    # Try Hugging Face as backup
    if hf_key:
        try:
            response_text = call_huggingface_api(messages, user_message, system_prompt, hf_key)
            quick_actions = get_quick_actions(intent)
            return (response_text, intent, quick_actions)
        except Exception as e:
            print(f"Hugging Face API error: {e}")
    
    # Fallback to rule-based (always works, no API needed)
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
