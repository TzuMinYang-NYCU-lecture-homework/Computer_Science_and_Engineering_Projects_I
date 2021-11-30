
$(function(){

    var dogDom = $('#showDogInfo > textarea');
    var ajaxInit = new XMLHttpRequest();
    var url = "dogData.json";
    ajaxInit.open("GET", url, true); // True for sync
    ajaxInit.setRequestHeader("content-type","application/json");
    ajaxInit.onreadystatechange = function(){
        if(ajaxInit.readyState == 4 && ajaxInit.status == 200)
            var dogJson = JSON.parse(ajaxInit.responseText);
        processData(dogJson);
    }   
    ajaxInit.send(null);

    function processData(dogJson)
    {
        $.each( dogJson, function(i, device) {
            if(device.code);
            else 
            {
                var trackerName;
                var trackerID;
                var GeoLo_E;
                var GeoLo_N;
                var receiveTime;
                var k = 0;

                function showData_Tracker1() {
                    var dogData = device[Object.keys(device)[0]][k].data;
                    trackerName = dogData.device_name;
                    GeoLo_N = dogData.GPS_N;
                    GeoLo_E = dogData.GPS_E;
                    receiveTime = dogData.recv;
                    var dataOut = trackerName + "\n" + GeoLo_E + "\n" + GeoLo_N + "\n" + receiveTime;
                    dogDom.text(dataOut);
                    k++;
                    if( k < device[Object.keys(device)[0]].length ){
                        setTimeout( showData_Tracker1, 1000 );
                    }
                    else 
                    {
                        k = 0;
                        showData_Tracker2();
                    }
                }
                showData_Tracker1();
                function showData_Tracker2() {
                    var dogData = device[Object.keys(device)[1]][k].data;
                    trackerName = dogData.device_name;
                    GeoLo_N = dogData.GPS_N;
                    GeoLo_E = dogData.GPS_E;
                    receiveTime = dogData.recv;
                    var dataOut = trackerName + "\n" + GeoLo_E + "\n" + GeoLo_N + "\n" + receiveTime;
                    dogDom.text(dataOut);
                    k++;
                    if( k < device[Object.keys(device)[1]].length ){
                        setTimeout( showData_Tracker1, 1000 );
                    }
                }
                
                var count = 1, urgent=0;    
                var dog_name = ['Happy', 'Puppy', 'Lucky'];  
                var dog_id = [0, 1, 2];         
                function GeoData_I  (){
                    var Arr = [];
                    // if(trackerName == "追蹤器_34")
                    //     trackerID = 0;
                    // else if(trackerName == "Tracker_0035")
                    //     trackerID = 1;
                    trackerID = count % 3;
                    count = count + 1;

                    // if(trackerID == 2)
                    //     urgent = 1;
                    // else
                    //     urgent = 0;

                    Arr.push( GeoLo_N);
                    Arr.push(GeoLo_E );
                    Arr.push(dog_name[trackerID]);
                    // var json = JSON.stringify({TrackerID: trackerID , N: GeoLo_N, E: GeoLo_E , Time: receiveTime, type:'dog', name: dog_name[trackerID]});
                    Arr.push(dog_id[trackerID]);
                    
                    var dt = new Date();
                    Arr.push(dt.getFullYear()+"-"+(dt.getMonth()+1)+"-"+dt.getDate()+" "+dt.getHours()+":"+dt.getMinutes()+":"+dt.getSeconds());
                    return Arr;
                }

                function iot_app(){
                  
                    
                }

                var profile = {
                    'dm_name': 'SensorSystem',
                    'is_sim': false,
                    'df_list':[GeoData_I],
                    'origin_df_list': [GeoData_I],
                }

        
                var ida = {
                        'iot_app': iot_app,
                    }; // How iot device receive data (format)
                dai(profile,ida);   
            }
        });
    }
})       
