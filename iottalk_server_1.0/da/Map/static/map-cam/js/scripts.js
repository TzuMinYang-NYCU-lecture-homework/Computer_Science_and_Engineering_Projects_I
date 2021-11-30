var ADDR_KURENTO_SERVER = "hi1.iottalk.tw";  // media server
var PORT_KURENTO_SERVER = "8433";

/* set url for IP cam and start automatically */
window.addEventListener('load', function(){
  document.getElementById("address").value = parent.cam_src;
  console.log('*******************************' + document.getElementById("address").value);
	document.getElementById('start').click();
	console.log("start");
})

/* auto click the stop button when unload the page */

window.addEventListener('unload', function(){  // not working
	document.getElementById('stop').click();
	console.log("stop");
})

function bodyOnUnload() {  // working
        document.getElementById('stop').click();
        console.log("stop");
}

window.addEventListener('load', function(){
  document.getElementById("videoOutput").addEventListener('click', function(){
	  toggleFullScreen();
	  });  //toggleFullScreen when click the video 
  args.ws_uri = 'wss://' + ADDR_KURENTO_SERVER + ':' + PORT_KURENTO_SERVER + '/kurento'; //set the kurento server address 
})

function toggleFullScreen() {
  var doc = window.document;
  var elem = document.getElementById("videoFSContainer"); //the element you want to make fullscreen

  var requestFullScreen = elem.requestFullscreen || elem.webkitRequestFullScreen || elem.mozRequestFullScreen || elem.msRequestFullscreen;
  var cancelFullScreen = doc.exitFullscreen || doc.webkitExitFullscreen || doc.mozCancelFullScreen|| doc.msExitFullscreen;

  if(!(doc.fullscreenElement || doc.mozFullScreenElement || doc.webkitFullscreenElement || doc.msFullscreenElement)) {
      requestFullScreen.call(elem);
	  elem.style.backgroundColor = "black";
  }
  else {
    cancelFullScreen.call(doc);
	elem.style.backgroundColor = "";
  }
}
