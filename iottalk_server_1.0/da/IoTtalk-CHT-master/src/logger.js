// Include dependency
const config = require(__base + 'config.js');
const colors = require('colors/safe');

function concatArguments(args) {
    var strs = [];
    for(var i=0; i<args.length; ++i)
        if( typeof args[i] !== 'string' )
            strs.push(JSON.stringify(args[i], null, 4));
        else
            strs.push(args[i]);
    return strs.join(' ');
}

function log() {
    if( config.LOG_LOG )
        console.log(colors.cyan(concatArguments(arguments)));
}

function info() {
    if( config.LOG_INFO )
        console.info(colors.green(concatArguments(arguments)));
}

function warn() {
    if( config.LOG_WARN )
        console.warn(colors.yellow.bold(concatArguments(arguments)));
}

function error() {
    if( config.LOG_ERROR )
        console.error(colors.red.bold(concatArguments(arguments)));
}



module.exports = {
    'log': log,
    'info': info,
    'warn': warn,
    'error': error,
};
