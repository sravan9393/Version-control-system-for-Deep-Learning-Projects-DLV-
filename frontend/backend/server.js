const express = require('express');
const upload = require('./upload');
const cors = require('cors');
// const listImages = require('./listImages');

const server = express();

var corsOptions = {
  origin: '*',
  optionsSuccessStatus: 200
};

server.use(cors(corsOptions));

server.post('/upload', upload);
// server.post('/getImages', listImages);
// server.get('/getImages1', listImages);

server.listen(3000, () => {
  console.log('Server started!');
});
