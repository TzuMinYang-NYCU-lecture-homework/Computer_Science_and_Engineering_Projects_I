var express = require("express"),
    app = express(),
    webServer = require("http").createServer(app),
    pageGen = require("./PageGen"),
    dan = require("./DAN").dan,
    config = require("./Config"),
    socketServer = require("./SocketServer").socketServer,
    iottalkIP = process.argv[2],
    Repeat = require("repeat");


app.use(express.static("./webapp"));

app.get("/ssctl", function (req, res) {
     pageGen.Page.getSsCtlPage(req,res,macAddr,iottalkIP.split(":")[0]+":7788");
});
webServer.listen((process.env.PORT || config.webServerPort), '0.0.0.0');

var genMacAddr = function () {
    var addr = '';
    for (var i = 0; i < 5; i++)
        addr += '0123456789abcdef'[Math.floor(Math.random() * 16)];
    return addr;
};
var macAddr = genMacAddr();
console.log('mac address:' + macAddr);


var registerSmartSockets = function() {
    var smartSockets = socketServer.getSmartSockets();
    for(var i = 0; i < smartSockets.length; i++){
        socketServer.updateSocketStateTable(smartSockets[i], function(smartSocket){
            //console.log(smartSocket.socketStateTable);
            var odf_list = [];
            for(var i = 0; i < smartSocket.socketStateTable.length; i++){
                var states = smartSocket.socketStateTable[i].length;
                for(var j = 0; j < states; j++){
                    if(smartSocket.socketStateTable[i][j] != -1){
                        odf_list.push('Socket' + (i*states+(j+1)));
                    }
                }
            }
            console.log(odf_list);
            if(odf_list.length == 0)
                dan.deregister();
            dan.init(smartSocket.pull, 'http://' + iottalkIP , macAddr, {
                'dm_name': 'SmartSocket',
                'd_name' : '1.SmartSocket',
                'u_name': 'yb',
                'is_sim': false,
                'df_list':odf_list

            }, function (result) {
                console.log('register:', result);
                //deregister when app is closing
                process.on('exit', dan.deregister);
                //catches ctrl+c event
                process.on('SIGINT', dan.deregister);
                //catches uncaught exceptions
                process.on('uncaughtException', dan.deregister);

            });
        });
    }
};
Repeat(registerSmartSockets).every(30000, 'ms').start();
//Repeat(registerSmartSockets).start(15000);
//registerSmartSockets();