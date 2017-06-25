const express = require('express');
const request = require('request');
const path = require('path');
const { exec } = require('child_process');

var app = express();

app.use('/img', express.static(path.join(__dirname, '../dump')));

app.get('/', (req, res)=>{
  res.send("HELLOWORLD");
});

// app.get('/img', (req, res)=>{
//   res.sendFile(path.join(__dirname,'../dump/img.jpg'));
// })

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
