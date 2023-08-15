const prot = 3000; // 端口号
const hostName = '127.0.0.1'; //代理服务器主机名
const express = require('express');
var bodyParser = require('body-parser');//解析,用req.body获取post参数
const morgan = require('morgan');
const aesObj = require("./aes_utls")
const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.get('/get_header_param',(req,res)=>{
    let timestamp = req.query.t;
    console.log(req.url)
    console.log('时间戳：',timestamp)
    s = aesObj.GetHeaderTimeStamp(timestamp)
    res.json({"code": 200,"headerTime":s})
})

app.post("/data",function(req,res){
    // console.log(JSON.stringify(req.body));
    let jd = JSON.parse(JSON.stringify(req.body));
    let timestamp = jd.timestamp;
    let body = jd.data;
    s = aesObj.AesDecryptData(body,timestamp)
    res.json({"code": 200,"data":s});
})

app.listen(prot,hostName,()=>{
    console.log(`server running.... at ${hostName}:${prot}`)
})