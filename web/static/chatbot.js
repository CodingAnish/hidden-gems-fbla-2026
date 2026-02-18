/**
 * Hidden Gems AI Chatbot
 * Frontend chat interface with Groq API backend
 * FBLA 2026
 */

// Global chat state
let chatState = {
  isOpen: false,
  isMinimized: false,
  conversationHistory: [],
  isLoading: false
};

// Initialize chat on page load
document.addEventListener('DOMContentLoaded', () => {
  initializeChat();
  loadWelcomeMessage();
});

/**
 * Initialize chat interface
 */
function initializeChat() {
  // Check if user is authenticated
  const chatButton = document.getElementById('chat-button');
  if (!chatButton) {
    console.error('Chat button not found in DOM');
    return;
  }

  // Setup event listeners
  document.getElementById('chat-input').addEventListener('keypress', handleChatKeypress);
  document.getElementById('send-button').addEventListener('click', sendChatMessage);

  // Show notification badge after 3 seconds
  setTimeout(() => {
    const badge = document.getElementById('chat-notification');
    if (badge) {
      badge.style.opacity = '1';
    }
  }, 3000);

  // Load conversation history from localStorage if exists
  const saved = localStorage.getItem('hiddenGemsChatHistory');
  if (saved) {
    try {
      chatState.conversationHistory = JSON.parse(saved);
    } catch (e) {
      console.error('Failed to load chat history:', e);
    }
  }
}

/**
 * Load welcome message from backend
 */
async function loadWelcomeMessage() {
  try {
    const response = await fetch('/api/chat/welcome', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error('Failed to load welcome message');
    }

    const data = await response.json();
    addMessageToChat(data.message, 'bot', data.quick_actions);
    
  } catch (error) {
    console.error('Welcome message error:', error);
    addMessageToChat(
      '👋 Welcome to Hidden Gems Assistant! I can help you find local businesses, get recommendations, and discover deals. What are you looking for?',
      'bot',
      ['Find Restaurants', 'Show Deals', 'Top Rated']
    );
  }
}

/**
 * Open the chat window
 */
function openChat() {
  const chatWindow = document.getElementById('chat-window');
  const chatButton = document.getElementById('chat-button');
  
  chatWindow.style.display = 'flex';
  chatButton.style.display = 'none';
  
  chatState.isOpen = true;
  chatState.isMinimized = false;
  
  // Focus input
  setTimeout(() => {
    document.getElementById('chat-input').focus();
  }, 100);
}

/**
 * Close the chat window
 */
function closeChat() {
  const chatWindow = document.getElementById('chat-window');
  const chatButton = document.getElementById('chat-button');
  
  chatWindow.style.display = 'none';
  chatButton.style.display = 'flex';
  
  chatState.isOpen = false;
  chatState.isMinimized = false;
}

/**
 * Minimize the chat window
 */
function minimizeChat() {
  closeChat();
}

/**
 * Handle Enter key in chat input
 */
function handleChatKeypress(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    sendChatMessage();
  }
}

/**
 * Send a chat message to the backend
 */
async function sendChatMessage() {
  if (chatState.isLoading) return;

  const input = document.getElementById('chat-input');
  const message = input.value.trim();

  if (!message) return;

  // Clear input
  input.value = '';
  input.focus();

  // Add user message to UI
  addMessageToChat(message, 'user');

  // Add to conversation history
  chatState.conversationHistory.push({
    role: 'user',
    content: message
  });

  // Show typing indicator
  showTypingIndicator();
  chatState.isLoading = true;

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: message,
        history: chatState.conversationHistory
      })
    });

    hideTypingIndicator();
    chatState.isLoading = false;

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Server error');
    }

    const data = await response.json();

    // Add bot response to UI
    addMessageToChat(
      data.response,
      'bot',
      data.quick_actions
    );

    // Add to conversation history
    chatState.conversationHistory.push({
      role: 'assistant',
      content: data.response
    });

    // Save to localStorage
    saveConversationHistory();

  } catch (error) {
    hideTypingIndicator();
    chatState.isLoading = false;
    
    console.error('Chat error:', error);
    
    const errorMessage = error.message === 'Failed to fetch'
      ? '⚠️ Connection error. Make sure you\'re logged in and try again.'
      : `⚠️ ${error.message}`;
    
    addMessageToChat(errorMessage, 'bot');
  }
}

