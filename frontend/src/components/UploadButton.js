// src/components/UploadButton.js
import './css/UploadButton.css';
import AnalysisContext from '../AnalysisContext';
import React, { useContext } from 'react';

const UploadButton = () => {
  const { handleFileSelect, setUploadError } = useContext(AnalysisContext); // Destructure setUploadError from the context
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.type.startsWith('audio/')) {
        handleFileSelect(file);
        setUploadError(''); // Reset the error message when a valid file is selected
      } else {
        // Set the error message when an invalid file is selected
        setUploadError('Please upload a valid audio file.');
      }
    }
  };

  return (
    <div>
      <button className="upload-button" onClick={() => document.getElementById('fileUpload').click()}>
        UPLOAD FILE
      </button>
      <input
        type="file"
        id="fileUpload"
        accept="audio/*" // This restricts the file dialog to only show audio files
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
    </div>
  );
};

export default UploadButton;
