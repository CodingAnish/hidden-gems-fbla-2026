# AI CHATBOT SETUP GUIDE - Hidden Gems FBLA 2026

## 🤖 You have 3 FREE options for the chatbot:

### OPTION 1: GROQ API ⭐ **RECOMMENDED** (Fastest, Free, Best for Demos)

**Why choose this:**
- ✅ 100% FREE forever (no credit card needed)
- ✅ INSTANT responses (faster than ChatGPT)
- ✅ 30 requests per minute, 14,400 per day
- ✅ Perfect for FBLA competition demos
- ✅ Uses Llama-3.3-70b (very smart AI)

**Setup (5 minutes):**
1. Go to https://console.groq.com
2. Click "Sign Up" (use Google/GitHub or email)
3. After login, click "API Keys" in sidebar
4. Click "Create API Key"
5. Name it "Hidden Gems Bot"
6. Copy the key (starts with `gsk_...`)
7. Open `config.py` and paste it:
   ```python
   GROQ_API_KEY = "gsk_your_key_here"
   ```
8. Done! Restart your Flask app

---

### OPTION 2: HUGGING FACE (FREE Backup - Good Quality)

**Why choose this:**
- ✅ 100% FREE forever
- ✅ 1,000 requests per day
- ✅ No credit card needed
- ⚠️ First response takes 20 seconds (model wakes up)
- ⚠️ Better for production than live demos

**Setup (5 minutes):**
1. Go to https://huggingface.co
2. Click "Sign Up" 
3. After login, click your profile picture → Settings
4. Click "Access Tokens" in sidebar
5. Click "New token"
6. Name: "Hidden Gems", Role: "Read"
7. Click "Generate"
8. Copy the token (starts with `hf_...`)
9. Open `config.py` and paste it:
   ```python
   HUGGINGFACE_API_KEY = "hf_your_key_here"
   ```
10. Done! Restart your Flask app

---

### OPTION 3: RULE-BASED (NO API NEEDED - Always Works)

**Why choose this:**
- ✅ 100% FREE (no API at all)
- ✅ Works offline
- ✅ Instant responses
- ✅ No setup needed
- ⚠️ Less conversational than AI options

**Setup:**
- Nothing! It's already built-in as the fallback
- If no API keys are set, chatbot automatically uses rule-based mode
- Still scores well on "intelligent features" for FBLA

---

## 🎯 Which One Should I Use?

**For FBLA Competition Demo:**
→ **Use GROQ** (best demo experience)

**For Development/Testing:**
→ **No API needed** (rule-based works great)

**For Production:**
→ **Groq or Hugging Face** (both free forever)

---

## 🚀 Priority Order (Automatic Fallback)

The chatbot automatically tries in this order:
1. **Groq API** (if key is set) - Fastest
2. **Hugging Face** (if Groq fails) - Backup
3. **Rule-Based** (if no APIs work) - Always works

---

## 📊 Comparison Table

| Feature          | Groq ⭐      | Hugging Face | Rule-Based |
|------------------|-------------|--------------|------------|
| Cost             | FREE        | FREE         | FREE       |
| Speed            | Instant     | 20s first    | Instant    |
| Setup Time       | 5 min       | 5 min        | 0 min      |
| Quality          | Excellent   | Very Good    | Good       |
| Rate Limit       | 30/min      | 1000/day     | Unlimited  |
| Best For         | Demos       | Production   | Offline    |
| Credit Card?     | NO          | NO           | NO         |

---

## 🎓 For Your FBLA Presentation

**When judges ask "How does the chatbot work?":**

"We implemented an intelligent AI chatbot using Groq's free API, which provides natural language understanding powered by Llama-3.3-70b. The system intelligently detects user intent, searches our Richmond business database, and provides personalized recommendations. As a backup, we also built a rule-based fallback system, ensuring the chatbot always works even without internet connectivity."

**Key points to mention:**
- ✅ Uses industry-standard AI (Llama-3.3-70b)
- ✅ Intent recognition and entity extraction
- ✅ Context-aware conversations
- ✅ Graceful error handling with fallback system
- ✅ Fully functional without requiring paid services

---

## 🔧 Testing Your Setup

1. Make sure your Flask app is running
2. Open http://127.0.0.1:5000 in your browser
3. Click the chat button (🤖 bottom-right)
4. Type: "find restaurants"
5. If you see a response, it's working! ✅

**Response speed indicates which API is being used:**
- **Instant (<1s)**: Groq API or Rule-Based ✅
- **20s then fast**: Hugging Face (first request only)
- **Structured list**: Rule-Based fallback

---

## 📝 Common Issues

**"I don't see any response"**
- Check that Flask app is running
- Check browser console for errors
- Try refreshing the page

**"Chatbot says 'I'm currently unavailable'"**
- Check your API key is correctly pasted in config.py
- Make sure there are no extra spaces
- Verify the key starts with `gsk_` (Groq) or `hf_` (Hugging Face)

**"Response takes forever"**
- If using Hugging Face, first response takes 20s (model waking up)
- After that, responses are fast
- Consider switching to Groq for faster demo experience

---

## 💡 Pro Tips

1. **For FBLA Demo**: Set up Groq API for best impression
2. **Test Before Presentation**: Make a few test queries the day before
3. **Have Backup**: Even with no API, rule-based mode always works
4. **Show Off**: During demo, show comparison, deals, and recommendations
5. **Explain Fallback**: Mention the multi-tier fallback system (shows advanced thinking)

---

## 🎉 You're Ready!

Your chatbot is already configured with a smart fallback system. Just add one (or both) free API keys to make it even smarter!

**Recommended setup for FBLA:**
```python
# In config.py:
GROQ_API_KEY = "your_groq_key_here"  # Best for demos
HUGGINGFACE_API_KEY = ""  # Optional backup
```

That's it! Good luck with your FBLA competition! 🏆
