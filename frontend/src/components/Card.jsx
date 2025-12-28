import React from 'react';
import PropTypes from 'prop-types';

const Card = ({ 
  children, 
  title, 
  subtitle, 
  actions, 
  className = '', 
  variant = 'default',
  ...props 
}) => {
  const baseClasses = 'rounded-xl shadow-lg p-6 transition-all duration-200 border';
  const variants = {
    default: 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700',
    elevated: 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:shadow-xl',
    glass: 'bg-white/70 dark:bg-gray-800/70 backdrop-blur-md border border-gray-200/50 dark:border-gray-700/50',
    glassStrong: 'bg-white/90 dark:bg-gray-800/90 backdrop-blur-lg border border-gray-200/80 dark:border-gray-700/80'
  };

  const cardClasses = [
    baseClasses,
    variants[variant],
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={cardClasses} {...props}>
      {(title || subtitle) && (
        <div className="mb-4">
          {title && <h3 className="text-xl font-semibold text-gray-900 dark:text-white">{title}</h3>}
          {subtitle && <p className="text-gray-600 dark:text-gray-400">{subtitle}</p>}
        </div>
      )}
      <div className="flex-grow">
        {children}
      </div>
      {actions && (
        <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
          {actions}
        </div>
      )}
    </div>
  );
};

Card.propTypes = {
  children: PropTypes.node.isRequired,
  title: PropTypes.string,
  subtitle: PropTypes.string,
  actions: PropTypes.node,
  className: PropTypes.string,
  variant: PropTypes.oneOf(['default', 'elevated', 'glass', 'glassStrong'])
};

export default Card;