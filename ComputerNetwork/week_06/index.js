// 모듈 호출 및 객체 생성
const bodyParser = require('body-parser');
const express = require('express');
const app = express();
const port = 3000;
const methodOverride = require('method-override');
const router = require('./routes/home') (app);

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:true}));
// views/home으로 ejs 파일의 위치 지정
app.set('views', __dirname + '/views/home');
// 서버가 HTML 랜더링을 할 때 EJS 엔진을 사용하도록 설정
app.set('view engine', 'ejs');
app.engine('html', require('ejs').renderFile);
// 정적 파일을 다루기 위한 코드 (css파일)
app.use(express.static(__dirname+'/public'));
// PUT, DELETE method 허옹
app.use(methodOverride('_method'));

// 서버를 연결하고 function() 이용
const server = app.listen(port, function() {
    console.log(`Example app listening at http://localhost:${port}`);
});


