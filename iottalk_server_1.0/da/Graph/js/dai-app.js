var seriesData = [];
var allData = [];
var palette;
var graph, preview, hoverDetail, legend, shelving, order, highlighter, ticksTreatment, xAxisUnit, xAxis, yAxis, controls;
var showamount = 50;
var cmdparam;

function draw(sequence, inputnamearray){
	document.getElementById('content').innerHTML = '<form id="side_panel"><h1 id="theTitle">Random Data in the Future</h1><section><div id="legend"></div></section><section><div id="renderer_form" class="toggler"><input type="radio" name="renderer" id="area" value="area"><label for="area">area</label><input type="radio" name="renderer" id="bar" value="bar"><label for="bar">bar</label><input type="radio" name="renderer" id="line" value="line" checked><label for="line">line</label><input type="radio" name="renderer" id="scatter" value="scatterplot"><label for="scatter">scatter</label></div></section><section><div id="offset_form"><label for="stack"><input type="radio" name="offset" id="stack" value="zero"><span>stack</span></label><label for="value"><input type="radio" name="offset" id="value" value="value" checked><span>value</span></label></div><div id="interpolation_form"><label for="cardinal"><input type="radio" name="interpolation" id="cardinal" value="cardinal" checked><span>cardinal</span></label><label for="linear"><input type="radio" name="interpolation" id="linear" value="linear"><span>linear</span></label></div></section><section><h4>limit pieces of information (must larger than 0)</h4><input type="text" id="inputnumber" value="50"><input type="button" id="changelimitbutton" disabled value="submit" onClick = "changeLimit()"></section><section></section></form><div id="chart_container"><div id="chart"></div><div id="preview"></div></div>';
	document.getElementById('theTitle').innerText = profile.d_name;
	seriesData = [];
	allData = [];
	showamount = 50;
	cmdparam = sequence;
	var inputcount = inputnamearray.length;
	var d = new Date(); d = d.getTime() / 1000;
	var series = [];
	palette = new Rickshaw.Color.Palette( { scheme: 'cool' } );
	for(i = 1; i <= inputcount; i++){
		seriesData.push([{x: d, y: null}]);
		allData.push([{x: d, y: null}]);
		var aliasname = inputnamearray.filter(function(obj){
			return obj.origin == 'Input' + i;
		});
		var serie = {
			color: palette.color(),
			data: seriesData[i - 1],
			name: aliasname[0].alias
		};
		series.push(serie);
	}
	graph = new Rickshaw.Graph( {
		element: document.getElementById("chart"),
		min: 'auto',
		width: 900,
		height: 400,
		renderer: 'line',
		stroke: true,
		preserve: true,
		series: series
	} );

	graph.render();

	preview = new Rickshaw.Graph.RangeSlider( {
		graph: graph,
		element: document.getElementById('preview'),
	} );

	hoverDetail = new Rickshaw.Graph.HoverDetail( {
		graph: graph,
		xFormatter: function(x) {
			return new Date(x * 1000).toString();
		}
	} );

	legend = new Rickshaw.Graph.Legend( {
		graph: graph,
		element: document.getElementById('legend')
	} );

	shelving = new Rickshaw.Graph.Behavior.Series.Toggle( {
		graph: graph,
		legend: legend
	} );

	order = new Rickshaw.Graph.Behavior.Series.Order( {
		graph: graph,
		legend: legend
	} );

	highlighter = new Rickshaw.Graph.Behavior.Series.Highlight( {
		graph: graph,
		legend: legend
	} );

	xAxis = new Rickshaw.Graph.Axis.Time( {
		graph: graph,
		timeFixture: new Rickshaw.Fixtures.Time.Local()
	} );

	xAxis.render();

	yAxis = new Rickshaw.Graph.Axis.Y( {
		graph: graph,
		tickFormat: Rickshaw.Fixtures.Number.formatKMBT
	} );

	yAxis.render();


	controls = new RenderControls( {
		element: document.querySelector('form'),
		graph: graph
	} );

	document.getElementById("changelimitbutton").disabled = false;

}

