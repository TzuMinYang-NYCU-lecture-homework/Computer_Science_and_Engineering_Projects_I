function initialize() {
  // Create a new StyledMapType object, passing it the array of styles,
  // as well as the name to be displayed on the map type control.
  var styledMap = new google.maps.StyledMapType(styles,
    {name: "Styled Map"});      
  // Create a map object, and include the MapTypeId to add
  // to the map type control.
  var mapOptions = {
    disableDefaultUI: true,
    zoom: 17,
    zoomControl: true,
    scaleControl: true,
    scrollwheel: true,
    center: new google.maps.LatLng(default_map_center.lat, default_map_center.lng),
    gestureHandling: 'greedy',
    mapTypeControlOptions: {
      mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'map_style']
    }
  };
  map = new google.maps.Map(document.getElementById('Location-map'), mapOptions);
  //Associate the styled map with the MapTypeId and set it to display.
  map.mapTypes.set('map_style', styledMap);
  map.setMapTypeId('map_style');
}

function getLocation_admin() {
    var startPos;
    var geoOptions = {
      enableHighAccuracy: true
    }
    var geoSuccess = function(position) {
      var lat = position.coords.latitude;
      var lng = position.coords.longitude;
      var CurrentPosition = {lat: lat, lng: lng};
      addMarker_routing(CurrentPosition);
    };
    var geoError = function(error) {
      console.log('Error occurred. Error code: ' + error.code);
      // error.code can be:
      //   0: unknown error
      //   1: permission denied
      //   2: position unavailable (error response from location provider)
      //   3: timed out
    };

    navigator.geolocation.getCurrentPosition(geoSuccess, geoError, geoOptions);
}

function addMarker_routing(location) {
  marker_now = new google.maps.Marker({
    position: location,
    label: "現在位置",
    map: map
  });

  map.setCenter(location);
}

function refresh_app_form()
{
  app_num = null;
  $('#app_name').val('');
  $("#app_mobility_select").val("Stationary");
  $("#app_icon_select").val("NoLetter");
  $('#picture_URL').val('');
  $("#app_visual_select").val("Text");
  $('#color_min').val('');
  $('#color_max').val('');
  $('#Quick_Access_decide').prop('checked', false);
  $('#Visual').hide();
  for(var letter=0; letter<26; letter++)
  {
    $("#app_icon_select option[value='"+String.fromCharCode(65+letter)+"']").remove();
  }
  $('#app_form').hide();
}

function refresh_icon_form()
{
  app_num = null;
  icon_num = null;
  icon_loc = null;
  if(marker_now != null) marker_now.setMap(null);
  if(icon_loc_marker != null) icon_loc_marker.setMap(null);
  if(icon_loc_listener != undefined) google.maps.event.removeListener(icon_loc_listener);
  $('#icon_name').val('');
  $('#icon_loc').val('');
  $('#icon_loc').removeAttr('disabled');
  $('#icon_desc').val('');
  $('#icon_form').hide();
}

//update icon location
function icon_loc_update()
{
  if(icon_loc_listener != undefined) google.maps.event.removeListener(icon_loc_listener);
  icon_loc_listener = google.maps.event.addListener(map, 'click', function(event) {
    if(icon_num != null)
    {
      all_static_icon_list[icon_num].marker.setVisible(false);
      all_static_icon_list[icon_num].info.close();
    }
    if(icon_loc_marker != null) icon_loc_marker.setMap(null);
    icon_loc = event.latLng;

    var lat = icon_loc.lat();
    var lng = icon_loc.lng();

    icon_loc_marker = icon_style(app_num, lat, lng);
    icon_loc_marker.setVisible(true);

    icon_loc_marker.addListener('click', function() {
      icon_loc_marker.setMap(null);
      $('#icon_loc').val('');
    });

    $('#icon_loc').val(lat.toFixed(8)+ ", " + lng.toFixed(8));
  });
}

function refresh_all_form()
{
  refresh_icon_form();
  refresh_app_form();
}

