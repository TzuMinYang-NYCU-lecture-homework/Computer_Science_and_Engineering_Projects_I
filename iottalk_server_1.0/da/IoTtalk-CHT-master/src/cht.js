const connector = require(__base + 'cht/connector.js');
const MsgPassive = require(__base + 'cht/msgPassive.js');
const MsgActive = require(__base + 'cht/msgActive.js');



module.exports = {
    'onSlaveArrived': MsgPassive('OnSlaveArrived'),
    'onSlaveExited': MsgPassive('OnSlaveExited'),
    'onValueChanged': MsgPassive('OnValueChanged'),
    'getManagedSlaveList': MsgActive('GetManagedSlaveListReq', 'GetManagedSlaveListReply'),
    'getArrivedSlaveList': MsgActive('GetArrivedSlaveListReq', 'GetArrivedSlaveListReply'),
    'askValue': MsgActive('AskValueReq', undefined),
    'readValue': MsgActive('ReadValueReq', 'ReadValueReply'),
    'writeValue': MsgActive('WriteValueReq', 'WriteValueReply'),
    
    'close': function() {
        connector.close();
    },
    'onClose': function(cb) {
        connector.onClose(cb);
    }
};
