const express = require('express')
const app = express();

app.use(express.json)

const PORT = 3000;

app.get('/',(req,res)=>{
    res.send('welcome to the Server');
})

app.post('/data',(req,res)=> {
    const receivedData = req.body;
    res.send()
})

app.listen(PORT, ()=> {
    console.log(`The server is run on http://localhost:${PORT}`);
})

app.listen(PORT, ()=> {
    console.log(`The server is run on http://localhost:${PORT}`);
})