// src/App.js

import React, { useState } from 'react';
import Header from './components/Header';
import UploadButton from './components/UploadButton';
import ProgressBar from './components/ProgressBar';
import ResultsDisplay from './components/ResultsDisplay';
import './App.css';
import AnalysisContext from './AnalysisContext';
import uploadFileToServer from './services/uploadService';

function App() {
  const [file, setFile] = useState(null); // State for the uploaded file
  const [isAnalyzing, setIsAnalyzing] = useState(false); // State to track if analysis is in progress
  const [results, setResults] = useState(null); // State for the analysis results
  const [uploadError, setUploadError] = useState('');

  // Function to handle file selection
  const handleFileSelect = async (selectedFile) => {
    setFile(selectedFile);
    setUploadError(''); // Reset any previous error messages
    setIsAnalyzing(true); // Indicate that the upload and analysis process has begun

    try {
      const analysisResults = await uploadFileToServer(selectedFile);
      handleResults(analysisResults);
    } catch (error) {
      setUploadError(error.message); // Display any error messages during the upload process
    } finally {
      setIsAnalyzing(false); // Reset the analyzing state regardless of success or error
    }
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
    uploadError,
    setUploadError,
    handleFileSelect,
    startAnalysis,
    handleResults,
  };


  return (
    <AnalysisContext.Provider value={contextValue}>
      <div className="App">
        <Header />
        {uploadError && <div className="error-message">{uploadError}</div>} {/* This line displays the error */}
        <UploadButton />
        {isAnalyzing && <ProgressBar />}
        {results && <ResultsDisplay />}
      </div>
    </AnalysisContext.Provider>
  );

}

export default App;