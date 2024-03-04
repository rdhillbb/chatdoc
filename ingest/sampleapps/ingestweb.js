  // Define the URL and the data to be sent
  const url = 'http://localhost:8050/ingestlocalweb/';
  const data = {
    request: "upload",
    filedrawer: "Garlic",
    filename: "https://www.webmd.com/vitamins/ai/ingredientmono-300/garlic"
  };

  // Configure the request options
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  };

  // Use fetch to send the request
  fetch(url, options)
    .then(response => response.json())  // Parse the JSON response
    .then(json => console.log(json))    // Hand

