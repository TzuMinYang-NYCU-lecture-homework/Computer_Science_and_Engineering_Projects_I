import time, DAN, requests, random, json
from datetime import datetime
#ServerURL = 'http://IP:9999' #with no secure connection
ServerURL = 'http://localhost:9999' #with SSL connection
Reg_addr = 'ScienceParkAir' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='Air'
DAN.profile['df_list']=['PM2.5-I', 'WS-I', 'WD-I', 'Humidity-I']
DAN.profile['d_name']= '1.Air' # None for autoNaming
DAN.device_registration_with_retry(ServerURL, Reg_addr)
def pushing(lat=None,lng=None,station=None,data=None,area=None):
    PM25='PM25_R'
    WS='WS'
    WD='WD'
    if area == 'south':
        PM25='PM25'
    elif area == 'central':
        WS='WindSpeed'
        WD='WindDirection'
    if area != 'central':
        DAN.push('PM2.5-I', lat , lng ,  station , data[PM25] ,data['modify_time'])
        print('PM2.5-I', lat , lng ,  station , data[PM25] ,data['modify_time'])
        time.sleep(1)
    DAN.push('WS-I', lat , lng ,  station , data[WS] ,data['modify_time'])
    print('WS-I', lat , lng ,  station , data[WS] ,data['modify_time'])
    time.sleep(1)
    DAN.push('WD-I', lat , lng ,  station , data[WD] ,data['modify_time'])
    print('WD-I', lat , lng ,  station , data[WD] ,data['modify_time'])
    time.sleep(1)
    DAN.push('Humidity-I', lat , lng ,  station , data['RH'] ,data['modify_time'])
    print('Humidity-I', lat , lng ,  station , data['RH'] ,data['modify_time'])
    time.sleep(1)
while True:
    url_hsinchu='https://www.twsp.org.tw/MOST/phpjson/air_hsinchu_json.php?year='+str(datetime.now().year-1911)+'&month='+str(datetime.now().strftime('%m'))
    url_south='https://www.twsp.org.tw/MOST/phpjson/air_south_json.php?year='+str(datetime.now().year-1911)+'&month='+str(datetime.now().strftime('%m'))
    url_central='https://www.twsp.org.tw/MOST/phpjson/air_central_json.php?year='+str(datetime.now().year-1911)+'&month='+str(datetime.now().strftime('%m'))
    response_hsinchu = requests.get(url_hsinchu)
    data_hsinchu = json.loads(response_hsinchu.text)
    length_hsinchu=len(data_hsinchu['air_hsinchu'])
    response_south = requests.get(url_south)
    data_south = json.loads(response_south.text)
    length_south=len(data_south['air_south'])
    response_central = requests.get(url_central)
    data_central = json.loads(response_central.text)
    length_central=len(data_central['air_central'])
    try:
        pushing(24.77834 , 121.01372 ,  '靜心湖站' , data_hsinchu['air_hsinchu'][length_hsinchu-3])
        pushing(24.766508 , 121.016270 ,  '力行站' , data_hsinchu['air_hsinchu'][length_hsinchu-4])
        pushing(24.778000 , 120.989823 ,  '興業站' , data_hsinchu['air_hsinchu'][length_hsinchu-5])
        pushing(23.122835 , 120.267865 ,  '公19(北)' , data_south['air_south'][length_south-1],'south')
        pushing(23.0901 , 120.284583 ,  '公13(南)' , data_south['air_south'][length_south-2],'south')
        pushing(23.106571 , 120.269329 ,  '公29(西)' , data_south['air_south'][length_south-3],'south')
        pushing(23.106919 , 120.290621 ,  '南科實中(東)' , data_south['air_south'][length_south-4],'south')
        pushing(24.1942 , 120.6077 ,  '國安國小' , data_central['air_central'][length_central-1],'central')
        pushing(24.193 , 120.594086 ,  '都會公園' , data_central['air_central'][length_central-2],'central')
        pushing(24.228139 , 120.627611 ,  '中科實中' , data_central['air_central'][length_central-3],'central')
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)
    time.sleep(600)