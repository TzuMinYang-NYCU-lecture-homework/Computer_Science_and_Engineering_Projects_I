const datetime = require('node-datetime');

function timestampCHT() {
    return datetime.create().format('Y-m-d H:M:S').toString();
}

module.exports = {
    'cht': timestampCHT,
};
