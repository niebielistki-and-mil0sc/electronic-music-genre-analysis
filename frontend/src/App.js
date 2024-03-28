// src/App.js

import React, { useState } from 'react';
import Header from './components/Header';
import UploadButton from './components/UploadButton';
import ProgressBar from './components/ProgressBar';
import ResultsDisplay from './components/ResultsDisplay';
import './App.css';
import AnalysisContext from './AnalysisContext';

function App() {
  const [file, setFile] = useState(null); // State for the uploaded file
  const [isAnalyzing, setIsAnalyzing] = useState(false); // State to track if analysis is in progress
  const [results, setResults] = useState(null); // State for the analysis results

  // Function to handle file selection
  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile);
    // You would also kick off the file upload process here
  };

  // Function to handle the analysis start
  const startAnalysis = () => {
    setIsAnalyzing(true);
    // This function would call the backend API to start the analysis process
  };

  // Function to handle the analysis results
  const handleResults = (analysisResults) => {
    setIsAnalyzing(false);
    setResults(analysisResults);
  };

  // The value you want to provide to all consuming components
  const contextValue = {
    file,
    isAnalyzing,
    results,
    handleFileSelect,
    startAnalysis,
    handleResults,
  };

  return (
    <AnalysisContext.Provider value={contextValue}>
      <div className="App">
        <Header />
        <UploadButton />
        {isAnalyzing && <ProgressBar />}
        {results && <ResultsDisplay />}
      </div>
    </AnalysisContext.Provider>
  );
}

export default App;