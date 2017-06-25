const express = require('express');
const request = require('request');
const { exec } = require('child_process');

var app = express();

app.get('/', (req, res)=>{
  res.send("HELLOWORLD");
});

app.get('/file-ready', (req, res)=>{
  exec('python ../dump/test.py', (err, stdout, stderr)=>{
    var result;
    if(stderr) {
      result = stderr;
    } else {
      result = stdout;
    }
    res.send(result);
  });
});

app.listen(8080);
