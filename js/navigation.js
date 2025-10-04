/**
 * Enhanced Navigation System
 * Features: Smooth scrolling, active section highlighting, scroll-to-top, and accessibility
 */

class EnhancedNavigation {
    constructor() {
        this.navigation = document.getElementById('mainNavigation');
        this.navItems = document.querySelectorAll('.nav-item');
        this.scrollToTopBtn = document.getElementById('scrollToTop');
        this.sections = document.querySelectorAll('section[id]');
        this.lastActiveSection = null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupScrollSpy();
        this.setupAccessibility();
        this.updateScrollToTopVisibility();
    }
    
    setupEventListeners() {
        // Smooth scrolling for navigation links
        this.navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                const targetId = item.getAttribute('href').substring(1);
                const targetSection = document.getElementById(targetId);
                
                if (targetSection) {
                    e.preventDefault();
                    this.scrollToSection(targetSection);
                }
            });
        });
        
        // Scroll to top button
        if (this.scrollToTopBtn) {
            this.scrollToTopBtn.addEventListener('click', () => {
                this.scrollToTop();
            });
        }
        
        // Handle scroll events
        window.addEventListener('scroll', this.throttle(this.handleScroll.bind(this), 100));
        
        // Handle window resize
        window.addEventListener('resize', this.throttle(this.handleResize.bind(this), 250));
        
        // Handle keyboard navigation
        document.addEventListener('keydown', this.handleKeydown.bind(this));
    }
    
    setupScrollSpy() {
        // Create intersection observer for better performance
        const observerOptions = {
            root: null,
            rootMargin: '-20% 0px -80% 0px',
            threshold: 0.1
        };
        
        this.observer = new IntersectionObserver((entries) => {
            let maxVisible = 0;
            let activeEntry = null;
            
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const visibility = this.getVisibilityPercentage(entry.target);
                    if (visibility > maxVisible) {
                        maxVisible = visibility;
                        activeEntry = entry.target;
                    }
                }
            });
            
            if (activeEntry && activeEntry.id !== this.lastActiveSection) {
                this.setActiveSection(activeEntry.id);
                this.lastActiveSection = activeEntry.id;
            }
        }, observerOptions);
        
        // Observe all sections
        this.sections.forEach(section => {
            this.observer.observe(section);
        });
    }
    
    setupAccessibility() {
        // Add ARIA attributes
        this.navItems.forEach(item => {
            const sectionId = item.getAttribute('href').substring(1);
            const section = document.getElementById(sectionId);
            
            if (section) {
                item.setAttribute('aria-label', `Navigate to ${item.querySelector('.nav-text').textContent} section`);
                if (!section.getAttribute('aria-labelledby')) {
                    section.setAttribute('aria-labelledby', `${sectionId}-heading`);
                    const heading = section.querySelector('h2');
                    if (heading) {
                        heading.id = `${sectionId}-heading`;
                    }
                }
            }
        });
        
        // Announce section changes to screen readers
        this.announcer = document.createElement('div');
        this.announcer.setAttribute('aria-live', 'polite');
        this.announcer.setAttribute('aria-atomic', 'true');
        this.announcer.style.position = 'absolute';
        this.announcer.style.left = '-10000px';
        this.announcer.style.width = '1px';
        this.announcer.style.height = '1px';
        this.announcer.style.overflow = 'hidden';
        document.body.appendChild(this.announcer);
    }
    
    handleScroll() {
        this.updateScrollToTopVisibility();
        this.updateActiveNavigation();
    }
    
    handleResize() {
        // Recalculate positions on resize
        this.updateScrollToTopVisibility();
    }
    
    handleKeydown(e) {
        // Enhanced keyboard navigation
        if (e.key === 'Tab' && e.target.classList.contains('nav-item')) {
            this.focusNavItem(e.target);
        }
        
        // Escape key behavior
        if (e.key === 'Escape') {
            const mobileToggle = document.querySelector('.navbar-toggler[aria-expanded="true"]');
            if (mobileToggle) {
                mobileToggle.click();
            }
        }
    }
    
    scrollToSection(section, offset = 80) {
        const targetPosition = section.offsetTop - offset;
        
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
        
        // Announce to screen readers
        this.announceSectionChange(section);
    }
    
    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
        
        // Announce to screen readers
        this.announceSectionChange(document.querySelector('section'));
    }
    
    setActiveSection(sectionId) {
        // Remove active class from all nav items
        this.navItems.forEach(item => {
            item.classList.remove('active');
            item.setAttribute('aria-current', 'false');
        });
        
        // Add active class to current nav item
        const activeNavItem = document.querySelector(`[data-section="${sectionId}"]`);
        if (activeNavItem) {
            activeNavItem.classList.add('active');
            activeNavItem.setAttribute('aria-current', 'true');
        }
        
        // Announce change to screen readers
        const section = document.getElementById(sectionId);
        if (section) {
            this.announceSectionChange(section);
        }
    }
    
    updateScrollToTopVisibility() {
        if (this.scrollToTopBtn) {
            const shouldShow = window.scrollY > window.innerHeight * 0.5;
            
            if (shouldShow) {
                this.scrollToTopBtn.classList.add('show');
            } else {
                this.scrollToTopBtn.classList.remove('show');
            }
        }
    }
    
    updateActiveNavigation() {
        // Fallback for older browsers or when intersection observer fails
        let activeSection = null;
        let minDistance = Infinity;
        
        this.sections.forEach(section => {
            const rect = section.getBoundingClientRect();
            const distance = Math.abs(rect.top);
            
            if (rect.top <= 100 && rect.bottom >= 100) {
                activeSection = section.id;
            } else if (distance < minDistance) {
                minDistance = distance;
                if (!activeSection) {
                    activeSection = section.id;
                }
            }
        });
        
        if (activeSection && activeSection !== this.lastActiveSection) {
            this.setActiveSection(activeSection);
            this.lastActiveSection = activeSection;
        }
    }
    
    focusNavItem(item) {
        // Enhanced focus styling
        item.style.outline = '2px solid rgba(255, 255, 255, 0.8)';
        item.style.outlineOffset = '3px';
        
        // Remove focus style after interaction
        setTimeout(() => {
            item.style.outline = '';
            item.style.outlineOffset = '';
        }, 300);
    }
    
    announceSectionChange(section) {
        if (this.announcer) {
            const heading = section.querySelector('h2');
            if (heading) {
                this.announcer.textContent = `Now viewing: ${heading.textContent}`;
            }
        }
    }
    
    getVisibilityPercentage(element) {
        const rect = element.getBoundingClientRect();
        const viewportHeight = window.innerHeight;
        
        const visibleTop = Math.max(0, rect.top);
        const visibleBottom = Math.min(viewportHeight, rect.bottom);
        const visibleHeight = Math.max(0, visibleBottom - visibleTop);
        
        return visibleHeight / rect.height;
    }
    
    throttle(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Public methods for external use
    destroy() {
        if (this.observer) {
            this.observer.disconnect();
        }
        
        window.removeEventListener('scroll', this.handleScroll);
        window.removeEventListener('resize', this.handleResize);
        document.removeEventListener('keydown', this.handleKeydown);
        
        if (this.announcer) {
            document.body.removeChild(this.announcer);
        }
    }
}

// Initialize enhanced navigation when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Add loading animation
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
        
        // Initialize navigation
        if (window.innerWidth >= 992) {
            window.enhancedNav = new EnhancedNavigation();
        } else {
            // Initialize mobile navigation
            window.enhancedNav = new EnhancedNavigation();
        }
    }, 100);
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (!document.hidden && window.enhancedNav) {
        // Update navigation state when page becomes visible
        window.enhancedNav.updateActiveNavigation();
        window.enhancedNav.updateScrollToTopVisibility();
    }
});