function iot_app(){
	document.getElementById('content').innerHTML = "<b>" + profile.d_name + "</b>";
}

function Input1(data){
	var d = new Date(); d = d.getTime() / 1000;

	//this means that there is already a object in the array we just need to change its y value
	if(d - allData[0][allData[0].length - 1].x <= 3) {
		if(allData[0][allData[0].length - 1].y == null) {
			var obj = {x: allData[0][allData[0].length - 1].x, y: data[0]};
			allData[0][allData[0].length - 1] = obj;
			seriesData[0][seriesData[0].length - 1] = allData[0][allData[0].length - 1];
		}
		else return;
	}
	//this means that we need to push a new object to the array.
	//In order to have same length in all arrays we will also add object to others array with y  value null
	else {
		var obj = {x: d, y: data[0]} ;
		var nullobj = {x: d, y: null};
		allData[0].push(obj);
		if(cmdparam[1] == '1') allData[1].push(nullobj);
		if(cmdparam[2] == '1') allData[2].push(nullobj);
		if(cmdparam[3] == '1') allData[3].push(nullobj);
		if(cmdparam[4] == '1') allData[4].push(nullobj);
		seriesData[0].push(obj);
		if(cmdparam[1] == '1') seriesData[1].push(nullobj);
		if(cmdparam[2] == '1') seriesData[2].push(nullobj);
		if(cmdparam[3] == '1') seriesData[3].push(nullobj);
		if(cmdparam[4] == '1') seriesData[4].push(nullobj);
		if(seriesData[0]. length > showamount) {
			seriesData[0].splice(0, 1);
			if(cmdparam[1] == '1') seriesData[1].splice(0, 1);
			if(cmdparam[2] == '1') seriesData[2].splice(0, 1);
			if(cmdparam[3] == '1') seriesData[3].splice(0, 1);
			if(cmdparam[4] == '1') seriesData[4].splice(0, 1);
		}
	}
	graph.update();	
}

function Input2(data){
	var d = new Date(); d = d.getTime() / 1000;
	if(d - allData[1][allData[1].length - 1].x <= 3) {
		if(allData[1][allData[1].length - 1].y == null){
			var obj = {x: allData[1][allData[1].length - 1].x, y: data[0]};
			allData[1][allData[1].length - 1] = obj;
			seriesData[1][seriesData[1].length - 1] = allData[1][allData[1].length - 1];
		}
		else return;
	}
	else {
		var obj = {x: d, y: data[0]};
		var nullobj = {x: d, y: null};
		allData[1].push(obj);
		allData[0].push(nullobj);
		if(cmdparam[2] == '1') allData[2].push(nullobj);
		if(cmdparam[3] == '1') allData[3].push(nullobj);
		if(cmdparam[4] == '1') allData[4].push(nullobj);
		seriesData[1].push(obj);
		seriesData[0].push(nullobj);
		if(cmdparam[2] == '1') seriesData[2].push(nullobj);
		if(cmdparam[3] == '1') seriesData[3].push(nullobj);
		if(cmdparam[4] == '1') seriesData[4].push(nullobj);
		if(seriesData[0]. length > showamount) {
			seriesData[0].splice(0, 1);
			seriesData[1].splice(0, 1);
			if(cmdparam[2] == '1') seriesData[2].splice(0, 1);
			if(cmdparam[3] == '1') seriesData[3].splice(0, 1);
			if(cmdparam[4] == '1') seriesData[4].splice(0, 1);
		}
	}
	graph.update();
}

