exports.socketServerPort = 7654;
exports.webServerPort = 8899;
exports.maxSocketGroups = 15;
exports.socketStateBits = 2;
exports.IDFList =  [];
var odf = [];
for(var i = 1; i <= exports.maxSocketGroups * exports.socketStateBits ; i++)
    odf.push("Socket" + i);
exports.ODFList = odf;

/*  Instruction Format

 OP GID R/W  state channel
 C2 00  01   03    00      (開啟group0兩開關)
 C2 00  00   00    00      (讀取group0狀態)

 OP GID state
 B3 00 00    (group0回覆兩開關為關閉)

 OP
 E1 (回復錯誤)

 */
exports.OPCode = [
    'C2',
    'B3',
    'E1'
];



