var default_map_center = { lat:24.7895711, lng:120.9967021};
var obstacle_area = 0.000086;//unit:度
var ob_route_dis_std = 0.0000303;//unit:度, 小於ob_route_dis_std代表路線經過障礙物
var map;

var app_mobility_select_on_off = 0;
var app_icon_select_on_off = 0;
var app_visual_select_on_off = 0;
var app_form_value = []; //app(0), mobility(1), icon(2), picture(3), visual(4), color_min(5), color_max(6), quick_access(7), kind(8)

var marker_now = null;
var icon_loc_listener, icon_loc_marker, icon_loc;
var cam_src;

var already_use_letter = [];
var all_static_icon_list = [];
var all_app_list = [];
var all_icon_list = [];
var all_iottalk_data_list = [];
var app_num = null;
var icon_num = null;

var form;
var optradio;
var interval;
var timeout;
var tracking_timeout;
var left = 0;

var quick_access_count = 0;
var mobile_width = 560;
var quick_access_space;

var offline_hours = 2; //If offline_hours = 1, represent latest update time over 1 hours ago

var marker_list = [];

var color_movable = [['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'], 
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'], 
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'], 
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'], 
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'], 
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'], 
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'], 
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'], 
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'], 
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
['#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d','#00ff7f', '#f5f505', '#ff7f00', '#ff0000', '#f5057d'],
];

var color_shape = ['#337ab7', '#b10876', '#f0ad4e', '#5cb85c','#cc6681', '#2690a9', '#5614c2', '#836eaa', '#f26649', '#86922f', '#5bc0de', '#BB5500', '#f53794','#a15a4a', '#F400F7', '#00BFA5', '#136edd', '#339966', '#ab4fe4', '#c01f41', '#00FF00', '#BBBB00', '#e80a02', '#f0ad4e', '#e12cf2', '#3d8a05', '#ff3eff'];

var color_range = ['#5bc0de','green', 'yellow', 'orange', 'red'];

var MarkerzIndex = 999;

// Create an array of styles.
var styles = 
[
  {
      "featureType": "water",
      "elementType": "geometry.fill",
      "stylers": [
          {
              "color": "#d3d3d3"
          }
      ]
  },
  {
      "featureType": "transit",
      "stylers": [
          {
              "color": "#808080"
          },
          {
              "visibility": "off"
          }
      ]
  },
  {
      "featureType": "road.highway",
      "elementType": "geometry.stroke",
      "stylers": [
          {
              "visibility": "on"
          },
          {
              "color": "#b3b3b3"
          }
      ]
  },
  {
      "featureType": "road.highway",
      "elementType": "geometry.fill",
      "stylers": [
          {
              "color": "#ffffff"
          }
      ]
  },
  {
      "featureType": "road.local",
      "elementType": "geometry.fill",
      "stylers": [
          {
              "visibility": "on"
          },
          {
              "color": "#ffffff"
          },
          // {
          //     "weight": 7
          // }
      ]
  },
  {
      "featureType": "road.local",
      "elementType": "geometry.stroke",
      "stylers": [
          {
              "color": "#d7d7d7"
          }
      ]
  },
  {
      "featureType": "poi",
      "elementType": "geometry.fill",
      "stylers": [
          {
              "visibility": "on"
          },
          {
              "color": "#ebebeb"
          }
      ]
  },
  {
      "featureType": "administrative",
      "elementType": "geometry",
      "stylers": [
          {
              "color": "#a7a7a7"
          }
      ]
  },
  {
      "featureType": "road.arterial",
      "elementType": "geometry.fill",
      "stylers": [
          {
              "color": "#ffffff"
          }
      ]
  },
  {
      "featureType": "road.arterial",
      "elementType": "geometry.fill",
      "stylers": [
          {
              "color": "#ffffff"
          }
      ]
  },
  {
      "featureType": "landscape",
      "elementType": "geometry.fill",
      "stylers": [
          {
              "visibility": "on"
          },
          {
              "color": "#efefef"
          }
      ]
  },
  {
      "featureType": "road",
      "elementType": "labels.text.fill",
      "stylers": [
          {
              "color": "#696969"
          }
      ]
  },
  {
      "featureType": "administrative",
      "elementType": "labels.text.fill",
      "stylers": [
          {
              "visibility": "on"
          },
          {
              "color": "#737373"
          }
      ]
  },
  {
      "featureType": "poi",
      "elementType": "labels.icon",
      "stylers": [
          {
              "visibility": "off"
          }
      ]
  },
  {
      "featureType": "poi",
      "elementType": "labels",
      "stylers": [
          {
              "visibility": "off"
          }
      ]
  },
  {
      "featureType": "road.arterial",
      "elementType": "geometry.stroke",
      "stylers": [
          {
              "color": "#d6d6d6"
          }
      ]
  },
  {
      "featureType": "road",
      "elementType": "labels.icon",
      "stylers": [
          {
              "visibility": "off"
          }
      ]
  },
  {},
  {
      "featureType": "poi",
      "elementType": "geometry.fill",
      "stylers": [
          {
              "color": "#dadada"
          }
      ]
  }
];

