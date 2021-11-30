/**
 * Created by kuan on 2017/11/21.
 */

/************** publish **************/

/* Publish when there is a MorSocket connect to MorSocketServer.
*  {
*       id: MorSocket ID (String),
*       room: MorSocket location (String),
*       sockets: [ {
*                    index: socket index in this MorSocket(Integer),
*                    state: on/off (Boolean),
*                    alias: plugin device name (String)
*       } ]
*  }
* */
exports.deviceInfoTopic = "DeviceInfo";

/* Publish when MorSocketCtl APP first time open(Receive SyncDeviceInfo topic),
*  or any MorSocket has been disconnect to MorSocketServer.
*  [
*      {
*          id: MorSocket ID (String),
*          room: MorSocket location (String),
*          sockets: [ {
*                       index: socket index in this MorSocket(Integer),
*                       state: on/off (Boolean),
*                       alias: plugin device name (String)
*          } ]
*      }
*  ]
*/
exports.devicesInfoTopic = "DevicesInfo";

/************** subscribe **************/

/*  MorSocketCtl APP will publish SyncDeviceInfo topic when first time open.
*   { }
* */
exports.syncDeviceInfoTopic = "SyncDeviceInfo";

/* MorSocketCtl APP will publish Switch topic when user switch any socket.
*  {
*       id: MorSocket ID (String),
*       index: socket index in this MorSocket(Integer),
*       state: on/off (Boolean)
*  }
* */
exports.switchTopic = "Switch";

/* MorSocketCtl APP will publish Alias topic when user change socket alias.
 *  {
 *       id: MorSocket ID (String),
 *       index: socket index in this MorSocket(Integer),
 *       alias: plugin device name (String)
 *  }
 * */
exports.aliasTopic = "Alias";

/* Due to implement convenient SetupDeviceRoom is a RESTful API
*  rather than a MQTT topic, MorSocketCtl APP will send the MorSocket location
*  when user setup the MorSocket.
*  {
*       id: MorSocket ID (String),
*       location: string
*  }
* */
exports.setupDeviceRoomTopic = "SetupDeviceRoom";
