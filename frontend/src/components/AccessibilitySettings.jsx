import React, { useState, useEffect } from 'react';
import { Button } from '../components/Button';

const AccessibilitySettings = () => {
  const [activeTab, setActiveTab] = useState('preferences'); // preferences, feedback, features
  const [preferences, setPreferences] = useState({
    high_contrast_mode: false,
    dyslexia_friendly_font: false,
    text_size: 'normal',
    reduce_motion: false,
    screen_reader_mode: false,
    captions_enabled: true,
    audio_description_enabled: false,
    transcript_language: 'en',
    simplify_interface: false,
    break_reminders: true,
    reading_support: false
  });
  const [newFeedback, setNewFeedback] = useState({
    issue_type: 'navigation',
    severity: 'medium',
    description: '',
    suggested_solution: ''
  });
  const [feedbackList, setFeedbackList] = useState([
    {
      id: 1,
      issue_type: 'color_contrast',
      severity: 'high',
      description: 'Low contrast text in the course player',
      suggested_solution: 'Increase contrast ratio to at least 4.5:1',
      created_at: '2023-05-15T10:30:00Z',
      is_resolved: false
    },
    {
      id: 2,
      issue_type: 'keyboard',
      severity: 'medium',
      description: 'Navigation menu not accessible via keyboard',
      suggested_solution: 'Add proper focus indicators and keyboard navigation',
      created_at: '2023-05-10T14:20:00Z',
      is_resolved: true
    }
  ]);
  const [platformFeatures, setPlatformFeatures] = useState([
    {
      id: 1,
      name: 'High Contrast Mode',
      description: 'Enhanced contrast for better visibility',
      enabled: true
    },
    {
      id: 2,
      name: 'Keyboard Navigation',
      description: 'Full keyboard navigation support',
      enabled: true
    },
    {
      id: 3,
      name: 'Screen Reader Support',
      description: 'Optimized for screen readers',
      enabled: true
    },
    {
      id: 4,
      name: 'Focus Indicators',
      description: 'Clear focus indicators for keyboard navigation',
      enabled: true
    }
  ]);

  const handlePreferenceChange = (field, value) => {
    setPreferences(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSavePreferences = () => {
    // In a real implementation, this would save to the API
    alert('Accessibility preferences saved successfully!');
  };

  const handleFeedbackChange = (field, value) => {
    setNewFeedback(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmitFeedback = () => {
    if (newFeedback.description.trim()) {
      const feedback = {
        id: feedbackList.length + 1,
        ...newFeedback,
        created_at: new Date().toISOString(),
        is_resolved: false
      };
      setFeedbackList([feedback, ...feedbackList]);
      setNewFeedback({
        issue_type: 'navigation',
        severity: 'medium',
        description: '',
        suggested_solution: ''
      });
      alert('Feedback submitted successfully!');
    }
  };

  const handleMarkResolved = (id) => {
    setFeedbackList(prev => 
      prev.map(feedback => 
        feedback.id === id ? { ...feedback, is_resolved: true } : feedback
      )
    );
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">Accessibility Settings</h2>
      
      <div className="flex space-x-4 mb-6 border-b border-gray-200 dark:border-gray-700">
        <button
          className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
            activeTab === 'preferences'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-gray-700 dark:text-blue-400'
              : 'text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300'
          }`}
          onClick={() => setActiveTab('preferences')}
        >
          Preferences
        </button>
        <button
          className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
            activeTab === 'feedback'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-gray-700 dark:text-blue-400'
              : 'text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300'
          }`}
          onClick={() => setActiveTab('feedback')}
        >
          Feedback
        </button>
        <button
          className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
            activeTab === 'features'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-gray-700 dark:text-blue-400'
              : 'text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300'
          }`}
          onClick={() => setActiveTab('features')}
        >
          Features
        </button>
      </div>
      
      <div className="mt-4">
        {activeTab === 'preferences' && (
          <div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Visual Accessibility</h3>
                
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        High Contrast Mode
                      </label>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Increases contrast between text and background
                      </p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={preferences.high_contrast_mode}
                        onChange={(e) => handlePreferenceChange('high_contrast_mode', e.target.checked)}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-'' after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Dyslexia-friendly Font
                      </label>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Uses OpenDyslexic font for better readability
                      </p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={preferences.dyslexia_friendly_font}
                        onChange={(e) => handlePreferenceChange('dyslexia_friendly_font', e.target.checked)}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-'' after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Text Size
                    </label>
                    <select
                      value={preferences.text_size}
                      onChange={(e) => handlePreferenceChange('text_size', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    >
                      <option value="small">Small</option>
                      <option value="normal">Normal</option>
                      <option value="large">Large</option>
                      <option value="xlarge">Extra Large</option>
                    </select>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Reduce Motion
                      </label>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Reduces animations and transitions
                      </p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={preferences.reduce_motion}
                        onChange={(e) => handlePreferenceChange('reduce_motion', e.target.checked)}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-'' after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>
                </div>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Audio & Cognitive Accessibility</h3>
                
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Captions Enabled
                      </label>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Show captions for video content
                      </p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={preferences.captions_enabled}
                        onChange={(e) => handlePreferenceChange('captions_enabled', e.target.checked)}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-'' after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Audio Description
                      </label>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Narrated descriptions of visual elements
                      </p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={preferences.audio_description_enabled}
                        onChange={(e) => handlePreferenceChange('audio_description_enabled', e.target.checked)}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-'' after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Transcript Language
                    </label>
                    <select
                      value={preferences.transcript_language}
                      onChange={(e) => handlePreferenceChange('transcript_language', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    >
                      <option value="en">English</option>
                      <option value="es">Spanish</option>
                      <option value="fr">French</option>
                      <option value="de">German</option>
                    </select>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Simplify Interface
                      </label>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Reduce visual complexity and distractions
                      </p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={preferences.simplify_interface}
                        onChange={(e) => handlePreferenceChange('simplify_interface', e.target.checked)}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-'' after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Break Reminders
                      </label>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Periodic reminders to take breaks
                      </p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={preferences.break_reminders}
                        onChange={(e) => handlePreferenceChange('break_reminders', e.target.checked)}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-'' after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="mt-6 flex justify-end">
              <Button variant="primary" onClick={handleSavePreferences}>
                Save Preferences
              </Button>
            </div>
          </div>
        )}
        
        {activeTab === 'feedback' && (
          <div>
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Submit Accessibility Feedback</h3>
              <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Issue Type
                    </label>
                    <select
                      value={newFeedback.issue_type}
                      onChange={(e) => handleFeedbackChange('issue_type', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-600 text-gray-900 dark:text-white"
                    >
                      <option value="navigation">Navigation</option>
                      <option value="color_contrast">Color Contrast</option>
                      <option value="screen_reader">Screen Reader</option>
                      <option value="keyboard">Keyboard Navigation</option>
                      <option value="audio">Audio Issues</option>
                      <option value="visual">Visual Issues</option>
                      <option value="cognitive">Cognitive</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Severity
                    </label>
                    <select
                      value={newFeedback.severity}
                      onChange={(e) => handleFeedbackChange('severity', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-600 text-gray-900 dark:text-white"
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                      <option value="critical">Critical</option>
                    </select>
                  </div>
                </div>
                
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Description
                  </label>
                  <textarea
                    value={newFeedback.description}
                    onChange={(e) => handleFeedbackChange('description', e.target.value)}
                    placeholder="Describe the accessibility issue you encountered..."
                    rows="3"
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-600 text-gray-900 dark:text-white"
                  />
                </div>
                
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Suggested Solution (Optional)
                  </label>
                  <textarea
                    value={newFeedback.suggested_solution}
                    onChange={(e) => handleFeedbackChange('suggested_solution', e.target.value)}
                    placeholder="How could this be improved?"
                    rows="2"
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-600 text-gray-900 dark:text-white"
                  />
                </div>
                
                <Button 
                  variant="primary" 
                  onClick={handleSubmitFeedback}
                  disabled={!newFeedback.description.trim()}
                >
                  Submit Feedback
                </Button>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Your Feedback History</h3>
              <div className="space-y-4">
                {feedbackList.map((feedback) => (
                  <div 
                    key={feedback.id} 
                    className={`p-4 rounded-lg border ${
                      feedback.is_resolved 
                        ? 'bg-green-50 dark:bg-green-900 border-green-200 dark:border-green-800' 
                        : 'bg-gray-50 dark:bg-gray-700 border-gray-200 dark:border-gray-600'
                    }`}
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center mb-2">
                          <span className={`text-xs font-medium px-2 py-1 rounded mr-2 ${
                            feedback.severity === 'low' 
                              ? 'bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-200'
                              : feedback.severity === 'medium'
                                ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-200'
                                : feedback.severity === 'high'
                                  ? 'bg-orange-100 text-orange-800 dark:bg-orange-800 dark:text-orange-200'
                                  : 'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-200'
                          }`}>
                            {feedback.severity.charAt(0).toUpperCase() + feedback.severity.slice(1)}
                          </span>
                          <span className="text-xs bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-200 px-2 py-1 rounded">
                            {feedback.issue_type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                          </span>
                        </div>
                        <h4 className="font-medium text-gray-800 dark:text-white">{feedback.description}</h4>
                        {feedback.suggested_solution && (
                          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                            <span className="font-medium">Suggestion:</span> {feedback.suggested_solution}
                          </p>
                        )}
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                          Submitted: {new Date(feedback.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      {!feedback.is_resolved && (
                        <Button 
                          variant="success" 
                          size="sm" 
                          onClick={() => handleMarkResolved(feedback.id)}
                        >
                          Mark Resolved
                        </Button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
        
        {activeTab === 'features' && (
          <div>
            <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Platform Accessibility Features</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {platformFeatures.map((feature) => (
                <div 
                  key={feature.id} 
                  className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 border border-gray-200 dark:border-gray-600"
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-medium text-gray-800 dark:text-white">{feature.name}</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{feature.description}</p>
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      feature.enabled 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' 
                        : 'bg-gray-100 text-gray-800 dark:bg-gray-600 dark:text-gray-200'
                    }`}>
                      {feature.enabled ? 'Enabled' : 'Disabled'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-6 bg-blue-50 dark:bg-blue-900 rounded-lg p-4 border border-blue-200 dark:border-blue-800">
              <h4 className="font-medium text-blue-800 dark:text-blue-200 mb-2">WCAG Compliance</h4>
              <p className="text-sm text-blue-700 dark:text-blue-300">
                This platform follows Web Content Accessibility Guidelines (WCAG) 2.1 AA standards to ensure 
                equal access for all users, including those with disabilities.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AccessibilitySettings;