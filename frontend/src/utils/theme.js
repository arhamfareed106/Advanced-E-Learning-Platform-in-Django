/**
 * Theme utility functions
 */


// Theme constants
export const THEMES = {
  LIGHT: 'light',
  DARK: 'dark',
  SYSTEM: 'system',
  HIGH_CONTRAST: 'high-contrast',
  DYSLEXIA_FRIENDLY: 'dyslexia-friendly'
};

// Get current theme from localStorage or system preference
export const getCurrentTheme = () => {
  return localStorage.getItem('theme') || THEMES.SYSTEM;
};

// Set theme and apply to document
export const setTheme = (theme) => {
  // Validate theme
  if (!Object.values(THEMES).includes(theme)) {
    console.warn(`Invalid theme: ${theme}`);
    return;
  }

  // Save to localStorage
  localStorage.setItem('theme', theme);

  // Remove all theme classes
  document.documentElement.classList.remove(
    THEMES.LIGHT,
    THEMES.DARK,
    THEMES.HIGH_CONTRAST,
    THEMES.DYSLEXIA_FRIENDLY,
    'system'
  );

  // Apply theme based on selection
  if (theme === THEMES.SYSTEM) {
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (systemPrefersDark) {
      document.documentElement.classList.add(THEMES.DARK);
    } else {
      document.documentElement.classList.add(THEMES.LIGHT);
    }
    document.documentElement.classList.add('system');
  } else {
    document.documentElement.classList.add(theme);
  }

  // Update theme in meta tag for web app manifest
  const themeColorMeta = document.querySelector('meta[name="theme-color"]');
  if (themeColorMeta) {
    themeColorMeta.setAttribute('content', getThemeColor(theme));
  }
};

// Get appropriate theme color for meta tag
const getThemeColor = (theme) => {
  switch (theme) {
    case THEMES.DARK:
      return '#1f2937'; // gray-800
    case THEMES.HIGH_CONTRAST:
      return '#000000'; // black
    case THEMES.DYSLEXIA_FRIENDLY:
      return '#faf9f6'; // light beige
    default:
      return '#f9fafb'; // gray-50
  }
};

// Initialize theme system
export const initThemeSystem = () => {
  // Apply saved theme on page load
  const savedTheme = getCurrentTheme();
  setTheme(savedTheme);

  // Watch for system theme changes
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  mediaQuery.addEventListener('change', (e) => {
    if (getCurrentTheme() === THEMES.SYSTEM) {
      const newTheme = e.matches ? THEMES.DARK : THEMES.LIGHT;
      document.documentElement.classList.remove(THEMES.LIGHT, THEMES.DARK);
      document.documentElement.classList.add(newTheme);
    }
  });
};

// Toggle between themes
export const cycleTheme = () => {
  const currentTheme = getCurrentTheme();
  const themeOrder = [
    THEMES.LIGHT,
    THEMES.DARK,
    THEMES.HIGH_CONTRAST,
    THEMES.DYSLEXIA_FRIENDLY,
    THEMES.SYSTEM
  ];
  
  const currentIndex = themeOrder.indexOf(currentTheme);
  const nextIndex = (currentIndex + 1) % themeOrder.length;
  setTheme(themeOrder[nextIndex]);
};

// Check if current theme is dark
export const isDarkTheme = () => {
  const currentTheme = getCurrentTheme();
  
  if (currentTheme === THEMES.SYSTEM) {
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  
  return currentTheme === THEMES.DARK;
};