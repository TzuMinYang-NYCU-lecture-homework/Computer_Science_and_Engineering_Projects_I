var fs = require('fs');
var util = require('util');

const filename = process.argv[2];
const target = filename + '.parse';

try {   
    if( !fs.statSync(filename).isFile() ) {
        console.error('ManagedSlave is not file.');
        process.exit();
    }
}
catch(e) {
    console.error('ManagedSlave not found.');
    process.exit();
}

const str = fs.readFileSync(filename);
const json = JSON.parse(str);

fs.writeFileSync(target, '');

function writeSet(title, st) {
    fs.appendFileSync(target, title+'\n');
    st.forEach((val) => {
        fs.appendFileSync(target, '    '+val+',\n');
    });
    fs.appendFileSync(target, '\n');
}



var deviceFeature = new Set();
var deviceModel = new Set();
var dfparameter_for_df = new Set();
var dfparameter_for_dm = new Set();



// parse DEVICE_FEATURE
json.slaves.forEach((slave) => {
    slave.devices.forEach((device) => {
        
        const dm_name = 'CHT_'+device.name;
        deviceModel.add(util.format("'%s': 'other'", dm_name));

        device.sensors.forEach((sensor) => {
            if( sensor.direction === 'AI' || sensor.direction === 'DI' ) {
                deviceFeature.add(util.format("'%s': ('input', 'Other', 1, '%s')", sensor.name, sensor.desc));
                dfparameter_for_df.add(util.format("'%s': [('string', 'sample', 0, 0, 0, None, 'None')]", sensor.name));
                dfparameter_for_dm.add(util.format("('%s', '%s'): [('string', 'sample', 0, 0, 0, None, 'None')]", dm_name, sensor.name));
            }
            else {
                deviceFeature.add(util.format("'%s-I': ('input', 'Other', 1, '%s')", sensor.name, sensor.desc));
                deviceFeature.add(util.format("'%s-O': ('output', 'Other', 1, '%s')", sensor.name, sensor.desc));
                dfparameter_for_df.add(util.format("'%s-I': [('string', 'sample', 0, 0, 0, None, 'None')]", sensor.name));
                dfparameter_for_df.add(util.format("'%s-O': [('string', 'sample', 0, 0, 0, None, 'None')]", sensor.name));
                dfparameter_for_dm.add(util.format("('%s', '%s-I'): [('string', 'sample', 0, 0, 0, None, 'None')]", dm_name, sensor.name));
                dfparameter_for_dm.add(util.format("('%s', '%s-O'): [('string', 'sample', 0, 0, 0, None, 'None')]", dm_name, sensor.name));
            }
        });
    });
});



writeSet('DEVICE_FEATURE', deviceFeature);
writeSet('DEVICE_MODEL', deviceModel);
writeSet('DFPARAMETER_FOR_DF', dfparameter_for_df);
writeSet('DFPARAMETER_FOR_DM', dfparameter_for_dm);
