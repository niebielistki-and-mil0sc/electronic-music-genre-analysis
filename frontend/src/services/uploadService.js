const API_URL = process.env.REACT_APP_BACKEND_URL;
console.log('API URL:', API_URL);  // Log the API URL to debug

const uploadFileToServer = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      body: formData,
      // Include headers if necessary, e.g., for CSRF
    });

    if (!response.ok) {
      throw new Error('File upload failed. Please try again.');
    }

    return await response.json();  // Parse the JSON response
  } catch (error) {
    console.error('Upload service encountered an error:', error);
    throw error;
  }
};

export default uploadFileToServer;
