const express = require('express');
const axios = require('axios');
const fs = require('fs');
const app = express();

app.use(express.static('public'));

app.get('/run-script', (req, res) => {
    var url = 'http://10.10.1.189/capture';
    var url = "https://api.github.com/users/xiaotian/repos";

    console.log("Link is requested!");
    axios.get(url, { responseType: 'arraybuffer' })
    .then(response => {
        fs.writeFileSync('file.txt', Buffer.from(response.data, 'binary'));
        console.log('File saved successfully.');
        res.send({ status: 'success' });
    })
    .catch(Error,() => {
        console.log("There is an error when starting the server side " + error);
        res.send({status: 'failed'})
    })
});

var port = 80
app.listen(port, () => console.log(`Server listening on port ${port}`));