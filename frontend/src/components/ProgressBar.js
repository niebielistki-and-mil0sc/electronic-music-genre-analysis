// src/components/ProgressBar.js
import React, { useContext } from 'react';
import './css/ProgressBar.css';
import AnalysisContext from '../AnalysisContext';
const ProgressBar = () => {
  const { isAnalyzing } = useContext(AnalysisContext);

  // Logic to display the progress bar if analyzing
  if (isAnalyzing) {
    return <div className="progress-bar">Analysis in progress...</div>;
  } else {
    return null;
  }
};

export default ProgressBar;
