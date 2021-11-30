$(function() {
    var feature_level_data = {
        //'feature_name' : ['min', 'max', 'default', 'step']
        'size':         [0, 10, 0, 1],
        'angle':        [0, 120, 0, 10]
        /*'color_r':      [0, 255, 255, 25.5],
        'color_g':      [0, 255, 255, 25.5],
        'color_b':      [0, 255, 255, 25.5],
        'bg_color_r':   [0, 255, 0, 25.5],
        'bg_color_g':   [0, 255, 0, 25.5],
        'bg_color_b':   [0, 255, 0, 25.5],
        's0':           [192, 476, 384, 28.4],
        's1':           [1, 19, 10, 1.8],
        's2':           [0, 60, 6, 6],
        's3':           [0, 60, 3, 6],
        'a1':           [0, 360, 120, 36],
        'easingRate' :  [0.01, 1, 0.1, 0.099]*/
    }

    var min, max, step, default_val;
    var rangeitem_str = "";
    for(var feature in feature_level_data) {
        min = feature_level_data[feature][0];
        max = feature_level_data[feature][1];
        default_val = feature_level_data[feature][2];
        step = feature_level_data[feature][3];
        rangeitem_str = 
            "<tr>\
              <td width='15%'>\
                <span class='name'>" + feature + "</span>\
              </td>\
              <td class='td_val' width='15%'>\
                <span id='" + feature + "_val'>" + default_val + "</span>\
              </td>\
              <td width='70%'>\
                <form action='#'>\
                  <p class='range-field'>\
                    <input type='range' id='" + feature + "-slider' min='" + min + "' max='" + max + "' step='" + step + "' value='" + default_val + "'/>\
                  </p>\
                </form>\
              </td>\
            </tr>";
        $('#range_items').append(rangeitem_str);
    }
    

    //for special color-btn
    min = 0;
    max = 6;
    default_val = "Red";
    step = 1;
    rangeitem_str = 
        "<tr>\
          <td width='15%'>\
            <span class='name'>color</span>\
          </td>\
          <td class='td_val' width='15%'>\
            <span id='color_val'>" + default_val + "</span>\
          </td>\
          <td width='70%'>\
            <form action='#'>\
              <p class='range-field'>\
                <input type='range' id='color-slider' min='" + min + "' max='" + max + "' step='" + step + "' value='0'/>\
              </p>\
            </form>\
          </td>\
        </tr>";
    $('#range_items').append(rangeitem_str);

});
