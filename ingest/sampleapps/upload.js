// Importing node-fetch and form-data in ES module syntax
import fetch from 'node-fetch';
import FormData from 'form-data';
import fs from 'fs';

const url = 'http://localhost:8050/uploadfile/';
const formData = new FormData();

// Add the 'filedrawer' field and files
formData.append('filedrawer', 'GovBotic');
formData.append('files', fs.createReadStream('.docs/garlic_antioxidants.pdf'));
formData.append('files', fs.createReadStream('.docs/nutrients-14-01183.pdf'));

// Set up the fetch options
const options = {
  method: 'POST',
  body: formData,
  headers: formData.getHeaders(),
};

// Perform the fetch request
fetch(url, options)
  .then(response => response.json())
  .then(json => console.log(json))
  .catch(err => console.error('Error:', err));

