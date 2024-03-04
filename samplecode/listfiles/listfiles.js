// Define variables
const govboticApiBaseUrl = 'http://127.0.0.1:8000';
const govboticApiToken = 'FIFTOKENFORMAT';
const endpoint = '/listfiledrawers/';

// JSON payload
const requestData = {
  requestType: "listfiles",
  dataOperands: "YourDataOperands",
  fileNames: ["file1.txt", "file2.txt"]
};

// Fetch options
const fetchOptions = {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${govboticApiToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(requestData)
};

// Execute the HTTP request
fetch(`${govboticApiBaseUrl}${endpoint}`, fetchOptions)
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => console.log(data))
  .catch(error => console.error('There was a problem with your fetch operation:', error));

