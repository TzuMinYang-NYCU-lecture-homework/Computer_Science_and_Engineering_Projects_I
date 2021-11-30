'use strict';
var os = require('os'),
    ifaces = os.networkInterfaces(),
    myIPAddress = '',
    net = require('net'),
    shortID = require('shortid'),
    sleep = require('sleep'),
    config = require('./Config'),
    events = require('events'),
    commandReceive = new events.EventEmitter();

Object.keys(ifaces).forEach(function (ifname) {

    // var alias = 0;
    ifaces[ifname].forEach(function (iface) {
        if ('IPv4' !== iface.family || iface.internal !== false) {
            // skip over internal (i.e. 127.0.0.1) and non-ipv4 addresses
            return;
        }
        // if (alias >= 1) {
        //     // this single interface has multiple ipv4 addresses
        //     console.log(ifname + ':' + alias, iface.address);
        // } else {
        //     // this interface has only one ipv4 adress
        //     console.log(ifname, iface.address);
        // }
        //++alias;
        if(ifname == 'en0')
            myIPAddress = iface.address;
    });

});
var integerToHexString = function (d) {

    return ((d < 16) ? ('0') : '') + (d.toString(16)).slice(-2).toUpperCase();

};

var hexToBytes = function(hex) {

    for (var bytes = [], c = 0; c < hex.length; c += 2)
        bytes.push(parseInt(hex.substr(c, 2), 16));
    return bytes;

};

var sendOnOffCommand = function(socketIndex, state, client){

    socketIndex--;

    var op = config.OPCode[0],
        gid = Math.floor(socketIndex/2),

    /*  socket position
        0 represent right: 00000001
        1 represent left:00000010
    */
        pos = socketIndex % 2,
        channel = 0,
        rw = 1,
        buffer,
        command,
        cmdByteArr;

    /* offline, command not send*/
    if(client.socketStateTable[gid][pos] == -1){
        console.log('offline command not send!');
        return
    }

    client.socketStateTable[gid][pos] = parseInt(state);
    var posArr = client.socketStateTable[gid].slice();
    state = parseInt(posArr.reverse().join(''),2);

    command = op + integerToHexString(gid) + integerToHexString(rw)
        + integerToHexString(state) + integerToHexString(channel);

    cmdByteArr = hexToBytes(command);

    buffer = new Buffer(cmdByteArr);

    console.log('send: ' + command);
    client.write(buffer);

};
var sendReadStateCommand = function(gid, client){

    var op = config.OPCode[0],
        state = 0,
        channel = 0,
        rw = 0,
        buffer,
        command,
        cmdByteArr;

    command = op + integerToHexString(gid) + integerToHexString(rw)
        + integerToHexString(state) + integerToHexString(channel);

    cmdByteArr = hexToBytes(command);

    buffer = new Buffer(cmdByteArr);

    console.log('send: ' + command + '->' + cmdByteArr);
    client.write(buffer);

};
var socketServer = (function () {

    var port = config.socketServerPort,
        host = myIPAddress,
        clientArray = [];

    var tcpServer = net.createServer(function (client) {

        client.id = shortID.generate();//will retrieve from client in later version
        client.pull = function (odf_name, data) {
            console.log(odf_name + ':' + data);
            if(odf_name.startsWith('Socket')){
                var socketIndex = odf_name.replace('Socket','');
                if(clientArray.length > 0)
                    sendOnOffCommand(socketIndex, data, client);
            }
        };
        client.socketStateTable = new Array(config.maxSocketGroups);
        for(var i = 0; i < config.maxSocketGroups; i++)
            client.socketStateTable[i] = new Array(config.socketStateBits).fill(-1);
        //updateSocketStateTable(client);
        console.log('connected: ' + client.remoteAddress + ':' + client.remotePort);
        clientArray.push(client);
        console.log(clientArray.length);

        client.on('data', function(cmd){
            cmd = cmd.toString('hex').toUpperCase();
            commandReceive.emit(client.id, cmd);
            console.log('client:' + client.remoteAddress + ' receive:' + cmd);
        });

    });
    tcpServer.listen(port, host);

    return {
      getSmartSockets: function(){
          return clientArray;
      },
      updateSocketStateTable: function(client, callback){

          var gid = 0,
              triggerCallback = false;

          sendReadStateCommand(gid, client);

          commandReceive.on(client.id, function(cmd){

              var op = cmd.substring(0, 2);
              switch(op){
                  case config.OPCode[1]: //B3
                      /* client is online, trigger callback */
                      if(client.socketStateTable[gid][0] == -1)
                          triggerCallback = true;
                      /* update socketStateTable of client */
                      var cmdGid = parseInt(cmd.substring(2, 4), 16),
                          cmdState = parseInt(cmd.substring(4, 6), 16).toString(2).split('').reverse();
                      for(var i = 0; i < config.socketStateBits; i++)
                          client.socketStateTable[cmdGid][i] = (cmdState.length > i) ?
                              cmdState[i] : 0;
                      break;

                  case config.OPCode[2]: //E1
                      /* client is offline, trigger callback */
                      if(client.socketStateTable[gid][0] != -1)
                          triggerCallback = true;
                      /* update socketStateTable of client */
                      for(var i = 0; i < config.socketStateBits; i++)
                          client.socketStateTable[gid][i] = -1;
                      break;

                  default:
                      console.log('from client: ' + client.remoteAddress + 'gid: ' + gid + 'reply: ' + cmd);
                      break;
              }

              if(gid+1 < config.maxSocketGroups)
                  sendReadStateCommand(++gid, client);
              else if(gid == config.maxSocketGroups-1 && triggerCallback){
                  callback(client);
              }

          });
      }

    };

})();

exports.socketServer = socketServer;