//with no secure connection, substitute map-server-port(default 8866)
//var socket = io.connect('http://'+location.hostname+':map-server-port/hpc');
var socket = io.connect('https://'+location.hostname+'/hpc');

//Routing setting
var selectedMode = "DRIVING";
var waypts = [ //中繼點
  [],
  [{
    location: {lat: 24.789457, lng: 120.995396},  //1  綜合球館前轉角
    stopover: true
  },
  {
    location: {lat: 24.789604, lng: 120.997128},  //  二餐前轉角
    stopover: true
  }],
  [{
    location: {lat: 24.787497, lng: 120.997339},  //2  小木屋前轉角
    stopover: true
  }],
  [{
    location: {lat: 24.784064, lng: 120.997999},  //3  土木結構實驗室前
    stopover: true
  }],
  [{
    location: {lat: 24.783849, lng: 120.998811},  //4  土木結構實驗室前偏右
    stopover: true
  }],
  [{
    location: {lat: 24.783832, lng: 120.998788},  //4  土木結構實驗室前偏右2
    stopover: true
  }],
  [{
    location: {lat: 24.789604, lng: 120.997128},  //5  二餐前轉角
    stopover: true
  },
  {
    location: {lat: 24.788613, lng: 120.999540},  //  中正堂旁停車場
    stopover: true
  }],
  [{
    location: {lat: 24.788744, lng: 120.998850},  //6   中正堂三角
    stopover: true
  }],
  [{
    location: {lat: 24.788613, lng: 120.999540},  //7  中正堂旁停車場
    stopover: true
  },
  {
    location: {lat: 24.784992, lng: 121.000237},  //  奈米電子研究大樓
    stopover: true
  }],
  [{
    location: {lat: 24.789604, lng: 120.997128},  //8  二餐前轉角
    stopover: true
  },
  {
    location: {lat: 24.783849, lng: 120.998811},  //  土木結構實驗室前偏右
    stopover: true
  }],
  [{
    location: {lat: 24.784134, lng: 120.999825},  //9  麥當勞轉角
    stopover: true
  }],
  [{
    location: {lat: 24.789457, lng: 120.995396},  //10  綜合球館前轉角
    stopover: true
  },
  {
    location: {lat: 24.789604, lng: 120.997128},  //  二餐前轉角
    stopover: true
  }
  ],
  [{
    location: {lat: 24.785409, lng: 120.995354},  //11  研二舍
    stopover: true
  }],
  [{
    location: {lat: 24.786650, lng: 121.000530},  //12  人社二館
    stopover: true
  }],
  [{
    location: {lat: 24.789604, lng: 120.997128},  //13  二餐前轉角
    stopover: true
  },
  {
    location: {lat: 24.786650, lng: 121.000530},  //  人社二館
    stopover: true
  }],
  [{
    location: {lat: 24.789604, lng: 120.997128},  //14  二餐前轉角
    stopover: true
  },
  {
    location: {lat: 24.785409, lng: 120.995354},  //  研二舍
    stopover: true
  }],
  [{
    location: {lat: 24.784064, lng: 120.997999},  //15 土木結構實驗室前
    stopover: true
  },
  {
    location: {lat: 24.786650, lng: 121.000530},  // 人社二館
    stopover: true
  }],
];