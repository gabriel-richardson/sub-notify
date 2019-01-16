var request = require('request');
const cheerio = require('cheerio');
const j = request.jar();
request = request.defaults({jar:j});
request.get({
    jar: j,
    url: 'https://login.frontlineeducation.com/login?signin=&productId=ABSMGMT&clientId=ABSMGMT#/login',
}, function (err, res, body) {
    request.post({
        jar: j,
        url: 'https://login.frontlineeducation.com/login?signin=&productId=ABSMGMT&clientId=ABSMGMT#/login',
        form: {
            Username: '',
            Password: ''
        }
    }, function (err, res, body) {
        request.get({
            url: 'https://adminweb.aesoponline.com/access'
        }, function (err, res, body) {
            request.get({
                
            })
        });
    });
});