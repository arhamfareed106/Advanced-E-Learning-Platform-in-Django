import React, { useState, useEffect } from 'react';
import Discussion from './Discussion';
import StudyGroup from './StudyGroup';
import { Button } from './Button';

const SocialLearningHub = () => {
  const [activeTab, setActiveTab] = useState('discussions'); // discussions, study-groups, connections
  const [discussions, setDiscussions] = useState([]);
  const [studyGroups, setStudyGroups] = useState([]);
  const [newDiscussion, setNewDiscussion] = useState({ title: '', content: '' });
  const [newGroup, setNewGroup] = useState({ name: '', description: '' });
  const [showNewDiscussionForm, setShowNewDiscussionForm] = useState(false);
  const [showNewGroupForm, setShowNewGroupForm] = useState(false);
  
  // Mock data for demonstration
  const mockDiscussions = [
    {
      id: 1,
      title: 'Understanding React Hooks',
      content: 'Can someone explain the difference between useState and useEffect hooks?',
      author: { username: 'john_doe' },
      created_at: new Date().toISOString(),
      likes_count: 5,
      comments_count: 3,
      comments: [
        {
          id: 1,
          content: 'useState is for managing state, useEffect is for side effects.',
          author: { username: 'jane_smith' },
          created_at: new Date().toISOString(),
          upvotes_count: 2
        }
      ]
    },
    {
      id: 2,
      title: 'Best practices for API calls in React',
      content: 'What are the recommended approaches for handling API calls in React components?',
      author: { username: 'alice_wonder' },
      created_at: new Date().toISOString(),
      likes_count: 8,
      comments_count: 5
    }
  ];
  
  const mockStudyGroups = [
    {
      id: 1,
      name: 'React Masterclass',
      description: 'Study group for advanced React concepts',
      member_count: 12,
      max_members: 15,
      is_member: true,
      course: { title: 'Advanced React' },
      recent_posts: [
        { title: 'Week 3: Context API Deep Dive' },
        { title: 'Week 2: Custom Hooks' }
      ]
    },
    {
      id: 2,
      name: 'Python for Beginners',
      description: 'Group for learning Python fundamentals',
      member_count: 8,
      max_members: 10,
      is_member: false,
      course: { title: 'Python Basics' },
      recent_posts: [
        { title: 'Week 1: Variables and Data Types' }
      ]
    }
  ];

  useEffect(() => {
    // In a real implementation, fetch data from API
    setDiscussions(mockDiscussions);
    setStudyGroups(mockStudyGroups);
  }, []);

  const handleAddDiscussion = () => {
    if (newDiscussion.title.trim() && newDiscussion.content.trim()) {
      const discussion = {
        id: discussions.length + 1,
        title: newDiscussion.title,
        content: newDiscussion.content,
        author: { username: 'current_user' },
        created_at: new Date().toISOString(),
        likes_count: 0,
        comments_count: 0,
        comments: []
      };
      
      setDiscussions([discussion, ...discussions]);
      setNewDiscussion({ title: '', content: '' });
      setShowNewDiscussionForm(false);
    }
  };

  const handleAddGroup = () => {
    if (newGroup.name.trim()) {
      const group = {
        id: studyGroups.length + 1,
        name: newGroup.name,
        description: newGroup.description,
        member_count: 1,
        max_members: 15,
        is_member: true,
        course: { title: 'General' },
        recent_posts: []
      };
      
      setStudyGroups([group, ...studyGroups]);
      setNewGroup({ name: '', description: '' });
      setShowNewGroupForm(false);
    }
  };

  const handleComment = (discussionId, comment) => {
    console.log(`Comment added to discussion ${discussionId}: ${comment}`);
    // In a real implementation, this would update the discussion with the new comment
  };

  const handleLike = (discussionId) => {
    console.log(`Liked discussion ${discussionId}`);
    // In a real implementation, this would update the like count
  };

  const handleJoinGroup = (groupId) => {
    console.log(`Joined group ${groupId}`);
    // In a real implementation, this would update the group membership
  };

  const handleLeaveGroup = (groupId) => {
    console.log(`Left group ${groupId}`);
    // In a real implementation, this would update the group membership
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">Social Learning Hub</h2>
      
      <div className="flex space-x-4 mb-6 border-b border-gray-200 dark:border-gray-700">
        <button
          className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
            activeTab === 'discussions'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-gray-700 dark:text-blue-400'
              : 'text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300'
          }`}
          onClick={() => setActiveTab('discussions')}
        >
          Discussions
        </button>
        <button
          className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
            activeTab === 'study-groups'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-gray-700 dark:text-blue-400'
              : 'text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300'
          }`}
          onClick={() => setActiveTab('study-groups')}
        >
          Study Groups
        </button>
        <button
          className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
            activeTab === 'connections'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-gray-700 dark:text-blue-400'
              : 'text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300'
          }`}
          onClick={() => setActiveTab('connections')}
        >
          Connections
        </button>
      </div>
      
      <div className="mt-4">
        {activeTab === 'discussions' && (
          <div>
            <div className="mb-6">
              {!showNewDiscussionForm ? (
                <Button 
                  variant="primary" 
                  onClick={() => setShowNewDiscussionForm(true)}
                >
                  Start New Discussion
                </Button>
              ) : (
                <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 mb-6">
                  <h3 className="font-semibold text-gray-800 dark:text-white mb-3">Start New Discussion</h3>
                  <div className="space-y-3">
                    <input
                      type="text"
                      value={newDiscussion.title}
                      onChange={(e) => setNewDiscussion({...newDiscussion, title: e.target.value})}
                      placeholder="Discussion title"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-600 text-gray-900 dark:text-white"
                    />
                    <textarea
                      value={newDiscussion.content}
                      onChange={(e) => setNewDiscussion({...newDiscussion, content: e.target.value})}
                      placeholder="What would you like to discuss?"
                      rows="4"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-600 text-gray-900 dark:text-white"
                    />
                    <div className="flex space-x-2">
                      <Button 
                        variant="primary" 
                        onClick={handleAddDiscussion}
                      >
                        Post Discussion
                      </Button>
                      <Button 
                        variant="secondary" 
                        onClick={() => setShowNewDiscussionForm(false)}
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                </div>
              )}
            </div>
            
            <div>
              {discussions.map((discussion) => (
                <Discussion
                  key={discussion.id}
                  discussion={discussion}
                  onComment={handleComment}
                  onLike={handleLike}
                  currentUser={{ id: 1, username: 'current_user' }}
                />
              ))}
            </div>
          </div>
        )}
        
        {activeTab === 'study-groups' && (
          <div>
            <div className="mb-6">
              {!showNewGroupForm ? (
                <Button 
                  variant="primary" 
                  onClick={() => setShowNewGroupForm(true)}
                >
                  Create Study Group
                </Button>
              ) : (
                <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 mb-6">
                  <h3 className="font-semibold text-gray-800 dark:text-white mb-3">Create Study Group</h3>
                  <div className="space-y-3">
                    <input
                      type="text"
                      value={newGroup.name}
                      onChange={(e) => setNewGroup({...newGroup, name: e.target.value})}
                      placeholder="Group name"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-600 text-gray-900 dark:text-white"
                    />
                    <textarea
                      value={newGroup.description}
                      onChange={(e) => setNewGroup({...newGroup, description: e.target.value})}
                      placeholder="Group description"
                      rows="3"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-600 text-gray-900 dark:text-white"
                    />
                    <div className="flex space-x-2">
                      <Button 
                        variant="primary" 
                        onClick={handleAddGroup}
                      >
                        Create Group
                      </Button>
                      <Button 
                        variant="secondary" 
                        onClick={() => setShowNewGroupForm(false)}
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                </div>
              )}
            </div>
            
            <div>
              {studyGroups.map((group) => (
                <StudyGroup
                  key={group.id}
                  group={group}
                  onJoin={handleJoinGroup}
                  onLeave={handleLeaveGroup}
                  currentUser={{ id: 1, username: 'current_user' }}
                />
              ))}
            </div>
          </div>
        )}
        
        {activeTab === 'connections' && (
          <div>
            <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6">
              <h3 className="font-semibold text-gray-800 dark:text-white mb-4">Your Connections</h3>
              <p className="text-gray-600 dark:text-gray-400">Connect with other learners to enhance your learning experience.</p>
              
              <div className="mt-6">
                <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-3">Suggested Connections</h4>
                <div className="space-y-3">
                  {[1, 2, 3].map((id) => (
                    <div key={id} className="flex items-center justify-between p-3 bg-white dark:bg-gray-600 rounded-md">
                      <div className="flex items-center">
                        <div className="bg-gray-200 dark:bg-gray-500 rounded-full w-10 h-10 flex items-center justify-center mr-3">
                          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                            U{id}
                          </span>
                        </div>
                        <div>
                          <div className="font-medium text-gray-800 dark:text-white">User {id}</div>
                          <div className="text-xs text-gray-500 dark:text-gray-400">Learner</div>
                        </div>
                      </div>
                      <Button variant="primary" size="sm">Connect</Button>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SocialLearningHub;