// src/components/ProgressBar.js
import React, { useContext } from 'react';
import './css/ProgressBar.css';
import AnalysisContext from '../AnalysisContext';

const ProgressBar = () => {
  const { isAnalyzing } = useContext(AnalysisContext);
  const text = "ANALYSIS IN PROGRESS...";

  // Map each character to a span with the letter-animation class
  const letters = text.split('').map((letter, index) => (
    <span key={index} className="letter-animation" style={{ '--i': index }}>
      {letter}
    </span>
  ));

  return (
    <div className="progress-bar-container" style={{ visibility: isAnalyzing ? 'visible' : 'hidden' }}>
      <div className="progress-bar">
        {letters}
      </div>
    </div>
  );
};

export default ProgressBar;