function load_all_app()
{
  if(all_app_list.length > 0)
  {
    for(var i=0; i<all_app_list.length; i++)
    {
      $(document).off('click', '#show_'+i);
      $(document).off('click', '#app_'+i);
      $(document).off('click', '#add_'+i);
      $('#'+i+'_menu').remove();
      $('#'+i+'_quick_menu').remove();  
    }
    for(var i=0; i<all_static_icon_list.length; i++)
    {
      $(document).off('click', '#icon_'+i);
      all_static_icon_list[i].marker.setMap(null);
      google.maps.event.removeListener(all_static_icon_list[i].marker_listener);
    }
    already_use_letter = [];
    all_static_icon_list = [];
    all_app_list = [];
  }
  //number(0), app(1), kind(2) mobility(3), icon(4), picture(5), visual(6), color_min(7), color_max(8), quick_access(9)
  $.getJSON($SCRIPT_ROOT + '/secure/_take_all_app', function(data) {
    all_app_list = data.result.map(function(obj) {return {
        'number': obj.number,
        'app': obj.app,
        'kind': obj.kind,
        'mobility': obj.mobility,
        'icon': obj.icon,
        'picture': obj.picture,
        'visual': obj.visual,
        'color_min': obj.color_min,
        'color_max':obj.color_max,
        'quick_access': obj.quick_access
      }; 
    });
    console.log(all_app_list);

    $.getJSON($SCRIPT_ROOT + '/secure/_take_all_static_icon', function(data) {
      all_static_icon_list = data.result.map(function(obj) {return  {
          'number': obj.number,
          'ori_app_num': obj.app_num,
          'name': obj.name,
          'lat': obj.lat,
          'lng': obj.lng,
          'description': obj.description
        }; 
      });
      console.log(all_static_icon_list);
      
      for(var i=0; i<all_app_list.length; i++)
      {            
        var app_name = all_app_list[i].app;

        str = '<div id="'+i+'_menu"><button type="button" style="cursor:default;background-color:#fff; min-width:138px; color:#555" class="list-group-item history btn btn-outline-primary" data-toggle="collapse" data-parent="#MainMenu" data-target="#'+i+'_list" id="app_'+i+'" value="'+i+'">'+app_name+' &#9662;</button></div>';
        $('#app_list').append(str);

        if(all_app_list[i].quick_access == 1)
        {
          console.log('quick_access == 1: ' + all_app_list[i].app);
          str = '<li id="'+i+'_quick_menu" role="presentation" class="menu-item dropdown dropdown-hover" class="active"> \
                  <button type="button" id="app_'+i+'" style="min-width:120px;height:40px;cursor:pointer;color:#fff;background:'+color_shape[i]+';" class="dropdown-toggle history btn btn-outline-primary" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false" value="'+i+'">'+app_name+'<span class="caret"></span></button> \
                </li>';
          $('#list').append(str);
        }
        

        if(all_app_list[i].kind>=1 && all_app_list[i].kind<=8)
        {
          console.log("app: " + $('#app_'+i).val() + ", kind: " + all_app_list[i].kind);

          str = '<div class="collapse subnav" style="min-width: 140px;" id="'+i+'_list"></div>';
          $('#'+i+'_menu').append(str);

          if(all_app_list[i].kind>=1 && all_app_list[i].kind<=4)
          {
          str = '<button type="button" style="border-color:white ;background-color:  #eee; min-width:100%; color:#337ab7" class="list-group-item history btn btn-outline-primary" id="add_'+i+'" value="'+i+'">Add '+all_app_list[i].app+'</button>';
          $('#'+i+'_list').append(str);
          }

          str = '<button type="button" style="border-color:white ;background-color:  #eee; min-width:100%; color:#337ab7" class="list-group-item history btn btn-outline-primary" id="show_'+i+'" value="'+i+'">Show All</button>';
          $('#'+i+'_list').append(str);

          if(all_app_list[i].quick_access == 1)
          {
            str = '<ul class="dropdown-menu pre-scrollable" id="'+i+'_quick_list" style="min-width: 130px;"></ul>';
            $('#'+i+'_quick_menu').append(str);

            if(all_app_list[i].kind>=1 && all_app_list[i].kind<=4)
            {
            str = '<li style="cursor:pointer;min-width: 140px;" ><button  type="button" style="border-color:white ;background-color:#eee; min-width:100%; color:#337ab7" class="history btn btn-outline-primary" id="add_'+i+'" value="'+i+'">Add '+all_app_list[i].app+'</button></li>';
            $('#'+i+'_quick_list').append(str);
            }
            str = '<li style="cursor:pointer;min-width: 140px;" ><button  type="button" style="border-color:white ;background-color:#eee; min-width:100%; color:#337ab7" class="history btn btn-outline-primary" id="show_'+i+'" value="'+i+'">Show All</button></li>';
            $('#'+i+'_quick_list').append(str);
          }

          all_app_list[i].show = 0;
          all_app_list[i].show_count = 0;

          for(var j=0; j<all_static_icon_list.length; j++)
          {
            if(all_static_icon_list[j].ori_app_num == all_app_list[i].number)
            {
              var marker = icon_style(i, all_static_icon_list[j].lat, all_static_icon_list[j].lng);
              all_static_icon_list[j].app_num = i;
              var marker_listener = icon_listener(j, marker);
              all_static_icon_list[j].show = 0;
              all_static_icon_list[j].marker = marker;
              all_static_icon_list[j].marker_listener = marker_listener[0];
              all_static_icon_list[j].info = marker_listener[1];

              str = '<button type="button" style="border-color:white ;background-color:  #eee; min-width:100%; color:#337ab7" class="list-group-item history btn btn-outline-primary" id="icon_'+j+'" value="'+j+'">'+all_static_icon_list[j].name+'</button>';
              $('#'+i+'_list').append(str);

              if(all_app_list[i].quick_access == 1)
              {
                str = '<li style="cursor:pointer;min-width: 140px;" ><button  type="button" style="border-color:white ;background-color:#eee; min-width:100%; color:#337ab7" class="history btn btn-outline-primary" id="icon_'+j+'" value="'+j+'">'+all_static_icon_list[j].name+'</button></li>';
                $('#'+i+'_quick_list').append(str);
              }

              $(document).on('click', '#icon_'+j, function(){
                  refresh_all_form();
                  icon_num = $(this).val();
                  app_num = all_static_icon_list[icon_num].app_num;
                  $('#MainMenu').collapse('hide');
                  $('#'+app_num+'_list').collapse('hide');
                  console.log('all_static_icon_list[icon_num].show: '+ all_static_icon_list[icon_num].show);
                  if(all_static_icon_list[icon_num].show == 0)
                  {
                    all_static_icon_list[icon_num].show = 1;
                    $('[id="icon_'+icon_num+'"]').css("background-color", color_shape[app_num]);
                    $('[id="icon_'+icon_num+'"]').css("color", "white");
                    $('#icon_name').val(all_static_icon_list[icon_num].name);
                    $('#icon_loc').val(all_static_icon_list[icon_num].lat.toFixed(8)+ ", " + all_static_icon_list[icon_num].lng.toFixed(8));
                    if(all_app_list[app_num].kind>=5 && all_app_list[app_num].kind<=8)
                      $('#icon_loc').attr('disabled', true);
                    else
                      $('#icon_loc').removeAttr('disabled');
                    $('#icon_desc').val(all_static_icon_list[icon_num].description);
                    map.setCenter({lat: all_static_icon_list[icon_num].lat, lng: all_static_icon_list[icon_num].lng});
                    if(all_app_list[app_num].kind>=1 && all_app_list[app_num].kind<=4)
                      icon_loc_update();
                    all_static_icon_list[icon_num].info.open(map, all_static_icon_list[icon_num].marker);
                    all_static_icon_list[icon_num].marker.setVisible(true);
                    $('#icon_form').show();
                  }
                  else //all_static_icon_list[icon_num].show == 1
                  {
                    if(all_app_list[app_num].show > 0)
                    {
                      all_app_list[app_num].show = 0;
                      $('[id="show_'+app_num+'"]').css("background-color", "#eee");
                      $('[id="show_'+app_num+'"]').css("color", "#337ab7");
                      $('[id="show_'+app_num+'"]').html('Show All');
                    }
                    all_static_icon_list[icon_num].show = 0;
                    $('[id="icon_'+icon_num+'"]').css("background-color", "#eee");
                    $('[id="icon_'+icon_num+'"]').css("color", "#337ab7");
                    all_static_icon_list[icon_num].info.close();
                    all_static_icon_list[icon_num].marker.setVisible(false);
                    refresh_icon_form();
                  }
              });

            }
          }
        }
        
        if(all_app_list[i].kind==3 || all_app_list[i].kind==4 || all_app_list[i].kind==7 || all_app_list[i].kind==8)
        {
          already_use_letter.push(all_app_list[i].icon);
          console.log(already_use_letter);
        }

        $(document).on('click', '#show_'+i, function(){
            app_num = $(this).val();
            $('#MainMenu').collapse('hide');
            $('#'+app_num+'_list').collapse('hide');
            console.log('app_num: '+ app_num);
            if(all_app_list[app_num].show == 0)
            {
              all_app_list[app_num].show = 1;
              $('[id="show_'+app_num+'"]').css("background-color", color_shape[app_num]);
              $('[id="show_'+app_num+'"]').css("color", "white");
              $('[id="show_'+app_num+'"]').html('Hide All');

              for(var j=0; j<all_static_icon_list.length; j++)
              {
                if(all_static_icon_list[j].app_num == app_num)
                {
                  all_static_icon_list[j].show = 1;
                  $('[id="icon_'+j+'"]').css("background-color", color_shape[app_num]);
                  $('[id="icon_'+j+'"]').css("color", "white");
                  all_static_icon_list[j].marker.setVisible(true);
                }
              }
            }
            else //all_app_list[app_num].show == 1
            {
              all_app_list[app_num].show = 0;
              $('[id="show_'+app_num+'"]').css("background-color", "#eee");
              $('[id="show_'+app_num+'"]').css("color", "#337ab7");
              $('[id="show_'+app_num+'"]').html('Show All');
              for(var j=0; j<all_static_icon_list.length; j++)
              {
                if(all_static_icon_list[j].app_num == app_num)
                {
                  all_static_icon_list[j].show = 0;
                  $('[id="icon_'+j+'"]').css("background-color", "#eee");
                  $('[id="icon_'+j+'"]').css("color", "#337ab7");
                  all_static_icon_list[j].info.close();
                  all_static_icon_list[j].marker.setVisible(false);
                }
              }
            }
        });

        $(document).on('click', '#app_'+i, function(){
            refresh_all_form();
            app_num = $(this).val();
            for(var letter=0; letter<26; letter++)
            {
              $("#app_icon_select").append($("<option></option>").attr("value", String.fromCharCode(65+letter)).text(String.fromCharCode(65+letter)));    
              for(var i=0; i<already_use_letter.length; i++)
              {
                if(String.fromCharCode(65+letter) == already_use_letter[i])
                {
                  if(String.fromCharCode(65+letter) != all_app_list[app_num].icon)
                    $("#app_icon_select option[value='"+String.fromCharCode(65+letter)+"']").remove();
                }
              }
            }

            $('#app_name').val(all_app_list[app_num].app);
            $("#app_mobility_select").val(all_app_list[app_num].mobility);
            $("#app_icon_select").val(all_app_list[app_num].icon);
            $('#picture_URL').val(all_app_list[app_num].picture);
            if(all_app_list[app_num].visual.length > 0)
            {
              $("#app_visual_select").val(all_app_list[app_num].visual);
              $('#Visual').show();
            }
            $('#color_min').val(all_app_list[app_num].color_min);
            $('#color_max').val(all_app_list[app_num].color_max);
            if(all_app_list[app_num].quick_access == 1)
              $('#Quick_Access_decide').prop('checked', true);
            $('#app_form').show();

        });

        $(document).on('click', '#add_'+i, function(){
            refresh_all_form();
            getLocation_admin();
            icon_loc_update();

            app_num = $(this).val();

            $('#icon_form').show();
        });

      }
    });
  });
}

