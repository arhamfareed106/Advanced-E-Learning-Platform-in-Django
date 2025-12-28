import React, { useState, useEffect } from 'react';
import { Button } from '../components/Button';
import { Modal } from '../components/Modal';

const CodeEditor = ({ initialCode = '', language = 'javascript', title = 'New Code Editor' }) => {
  const [code, setCode] = useState(initialCode);
  const [output, setOutput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editorTitle, setEditorTitle] = useState(title);

  const languages = [
    { value: 'javascript', label: 'JavaScript' },
    { value: 'python', label: 'Python' },
    { value: 'html', label: 'HTML' },
    { value: 'css', label: 'CSS' },
    { value: 'java', label: 'Java' },
    { value: 'cpp', label: 'C++' },
  ];

  const runCode = async () => {
    setIsLoading(true);
    setOutput('Running code...');
    
    // In a real implementation, this would connect to a code execution API
    // For now, we'll simulate the execution
    setTimeout(() => {
      setOutput('Code executed successfully!\nHello, World!');
      setIsLoading(false);
    }, 1000);
  };

  const saveCode = () => {
    // Save code logic would go here
    alert('Code saved successfully!');
  };

  const handleLanguageChange = (e) => {
    // Language change logic would go here
    // For now, just update the state
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-800 dark:text-white">{editorTitle}</h3>
        <div className="flex space-x-2">
          <select
            value={language}
            onChange={handleLanguageChange}
            className="bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white rounded-md px-2 py-1 text-sm"
          >
            {languages.map((lang) => (
              <option key={lang.value} value={lang.value}>
                {lang.label}
              </option>
            ))}
          </select>
          <Button variant="primary" size="sm" onClick={() => setShowModal(true)}>
            Save
          </Button>
          <Button 
            variant="secondary" 
            size="sm" 
            onClick={runCode} 
            loading={isLoading}
            disabled={isLoading}
          >
            Run
          </Button>
        </div>
      </div>
      
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        className="w-full h-64 font-mono text-sm p-3 rounded border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-800 dark:text-white"
        placeholder="Write your code here..."
      />
      
      <div className="mt-4">
        <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">Output:</h4>
        <div className="bg-gray-900 text-green-400 font-mono text-sm p-3 rounded min-h-16 overflow-auto">
          {output || 'Click "Run" to execute your code...'}
        </div>
      </div>

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title="Save Code"
      >
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Title
            </label>
            <input
              type="text"
              value={editorTitle}
              onChange={(e) => setEditorTitle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              placeholder="Enter a title for your code"
            />
          </div>
          <div className="flex justify-end space-x-2">
            <Button variant="secondary" onClick={() => setShowModal(false)}>
              Cancel
            </Button>
            <Button 
              variant="primary" 
              onClick={() => {
                saveCode();
                setShowModal(false);
              }}
            >
              Save
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default CodeEditor;