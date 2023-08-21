const express = require('express');
const updateyml = require('./update_yaml.js')
const axios = require('axios');
const fs = require('fs');
const labelImg = require('./labelImg.js');
const get_images = require('./model.js');
// const sqlite3 = require('sqlite3');
const execute = require('./sql.js');
// const train = require('./train.js');
const app = express();
const path = require('path');
const multer = require('multer');
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());
app.use(express.urlencoded());

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        if (file.fieldname === 'train_files') {
            cb(null, './labels/train/');
        } else if (file.fieldname === 'val_files') {
            cb(null, './labels/val/');
        } else {
            cb(new Error('Invalid fieldname'));
        }
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname);
    },
});

const upload = multer({ storage });




app.get("/", function (req, res) {
    res.sendFile(path.join(__dirname, './index.html'));
});
app.get("/learn", function (req, res) {
    res.sendFile(path.join(__dirname, './learn.html'));
});
app.post('/learn', (req, res) => {
    updateyml.updateYaml(req.body.new_class);
    get_images.get_images();
    res.redirect('/upload');
});
app.post('/upload', upload.fields([{ name: 'train_files', maxCount: 10 }, { name: 'val_files', maxCount: 10 }]), (req, res) => {
    const trainFiles = req.files['train_files'];
    const valFiles = req.files['val_files'];
    if (typeof trainFiles === 'undefined' || typeof valFiles === 'undefined') {
        res.redirect('/upload');
    }
    res.send("uploaded files successfully")
    // setTimeout(() => {
    //     train();
    // }, 2000)
    // res.send('training');
});
app.get('/upload', function (req, res) {
    res.sendFile(path.join(__dirname, './upload.html'));
    setTimeout(() => {
        labelImg();
    }, 16000);
});
app.get('/get-fridge', (req, res) => {
    let url = 'http://192.168.100.200/capture';
    axios.get(url, { responseType: 'arraybuffer' })
        .then(response => {
            fs.writeFileSync(`try.jpg`, Buffer.from(response.data, 'binary'));
        });
    execute()
        .then(items => {
            let result = '<table style="border-collapse: collapse; width: 100%;">';
            result += '<tr><th style="border: 1px solid black; padding: 8px;">Item</th><th style="border: 1px solid black; padding: 8px;">Quantity</th></tr>';
            if (items.length > 0) {
                for (let i = 0; i < items.length; i++) {
                    result += `<tr><td style="border: 1px solid black; padding: 8px;">${items[i][1]}</td><td style="border: 1px solid black; padding: 8px;">${items[i][0]}</td></tr>`;
                }
            }
            result += '</table>';
            res.send(result);
        })
        .catch(error => {
            console.error(error);
            res.status(500).send('An error occurred');
        });
})
var port = 80
app.listen(port, () => console.log(`Server listening on port ${port}`));
