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

const api_ip   = process.env.API_IP   || "localhost";
const api_port = process.env.API_PORT || 8080;

app.get('/css/:file', (req, res) => {
    res.sendFile(publicPath + "/css/" + req.params.file);
});

app.get('/js/:file', (req, res) => {
    res.sendFile(publicPath + "/js/" + req.params.file);
});

router.get('/', (req, res) => {
    http.get(`http://${api_ip}:${api_port}/menu`, (response) => {
        let data = "";
        response.on("data", (chunk) => {
            data += chunk;
        });
        response.on("end", () => {
            res.render("index", { array: JSON.parse(data) });
        });
    }).on("error", (err) => {
        console.log("Error: " + err.message);
    });
});

const PORT = process.env.PORT || 80;
const HOST = "0.0.0.0";

app.listen(PORT, HOST, () => {
    console.log(`Server running on ${HOST}:${PORT}`);
});
