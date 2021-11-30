IoTtalkIP = 'http://127.0.0.1:9999'  # DomainName or IP
DatabaseURL = 'mysql+pymysql://map:password@localhost/map?charset=utf8'
#Map Admin page "username":"password"
users = {
    "iottalk": "password"
}
MapServerPort = "8866"

default_app_list = [
{'app': 'Camera', 'kind': 2, 'mobility': 'Stationary', 'icon': 'Picture', 'picture': 'https://i.imgur.com/Eh9U0qI.png', 'visual': '', 'color_min': None, 'color_max': None, 'quick_access': 1},
{'app': 'Obstacle', 'kind': 2, 'mobility': 'Stationary', 'icon': 'Picture', 'picture': 'https://maps.google.com/mapfiles/kml/pal3/icon33.png', 'visual': '', 'color_min': None, 'color_max': None, 'quick_access': 1},
]