// src/components/ProgressBar.js
import React, { useContext } from 'react';
import './css/ProgressBar.css';
import AnalysisContext from '../AnalysisContext';

const ProgressBar = () => {
  const { isAnalyzing } = useContext(AnalysisContext);

  return (
    <div className="progress-bar-container" style={{ visibility: isAnalyzing ? 'visible' : 'hidden' }}>
      <div className="progress-bar">
        Analysis in progress...
      </div>
    </div>
  );
};

export default ProgressBar;
