/**
 * Personal Webpage - Main JavaScript File
 * Enhanced with modern features and optimizations
 */

// Initial page setup and performance optimizations
const initializePage = () => {
    // Add loading state
    document.body.classList.add('loading');
    
    // Performance optimization: Lazy load images
    const images = document.querySelectorAll('img');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
    
    // Add smooth page transitions
    setTimeout(() => {
        document.body.classList.remove('loading');
        document.body.classList.add('loaded');
    }, 500);
    
    // Announce page load for screen readers
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.style.position = 'absolute';
    announcement.style.left = '-10000px';
    announcement.textContent = 'Valantis Zervos personal webpage loaded';
    document.body.appendChild(announcement);
    
    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
};

// Utility functions
const utils = {
    // Debounce function for performance optimization
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func.apply(this, args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Check if user prefers reduced motion
    prefersReducedMotion() {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    },
    
    // Format dates for better readability
    formatDate(date) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(date).toLocaleDateString(undefined, options);
    }
};

// Analytics and performance tracking (placeholder for future integration)
const analytics = {
    trackPageView() {
        // Future: integrate with Google Analytics or similar
        console.log('📊 Page view tracked');
    },
    
    trackInteraction(action, element) {
        // Future: track user interactions for UX improvements
        console.log(`🎯 Interaction: ${action} on ${element}`);
    }
};

// Enhanced error handling
window.addEventListener('error', (event) => {
    console.error('❌ JavaScript Error:', event.error);
    // Future: send error reports to monitoring service
});

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', initializePage);

// Listen for performance events
window.addEventListener('load', () => {
    analytics.trackPageView();
    
    // Report performance metrics
    if ('performance' in window) {
        const perfData = performance.getEntriesByType('navigation')[0];
        console.log(`⚡ Page load time: ${perfData.loadEventEnd - perfData.fetchStart}ms`);
    }
});

export { utils, analytics };
