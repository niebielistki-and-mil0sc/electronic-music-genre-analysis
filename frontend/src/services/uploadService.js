// Replace the hardcoded API_URL with the environment variable
const API_URL = process.env.REACT_APP_BACKEND_URL;

const uploadFileToServer = async (file) => {
  const formData = new FormData();
  formData.append('file', file); // 'file' is the key that your Django backend expects for the file upload

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      body: formData,
    });

    console.log("API URL used:", API_URL); // Log the API URL being used
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
