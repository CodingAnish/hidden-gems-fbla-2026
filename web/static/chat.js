// AI Chatbot JavaScript - Left Slide-Out Panel
console.log('🤖 Chat.js loaded successfully!');

class ChatBot {
    constructor() {
        this.conversationHistory = [];
        this.isOpen = false;
        this.isTyping = false;
        console.log('🤖 ChatBot initializing...');
        this.init();
    }

    init() {
        this.createChatUI();
        this.attachEventListeners();
    }

    createChatUI() {
        // Create overlay
        const overlay = document.createElement('div');
        overlay.className = 'chat-overlay';
        overlay.id = 'chatOverlay';
        document.body.appendChild(overlay);

        // Create chat tab (sticks out from left)
        const chatTab = document.createElement('div');
        chatTab.className = 'chat-tab';
        chatTab.id = 'chatTab';
        chatTab.innerHTML = `
            <div class="chat-tab-icon">🤖</div>
            AI ASSISTANT
        `;
        document.body.appendChild(chatTab);

        // Create chat panel
        const chatPanel = document.createElement('div');
        chatPanel.className = 'chat-panel';
        chatPanel.id = 'chatPanel';
        chatPanel.innerHTML = `
            <div class="chat-header">
                <div class="chat-header-left">
                    <div class="chat-avatar">🤖</div>
                    <div class="chat-header-info">
                        <h3>Hidden Gems Assistant</h3>
                        <div class="chat-status">
                            <span class="status-dot"></span>
                            <span>Online</span>
                        </div>
                    </div>
                </div>
                <button class="chat-close-btn" id="closeChat" aria-label="Close chat">×</button>
            </div>
            <div class="chat-messages" id="chatMessages"></div>
            <div class="chat-input-area">
                <input 
                    type="text" 
                    class="chat-input" 
                    id="chatInput" 
                    placeholder="Ask me anything about local businesses..."
                    maxlength="500"
                />
                <button class="chat-send-btn" id="chatSendBtn" aria-label="Send message">
                    <span>➤</span>
                </button>
            </div>
        `;
        document.body.appendChild(chatPanel);
    }

    attachEventListeners() {
        // Tab click - open chat
        document.getElementById('chatTab').addEventListener('click', () => {
            this.openChat();
        });

        // Overlay click - close chat
        document.getElementById('chatOverlay').addEventListener('click', () => {
            this.closeChat();
        });

        // Close button
        document.getElementById('closeChat').addEventListener('click', () => {
            this.closeChat();
        });

        // Input handling
        const input = document.getElementById('chatInput');
        const sendBtn = document.getElementById('chatSendBtn');

        input.addEventListener('input', () => {
            if (input.value.trim().length > 0) {
                sendBtn.classList.add('active');
            } else {
                sendBtn.classList.remove('active');
            }
        });

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && input.value.trim().length > 0) {
                this.sendMessage(input.value.trim());
            }
        });

        sendBtn.addEventListener('click', () => {
            if (input.value.trim().length > 0) {
                this.sendMessage(input.value.trim());
            }
        });
    }

    async openChat() {
        if (this.isOpen) return;
        
        this.isOpen = true;
        document.getElementById('chatPanel').classList.add('open');
        document.getElementById('chatOverlay').classList.add('visible');
        
        // Load welcome message if conversation is empty
        if (this.conversationHistory.length === 0) {
            await this.loadWelcomeMessage();
        }
        
        // Focus input
        setTimeout(() => {
            document.getElementById('chatInput').focus();
        }, 400);
    }

    closeChat() {
        this.isOpen = false;
        document.getElementById('chatPanel').classList.remove('open');
        document.getElementById('chatOverlay').classList.remove('visible');
    }

    async loadWelcomeMessage() {
        try {
            const response = await fetch('/api/chat/welcome');
            const data = await response.json();
            
            if (data.message) {
                this.addBotMessage(data.message, data.quick_actions || []);
            }
        } catch (error) {
            console.error('Error loading welcome message:', error);
            this.addBotMessage(
                "👋 Hi! I'm the Hidden Gems AI Assistant!\n\nI can help you:\n• Find local businesses\n• Show deals and promotions\n• Get personalized recommendations\n• Answer questions about Richmond businesses\n\nWhat would you like to explore?",
                ["Find Restaurants", "Show Deals", "Top Rated"]
            );
        }
    }

    async sendMessage(message) {
        // Clear input
        const input = document.getElementById('chatInput');
        input.value = '';
        document.getElementById('chatSendBtn').classList.remove('active');

        // Add user message to UI
        this.addUserMessage(message);

        // Add to conversation history
        this.conversationHistory.push({
            role: "user",
            content: message
        });

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Send to backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    history: this.conversationHistory.slice(-20)
                })
            });

            const data = await response.json();

            // Remove typing indicator
            this.removeTypingIndicator();

            if (data.response) {
                // Add bot response
                this.addBotMessage(data.response, data.quick_actions || []);
                
                // Add to conversation history
                this.conversationHistory.push({
                    role: "assistant",
                    content: data.response
                });
            } else if (data.error) {
                this.addBotMessage(
                    `❌ Error: ${data.error}`,
                    ["Try Again", "Browse Directory"]
                );
            }
        } catch (error) {
            this.removeTypingIndicator();
            console.error('Chat error:', error);
            this.addBotMessage(
                "❌ I'm having trouble connecting. Please check your internet connection and try again!",
                ["Try Again", "Browse Directory"]
            );
        }
    }

    addUserMessage(text) {
        const messagesContainer = document.getElementById('chatMessages');
        const timestamp = this.getTimestamp();

        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message user';
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-bubble">${this.escapeHtml(text)}</div>
                <div class="message-timestamp">${timestamp}</div>
            </div>
        `;

        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    addBotMessage(text, quickActions = []) {
        const messagesContainer = document.getElementById('chatMessages');
        const timestamp = this.getTimestamp();

        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message bot';
        
        // Format text (preserve line breaks)
        const formattedText = text.replace(/\n/g, '<br>');
        
        let quickActionsHtml = '';
        if (quickActions.length > 0) {
            quickActionsHtml = '<div class="quick-actions">';
            quickActions.forEach(action => {
                quickActionsHtml += `<button class="quick-action-btn" data-action="${this.escapeHtml(action)}">${this.escapeHtml(action)}</button>`;
            });
            quickActionsHtml += '</div>';
        }

        messageDiv.innerHTML = `
            <span class="message-avatar">🤖</span>
            <div class="message-content">
                <div class="message-bubble">${formattedText}</div>
                <div class="message-timestamp">${timestamp}</div>
                ${quickActionsHtml}
            </div>
        `;

        messagesContainer.appendChild(messageDiv);

        // Attach click handlers to quick action buttons
        messageDiv.querySelectorAll('.quick-action-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.getAttribute('data-action');
                this.sendMessage(action);
            });
        });

        this.scrollToBottom();
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-message bot';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <span class="message-avatar">🤖</span>
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }

    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    scrollToBottom() {
        const messagesContainer = document.getElementById('chatMessages');
        setTimeout(() => {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, 100);
    }

    getTimestamp() {
        const now = new Date();
        return now.toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit',
            hour12: true 
        });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize chatbot when page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing Hidden Gems AI Chatbot...');
    window.chatbot = new ChatBot();
    console.log('Chatbot ready!');
});
