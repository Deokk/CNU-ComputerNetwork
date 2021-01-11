// Request가 발생했을 때 서버에서 어떤 작업을 할 지 결정
module.exports = function(app) {

    app.get('/', function(req, res) {
        res.render('welcome.ejs')
    });

    app.get('/about', function(req, res) {
        res.render('about.ejs');
    })
}


