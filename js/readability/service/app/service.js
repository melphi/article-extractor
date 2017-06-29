'use strict';

var jsdom = require('jsdom');
var readability = require('./readability');
var restify = require('restify');

var server = restify.createServer({
    name: 'readability-service',
    version: '1.0.0'
});
server.use(restify.acceptParser(server.acceptable));
server.use(restify.queryParser({mapParams: false}));
server.use(restify.bodyParser());

server.get('/health', function (req, res, next) {
    res.send({message: "I'm healthy :)"});
    return next();
});

server.post('/extract', function (req, res, next) {
    const dom = new jsdom.JSDOM(req.params.content);
    if (!dom || !dom.window.document) {
        res.send(400, 'HTML can not be parsed.');
        return next();
    }
    const result = new readability.Readability(req.params.url, dom.window.document).parse();
    if (!result) {
        res.send(200, {});
    } else {
        res.send(200, result);
    }
    return next();
});

server.listen(5000, function () {
    console.log('%s listening at %s', server.name, server.url);
});
