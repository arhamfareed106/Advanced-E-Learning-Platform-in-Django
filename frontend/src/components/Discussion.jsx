import React, { useState, useEffect } from 'react';
import { Button } from '../components/Button';
import { format } from 'date-fns';

const Discussion = ({ discussion, onComment, onLike, currentUser }) => {
  const [showComments, setShowComments] = useState(false);
  const [newComment, setNewComment] = useState('');

  const handleAddComment = () => {
    if (newComment.trim()) {
      onComment(discussion.id, newComment);
      setNewComment('');
    }
  };

  const handleLike = () => {
    onLike(discussion.id);
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 mb-4">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center mb-2">
            <div className="bg-gray-200 dark:bg-gray-600 rounded-full w-8 h-8 flex items-center justify-center mr-2">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                {discussion.author.username.charAt(0).toUpperCase()}
              </span>
            </div>
            <div>
              <h4 className="font-semibold text-gray-800 dark:text-white">{discussion.author.username}</h4>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                {format(new Date(discussion.created_at), 'MMM d, yyyy h:mm a')}
              </p>
            </div>
          </div>
          
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">{discussion.title}</h3>
          <p className="text-gray-700 dark:text-gray-300 mb-4">{discussion.content}</p>
          
          <div className="flex items-center space-x-4">
            <button 
              onClick={handleLike}
              className="flex items-center text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400"
            >
              <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905a3.61 3.61 0 01-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5"></path>
              </svg>
              {discussion.likes_count || 0}
            </button>
            <button 
              onClick={() => setShowComments(!showComments)}
              className="flex items-center text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400"
            >
              <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
              </svg>
              {discussion.comments_count || 0} comments
            </button>
          </div>
        </div>
      </div>
      
      {showComments && (
        <div className="mt-4 pl-4 border-l-2 border-gray-200 dark:border-gray-700">
          <div className="flex items-center mb-4">
            <input
              type="text"
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              placeholder="Add a comment..."
              className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-l-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
            <Button 
              variant="primary" 
              size="sm" 
              onClick={handleAddComment}
              className="rounded-l-none"
            >
              Post
            </Button>
          </div>
          
          {discussion.comments && discussion.comments.map((comment) => (
            <div key={comment.id} className="flex items-start mb-3">
              <div className="bg-gray-200 dark:bg-gray-600 rounded-full w-6 h-6 flex items-center justify-center mr-2 mt-1">
                <span className="text-xs font-medium text-gray-700 dark:text-gray-300">
                  {comment.author.username.charAt(0).toUpperCase()}
                </span>
              </div>
              <div className="flex-1">
                <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
                  <div className="flex justify-between">
                    <span className="font-medium text-gray-800 dark:text-white">{comment.author.username}</span>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      {format(new Date(comment.created_at), 'MMM d, h:mm a')}
                    </span>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300 mt-1">{comment.content}</p>
                </div>
                <div className="flex items-center mt-1 ml-2">
                  <button className="text-xs text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400">
                    Like ({comment.upvotes_count || 0})
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Discussion;