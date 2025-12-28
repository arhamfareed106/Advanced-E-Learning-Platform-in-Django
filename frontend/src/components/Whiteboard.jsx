import React, { useState, useRef, useEffect } from 'react';
import { Button } from '../components/Button';

const Whiteboard = ({ title = 'Whiteboard', onSave = () => {}, initialDrawing = null }) => {
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [tool, setTool] = useState('pen'); // pen, eraser
  const [color, setColor] = useState('#000000');
  const [lineWidth, setLineWidth] = useState(3);
  const [drawingHistory, setDrawingHistory] = useState([]);
  const [historyStep, setHistoryStep] = useState(-1);

  const colors = [
    '#000000', '#FF0000', '#00FF00', '#0000FF', 
    '#FFFF00', '#FF00FF', '#00FFFF', '#FFA500'
  ];

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    
    // Set initial drawing if provided
    if (initialDrawing) {
      // In a real implementation, this would restore the drawing from data
    }
  }, [initialDrawing]);

  const startDrawing = (e) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    setIsDrawing(true);
    const { offsetX, offsetY } = getEventOffset(e, canvas);
    
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY);
  };

  const draw = (e) => {
    if (!isDrawing) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    const { offsetX, offsetY } = getEventOffset(e, canvas);
    
    ctx.lineTo(offsetX, offsetY);
    ctx.strokeStyle = tool === 'eraser' ? '#FFFFFF' : color;
    ctx.lineWidth = lineWidth;
    ctx.stroke();
  };

  const stopDrawing = () => {
    if (isDrawing) {
      setIsDrawing(false);
      saveDrawingState();
    }
  };

  const getEventOffset = (e, canvas) => {
    let offsetX = 0, offsetY = 0;
    const rect = canvas.getBoundingClientRect();
    
    if (e.type.includes('touch')) {
      offsetX = e.touches[0].clientX - rect.left;
      offsetY = e.touches[0].clientY - rect.top;
    } else {
      offsetX = e.nativeEvent.offsetX;
      offsetY = e.nativeEvent.offsetY;
    }
    
    return { offsetX, offsetY };
  };

  const saveDrawingState = () => {
    const canvas = canvasRef.current;
    const newHistory = drawingHistory.slice(0, historyStep + 1);
    newHistory.push(canvas.toDataURL());
    setDrawingHistory(newHistory);
    setHistoryStep(newHistory.length - 1);
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    saveDrawingState();
  };

  const undo = () => {
    if (historyStep > 0) {
      const prevStep = historyStep - 1;
      setHistoryStep(prevStep);
      redrawFromHistory(prevStep);
    }
  };

  const redo = () => {
    if (historyStep < drawingHistory.length - 1) {
      const nextStep = historyStep + 1;
      setHistoryStep(nextStep);
      redrawFromHistory(nextStep);
    }
  };

  const redrawFromHistory = (step) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    img.onload = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0);
    };
    
    img.src = drawingHistory[step];
  };

  const saveDrawing = () => {
    const canvas = canvasRef.current;
    const dataUrl = canvas.toDataURL('image/png');
    onSave(dataUrl);
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-800 dark:text-white">{title}</h3>
        
        <div className="flex space-x-2">
          <Button 
            variant={tool === 'pen' ? 'primary' : 'secondary'} 
            size="sm" 
            onClick={() => setTool('pen')}
          >
            Pen
          </Button>
          <Button 
            variant={tool === 'eraser' ? 'primary' : 'secondary'} 
            size="sm" 
            onClick={() => setTool('eraser')}
          >
            Eraser
          </Button>
        </div>
      </div>
      
      <div className="flex flex-col items-center mb-4">
        <div className="flex space-x-2 mb-2">
          {colors.map((c) => (
            <button
              key={c}
              className={`w-6 h-6 rounded-full border-2 ${color === c ? 'border-gray-800 dark:border-gray-200' : 'border-gray-300 dark:border-gray-600'}`}
              style={{ backgroundColor: c }}
              onClick={() => setColor(c)}
              aria-label={`Select color ${c}`}
            />
          ))}
        </div>
        
        <div className="flex items-center space-x-2">
          <label className="text-sm text-gray-700 dark:text-gray-300">Size:</label>
          <input
            type="range"
            min="1"
            max="20"
            value={lineWidth}
            onChange={(e) => setLineWidth(e.target.value)}
            className="w-24"
          />
          <span className="text-sm text-gray-700 dark:text-gray-300 w-8">{lineWidth}px</span>
        </div>
      </div>
      
      <div className="relative mb-4 border border-gray-300 dark:border-gray-600 rounded">
        <canvas
          ref={canvasRef}
          width={800}
          height={500}
          onMouseDown={startDrawing}
          onMouseMove={draw}
          onMouseUp={stopDrawing}
          onMouseOut={stopDrawing}
          onTouchStart={startDrawing}
          onTouchMove={draw}
          onTouchEnd={stopDrawing}
          className="bg-white border-0 cursor-crosshair"
        />
      </div>
      
      <div className="flex justify-between items-center">
        <div className="flex space-x-2">
          <Button variant="secondary" size="sm" onClick={undo} disabled={historyStep <= 0}>
            Undo
          </Button>
          <Button variant="secondary" size="sm" onClick={redo} disabled={historyStep >= drawingHistory.length - 1}>
            Redo
          </Button>
          <Button variant="secondary" size="sm" onClick={clearCanvas}>
            Clear
          </Button>
        </div>
        
        <div className="flex space-x-2">
          <Button variant="secondary" size="sm" onClick={saveDrawing}>
            Save
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Whiteboard;