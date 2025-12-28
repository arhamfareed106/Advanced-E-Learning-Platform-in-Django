import React from 'react';
import PropTypes from 'prop-types';

const MainLayout = ({ 
  children, 
  header, 
  sidebar, 
  footer, 
  className = '',
  hasSidebar = true,
  ...props 
}) => {
  return (
    <div className={`min-h-screen flex flex-col ${className}`} {...props}>
      {header && (
        <header className="bg-white dark:bg-gray-900 shadow-sm">
          {header}
        </header>
      )}
      
      <div className="flex flex-1">
        {hasSidebar && sidebar && (
          <aside className="w-64 bg-white dark:bg-gray-900 shadow-sm hidden md:block">
            {sidebar}
          </aside>
        )}
        
        <main className="flex-1 p-4 md:p-6">
          {children}
        </main>
      </div>
      
      {footer && (
        <footer className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700">
          {footer}
        </footer>
      )}
    </div>
  );
};

MainLayout.propTypes = {
  children: PropTypes.node.isRequired,
  header: PropTypes.node,
  sidebar: PropTypes.node,
  footer: PropTypes.node,
  className: PropTypes.string,
  hasSidebar: PropTypes.bool
};

export default MainLayout;