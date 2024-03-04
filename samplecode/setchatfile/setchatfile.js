// Define variables
const govboticApiBaseUrl = "http://localhost:8000"; // Replace with the actual base URL
const endpoint = "/setfiledrawer/";
const url = `${govboticApiBaseUrl}${endpoint}`;
const bearerToken = "your_bearer_token_here"; // Replace with your actual bearer token

// JSON payload
const requestPayload = {
  requestType: "setchatfile",
  persona: "AI Assistant",
  uid: "user123",
  message: "/CHAINOFTHOUGHT/2201.11903",
  document: null,
  context: "User asks for help.",
  maxTokens: 150,
  temperature: 0.5,
  sessionId: "session456",
  language: "en"
};

// Fetch options
const fetchOptions = {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${bearerToken}`
  },
  body: JSON.stringify(requestPayload)
};

// Execute the HTTP request
fetch(url, fetchOptions)
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => console.log(data))
  .catch(error => console.error('There was a problem with your fetch operation:', error));

// Add additional logic to handle the response as needed

