var password = 0;

(function() {
    function update(mac, feature, data, callback) {
        $.ajax({
            type: "PUT",
            url: '/' + mac + '/' + feature,
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({'data': [data]}),
            'headers': {'password-key': password},
            error: function(err, st) {
                console.log(err);
                console.log(st);
                console.log('Update failed');
            },
            complete: function() {
                if( typeof callback === 'function' )
                    callback();
            },
            dataType: 'text',
        });
    }

    // Export to browser's global for debug
    window.IoTtalk = {
        update: update,
    };
})();

(function() {
    console.log('Loaded.');
    $.get(window.location.origin + '/da/Dandelion_control\(mobile\)/passwd_dandelion_control'
        ).done(function(result){
            password = result;
            console.log(password);
        });
})();
