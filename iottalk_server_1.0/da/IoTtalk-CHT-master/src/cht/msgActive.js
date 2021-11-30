// Include dependency
const connector = require(__base + 'cht/connector.js');
const timestamp = require(__base + 'timestamp.js');

// Closure creator
var MsgActive = function(triggerOpcode, feedbackOpcode) {
    // Registered op handler
    // As spec said, seq identify which request it reponse to.
    var __seq = -1;
    var handlers = {};

    // Listen for feedback.
    if( feedbackOpcode !== undefined )
        connector.register(feedbackOpcode, function(data) {
            var seq = data['seq'];
            if( data['sc'] === 200 )
                handlers[seq].fulfill(data);
            else
                handlers[seq].reject(data);
            delete handlers[seq];
        });

    // Output trigger. Handler feeadback with Promise.
    return (function(args) {
        return new Promise(function(fulfill, reject) {
            ++__seq;

            var opts = {};
            Object.assign(opts, {
                "op": triggerOpcode,
                "timestamp": timestamp.cht(),
                "seq": __seq,
            }, args);

            if( feedbackOpcode !== undefined )
                handlers[__seq] = {
                    'fulfill': fulfill,
                    'reject': reject,
                };

            connector.send(JSON.stringify(opts));
        });
    });
};




module.exports = MsgActive;
