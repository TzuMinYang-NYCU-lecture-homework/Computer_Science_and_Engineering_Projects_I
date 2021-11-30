var watchID, sendFlag = 1;
function query_string_check()
{
    if(location.search.length > 0)
    {
      var urlParams = new URLSearchParams(window.location.search);
      window.person = urlParams.get('name');
      window.trackingAppNum = urlParams.get('app');
      $('#my_location').show();
    }
}

function hash_tag_check()
{
    if(location.hash.length > 0)
    {
      window.mac = 'TRACKING_DEFAULT';
      window.trackingApp = location.hash.split("#")[1];
      $.get(window.location.origin + '/static/passwd_tracking?v='+Math.random()     
        ).done(function(result){
            window.passwd_tracking = result;
            console.log(passwd_tracking);
      });
      person_input_name();
    }
}

function person_input_name(){
  console.log('person_input_name');

	window.person = prompt("Please enter your name");
  if(window.person != null)
  {
    getTrackingLocation();
    set_person_id();
  }
}

function set_person_id(){
		console.log('set_person_id', trackingApp, person);
    $.getJSON($SCRIPT_ROOT + '/secure/_set_tracking_id',{
        app: window.trackingApp,
        name: window.person
      }, function(data) {
        tracking_list_with_id = data.result.map(function(obj) {return  {
            'app_num': obj.app_num,
            'id': obj.id
           }; 
        });

        console.log('tracking_list_with_id', tracking_list_with_id);
        window.trackingAppNum = tracking_list_with_id[0].app_num;
        window.id = tracking_list_with_id[0].id;
        console.log(id);
        window.onunload = unloadPage;
        window.onbeforeunload = unloadPage;
        window.onclose = unloadPage;
        window.onpagehide = unloadPage;

        $('#my_location').show();
    });
    
}

function reGetTrackingLocation() {
  clearTimeout(tracking_timeout);

  tracking_timeout = setTimeout(function(){
      console.log('setTimeout in');
      sendFlag = 1;
  },5000);

}


function getTrackingLocation() {
	var output = {lat: 0, lng:0};

	var geoOptions = {
	   enableHighAccuracy : true,
       timeout: 10 * 1000,
       maximumAge : 0
    }

    var geoSuccess = function(position) {
      console.log('geoSuccess');

      output.lat = position.coords.latitude;
      output.lng = position.coords.longitude;

      if(window.id != undefined && sendFlag == 1)
      {
        var dt = new Date();
	      dt = dt.getFullYear()+"-"+(dt.getMonth()+1)+"-"+dt.getDate()+" "+dt.getHours()+":"+dt.getMinutes()+":"+dt.getSeconds();

	      IoTtalk.update(mac, 'GeoData-I', [output.lat, output.lng, person, id, dt]);
	      console.log("Latitude: " + output.lat + " Longitude: " + output.lng + " person: " + person + " id: "+ id);

        sendFlag = 0;
        reGetTrackingLocation();
      }
      
    };

    var geoError = function(error) {
      alert("Please open your GPS.");
      console.log('Error occurred. Error code: ' + error.code);
      navigator.geolocation.clearWatch(watchID);
      getTrackingLocation();
      // error.code can be:
      //   0: unknown error
      //   1: permission denied
      //   2: position unavailable (error response from location provider)
      //   3: timed out
    };

    watchID = navigator.geolocation.watchPosition(geoSuccess,geoError, geoOptions);

}

function unloadPage() {
  $.getJSON($SCRIPT_ROOT + '/secure/_del_movable_icon',{
      app_num: trackingAppNum,
      name: person
    }, function(data) {

  });
}

function show_tracking_target(icon_num, lat, lng, map)
{
  console.log('show_tracking_target', icon_num, lat, lng, map);

  window.trackingCoord = {lat: lat, lng: lng};

  if(all_icon_list[icon_num].show == 0)
    $('#icon_'+icon_num).click();

  map.setCenter({lat: lat, lng: lng});
}