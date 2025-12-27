// Advanced theme system
(function() {
    'use strict';
    
    // Theme manager class
    class ThemeManager {
        constructor() {
            this.currentTheme = this.getStoredTheme() || 'system';
            this.init();
        }
        
        init() {
            // Set initial theme
            this.applyTheme(this.currentTheme);
            
            // Listen for system theme changes
            this.watchSystemTheme();
            
            // Initialize theme toggle buttons
            this.initThemeToggles();
        }
        
        getStoredTheme() {
            return localStorage.getItem('theme');
        }
        
        setStoredTheme(theme) {
            localStorage.setItem('theme', theme);
        }
        
        applyTheme(theme) {
            this.currentTheme = theme;
            this.setStoredTheme(theme);
            
            // Remove all theme classes
            document.documentElement.classList.remove('light', 'dark', 'high-contrast', 'dyslexia-friendly', 'system');
            
            if (theme === 'system') {
                // Apply theme based on system preference
                const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                if (systemPrefersDark) {
                    document.documentElement.classList.add('dark');
                } else {
                    document.documentElement.classList.add('light');
                }
                document.documentElement.classList.add('system');
            } else {
                document.documentElement.classList.add(theme);
            }
            
            // Update theme toggle UI
            this.updateThemeToggleUI();
        }
        
        toggleTheme() {
            const themes = ['light', 'dark', 'high-contrast', 'dyslexia-friendly', 'system'];
            const currentIndex = themes.indexOf(this.currentTheme);
            const nextIndex = (currentIndex + 1) % themes.length;
            this.applyTheme(themes[nextIndex]);
        }
        
        watchSystemTheme() {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', (e) => {
                if (this.currentTheme === 'system') {
                    const newTheme = e.matches ? 'dark' : 'light';
                    document.documentElement.classList.remove('light', 'dark');
                    document.documentElement.classList.add(newTheme);
                }
            });
        }
        
        initThemeToggles() {
            // Add click listeners to theme toggle buttons
            const themeButtons = document.querySelectorAll('[data-theme-toggle]');
            themeButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    const theme = e.currentTarget.getAttribute('data-theme-toggle');
                    this.applyTheme(theme);
                });
            });
            
            // Add click listener to general theme toggle
            const generalToggle = document.querySelector('[data-theme-general-toggle]');
            if (generalToggle) {
                generalToggle.addEventListener('click', () => {
                    this.toggleTheme();
                });
            }
        }
        
        updateThemeToggleUI() {
            // Update theme toggle button icons/text based on current theme
            const themeToggleButtons = document.querySelectorAll('[data-theme-toggle]');
            themeToggleButtons.forEach(button => {
                const theme = button.getAttribute('data-theme-toggle');
                if (theme === this.currentTheme) {
                    button.classList.add('active');
                } else {
                    button.classList.remove('active');
                }
            });
            
            // Update general toggle icon
            const generalToggle = document.querySelector('[data-theme-general-toggle]');
            if (generalToggle) {
                const icon = generalToggle.querySelector('i');
                if (icon) {
                    icon.className = this.getThemeIcon();
                }
            }
        }
        
        getThemeIcon() {
            switch (this.currentTheme) {
                case 'light':
                    return 'fas fa-sun text-gray-700 dark:text-gray-300';
                case 'dark':
                    return 'fas fa-moon text-gray-300';
                case 'high-contrast':
                    return 'fas fa-adjust text-gray-700 dark:text-gray-300';
                case 'dyslexia-friendly':
                    return 'fas fa-font text-gray-700 dark:text-gray-300';
                case 'system':
                default:
                    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                    return systemPrefersDark ? 'fas fa-moon text-gray-300' : 'fas fa-sun text-gray-700 dark:text-gray-300';
            }
        }
        
        // Accessibility methods
        setReducedMotion(reduced) {
            if (reduced) {
                document.documentElement.style.setProperty('--animation-duration', '0.01ms');
            } else {
                document.documentElement.style.setProperty('--animation-duration', '');
            }
        }
        
        // Get current theme info
        getThemeInfo() {
            return {
                current: this.currentTheme,
                isDark: this.currentTheme === 'dark' || 
                         (this.currentTheme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches),
                isHighContrast: this.currentTheme === 'high-contrast',
                isDyslexiaFriendly: this.currentTheme === 'dyslexia-friendly'
            };
        }
    }
    
    // Initialize theme manager when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        window.themeManager = new ThemeManager();
    });
    
    // Make ThemeManager globally available
    window.ThemeManager = ThemeManager;
})();
