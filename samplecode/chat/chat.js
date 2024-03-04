const url = 'http://127.0.0.1:8000/message/';
const GOVBOTIC_API_TOKEN = 'your_api_token_here'; // Replace with your actual API token

const data = {
  persona: "examplePersona",
  uid: "exampleUID",
  message: "Health Benefits",
  document: "LemonPeel/LemmonPeels",
  context: "Asking about weather conditions in New York City.",
  maxTokens: 100,
  temperature: 0.5,
  topP: 0.9,
  stopSequences: ["\n"],
  sessionId: "exampleUID",
  language: "en-US",
  requestType: "query"
};

fetch(url, {
  method: 'POST', // Method itself
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${GOVBOTIC_API_TOKEN}` // Template literal for including the API token
  },
  body: JSON.stringify(data) // Converting the JavaScript object to a JSON string
})
.then(response => response.json()) // Parsing the JSON response
.then(json => console.log(json)) // Displaying the result in the console
.catch(error => console.error('Error:', error)); // Handling errors

