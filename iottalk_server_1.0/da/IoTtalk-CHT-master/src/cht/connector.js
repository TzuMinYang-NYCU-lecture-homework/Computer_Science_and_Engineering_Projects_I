/*
*   Create websocket connection and doing authentication with cht server
*   Other module must used below exported method to communicate with cht:
*       register: regist a handler for specific cht's opcode
*       send: send string data to cht server, queuing if not yet authenticated
*       close: gracefully close websocket and exit process
*/
// Include dependency
const config = require(__base + 'config.js');
const logger = require(__base + 'logger.js');
const timestamp = require(__base + 'timestamp.js');
const WebSocket = require('ws');
const md5 = require('md5');

// Init connection
const ws = new WebSocket(config.CHT_URL);
var onCloseCallback = function() {};
logger.info('CHT: connecting to', config.CHT_URL);

// Quening data to be sent
var authenticated = false;
var toBeSent = [];

// Regitster cht op handler
// chtOpCode -> handlerFunction
// Init with authentication handler
// Exit process if fail to authentication
var opHandler = {
    'Introduce': function(data) {
        delete opHandler['Introduce'];
        
        var digest = md5(data['salt'].toString().concat(config.CHT_APIKEY));
        logger.info('CHT: challenge with digest:', digest);

        ws.send(JSON.stringify({
            "op": "ChallengeReq",
            "timestamp": timestamp.cht(),
            "seq": 0,
            "digest": digest,
        }));
    },

    'ChallengeReply': function(data) {
        delete opHandler['ChallengeReply'];

        if( data['sc'] === 200 )  {
            logger.info('CHT: challenge success!');
            authenticated = true;
            toBeSent.forEach(function(str) {
                ws.send(str);
            });
            toBeSent = null;
        }
        else {
            logger.warn('CHT: challenge failed. Reason', data['reason']);
            ws.close();
        }
    },

    'Heartbeat': function(data) {
        // Server use HeartBeat to keep connection
        // We no need to do anything
    },
};


/* Below define websocket event */
ws.on('open', function() {
    logger.info('CHT: connection success!');
    logger.info('CHT: protocal version:', ws.protocolVersion);
    logger.info('CHT: server supported feature:', ws.supports);
    logger.info('==========================================');
});


ws.on('message', function(data, flags) {
    try {
        data = JSON.parse(data);
        logger.log('\nCHT: received data:', data);
    }
    catch(e) {
        logger.error('CHT: error while parsing received message:', e, '\n');
        return;
    }
    
    // Dispatch data to correspond event handler
    var op = data['op'];
    if( opHandler[op] )
        opHandler[op](data);
    else
        logger.warn('CHT: no handler for op', op);
});


ws.on('close', function() {
    logger.info('==========================================');
    logger.info('CHT: total received', ws.bytesReceived, 'bytes from CHT.');
    logger.info('CHT: websocket connection closed.');
    onCloseCallback();
});


ws.on('error', function(error) {
    logger.error('CHT: error occur:', error);
});



module.exports = {
    'register': function(op, handler) {
        if( opHandler[op] )
            logger.warn('CHT: opHandler', op, 'was replaced by new one.');
        opHandler[op] = handler;
    },
    'send': function(str) {
        if( authenticated )
            ws.send(str);
        else
            toBeSent.push(str);
    },
    'close': function() {
        ws.close();
    },
    'onClose': function(cb) {
        onCloseCallback = cb;
    },
};
