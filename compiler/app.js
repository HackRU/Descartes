const express = require('express');
const request = require('request');
const path = require('path');
const { exec } = require('child_process');
const config = require('./config.js');

var app = express();
var global_data = fs.readFileSync('../dump/test.py').toString();

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
    request({
      method: 'POST',
      headers: {
        'User-Agent': 'michaelyoo',
        Authorization: config.GitHubAPIKey
      },
      body: JSON.stringify({
        description: 'whatever you want',
        public: true,
        files: {
          'test.py': {
            content: global_data
          }
        }
      }),
      uri:"https://api.github.com/gists"

    }, function(error, response, body){
      console.log('error:', error);
      console.log('statusCode:', response.statusCode);
      console.log('body:', body);
    })
  });
});

app.listen(8080);
