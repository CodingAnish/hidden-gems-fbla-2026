/**
 * Hidden Gems - Advanced Features JS
 * Reviews, Favorites, Filtering, Validation
 * FBLA 2026
 */

// ============================================
// PART 1: FAVORITES SYSTEM (localStorage)
// ============================================

const Favorites = {
    storageKey: 'hidden_gems_favorites',
    
    get all() {
        const stored = localStorage.getItem(this.storageKey);
        return stored ? JSON.parse(stored) : [];
    },
    
    add(businessId) {
        const favs = this.all;
        if (!favs.includes(businessId)) {
            favs.push(businessId);
            localStorage.setItem(this.storageKey, JSON.stringify(favs));
            return true;
        }
        return false;
    },
    
    remove(businessId) {
        const favs = this.all.filter(id => id !== businessId);
        localStorage.setItem(this.storageKey, JSON.stringify(favs));
        return true;
    },
    
    has(businessId) {
        return this.all.includes(businessId);
    },
    
    toggle(businessId, businessName, button = null) {
        const isCurrentlyFavorited = this.has(businessId);
        
        // Update localStorage immediately for UX
        if (isCurrentlyFavorited) {
            this.remove(businessId);
            Notifications.show(`Removed "${businessName}" from favorites`, 'success');
            if (button) button.classList.remove('active');
        } else {
            this.add(businessId);
            Notifications.show(`Added "${businessName}" to favorites ❤️`, 'success');
            if (button) button.classList.add('active');
        }
        
        // Sync with backend
        fetch('/api/favorites', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                business_id: businessId,
                action: 'toggle'
            })
        }).catch(error => console.error('Failed to sync favorites:', error));
        
        return !isCurrentlyFavorited;
    },
    
    clear() {
        localStorage.removeItem(this.storageKey);
    }
};

// ============================================
// PART 2: INPUT VALIDATION
// ============================================

const Validator = {
    review: function(data) {
        const errors = [];
        
        if (!data.userName || data.userName.trim().length < 2) {
            errors.push('Name must be at least 2 characters');
        }
        if (data.userName && data.userName.length > 50) {
            errors.push('Name too long (max 50 characters)');
        }
        
        if (!data.rating || data.rating < 1 || data.rating > 5) {
            errors.push('Please select a star rating (1-5)');
        }
        
        if (!data.comment || data.comment.trim().length < 10) {
            errors.push('Review must be at least 10 characters');
        }
        if (data.comment && data.comment.length > 500) {
            errors.push('Review too long (max 500 characters)');
        }
        
        if (!data.captchaAnswer) {
            errors.push('Please answer the verification question');
        }
        
        return {valid: errors.length === 0, errors};
    },
    
    search: function(input) {
        const errors = [];
        
        if (!input || input.trim() === '') {
            errors.push('Search cannot be empty');
        }
        if (input && input.length < 2) {
            errors.push('Search must be at least 2 characters');
        }
        if (input && input.length > 100) {
            errors.push('Search too long (max 100 characters)');
        }
        
        return {valid: errors.length === 0, errors};
    },
    
    updateCharCount: function(textarea) {
        const counter = document.getElementById('char-count');
        if (counter) {
            counter.textContent = `${textarea.value.length} / 500 characters`;
        }
    },
    
    showErrors: function(errors, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        container.innerHTML = errors.map(e => 
            `<div class="error-message" role="alert">⚠️ ${e}</div>`
        ).join('');
        
        // Auto-clear after 5 seconds
        setTimeout(() => {
            container.innerHTML = '';
        }, 5000);
    }
};

// ============================================
// PART 3: NOTIFICATIONS
// ============================================

const Notifications = {
    show: function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.setAttribute('role', 'status');
        notification.setAttribute('aria-live', 'polite');
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Trigger animation
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // Remove after 3.5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3500);
    }
};

// ============================================
// PART 4: REVIEWS SYSTEM
// ============================================

