/* 
*   Maintain current state via incoming value.
*   Responsible for alert correct side(CHT or IoTtalk) to sync
*/

/* Shared variable in this module */
const util = require('util');
const baseurl = require(__base + 'config.js').IOTTALK_URL;
const logger = require(__base + 'logger.js');
const cht = require(__base + 'cht.js');
const iottalk = require(__base + 'iottalk.js');
const dashboard = require(__base + 'dashboard.js');

// Dictionary for connection usage
var deviceDict = {};
var sensorDict = {};

// Mapping: operation target -> last updated timestamp
// All timestamp just can be updated non-decreasingly
// So do nothing if failed to update timestamp
var lastUpdateTimestamp = {};

// Only issue http request to attached slave
// Manner:
//      Add slave into set only when all http request for attaching completed
//      Delete slave from set before requests for detaching
var attachedSlave = new Set();



/* Functions not export to outer prefix with __ */
function __deviceUrl(slaveID, deviceName) {
    return baseurl + '/' + slaveID + '_' + deviceName;
}

function __featureUrl(slaveID, deviceName, sensorName) {
    if( !sensorName )
        return null;
    return __deviceUrl(slaveID, deviceName) + '/' + sensorName;
}

function __hasSlaveID(slaveID) {
    if( !sensorDict[slaveID] ) {
        logger.error('CHT: unknown slaveID', slaveID);
        return false;
    }
    return true;
}

function __hasSensor(slaveID, deviceName, sensorName) {
    if( !__hasSlaveID(slaveID) )
        return false;
    if( !sensorDict[slaveID][deviceName] || !sensorDict[slaveID][deviceName][sensorName] ) {
        logger.error('CHT: unknown sensor', slaveID, deviceName, sensorName);
        return false;
    }
    return true;
}

function __updateTimestamp(slaveID, deviceName, sensorName, timestamp) {
    const opTarget = [slaveID, deviceName, sensorName].join('.');
    if( lastUpdateTimestamp[opTarget] && lastUpdateTimestamp[opTarget] > timestamp )
        return false;
    lastUpdateTimestamp[opTarget] = timestamp;
    return true;
}



/* Below implement functions exporting to outer */
function init(managedSlaveList) {
    managedSlaveList.forEach((rawSlave) => {

        const slaveID = rawSlave.id;

        // Init one slave
        deviceDict[slaveID] = {};
        sensorDict[slaveID] = {};
        dashboard.addSlave(slaveID);
        
        rawSlave.devices.forEach((rawDevice) => {

            const deviceName = rawDevice.name;
            const attr = rawDevice.attributes;
            const df_list = [];

            // Init one device
            deviceDict[slaveID][deviceName] = {
                'url': __deviceUrl(slaveID, deviceName),
                'profile': {
                    'd_name': slaveID, //[attr.vendor, attr.model, attr.series].join(' '),
                    'dm_name': 'CHT_' + deviceName,
                    'is_sim': false,
                    'df_list': df_list,
                },
            };
            sensorDict[slaveID][deviceName] = {};
            dashboard.addDevice(slaveID, deviceName);

            rawDevice.sensors.forEach((rawSensor) => {

                const sensorName = rawSensor.name;
                const isOutput = (rawSensor.direction[1] === 'O');
                const idfName = (isOutput)? sensorName+'-I' : sensorName;
                const odfName = (isOutput)? sensorName+'-O' : null;
                const url = {
                    'idf': __featureUrl(slaveID, deviceName, idfName),
                    'odf': __featureUrl(slaveID, deviceName, odfName),
                };

                // Init one sensor
                sensorDict[slaveID][deviceName][sensorName] = {
                    'slaveID': slaveID,
                    'deviceName': deviceName,
                    'sensorName': sensorName,
                    'url': url,
                };
                dashboard.addSensor(slaveID, deviceName, sensorName);

                // Also binding url to sensorDict
                sensorDict[url.idf] = sensorDict[slaveID][deviceName][sensorName];
                if( url.odf )
                    sensorDict[url.odf] = sensorDict[slaveID][deviceName][sensorName];

                // Push device feature to profile
                df_list.push(idfName);
                if( odfName )
                    df_list.push(odfName);
                    
            });
        });
    });
}

