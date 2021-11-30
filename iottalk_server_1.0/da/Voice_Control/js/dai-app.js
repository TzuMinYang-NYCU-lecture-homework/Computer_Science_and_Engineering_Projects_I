$(function () {
    //init UI
    $("#not_support").hide();
    if (!('webkitSpeechRecognition' in window) || !('speechSynthesis' in window)) {
    	$("#not_support").show();
        console.log( "not support!" );
        return;
    }
    var siriwave = new SiriWave({
        style: 'ios9',
        speed: 0.08,
        amplitude: 0.3,
        autostart: false,
    });
    var eventQueue = [];
	var processing = true;
	var id = -1;
	var endRecognition = false;
	var recognition = new webkitSpeechRecognition();
	recognition.continuous = false;
	recognition.interimResults = true;
	recognition.lang="cmn-Hant-TW";

	recognition.onstart=function(){
		console.log("on start");
		endRecognition = false;
		siriwave.start();
		$("#recognizeText").text("");
	};
	recognition.onend=function(){
		if(!endRecognition){
			recognition.start();
			return;
		}
		processing = true;
		console.log("on end");
	};
	recognition.onresult=function(event){
		if(event != undefined){
			var index = event.results[event.resultIndex].length-1;
			console.log(event);
			// recognize text animation
			$("#recognizeText").text(event.results[event.resultIndex][index].transcript);
			$('#recognizeText').textillate();
			if(event.results[event.resultIndex].isFinal){
				dan.push("IDText-I", [id, event.results[event.resultIndex][index].transcript]);
				siriwave.stop();
				endRecognition = true;
			}
		}
	};
	function processQueue(){
		console.log("process!");
		if(eventQueue.length != 0 && processing){
			processing = false;
			var script = eventQueue.shift();
			id = script[0];
			var msg = new SpeechSynthesisUtterance(script[1]);
			msg.lang = "zh-TW";
			window.speechSynthesis.speak(msg);
			$("#scriptText").text(script[1]);
			$('#scriptText').textillate();
			msg.onend = function(){
				recognition.start();
			};
		}
	}
	setInterval(processQueue, 500);
    function IDText_I (data) {}
    function IDText_O (data) {
        console.log(data);
		eventQueue.push(data[0]);
    }
    function iot_app () {

    }

    var profile = {
        'dm_name': 'SpeechCtl',
        'df_list': [IDText_I,IDText_O]
    }

    var ida = {
        'iot_app': iot_app,
    };

    dai(profile, ida);
});