const Reviews = {
    currentBusinessId: null,
    
    openModal: function(businessId, businessName) {
        this.currentBusinessId = businessId;
        const modal = document.getElementById('review-modal');
        if (!modal) return;
        
        modal.style.display = 'block';
        modal.setAttribute('aria-hidden', 'false');
        
        // Reset form
        document.getElementById('review-form').reset();
        document.getElementById('char-count').textContent = '0/500';
        
        // Load captcha
        this.loadCaptcha();
        
        // Setup character counter
        const textarea = document.getElementById('review-comment');
        if (textarea) {
            textarea.addEventListener('input', () => {
                document.getElementById('char-count').textContent = `${textarea.value.length}/500`;
            });
        }
    },
    
    closeModal: function() {
        const modal = document.getElementById('review-modal');
        if (modal) {
            modal.style.display = 'none';
            modal.setAttribute('aria-hidden', 'true');
        }
    },
    
    loadCaptcha: async function() {
        try {
            const response = await fetch('/get-captcha', {
                credentials: 'include'
            });
            const data = await response.json();
            const questionEl = document.getElementById('captcha-question');
            if (questionEl) {
                questionEl.textContent = data.question;
            }
        } catch (error) {
            console.error('Failed to load captcha:', error);
            Notifications.show('Failed to load verification question', 'error');
        }
    },
    
    submit: async function(event) {
        if (event) event.preventDefault();
        
        const data = {
            userName: document.getElementById('reviewer-name').value,
            rating: document.querySelector('input[name="rating"]:checked')?.value,
            comment: document.getElementById('review-comment').value,
            captchaAnswer: document.getElementById('captcha-answer').value
        };
        
        const validation = Validator.review(data);
        if (!validation.valid) {
            Validator.showErrors(validation.errors, 'review-errors');
            return;
        }
        
        try {
            const response = await fetch('/submit-review', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                credentials: 'include',
                body: JSON.stringify({
                    business_id: this.currentBusinessId,
                    user_name: data.userName,
                    rating: parseInt(data.rating),
                    comment: data.comment,
                    captcha_answer: parseInt(data.captchaAnswer)
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                Notifications.show('Review submitted successfully! ✅', 'success');
                this.closeModal();
                // Reload reviews after delay
                setTimeout(() => this.loadReviews(this.currentBusinessId), 500);
            } else {
                const errorMsg = result.errors ? result.errors.join(', ') : (result.error || 'Failed to submit review');
                Validator.showErrors([errorMsg], 'review-errors');
            }
        } catch (error) {
            console.error('Submission error:', error);
            Notifications.show('Failed to submit review. Please try again.', 'error');
        }
    },
    
    loadReviews: async function(businessId) {
        try {
            const response = await fetch(`/get-reviews/${businessId}`);
            const data = await response.json();
            this.displayReviews(data.reviews, data.average_rating, data.count);
        } catch (error) {
            console.error('Failed to load reviews:', error);
        }
    },
    
    displayReviews: function(reviews, avgRating, count) {
        const container = document.getElementById('reviews-container');
        if (!container) return;
        
        if (!reviews || reviews.length === 0) {
            container.innerHTML = '<p class="no-reviews">No reviews yet. Be the first to review!</p>';
            return;
        }
        
        let html = `
            <div class="rating-summary">
                <h3>${this.getStarHTML(avgRating)} ${avgRating} (${count} reviews)</h3>
            </div>
            <div class="reviews-list">
        `;
        
        reviews.forEach(review => {
            html += `
                <div class="review-card">
                    <div class="review-header">
                        <strong>${this.escapeHtml(review.user_name)}</strong>
                        <span class="review-date">${review.date}</span>
                    </div>
                    <div class="review-rating">${this.getStarHTML(review.rating)}</div>
                    <p class="review-comment">${this.escapeHtml(review.comment)}</p>
                    ${review.verified ? '<span class="verified-badge">✓ Verified</span>' : ''}
                </div>
            `;
        });
        
        html += '</div>';
        container.innerHTML = html;
    },
    
    getStarHTML: function(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        let stars = '';
        
        for (let i = 0; i < fullStars; i++) {
            stars += '⭐';
        }
        if (hasHalfStar) {
            stars += '½⭐';
        }
        const emptyStars = 5 - Math.ceil(rating);
        for (let i = 0; i < emptyStars; i++) {
            stars += '☆';
        }
        
        return stars;
    },
    
    escapeHtml: function(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// ============================================
// PART 5: SORTING & FILTERING
// ============================================

const Filters = {
    apply: function() {
        const minRating = parseFloat(document.getElementById('min-rating')?.value) || 0;
        const hasDeals = document.getElementById('filter-deals')?.checked || false;
        const category = document.getElementById('filter-category')?.value || 'all';
        
        document.querySelectorAll('[data-business-card]').forEach(card => {
            const rating = parseFloat(card.dataset.rating) || 0;
            const cardCategory = card.dataset.category;
            const cardHasDeals = card.dataset.hasDeals === 'true';
            
            let show = true;
            
            // Check rating
            if (rating < minRating) show = false;
            
            // Check category
            if (category !== 'all' && cardCategory !== category) show = false;
            
            // Check deals
            if (hasDeals && !cardHasDeals) show = false;
            
            card.style.display = show ? 'block' : 'none';
        });
    },
    
    sortBy: function(sortType) {
        const container = document.querySelector('[data-business-grid]');
        if (!container) return;
        
        const cards = Array.from(container.querySelectorAll('[data-business-card]'));
        
        cards.sort((a, b) => {
            switch(sortType) {
                case 'name-asc':
                    return a.dataset.name.localeCompare(b.dataset.name);
                case 'name-desc':
                    return b.dataset.name.localeCompare(a.dataset.name);
                case 'rating-desc':
                    return (parseFloat(b.dataset.rating) || 0) - (parseFloat(a.dataset.rating) || 0);
                case 'rating-asc':
                    return (parseFloat(a.dataset.rating) || 0) - (parseFloat(b.dataset.rating) || 0);
                case 'reviews-desc':
                    return (parseInt(b.dataset.reviews) || 0) - (parseInt(a.dataset.reviews) || 0);
                default:
                    return 0;
            }
        });
        
        container.innerHTML = '';
        cards.forEach(card => container.appendChild(card));
    },
    
    clear: function() {
        document.getElementById('min-rating').value = '0';
        document.getElementById('filter-deals').checked = false;
        document.getElementById('filter-category').value = 'all';
        document.getElementById('sort-by').value = '';
        this.apply();
        Notifications.show('Filters cleared', 'success');
    }
};

// ============================================
// PART 6: HELP MENU & ACCESSIBILITY
// ============================================

const Help = {
    toggle: function() {
        const menu = document.getElementById('help-menu');
        if (!menu) return;
        
        const isHidden = menu.style.display === 'none';
        menu.style.display = isHidden ? 'block' : 'none';
        menu.setAttribute('aria-hidden', !isHidden);
    },
    
    close: function() {
        const menu = document.getElementById('help-menu');
        if (menu) {
            menu.style.display = 'none';
            menu.setAttribute('aria-hidden', 'true');
        }
    }
};

// ============================================
// PART 7: INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Update favorite count
    updateFavoriteCount();
    
    // Update favorite buttons based on saved state
    document.querySelectorAll('[data-business-card]').forEach(card => {
        const businessId = card.dataset.businessId;
        if (businessId && Favorites.has(businessId)) {
            const btn = card.querySelector('[data-action="favorite"]');
            if (btn) {
                btn.innerHTML = '❤️ Saved';
                btn.classList.add('active');
            }
        }
    });
    
    // Close modals when clicking outside
    window.addEventListener('click', (e) => {
        const reviewModal = document.getElementById('review-modal');
        const helpMenu = document.getElementById('help-menu');
        
        if (e.target === reviewModal) {
            Reviews.closeModal();
        }
        if (e.target === helpMenu) {
            Help.close();
        }
    });
    
    // Close modals with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            Reviews.closeModal();
            Help.close();
        }
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === '/') {
            e.preventDefault();
            const searchInput = document.getElementById('search-input');
            if (searchInput) searchInput.focus();
        }
    });
});

function updateFavoriteCount() {
    const count = Favorites.all.length;
    const badge = document.getElementById('favorites-count');
    if (badge) {
        badge.textContent = count;
    }
}

function toggleFavorite(businessId, businessName, button) {
    const isFav = Favorites.toggle(businessId, businessName);
    
    if (button) {
        button.innerHTML = isFav ? '❤️ Saved' : '🤍 Save';
        button.classList.toggle('active', isFav);
    }
    
    updateFavoriteCount();
    
    // Update card data attribute
    const card = document.querySelector(`[data-business-id="${businessId}"]`);
    if (card) {
        card.dataset.isFavorited = isFav;
    }
}
