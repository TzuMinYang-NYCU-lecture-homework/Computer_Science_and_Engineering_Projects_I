var csmapi = (function () {
    var ENDPOINT = window.location.origin;

    function set_endpoint (endpoint) {
        ENDPOINT = endpoint;
    }

    function get_endpoint () {
        return ENDPOINT;
    }

    function register (mac_addr, profile, callback) {
        jQuery.ajax({
            type: 'POST',
            url: ENDPOINT +'/'+ mac_addr,
            data: JSON.stringify({'profile': profile}),
            contentType:"application/json; charset=utf-8",
        }).done(function () {
            if (callback) {
                callback(true);
            }
        }).fail(function () {
            if (callback) {
                callback(false);
            }
        });
    }

    function deregister (mac_addr, callback) {
        jQuery.ajax({
            type: 'DELETE',
            url: ENDPOINT +'/'+ mac_addr,
            contentType:"application/json; charset=utf-8",
        }).done(function () {
            if (callback) {
                callback(true);
            }
        }).fail(function () {
            if (callback) {
                callback(false);
            }
        });
    }

    function pull (mac_addr, odf_name, callback) {
        jQuery.ajax({
            type: 'GET',
            url: ENDPOINT +'/'+ mac_addr +'/'+ odf_name,
            contentType:"application/json; charset=utf-8",
        }).done(function (obj) {
            if (typeof obj === 'string') {
                obj = JSON.parse(obj);
            }

            if (callback) {
                callback(obj['samples']);
            }
        }).fail(function (error) {
            if (callback) {
                callback([], error);
            }
        });
    }

    function get_alias_name (mac_addr, odf_name, callback) {
        jQuery.ajax({
            type: 'GET',
            url: ENDPOINT +'/get_alias/'+ mac_addr +'/'+ odf_name,
            contentType:"application/json; charset=utf-8",
        }).done(function (obj) {
            if (typeof obj === 'string') {
                obj = JSON.parse(obj);
            }

            if (callback) {
                callback({alias: obj['alias_name'], origin: odf_name});
            }
        }).fail(function (error) {
            if (callback) {
                callback([], error);
            }
        });
    }

    function push (mac_addr, idf_name, data, callback) {
        jQuery.ajax({
            type: 'PUT',
            url: ENDPOINT +'/'+ mac_addr +'/'+ idf_name,
            data: JSON.stringify({'data': data}),
            contentType:"application/json; charset=utf-8",
        }).done(function () {
            if (callback) {
                callback(true);
            }
        }).fail(function () {
            if (callback) {
                callback(false);
            }
        });
    }

    return {
        'set_endpoint': set_endpoint,
        'get_endpoint': get_endpoint,
        'register': register,
        'deregister': deregister,
        'pull': pull,
        'get_alias_name': get_alias_name,
        'push': push,
    };
})();