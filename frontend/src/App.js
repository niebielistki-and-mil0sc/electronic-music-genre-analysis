// src/App.js
import './index.css'
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
  const [fileName, setFileName] = useState('');

  // Function to handle file selection
  const handleFileSelect = async (selectedFile) => {
    setFile(selectedFile);
    setFileName(selectedFile.name); // Add this line to save the file name
    setResults(null); // Reset results when new file is selected
    setUploadError(''); // Reset any previous error messages
    setIsAnalyzing(true); // Indicate that the upload and analysis process has begun

    try {
      const analysisResults = await uploadFileToServer(selectedFile);
      console.log("Analysis Results:", analysisResults); // Log the results to ensure they're received
      handleResults(analysisResults);
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadError('Error: ' + error.message); // Update: Ensure this line properly updates the state
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
    fileName,
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