function setSlaveOnline(slaveID, timestamp) {
    if( !__hasSlaveID(slaveID) ||
        !__updateTimestamp(slaveID, '', '', timestamp) )
        return;

    dashboard.setOnline(slaveID);

    const slavedDevice = deviceDict[slaveID];
    const deviceList = Object.keys(slavedDevice);
    
    // Count for completed http request to IoTtalk
    // when count to 0, set slave as attached
    // Only talk to attached slaves' devices
    var cnt = deviceList.length;

    deviceList.forEach((deviceName) => {

        const info = slavedDevice[deviceName];
        iottalk.attach(info.url, info.profile).then(() => {
            
            // After successfully attached,
            // ask value for all sensors under the device
            const sensorList = Object.keys(sensorDict[slaveID][deviceName]);
            sensorList.forEach((sensorName) => {

                cht.askValue({
                    'id': slaveID,
                    'device': deviceName,
                    'sensor': sensorName,
                });

            });

        }).finally(() => {

            // No matter http request success or not, just countdown
            if( --cnt <= 0 )
                attachedSlave.add(slaveID);

        });

    });
}

function setSlaveOffline(slaveID, timestamp) {
    if( !__hasSlaveID(slaveID) ||
        !__updateTimestamp(slaveID, '', '', timestamp) )
        return;

    attachedSlave.delete(slaveID);
    dashboard.setOffline(slaveID);

    const slavedDevice = deviceDict[slaveID];
    const deviceList = Object.keys(slavedDevice);

    deviceList.forEach((deviceName) => {

        const info = slavedDevice[deviceName];
        iottalk.detach(info.url);

    });
}

function updateIDF(slaveID, deviceName, sensorName, value, timestamp) {
    if( !__hasSensor(slaveID, deviceName, sensorName) || 
        !__updateTimestamp(slaveID, deviceName, sensorName, timestamp) )
        return;

    const url = sensorDict[slaveID][deviceName][sensorName].url.idf;
    iottalk.update(url, value);
    dashboard.update(slaveID, deviceName, sensorName, value);
}

function updateODF(slaveID, deviceName, sensorName, value, timestamp) {
    if( !__hasSensor(slaveID, deviceName, sensorName) ||
        !__updateTimestamp(slaveID, deviceName, sensorName+'ODF', timestamp) )
        return;

    cht.writeValue({
        'id': slaveID,
        'device': deviceName,
        'sensor': sensorName,
        'value': value.toString(),
    }).then(() => {
        cht.readValue({
            'id': slaveID,
            'device': deviceName,
            'sensor': sensorName,
        }).then((data) => {
            updateIDF(slaveID, deviceName, sensorName, data['value'], data['last']);
        });
    }).catch((res) => {
        logger.error('CHT: fail to write value', value.toString(), 'to', slaveID, deviceName, sensorName);
        if( typeof res === 'object' && 'reason' in res )
            logger.error('CHT: reason', res.reason);
    });
}

function forEachAttachedOdf(func) {
    attachedSlave.forEach((slaveID) => {

        const slavedDevice = deviceDict[slaveID];
        const deviceList = Object.keys(slavedDevice);

        deviceList.forEach((deviceName) => {

            const sensorList = Object.keys(sensorDict[slaveID][deviceName]);

            sensorList.forEach((sensorName) => {

                const info = sensorDict[slaveID][deviceName][sensorName];
                if( info.url.odf )
                    func(info);

            });
        });
    });
}

function forEachAttachedDevice(func) {
    attachedSlave.forEach((slaveID) => {

        const slavedDevice = deviceDict[slaveID];
        const deviceList = Object.keys(slavedDevice);

        deviceList.forEach((deviceName) => {

            const info = slavedDevice[deviceName];
            func(info);

        });
    });
}


process.on('unhandledRejection', (reason, p) => {});


module.exports = {
    'init': init,
    'setSlaveOnline': setSlaveOnline,
    'setSlaveOffline': setSlaveOffline,
    'updateIDF': updateIDF,
    'updateODF': updateODF,
    'forEachAttachedOdf': forEachAttachedOdf,
    'forEachAttachedDevice': forEachAttachedDevice,
    get attachedDeviceUrlSize() {
        return attachedSlave.size;
    },
};
