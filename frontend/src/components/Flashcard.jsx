import React, { useState } from 'react';
import { Button } from '../components/Button';

const Flashcard = ({ question, answer, onFlip = () => {}, isFlipped = false, className = '' }) => {
  const [flipped, setFlipped] = useState(isFlipped);

  const handleFlip = () => {
    const newFlipped = !flipped;
    setFlipped(newFlipped);
    onFlip(newFlipped);
  };

  return (
    <div 
      className={`relative w-full h-64 cursor-pointer perspective-1000 ${className}`}
      onClick={handleFlip}
    >
      <div className={`relative w-full h-full transition-transform duration-700 transform-style-3d ${flipped ? 'rotate-y-180' : ''}`}>
        {/* Front of card */}
        <div className={`absolute w-full h-full backface-hidden bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 flex flex-col justify-center items-center ${flipped ? 'hidden' : ''}`}>
          <div className="text-center">
            <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Question</h3>
            <p className="text-gray-700 dark:text-gray-300 text-center">{question}</p>
          </div>
          <div className="absolute bottom-4 text-sm text-gray-500 dark:text-gray-400">
            Click to flip
          </div>
        </div>
        
        {/* Back of card */}
        <div className={`absolute w-full h-full backface-hidden bg-blue-50 dark:bg-gray-700 rounded-lg shadow-md p-6 flex flex-col justify-center items-center rotate-y-180 ${!flipped ? 'hidden' : ''}`}>
          <div className="text-center">
            <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Answer</h3>
            <p className="text-gray-700 dark:text-gray-300 text-center">{answer}</p>
          </div>
          <div className="absolute bottom-4 text-sm text-gray-500 dark:text-gray-400">
            Click to flip back
          </div>
        </div>
      </div>
    </div>
  );
};

const FlashcardDeck = ({ title, cards = [], onCardReview = () => {} }) => {
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [reviewStatus, setReviewStatus] = useState({}); // Track review status for spaced repetition

  const currentCard = cards[currentCardIndex];
  
  if (!currentCard) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">{title}</h3>
        <p className="text-gray-600 dark:text-gray-400">No flashcards in this deck.</p>
      </div>
    );
  }

  const handleNext = () => {
    if (currentCardIndex < cards.length - 1) {
      setCurrentCardIndex(currentCardIndex + 1);
    }
  };

  const handlePrevious = () => {
    if (currentCardIndex > 0) {
      setCurrentCardIndex(currentCardIndex - 1);
    }
  };

  const handleCardReview = (difficulty) => {
    // Update review status for spaced repetition algorithm
    setReviewStatus(prev => ({
      ...prev,
      [currentCard.id]: { difficulty, reviewedAt: new Date() }
    }));
    
    onCardReview(currentCard, difficulty);
    
    // Move to next card after review
    if (currentCardIndex < cards.length - 1) {
      setCurrentCardIndex(currentCardIndex + 1);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">{title}</h3>
      
      <div className="mb-6">
        <Flashcard 
          question={currentCard.question} 
          answer={currentCard.answer} 
        />
      </div>
      
      <div className="flex justify-between items-center">
        <div className="text-sm text-gray-600 dark:text-gray-400">
          Card {currentCardIndex + 1} of {cards.length}
        </div>
        
        <div className="flex space-x-2">
          <Button 
            variant="secondary" 
            size="sm" 
            onClick={handlePrevious}
            disabled={currentCardIndex === 0}
          >
            Previous
          </Button>
          
          <div className="flex space-x-1">
            <Button 
              variant="success" 
              size="sm" 
              onClick={() => handleCardReview('easy')}
            >
              Easy
            </Button>
            <Button 
              variant="primary" 
              size="sm" 
              onClick={() => handleCardReview('medium')}
            >
              Medium
            </Button>
            <Button 
              variant="warning" 
              size="sm" 
              onClick={() => handleCardReview('hard')}
            >
              Hard
            </Button>
          </div>
          
          <Button 
            variant="secondary" 
            size="sm" 
            onClick={handleNext}
            disabled={currentCardIndex === cards.length - 1}
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  );
};

export { Flashcard, FlashcardDeck };