// create marker
function icon_style(app_num, lat, lng)
{
  if(all_app_list[app_num].kind == 1 || all_app_list[app_num].kind == 5)
  {
    var marker = new google.maps.Marker({
      position:{lat: lat, lng: lng},
      map: map,
      title: all_app_list[app_num].app,
      icon:{
        path: google.maps.SymbolPath.CIRCLE,
        scale: 15,
        strokeWeight:7,
        fillColor:color_shape[app_num],
        fillOpacity: 1,
        strokeColor:color_shape[app_num]
      },
      visible: false,
      zIndex: 999
    });
    return marker;
  }
  else if(all_app_list[app_num].kind == 2 || all_app_list[app_num].kind == 6)
  {
    var marker = new google.maps.Marker({
        position: {lat: lat, lng: lng},
        icon: all_app_list[app_num].picture,
        map: map,
        title: all_app_list[app_num].app,
        visible: false
    });
    return marker;
  }
  else if(all_app_list[app_num].kind == 3 || all_app_list[app_num].kind == 7)
  {
    var marker = new google.maps.Marker({
      position:{lat: lat, lng: lng},
      map: map,
      title: all_app_list[app_num].app,
      label: {text: all_app_list[app_num].icon.toString(), fontSize: "25px"},
      icon:{
        path: 'M -1.5,-0.5 1.5,-0.5 1.5,0.5 -1.5,0.5 z',
        scale: 15,
        strokeWeight:10,
        fillColor:color_shape[app_num],
        fillOpacity: 1,
        strokeColor:color_shape[app_num]
      },
      visible: false,
      zIndex: 999
    });
    return marker;
  }
  else if(all_app_list[app_num].kind == 4 || all_app_list[app_num].kind == 8)
  {
    var marker = new google.maps.Marker({
      position:{lat: lat, lng: lng},
      map: map,
      title: all_app_list[app_num].app,
      label: {text: all_app_list[app_num].icon.toString(), fontSize: "25px"},
      icon:{
        path: 'M -0.5,-0.5 0.5,-0.5 0.5,0.5 -0.5,0.5 z',
        scale: 15,
        strokeWeight:10,
        fillColor:color_shape[app_num],
        fillOpacity: 1,
        strokeColor:color_shape[app_num]
      },
      visible: false,
      zIndex: 999
    });
    return marker;
  }
}

