// Include dependency
const config = require(__base + 'config.js');
const logger = require(__base + 'logger.js');
const request = require('request');


function attach(url, profile) {
    const option = {
        timeout: config.IOTTALK_TIMEOUT,
        body: {'profile': profile},
        json: true,
    };
    return new Promise(function(fulfill, reject) {

        var lastTimestamp = Date.now();
        
        request.post(url, option, function(err, http, body) {
            if(!err && http.statusCode === 200) {
                logger.info('IoTtalk: attached', url);
                fulfill(body);
            }
            else {
                if( http )
                    logger.error('IoTtalk: fail to attach', url, 'due to:', http.statusCode, body);
                else if( Date.now()-lastTimestamp >= config.IOTTALK_TIMEOUT )
                    logger.error('IoTtalk: timeout while attach');
                reject(body);
            }
        });

    });
}


function detach(url) {
    const option = {
        timeout: config.IOTTALK_TIMEOUT,
    };
    return new Promise(function(fulfill, reject) {

        var lastTimestamp = Date.now();

        request.devare(url, option, function(err, http, body) {
            if(!err && http.statusCode === 200) {
                logger.info('IoTtalk: detached', url);
                fulfill(body);
            }
            else {
                if(http)
                    logger.error('IoTtalk: fail to detach', url, 'due to:', http.statusCode, body);
                else if( Date.now()-lastTimestamp >= config.IOTTALK_TIMEOUT )
                    logger.error('IoTtalk: timeout while detach');
                reject(body);
            }
        });

    });
}


function update(url, value) {
    const option = {
        timeout: config.IOTTALK_TIMEOUT,
        body: {'data': [value]},
        json: true,
    };
    return new Promise(function(fulfill, reject) {

        var lastTimestamp = Date.now();

        request.put(url, option, function(err, http, body) {
            if(!err && http.statusCode === 200)
                fulfill(body);
            else {
                if(http)
                    logger.error('IoTtalk: fail to update', url, 'due to:', http.statusCode, body);
                else if( Date.now()-lastTimestamp >= config.IOTTALK_TIMEOUT )
                    logger.error('IoTtalk: timeout while update');
                reject(body);
            }
        });

    });
}


function get(url) {
    const option = {
        timeout: config.IOTTALK_TIMEOUT,
    };
    return new Promise(function(fulfill, reject) {

        var lastTimestamp = Date.now();

        request.get(url, option, function(err, http, body) {
            if(!err && http.statusCode === 200) {
                try {
                    fulfill(JSON.parse(body)['samples'][0]);
                }
                catch(e) {
                    reject(body);
                }
            }
            else {
                if(http)
                    logger.error('IoTtalk: fail to get', url, 'due to:', http.statusCode, body);
                else if( Date.now()-lastTimestamp > config.IOTTALK_TIMEOUT )
                    logger.error('IoTtalk: timeout while get');
                reject(body);
            }
        });

    });
}



module.exports = {
    'attach': attach,
    'detach': detach,
    'update': update,
    'get': get,
}

