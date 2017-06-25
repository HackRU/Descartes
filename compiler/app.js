const express = require('express');
const request = require('request');
const path = require('path');
const fs = require('fs');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const config = require('./config.js');

var app = express();
var currentGist = "N/A";

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

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

});

app.post('/payload', (req, res)=>{
  console.log(req);
  var body = req.body;
  console.log(req.body);
  console.log(body);
  var resultdata = body.data.replace(/\\\\/g,"");
  resultdata = unescape(resultdata);
  console.log(resultdata);
  fs.writeFile(path.join(__dirname, '../dump/test.py'), resultdata, (err)=>{
    if (err) {
      console.log(err);
    }
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
});

app.listen(8080);
