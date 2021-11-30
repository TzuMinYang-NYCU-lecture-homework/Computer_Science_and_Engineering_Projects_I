// Setting base include path, no relative path needed
global.__base = __dirname + '/src/';

// Patch for Promise
Promise.prototype.finally = function(f) {
    return this.then(function(value) {
        return Promise.resolve(f()).then(function() {
            return value;
        });
    }, function(err) {
        return Promise.resolve(f()).then(function() {
            throw err;
        });
    });
};



// Include dependency
const fs = require('fs');
const config = require(__base + 'config.js');
const logger = require(__base + 'logger.js');
const cht = require(__base + 'cht.js');
const iottalk = require(__base + 'iottalk.js');
const state = require(__base + 'state.js');
const util = require('util');



// Init log directory
try {
    fs.accessSync('log', fs.F_OK);
}
catch (e) {
    fs.mkdirSync('log');
}



// Listening cht side event
cht.getManagedSlaveList().then((data) => {
    
    // Logging ManagedSlaveList
    fs.writeFile('log/ManagedSlaveList', JSON.stringify(data, null, 4));

    // Init state
    state.init(data['slaves']);

    // Chaining
    return cht.getArrivedSlaveList();

}).then((data) => {
    
    // Init already online slave
    var timestamp = data['timestamp'];
    data['slaves'].forEach((slave) => {
        state.setSlaveOnline(slave.id, timestamp);
    });

    // Start listening cht
    cht.onSlaveArrived((data) => {
        state.setSlaveOnline(data['id'], data['timestamp']);
    });

    cht.onSlaveExited((data) => {
        state.setSlaveOffline(data['id'], data['timestamp']);
    });

    cht.onValueChanged((data) => {
        state.updateIDF(data['id'], data['device'], data['sensor'], data['value'], data['last']);
    });

});



// Setting IoTtalk side
var pullerID = null;
var iottalkDataRecord = {};
var toBePulled = {
    list: [],
    id: 0,
    delay: config.IOTTALK_PULL_INTERVAL,
    processing: new Set(),
};
function puller() {
    if( pullerID === null )
        return;

    if( toBePulled.id >= toBePulled.list.length ) {

        toBePulled.list = [];
        toBePulled.id = 0;

        state.forEachAttachedOdf((info) => {
            toBePulled.list.push(info);
        });

        if( toBePulled.list.length > 0 )
            toBePulled.delay = Math.max(config.IOTTALK_PULL_INTERVAL/toBePulled.list.length, 10);

    }
    else if( !toBePulled.processing.has(url) ) {

        const info = toBePulled.list[toBePulled.id++];
        const url = info.url.odf;
        const slaveID = info.slaveID;
        const deviceName = info.deviceName;
        const sensorName = info.sensorName;

        toBePulled.processing.add(url);

        iottalk.get(url).then(function(data) {
            if( pullerID === null )
                return;

            const value = data[1][0];
            const timestamp = data[0];

            if( iottalkDataRecord[url] !== value ) {
                iottalkDataRecord[url] = value;
                state.updateODF(slaveID, deviceName, sensorName, value, timestamp);
            }

        }).finally(function() {
            toBePulled.processing.delete(url);
        });

    }

    pullerID = setTimeout(puller, toBePulled.delay);

}
pullerID = setTimeout(puller, toBePulled.delay);



// Close process and clear up
var exitCalled = false;
function exit() {
    if( exitCalled ) return;
    exitCalled = true;
    logger.info('Exiting');

    // Wait all async clearing process, exit process when count to 0
    var count = 1 + state.attachedDeviceUrlSize;
    var countdown = function() {
        if( --count <= 0 )
            process.exit();
    };

    // Clear iottalk data puller
    clearTimeout(pullerID);
    pullerID = null;
    
    // Closing cht websocket
    cht.close();

    // Detach all device from iottalk
    state.forEachAttachedDevice((info) => {
        iottalk.detach(info.url, info.profile).finally(countdown);
    });

    countdown();

    setTimeout(process.exit, 10000);
}

cht.onClose(exit);
process.on('SIGINT', exit);

process.on('unhandledRejection', (reason, p) => {});

