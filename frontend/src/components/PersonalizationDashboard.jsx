import React, { useState, useEffect } from 'react';
import { Button } from '../components/Button';

const PersonalizationDashboard = () => {
  const [activeTab, setActiveTab] = useState('preferences'); // preferences, learning-paths, recommendations
  const [preferences, setPreferences] = useState({
    learning_style: 'visual',
    difficulty_level: 'intermediate',
    preferred_language: 'en',
    study_time_preference: 'morning',
    notification_frequency: 'moderate'
  });
  const [learningPaths, setLearningPaths] = useState([
    {
      id: 1,
      title: 'React Masterclass',
      description: 'Master React with advanced concepts and real-world projects',
      courses: [
        { id: 1, title: 'React Fundamentals', progress: 85 },
        { id: 2, title: 'Advanced React Patterns', progress: 45 },
        { id: 3, title: 'React Performance', progress: 0 }
      ],
      is_active: true
    },
    {
      id: 2,
      title: 'Python for Data Science',
      description: 'Learn Python for data analysis and machine learning',
      courses: [
        { id: 4, title: 'Python Basics', progress: 100 },
        { id: 5, title: 'Data Analysis with Pandas', progress: 70 }
      ],
      is_active: true
    }
  ]);
  const [recommendations, setRecommendations] = useState([
    {
      id: 1,
      title: 'Advanced JavaScript Patterns',
      description: 'Learn advanced patterns and techniques in JavaScript',
      content_type: 'course',
      confidence_score: 0.9,
      is_seen: false
    },
    {
      id: 2,
      title: 'CSS Grid Masterclass',
      description: 'Master CSS Grid layout system',
      content_type: 'course',
      confidence_score: 0.8,
      is_seen: true
    },
    {
      id: 3,
      title: 'Introduction to Machine Learning',
      description: 'Get started with ML concepts and algorithms',
      content_type: 'course',
      confidence_score: 0.7,
      is_seen: false
    }
  ]);
  const [showNewPathForm, setShowNewPathForm] = useState(false);
  const [newPath, setNewPath] = useState({ title: '', description: '' });

  const handlePreferenceChange = (field, value) => {
    setPreferences(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSavePreferences = () => {
    // In a real implementation, this would save to the API
    alert('Preferences saved successfully!');
  };

  const handleCreateLearningPath = () => {
    if (newPath.title.trim()) {
      const path = {
        id: learningPaths.length + 1,
        title: newPath.title,
        description: newPath.description,
        courses: [],
        is_active: true
      };
      setLearningPaths([path, ...learningPaths]);
      setNewPath({ title: '', description: '' });
      setShowNewPathForm(false);
    }
  };

  const handleMarkRecommendationSeen = (id) => {
    setRecommendations(prev => 
      prev.map(rec => 
        rec.id === id ? { ...rec, is_seen: true } : rec
      )
    );
  };

  const handleMarkRecommendationActedUpon = (id) => {
    setRecommendations(prev => 
      prev.map(rec => 
        rec.id === id ? { ...rec, is_seen: true, is_acted_upon: true } : rec
      )
    );
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">Personal Learning Experience</h2>
      
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
            activeTab === 'learning-paths'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-gray-700 dark:text-blue-400'
              : 'text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300'
          }`}
          onClick={() => setActiveTab('learning-paths')}
        >
          Learning Paths
        </button>
        <button
          className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
            activeTab === 'recommendations'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-gray-700 dark:text-blue-400'
              : 'text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300'
          }`}
          onClick={() => setActiveTab('recommendations')}
        >
          Recommendations
        </button>
      </div>
      
      <div className="mt-4">
        {activeTab === 'preferences' && (
          <div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Learning Preferences</h3>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Learning Style
                    </label>
                    <select
                      value={preferences.learning_style}
                      onChange={(e) => handlePreferenceChange('learning_style', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    >
                      <option value="visual">Visual</option>
                      <option value="auditory">Auditory</option>
                      <option value="kinesthetic">Kinesthetic</option>
                      <option value="reading">Reading/Writing</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Difficulty Level
                    </label>
                    <select
                      value={preferences.difficulty_level}
                      onChange={(e) => handlePreferenceChange('difficulty_level', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    >
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Preferred Language
                    </label>
                    <select
                      value={preferences.preferred_language}
                      onChange={(e) => handlePreferenceChange('preferred_language', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    >
                      <option value="en">English</option>
                      <option value="es">Spanish</option>
                      <option value="fr">French</option>
                      <option value="de">German</option>
                    </select>
                  </div>
                </div>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Study Habits</h3>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Study Time Preference
                    </label>
                    <select
                      value={preferences.study_time_preference}
                      onChange={(e) => handlePreferenceChange('study_time_preference', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    >
                      <option value="morning">Morning (6AM-12PM)</option>
                      <option value="afternoon">Afternoon (12PM-6PM)</option>
                      <option value="evening">Evening (6PM-10PM)</option>
                      <option value="night">Night (10PM-6AM)</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Notification Frequency
                    </label>
                    <select
                      value={preferences.notification_frequency}
                      onChange={(e) => handlePreferenceChange('notification_frequency', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    >
                      <option value="frequent">Frequent</option>
                      <option value="moderate">Moderate</option>
                      <option value="minimal">Minimal</option>
                    </select>
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
        
        {activeTab === 'learning-paths' && (
          <div>
            <div className="mb-6">
              {!showNewPathForm ? (
                <Button 
                  variant="primary" 
                  onClick={() => setShowNewPathForm(true)}
                >
                  Create New Learning Path
                </Button>
              ) : (
                <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 mb-6">
                  <h3 className="font-semibold text-gray-800 dark:text-white mb-3">Create New Learning Path</h3>
                  <div className="space-y-3">
                    <input
                      type="text"
                      value={newPath.title}
                      onChange={(e) => setNewPath({...newPath, title: e.target.value})}
                      placeholder="Learning path title"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-600 text-gray-900 dark:text-white"
                    />
                    <textarea
                      value={newPath.description}
                      onChange={(e) => setNewPath({...newPath, description: e.target.value})}
                      placeholder="Learning path description"
                      rows="3"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-600 text-gray-900 dark:text-white"
                    />
                    <div className="flex space-x-2">
                      <Button 
                        variant="primary" 
                        onClick={handleCreateLearningPath}
                      >
                        Create Path
                      </Button>
                      <Button 
                        variant="secondary" 
                        onClick={() => setShowNewPathForm(false)}
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                </div>
              )}
            </div>
            
            <div className="space-y-4">
              {learningPaths.map((path) => (
                <div key={path.id} className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-800 dark:text-white">{path.title}</h3>
                      <p className="text-gray-600 dark:text-gray-400 text-sm">{path.description}</p>
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      path.is_active 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' 
                        : 'bg-gray-100 text-gray-800 dark:bg-gray-600 dark:text-gray-200'
                    }`}>
                      {path.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                  
                  <div className="mt-3">
                    <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">Courses in this path:</h4>
                    <div className="space-y-2">
                      {path.courses.map((course) => (
                        <div key={course.id} className="flex justify-between items-center bg-white dark:bg-gray-600 p-2 rounded">
                          <span className="text-gray-800 dark:text-white">{course.title}</span>
                          <div className="flex items-center">
                            <div className="w-24 bg-gray-200 dark:bg-gray-500 rounded-full h-2 mr-2">
                              <div 
                                className="bg-blue-600 h-2 rounded-full" 
                                style={{ width: `${course.progress}%` }}
                              ></div>
                            </div>
                            <span className="text-sm text-gray-600 dark:text-gray-300">{course.progress}%</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {activeTab === 'recommendations' && (
          <div>
            <div className="space-y-4">
              {recommendations.map((recommendation) => (
                <div 
                  key={recommendation.id} 
                  className={`p-4 rounded-lg border ${
                    recommendation.is_seen 
                      ? 'bg-gray-50 dark:bg-gray-700 border-gray-200 dark:border-gray-600' 
                      : 'bg-blue-50 dark:bg-blue-900 border-blue-200 dark:border-blue-800'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold text-gray-800 dark:text-white">{recommendation.title}</h3>
                      <p className="text-gray-600 dark:text-gray-400 text-sm mt-1">{recommendation.description}</p>
                      <div className="flex items-center mt-2">
                        <span className="text-xs bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-200 px-2 py-1 rounded mr-2">
                          {recommendation.content_type}
                        </span>
                        <span className="text-xs text-gray-500 dark:text-gray-400">
                          Confidence: {(recommendation.confidence_score * 100).toFixed(0)}%
                        </span>
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      {!recommendation.is_seen && (
                        <Button 
                          variant="secondary" 
                          size="sm" 
                          onClick={() => handleMarkRecommendationSeen(recommendation.id)}
                        >
                          Mark Seen
                        </Button>
                      )}
                      <Button 
                        variant="primary" 
                        size="sm" 
                        onClick={() => handleMarkRecommendationActedUpon(recommendation.id)}
                      >
                        Start
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PersonalizationDashboard;