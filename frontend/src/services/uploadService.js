// src/services/uploadService.js

const API_URL = 'http://127.0.0.1:8000/api/predict-genre/';

const uploadFileToServer = async (file) => {
  const formData = new FormData();
  formData.append('file', file); // 'file' is the key that your Django backend expects for the file upload

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      body: formData,
      // You may need to include headers for CSRF if you have CSRF protection enabled in Django
    });

    if (!response.ok) {
      throw new Error('File upload failed. Please try again.');
    }

    return await response.json(); // This should be the analysis result from your Django backend
  } catch (error) {
    console.error('Upload service encountered an error:', error);
    throw error;
  }
};

export default uploadFileToServer;
