// Keypad
$(function() {
    var feature_list = ['size', 
                        'angle'
                        /*'color_r', 
                        'color_g', 
                        'color_b',
                        'bg_color_r', 
                        'bg_color_g', 
                        'bg_color_b', 
                        's0', 
                        's1', 
                        's2', 
                        's3', 
                        'a1', 
                        'easingRate'*/];

    for(var index in feature_list) {
        var feature = feature_list[index];
        var name = "#" + feature + "-slider";
        $(document).on('input', name, function() {
            var data = $(this).val();
            var feature_name = $(this).attr('id').split('-')[0];
            var feature_val = "#" + feature_name + "_val";
            $(feature_val).text(data);
            IoTtalk.update(mac, feature_name+"-I", Number(data));
            console.log(feature_name, data);
        });
    }

    //for special color-btn
    
    function set_color(color_r_val, color_g_val, color_b_val){
        IoTtalk.update(mac, "color_r-I", Number(color_r_val));
        IoTtalk.update(mac, "color_g-I", Number(color_g_val));
        IoTtalk.update(mac, "color_b-I", Number(color_b_val));
        console.log("set rgb:", color_r_val, color_g_val, color_b_val);
    }

    var rainbow = [
                //r, g ,b, name
                [255,   0,   0, "Red"],
                [255, 165,   0, "Orange"],
                [255, 255,   0, "Yellow"],
                [  0, 255,   0, "Green"],
                [  0,   0, 255, "Blue"],
                [  0, 127, 255, "Indigo"],
                [139,   0, 255, "Violet"],
    ]

    $(document).on('input', "#color-slider", function() {
        var data = Number($(this).val());
        var color_r_val = rainbow[data][0];
        var color_g_val = rainbow[data][1];
        var color_b_val = rainbow[data][2];
        var color_name = rainbow[data][3];

        set_color(color_r_val, color_g_val, color_b_val);
        $("#color_val").text(color_name);
        console.log(color_name);
    });

});