// create InfoWindow
function icon_listener(icon, marker)
{
  var content_text = all_static_icon_list[icon].description;
  content_text = content_text.replace(/((http|https|ftp):\/\/[\w?=&.\/-;#~%-]+(?![\w\s?&.\/;#~%"=-]*>))/g, '<a target="_blank" href="$1">$1</a> ');
  var info = new google.maps.InfoWindow({
    content: content_text
  });
  var marker_listener = marker.addListener('click', function() {
    info.open(map, marker);
    refresh_all_form();
    icon_num = icon;
    app_num = all_static_icon_list[icon].app_num;
    $('#icon_name').val(all_static_icon_list[icon].name);
    $('#icon_loc').val(all_static_icon_list[icon].lat.toFixed(8)+ ", " + all_static_icon_list[icon].lng.toFixed(8));
    if(all_app_list[app_num].kind>=5 && all_app_list[app_num].kind<=8)
      $('#icon_loc').attr('disabled', true);
    else
      $('#icon_loc').removeAttr('disabled');
    $('#icon_desc').val(all_static_icon_list[icon].description);
    map.setCenter({lat: all_static_icon_list[icon].lat, lng: all_static_icon_list[icon].lng});
    if(all_app_list[app_num].kind>=1 && all_app_list[app_num].kind<=4)
      icon_loc_update();
    $('#icon_form').show();
  });
  return [marker_listener, info];
}

//Do after js files loading finish
$(function(){
    initialize();
    load_all_app();

    // ‘Add app’ item
    $(document).on('click', '#app_add', function(){
        $('#MainMenu').collapse('hide');
        refresh_all_form();

        for(var letter=0; letter<26; letter++)
        {
          $("#app_icon_select").append($("<option></option>").attr("value", String.fromCharCode(65+letter)).text(String.fromCharCode(65+letter)));    
          for(var i=0; i<already_use_letter.length; i++)
          {
            if(String.fromCharCode(65+letter) == already_use_letter[i])
            {
              $("#app_icon_select option[value='"+String.fromCharCode(65+letter)+"']").remove();
            }
          }
        }
        $('#app_form').show();
    });

    // The Location field (Figure 4(b)) implements
    // the location attribute of the cyber object (Figure 2(7)), where either
    // ‘Stationary’ or ‘Movable’ should be selected.
    $(document).on('click', '#app_mobility_select', function(){
        if(app_mobility_select_on_off == 0)
          app_mobility_select_on_off = 1;
        else       //app_mobility_select_on_off == 1
        {
          app_mobility_select_on_off = 0;
          var mobility = $("#app_mobility_select").val();
          console.log(mobility);
        }
    });

    // The Layout field (Figure 4(c)) implements the layout attribute (Figure 2(1)),
    // which provides three options.
    $(document).on('click', '#app_icon_select', function(){
        if(app_icon_select_on_off == 0)
          app_icon_select_on_off = 1;
        else       //app_icon_select_on_off == 1
        {
          app_icon_select_on_off = 0;
          var icon = $("#app_icon_select").val();
          console.log(icon);
          if(icon.localeCompare("Picture") == 0)
          {
          $('#Picture').modal('show');
          $('#Visual').hide();
          $('#Color').modal('hide');
          }
          else if(icon.localeCompare("NoLetter") == 0)
          {
            $('#Picture').modal('hide');
            $('#Visual').hide();
            $('#Color').modal('hide');
          }
          else
          {
            $('#Visual').show();
            $('#Picture').modal('hide');
          }
        }
    });

    // The Quick Access field (Figure 4(j)) allows the administrator to put the
    // created application in the menu bar (e.g. Figure 7(c)) for quick access.
    $('#Quick_Access_decide').attr("checked", false);

    // The Value field (Figure 4(g)) implements the value attribute of the cyber object
    // (Figure 2(4)) with two options. 
    $(document).on('click', '#app_visual_select', function(){
        if(app_visual_select_on_off == 0)
          app_visual_select_on_off = 1;
        else
        {
          app_visual_select_on_off = 0;
          var Visual = $("#app_visual_select").find(":selected").val();
          console.log(Visual);
          if(Visual.localeCompare("Color") == 0)
          {
             $('#Color').modal('show');
          }
          else
          {
             $('#Color').modal('hide');
          }
        }
    });


    $(document).on('click', '#app_save', function(){
        app_form_value.push($('#app_name').val());
        app_form_value.push($('#app_mobility_select').val());
        app_form_value.push($('#app_icon_select').val());
        app_form_value.push($('#picture_URL').val());
        app_form_value.push($('#app_visual_select').val());
        app_form_value.push($('#color_min').val());
        app_form_value.push($('#color_max').val());

        if($("#Quick_Access_decide").prop('checked') == true)
          app_form_value.push(1);
        else
          app_form_value.push(0);


        if(app_form_value[1] == "Stationary")
        {
          if(app_form_value[2] == "NoLetter")
          {
            app_form_value.push(1);
            app_form_value[4] = null;
          }
          else if(app_form_value[2] == "Picture")
          {
            app_form_value.push(2);
            app_form_value[4] = null;
          }
          else
          {
            if(app_form_value[4] == "Text")
            {
              app_form_value.push(3);   
            }
            else if(app_form_value[4] == "Color")
            {
              app_form_value.push(4);    
            }
          }
        }
        else if(app_form_value[1] == "Movable")
        {
          if(app_form_value[2] == "NoLetter")
          {
            app_form_value.push(5);
            app_form_value[4] = null;
          }
          else if(app_form_value[2] == "Picture")
          {
            app_form_value.push(6);
            app_form_value[4] = null;
          }
          else
          {
            if(app_form_value[4] == "Text")
            {
              app_form_value.push(7);   
            }
            else if(app_form_value[4] == "Color")
            {
              app_form_value.push(8);    
            }
          }
        }

        if(app_num == null)
        {
          $.getJSON($SCRIPT_ROOT + '/secure/_add_app',{
              app: app_form_value[0],
              kind: app_form_value[8],
              mobility: app_form_value[1],
              icon: app_form_value[2],
              picture: app_form_value[3],
              visual: app_form_value[4],
              color_min: app_form_value[5],
              color_max: app_form_value[6],
              quick_access: app_form_value[7]
            }, function(data) {
              console.log(app_form_value);
              app_form_value = [];
              load_all_app();
              refresh_app_form();
          });
        }
        else
        {
          $.getJSON($SCRIPT_ROOT + '/secure/_modify_app',{
              number: all_app_list[app_num].number,
              app: app_form_value[0],
              kind: app_form_value[8],
              mobility: app_form_value[1],
              icon: app_form_value[2],
              picture: app_form_value[3],
              visual: app_form_value[4],
              color_min: app_form_value[5],
              color_max: app_form_value[6],
              quick_access: app_form_value[7]
            }, function(data) {
              console.log( app_num+ " " + app_form_value);
              app_form_value = [];
              load_all_app();
              refresh_app_form();
          });
        }
    });

    $(document).on('click', '#app_del', function(){
        console.log('app_del num:' + app_num);
        if(app_num != null)
        {
          $.getJSON($SCRIPT_ROOT + '/secure/_del_app',{
              number: all_app_list[app_num].number
            }, function(data) {
              load_all_app();
          });
        }
        refresh_app_form();
    });

    $(document).on('click', '#app_cancel', function(){
      refresh_app_form();
    });

    $(document).on('click', '#icon_save', function(){
        icon_loc = $('#icon_loc').val().split(",");
        if(icon_num != null)
            all_static_icon_list[icon_num].marker.setVisible(false);
        if(icon_num == null)
        {
          $.getJSON($SCRIPT_ROOT + '/secure/_add_static_icon',{
              app_num: all_app_list[app_num].number,
              name: $('#icon_name').val(),
              lat: icon_loc[0],
              lng: icon_loc[1],
              description: $('#icon_desc').val()
            }, function(data) {
              load_all_app();
              refresh_icon_form();
          });
        }
        else
        {
          $.getJSON($SCRIPT_ROOT + '/secure/_modify_static_icon',{
              number: all_static_icon_list[icon_num].number,
              name: $('#icon_name').val(),
              lat: icon_loc[0],
              lng: icon_loc[1],
              description: $('#icon_desc').val()
            }, function(data) {
              load_all_app();
              refresh_icon_form();
          });
        }
    });

    $(document).on('click', '#icon_del', function(){
        console.log('icon_del num:' + icon_num);
        if(icon_num != null)
        {
          $.getJSON($SCRIPT_ROOT + '/secure/_del_static_icon',{
              number: all_static_icon_list[icon_num].number
            }, function(data) {
              load_all_app();
              refresh_icon_form();
          });
        }
        else
        {
          refresh_icon_form();
        }
    });

    $(document).on('click', '#icon_cancel', function(){
      refresh_icon_form();
    });

    $(document).on('mouseleave', '#MainMenu', function(){
        $('.collapse').collapse('hide');  
    });

    $(document).click(function(e) {
        console.log(e.target);
        if (!$(e.target).is('.list-group-item')) {
            $('.collapse').collapse('hide');      
        }
    });
    
});