function Input3(data){
	var d = new Date(); d = d.getTime() / 1000;
	if(d - allData[2][allData[2].length - 1].x <= 3) {
		if(allData[2][allData[2].length - 1].y == null){
			var obj = {x: allData[2][allData[2].length - 1].x, y: data[0]};
			allData[2][allData[2].length - 1] = obj;
			seriesData[2][seriesData[2].length - 1] = allData[2][allData[2].length - 1];
		}
		else return;
	}
	else {
		var obj = {x: d, y: data[0]};
		var nullobj = {x: d, y: null};
		allData[2].push(obj);
		allData[0].push(nullobj);
		allData[1].push(nullobj);
		if(cmdparam[3] == '1') allData[3].push(nullobj);
		if(cmdparam[4] == '1') allData[4].push(nullobj);
		seriesData[2].push(obj);
		seriesData[0].push(nullobj);
		seriesData[1].push(nullobj);
		if(cmdparam[3] == '1') seriesData[3].push(nullobj);
		if(cmdparam[4] == '1') seriesData[4].push(nullobj);
		if(seriesData[0]. length > showamount) {
			seriesData[0].splice(0, 1);
			seriesData[1].splice(0, 1);
			seriesData[2].splice(0, 1);
			if(cmdparam[3] == '1') seriesData[3].splice(0, 1);
			if(cmdparam[4] == '1') seriesData[4].splice(0, 1);
		}
	}
	graph.update();
}

function Input4(data){
	var d = new Date(); d = d.getTime() / 1000;
	if(d - allData[3][allData[3].length - 1].x <= 3) {
		if(allData[3][allData[3].length - 1].y == null){
			var obj = {x: allData[3][allData[3].length - 1].x, y: data[0]};
			allData[3][allData[3].length - 1] = obj;
			seriesData[3][seriesData[3].length - 1] = allData[3][allData[3].length - 1];
		}
		else return;
	}
	else {
		var obj = {x: d, y: data[0]};
		var nullobj = {x: d, y: null};
		allData[3].push(obj);		
		allData[0].push(nullobj);
		allData[1].push(nullobj);
		allData[2].push(nullobj);
		if(cmdparam[4] == '1') allData[4].push(nullobj);
		seriesData[3].push(obj);
		seriesData[0].push(nullobj);
		seriesData[1].push(nullobj);
		seriesData[2].push(nullobj);
		if(cmdparam[4] == '1') seriesData[4].push(nullobj);
		if(seriesData[0]. length > showamount) {
			seriesData[0].splice(0, 1);
			seriesData[1].splice(0, 1);
			seriesData[2].splice(0, 1);
			seriesData[3].splice(0, 1);
			if(cmdparam[4] == '1') seriesData[4].splice(0, 1);
		}
	}
	graph.update();
}

function Input5(data){
	var d = new Date(); d = d.getTime() / 1000;
	if(d - allData[4][allData[4].length - 1].x <= 3) {
		if(allData[4][allData[4].length - 1].y == null){
			var obj = {x: allData[4][allData[4].length - 1].x, y: data[0]};
			allData[4][allData[4].length - 1] = obj;
			seriesData[4][seriesData[4].length - 1] = allData[4][allData[4].length - 1];
		}
		else return;
	}
	else {
		var obj = {x: d, y: data[0]};
		var nullobj = {x: d, y: null};
		allData[4].push(obj);		
		allData[0].push(nullobj);
		allData[1].push(nullobj);
		allData[2].push(nullobj);
		allData[3].push(nullobj);
		seriesData[4].push(obj);
		seriesData[0].push(nullobj);
		seriesData[1].push(nullobj);
		seriesData[2].push(nullobj);
		seriesData[3].push(nullobj);
		if(seriesData[0]. length > showamount) {
			seriesData[0].splice(0, 1);
			seriesData[1].splice(0, 1);
			seriesData[2].splice(0, 1);
			seriesData[3].splice(0, 1);
			seriesData[4].splice(0, 1);
		}
	}
	graph.update();
}

var profile = {
	'dm_name' : 'Graph',
	'df_list' : [Input1, Input2, Input3, Input4, Input5],
}

var ida = {
	'iot_app': iot_app,
	'onMount': draw
}

dai(profile, ida);
