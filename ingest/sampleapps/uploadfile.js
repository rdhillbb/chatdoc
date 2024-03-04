const fetch = require('node-fetch'); // For Node.js

const url = 'http://localhost:8050/ingestlocalweb/';
const data = {
    request: "upload", 
    filedrawer: "GARLIC", 
    filename: "https://downloads.hindawi.com/journals/tswj/2021/8817288.pdf"
};

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json' 
    },
    body: JSON.stringify(data) 
})
.then(response => response.json()) // Assuming the response is also JSON
.then(data => console.log(data))
.catch(error => console.error(error));