/**
 * Handle quick action button click
 */
function handleQuickAction(action) {
  document.getElementById('chat-input').value = action;
  sendChatMessage();
}

/**
 * Add a message to the chat display
 */
function addMessageToChat(text, sender, actions = null) {
  const messagesContainer = document.getElementById('chat-messages');
  
  // Create message element
  const messageDiv = document.createElement('div');
  messageDiv.className = `chat-message ${sender}-message`;

  // Message bubble
  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';

  // Parse text with line breaks
  const lines = text.split('\n').filter(line => line.trim());
  
  if (lines.length === 0) {
    lines.push(text);
  }

  lines.forEach((line, index) => {
    if (line.trim()) {
      const p = document.createElement('p');
      p.textContent = line;
      bubble.appendChild(p);
    }
  });

  messageDiv.appendChild(bubble);

  // Add timestamp
  const time = document.createElement('span');
  time.className = 'message-time';
  time.textContent = new Date().toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  });
  messageDiv.appendChild(time);

  // Add quick action buttons if provided
  if (actions && actions.length > 0 && sender === 'bot') {
    const actionsDiv = document.createElement('div');
    actionsDiv.className = 'message-actions';

    actions.forEach(action => {
      const btn = document.createElement('button');
      btn.className = 'quick-action-btn';
      btn.textContent = action;
      btn.onclick = () => handleQuickAction(action);
      actionsDiv.appendChild(btn);
    });

    messageDiv.appendChild(actionsDiv);
  }

  messagesContainer.appendChild(messageDiv);

  // Auto-scroll to bottom
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
  const messagesContainer = document.getElementById('chat-messages');
  
  const typingDiv = document.createElement('div');
  typingDiv.className = 'chat-message bot-message typing-indicator';
  typingDiv.id = 'typing-indicator';

  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';

  // Create typing dots
  for (let i = 0; i < 3; i++) {
    const dot = document.createElement('span');
    dot.className = 'typing-dot';
    bubble.appendChild(dot);
  }

  typingDiv.appendChild(bubble);
  messagesContainer.appendChild(typingDiv);

  // Auto-scroll to bottom
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

/**
 * Hide typing indicator
 */
function hideTypingIndicator() {
  const indicator = document.getElementById('typing-indicator');
  if (indicator) {
    indicator.remove();
  }
}

/**
 * Save conversation history to localStorage
 */
function saveConversationHistory() {
  try {
    localStorage.setItem(
      'hiddenGemsChatHistory',
      JSON.stringify(chatState.conversationHistory)
    );
  } catch (e) {
    console.warn('Failed to save chat history:', e);
  }
}

/**
 * Clear conversation history
 */
function clearChatHistory() {
  chatState.conversationHistory = [];
  localStorage.removeItem('hiddenGemsChatHistory');
  
  const messagesContainer = document.getElementById('chat-messages');
  messagesContainer.innerHTML = '';
  
  loadWelcomeMessage();
}

/**
 * Export conversation as text
 */
function exportConversation() {
  let text = 'Hidden Gems Chat History\n';
  text += new Date().toLocaleString() + '\n';
  text += '='.repeat(50) + '\n\n';

  chatState.conversationHistory.forEach(msg => {
    const role = msg.role.toUpperCase();
    text += `${role}:\n${msg.content}\n\n`;
  });

  // Create download link
  const blob = new Blob([text], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `hidden-gems-chat-${Date.now()}.txt`;
  a.click();
  URL.revokeObjectURL(url);
}
