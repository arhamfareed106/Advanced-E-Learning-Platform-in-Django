import React, { useState } from 'react';
import { Button } from '../components/Button';

const StudyGroup = ({ group, onJoin, onLeave, currentUser }) => {
  const [isMember, setIsMember] = useState(group.is_member || false);
  
  const handleJoin = () => {
    onJoin(group.id);
    setIsMember(true);
  };
  
  const handleLeave = () => {
    onLeave(group.id);
    setIsMember(false);
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 mb-4">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white">{group.name}</h3>
          <p className="text-gray-600 dark:text-gray-400 text-sm mt-1">{group.description}</p>
          <div className="flex items-center mt-2 text-sm text-gray-500 dark:text-gray-400">
            <span>{group.member_count} members</span>
            <span className="mx-2">•</span>
            <span>{group.course?.title || 'General'}</span>
          </div>
        </div>
        
        <div>
          {isMember ? (
            <Button 
              variant="secondary" 
              size="sm" 
              onClick={handleLeave}
              className="bg-red-100 hover:bg-red-200 text-red-700 dark:bg-red-900 dark:hover:bg-red-800 dark:text-red-200"
            >
              Leave Group
            </Button>
          ) : (
            <Button 
              variant="primary" 
              size="sm" 
              onClick={handleJoin}
              disabled={group.member_count >= group.max_members}
            >
              {group.member_count >= group.max_members ? 'Full' : 'Join Group'}
            </Button>
          )}
        </div>
      </div>
      
      <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">Recent Activity</h4>
        <ul className="text-sm text-gray-600 dark:text-gray-400">
          {group.recent_posts && group.recent_posts.slice(0, 2).map((post, index) => (
            <li key={index} className="mb-1 flex items-start">
              <span className="text-gray-400 mr-2">•</span>
              <span>{post.title}</span>
            </li>
          ))}
          {(!group.recent_posts || group.recent_posts.length === 0) && (
            <li>No recent activity</li>
          )}
        </ul>
      </div>
    </div>
  );
};

export default StudyGroup;