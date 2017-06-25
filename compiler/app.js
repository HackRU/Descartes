const express = require('express');
const request = require('request');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');
const config = require('./config.js');

var app = express();
var currentGist = "N/A";

app.use('/img', express.static(path.join(__dirname, '../dump')));
app.set('json spaces', 2);

app.get('/', (req, res)=>{
  res.send("HELLOWORLD");
});

// app.get('/img', (req, res)=>{
//   res.sendFile(path.join(__dirname,'../dump/img.jpg'));
// })

app.get('/gist', (req, res)=>{
  res.json({ url: currentGist });
});

app.get('/file-ready', (req, res)=>{
  var global_data = fs.readFileSync(path.join(__dirname, '../dump/test.py')).toString();
  exec('python '+ path.join(__dirname, '../dump/test.py'), (err, stdout, stderr)=>{
    var result;
    if(stderr) {
      result = stderr;
    } else {
      result = stdout;
    }
    request({
      method: 'POST',
      headers: {
        'User-Agent': 'dominusbelli',
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
      console.log();
      console.log();
      console.log();
      var parsedbody = JSON.parse(body);
      console.log(parsedbody.html_url);
      currentGist = parsedbody.html_url;
      res.json({result: result, url: currentGist});
    });
  });
});

app.post('/payload', (req, res)=>{
  var body = JSON.parse(res.body);
  console.log(body);
  fs.writeFile(path.join(__dirname, '../dump/test.py'), body, (err)=>{
    if (err) {
      console.log('shiiiit');
    }

  });
});

app.listen(8080);
