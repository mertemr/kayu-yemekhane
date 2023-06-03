const http = require('http');
const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const router = express.Router();
app.use('/', router);

app.use(cors({origin: '*'}));
app.use(express.static('web'));
app.set("views", path.join(__dirname, "views"));

app.set('view engine', 'html');
app.engine('html', require('ejs').renderFile);

const publicPath = path.resolve(__dirname, 'public');

app.get('/css/:file', (req, res) => {
    res.sendFile(publicPath + "/css/" + req.params.file);
});

app.get('/js/:file', (req, res) => {
    res.sendFile(publicPath + "/js/" + req.params.file);
});

router.get('/', (req, res) => {
    http.get('http://localhost:8080/menu', (response) => {
        let data = '';
        response.on('data', (chunk) => {
            data += chunk;
        });
        response.on('end', () => {
            res.render("index", { array: JSON.parse(data) });
        });
    }).on('error', (err) => {
        console.log('Error: ' + err.message);
    });
});

app.listen(80, () => {
    console.log('App running on http://127.0.0.1:80');
});
