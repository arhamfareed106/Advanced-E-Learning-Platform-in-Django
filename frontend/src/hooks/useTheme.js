import { useState, useEffect } from 'react';
import { THEMES, getCurrentTheme, setTheme, cycleTheme, isDarkTheme } from '../utils/theme';

const useTheme = () => {
  const [currentTheme, setCurrentTheme] = useState(getCurrentTheme);
  const [isDark, setIsDark] = useState(isDarkTheme());

  useEffect(() => {
    // Initialize theme
    const theme = getCurrentTheme();
    setCurrentTheme(theme);
    setIsDark(isDarkTheme());

    // Listen for theme changes
    const handleThemeChange = () => {
      setCurrentTheme(getCurrentTheme());
      setIsDark(isDarkTheme());
    };

    // Watch for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', handleThemeChange);

    return () => {
      mediaQuery.removeEventListener('change', handleThemeChange);
    };
  }, []);

  const toggleTheme = () => {
    cycleTheme();
    setCurrentTheme(getCurrentTheme());
    setIsDark(isDarkTheme());
  };

  const changeTheme = (theme) => {
    setTheme(theme);
    setCurrentTheme(theme);
    setIsDark(isDarkTheme());
  };

  return {
    theme: currentTheme,
    isDark,
    THEMES,
    toggleTheme,
    changeTheme,
    setLightTheme: () => changeTheme(THEMES.LIGHT),
    setDarkTheme: () => changeTheme(THEMES.DARK),
    setSystemTheme: () => changeTheme(THEMES.SYSTEM),
    setHighContrastTheme: () => changeTheme(THEMES.HIGH_CONTRAST),
    setDyslexiaFriendlyTheme: () => changeTheme(THEMES.DYSLEXIA_FRIENDLY)
  };
};

export default useTheme;