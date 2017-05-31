'use strict';

const express = require('express');
const uuidV4 = require('uuid/v4');

// Constants
const PORT = 8080;

// App
const app = express();
app.get('/', function (req, res) {
    res.send('Hello world v4\n');
    console.log(uuidV4());
});

app.listen(PORT);
console.log('Running on http://localhost:' + PORT);
