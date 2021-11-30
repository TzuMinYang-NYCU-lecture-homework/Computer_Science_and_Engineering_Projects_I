#airbox
airbox_url = 'https://nctuairbox.edimaxcloud.com:55443/devices?token=c58affa8-b74e-4341-a020-82b4ba776a69'
#airbox sensor list
#data read from {icon name on the airbox, davice feature name, icon name on the map}
airbox_sensor_list = [
# {'NAME_ON_AIRBOX': 'co2', 'FEATURE_NAME': 'CO2', 'NAME_ON_MAP': 'airbox_CO2'},
{'NAME_ON_AIRBOX': 'h', 'FEATURE_NAME': 'Humidity', 'NAME_ON_MAP': 'airbox_Humidity'},
{'NAME_ON_AIRBOX': 'pm25', 'FEATURE_NAME': 'PM2.5', 'NAME_ON_MAP': 'airbox_PM2.5'},
{'NAME_ON_AIRBOX': 't', 'FEATURE_NAME': 'Temperature', 'NAME_ON_MAP': 'airbox_Temperature'},
]

airbox_sensor_mac = {
'74DA38C7D3E4': {'name': '國立交通大學台南-奇美樓南側'},
'74DA38C7D432': {'name': '國立交通大學博愛-實驗一館'},
'74DA38C7D3CC': {'name': '國立交通大學六家-大門口'},
'74DA38C7D3CE': {'name': '國立交通大學光復-綜合一館'},
'74DA38C7D3DA': {'name': '國立交通大學光復-基礎科學教學研究大樓'},
'74DA38C7D3DC': {'name': '國立交通大學博愛-竹銘館後門'},
'74DA38C7D0B6': {'name': '國立交通大學台北'},
'74DA38C7D448': {'name': '國立交通大學光復-學生活動中心'},
'74DA38C7D384': {'name': '國立交通大學六家-東北側六家一路面'},
'74DA38C7D380': {'name': '國立交通大學光復-女二舍'},
'74DA38C7D3E0': {'name': '國立交通大學六家-西北側自強南路面'},
'74DA38C7D430': {'name': '國立交通大學博愛-學生活動中心'},
'74DA38C7D3E2': {'name': '國立交通大學光復-電子資訊研究大樓'},
'74DA38C7D382': {'name': '國立交通大學六家-東南側六家古厝面'},
'74DA38C7D45A': {'name': '國立交通大學台南-奇美樓北側'},
'74DA38C7D3DE': {'name': '國立交通大學博愛-竹銘館大門'},
'74DA38C7D442': {'name': '國立交通大學光復-人社一館'},
'74DA38C7D446': {'name': '國立交通大學光復-浩然圖書資訊中心'},
}