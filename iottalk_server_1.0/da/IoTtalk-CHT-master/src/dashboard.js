// For IoTtalk cht dashboard
const iottalk = require(__base + 'iottalk.js');
const url = require(__base + 'config.js').IOTTALK_URL + '/CHT_Dashboard';
const furl = url + '/Json';
var registered = false;
var dashboard = {};
var dashboardUpdated = false;
var dashboardPostTimestamp = -1;


// Post profile data to iottalk's cht dashboard
iottalk.attach(url, {
    'd_name': 'nodeJs',
    'dm_name': 'CHT_Dashboard',
    'is_sim': false,
    'df_list': ['Json'],
}).then(() => {
    registered = true;
});
function checkDashboard() {
    if( dashboardUpdated && registered ) {
        dashboardUpdated = false;
        iottalk.update(furl, dashboard);
    }
}
var clocker = setInterval(checkDashboard, 1000);


process.on('SIGINT', () => {
    iottalk.detach(url).finally(() => {
        clearInterval(clocker);
    });
});


process.on('unhandledRejection', (reason, p) => {});


module.exports = {
    addSlave: function(slaveID) {
        dashboard[slaveID] = {
            'online': false
        };
    },
    addDevice: function(slaveID, deviceName) {
        dashboard[slaveID][deviceName] = {};  
    },
    addSensor: function(slaveID, deviceName, sensorName) {
        dashboard[slaveID][deviceName][sensorName] = 0;
    },
    setOnline: function(slaveID) {
        dashboard[slaveID].online = true;
        dashboardUpdated = true;
    },
    setOffline: function(slaveID) {
        dashboard[slaveID].online = false;
        dashboardUpdated = true;
    },
    update: function(slaveID, deviceName, sensorName, value) {
        dashboard[slaveID][deviceName][sensorName] = value;
        dashboardUpdated = true;
    }, 
};
