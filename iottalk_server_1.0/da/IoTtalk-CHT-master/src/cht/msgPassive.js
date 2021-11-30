/*
*   We only passively listen for below opcode:
*       OnSlaveArrived, OnSlaveExited, OnValueChanged
*/
// Include dependency
const connector = require(__base + 'cht/connector.js');

// Closure creator
var MsgPassive = function(opcode) {
    var callbacks = [];
    connector.register(opcode, function(data) {
        callbacks.forEach(function(cb) {
            cb(data);
        });
    });

    return (function(cb) {
        callbacks.push(cb);
    });
};



module.exports = MsgPassive;
