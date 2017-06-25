const express = require('express');
const request = require('request');

var app = express();

app.get('/', function(req, res){
  res.send("HELLOWORLD");
});

app.listen(8080);
