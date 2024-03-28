// src/components/ResultsDisplay.js
import React, { useContext } from 'react';
import './css/ResultsDisplay.css';
import AnalysisContext from '../AnalysisContext';
const ResultsDisplay = () => {
  const { results } = useContext(AnalysisContext);

  // Logic to display results if available
  return (
    <div className="results-display">
      {results && (
        <>
          <h2>Analysis Results</h2>
          {/* Render results here */}
        </>
      )}
    </div>
  );
};

export default ResultsDisplay;
