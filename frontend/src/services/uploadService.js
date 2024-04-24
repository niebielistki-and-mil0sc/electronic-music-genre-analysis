// src/services/uploadService.js

const API_URL = 'http://127.0.0.1:8000/api/predict-genre/';

const uploadFileToServer = async (file) => {
  const formData = new FormData();
  formData.append('file', file); // 'file' is the key that your Django backend expects for the file upload

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      body: formData,
    });

    console.log(response); // Log the raw response

    if (!response.ok) {
      throw new Error('File upload failed. Please try again.');
    }
    const responseData = await response.json();
    console.log("Response Data:", responseData); // Log the response data
    return responseData;
  } catch (error) {
    console.error('Upload service encountered an error:', error);
    throw error; // Just throw the error
  }
};

export default uploadFileToServer;
