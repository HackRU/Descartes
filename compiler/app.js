const express = require('express');
const request = require('request');
const { exec } = require('child_process');

var app = express();

app.get('/', (req, res)=>{
  res.send("HELLOWORLD");
});

app.get('/file-ready', (req, res)=>{
  exec('python ../dump/test.py', (err, stdout, stderr)=>{
    if(stderr) {
      console.log(stderr);
    }
    console.log(stdout);
    res.status(200);
  });
});

app.listen(8080);
