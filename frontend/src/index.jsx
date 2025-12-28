import React from 'react';
import ReactDOM from 'react-dom/client';
import { initThemeSystem } from './utils/theme';

// Initialize theme system
initThemeSystem();

// Export all components and utilities
export { default as Button } from './components/Button';
export { default as Input } from './components/Input';
export { default as Card } from './components/Card';
export { default as Modal } from './components/Modal';
export { default as Toast } from './components/Toast';
export { default as ProgressBar } from './components/ProgressBar';
export { default as MainLayout } from './layouts/MainLayout';
export { default as useTheme } from './hooks/useTheme';
export { THEMES, setTheme, getCurrentTheme, cycleTheme, isDarkTheme } from './utils/theme';

// Basic React app setup
export const App = ({ children }) => {
  return (
    <div className="app" data-theme={localStorage.getItem('theme') || 'system'}>
      {children}
    </div>
  );
};

// Render function for demo purposes
export const renderApp = (element, containerId = 'root') => {
  const container = document.getElementById(containerId);
  if (container) {
    const root = ReactDOM.createRoot(container);
    root.render(<App>{element}</App>);
  }
};

// Initialize the theme system when this module is imported
document.addEventListener('DOMContentLoaded', initThemeSystem);