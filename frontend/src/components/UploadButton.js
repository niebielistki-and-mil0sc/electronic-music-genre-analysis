// src/components/UploadButton.js
import './css/UploadButton.css';
import AnalysisContext from '../AnalysisContext';
import React, { useContext } from 'react';

const UploadButton = () => {
  const { handleFileSelect } = useContext(AnalysisContext);
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      handleFileSelect(file);
      // Optionally, start analysis right after file selection
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
        style={{ display: 'none' }}
        onChange={handleFileChange} // Changed from handleFileUpload to handleFileChange
      />
    </div>
  );
};

export default UploadButton;
