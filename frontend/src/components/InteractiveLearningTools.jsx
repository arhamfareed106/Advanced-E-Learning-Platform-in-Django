import React, { useState } from 'react';
import CodeEditor from './CodeEditor';
import { FlashcardDeck } from './Flashcard';
import Whiteboard from './Whiteboard';
import { Button } from './Button';

const InteractiveLearningTools = () => {
  const [activeTool, setActiveTool] = useState('code-editor'); // code-editor, flashcards, whiteboard

  // Sample data for flashcards
  const sampleFlashcards = [
    {
      id: 1,
      question: 'What is React?',
      answer: 'React is a JavaScript library for building user interfaces.'
    },
    {
      id: 2,
      question: 'What is JSX?',
      answer: 'JSX is a syntax extension for JavaScript that looks similar to HTML.'
    },
    {
      id: 3,
      question: 'What is a React component?',
      answer: 'A component is a reusable piece of code that returns React elements.'
    }
  ];

  const handleCardReview = (card, difficulty) => {
    console.log(`Card reviewed: ${card.question}, Difficulty: ${difficulty}`);
  };

  const handleSaveDrawing = (drawingData) => {
    console.log('Drawing saved:', drawingData);
    alert('Drawing saved successfully!');
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">Interactive Learning Tools</h2>
      
      <div className="flex space-x-4 mb-6 border-b border-gray-200 dark:border-gray-700">
        <button
          className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
            activeTool === 'code-editor'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-gray-700 dark:text-blue-400'
              : 'text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300'
          }`}
          onClick={() => setActiveTool('code-editor')}
        >
          Code Editor
        </button>
        <button
          className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
            activeTool === 'flashcards'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-gray-700 dark:text-blue-400'
              : 'text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300'
          }`}
          onClick={() => setActiveTool('flashcards')}
        >
          Flashcards
        </button>
        <button
          className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
            activeTool === 'whiteboard'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-gray-700 dark:text-blue-400'
              : 'text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300'
          }`}
          onClick={() => setActiveTool('whiteboard')}
        >
          Whiteboard
        </button>
      </div>
      
      <div className="mt-4">
        {activeTool === 'code-editor' && (
          <CodeEditor 
            initialCode="// Write your JavaScript code here\nconsole.log('Hello, World!');"
            language="javascript"
            title="JavaScript Practice"
          />
        )}
        
        {activeTool === 'flashcards' && (
          <FlashcardDeck 
            title="React Fundamentals"
            cards={sampleFlashcards}
            onCardReview={handleCardReview}
          />
        )}
        
        {activeTool === 'whiteboard' && (
          <Whiteboard 
            title="Collaborative Whiteboard"
            onSave={handleSaveDrawing}
          />
        )}
      </div>
    </div>
  );
};

export default InteractiveLearningTools;