import time, DAN, requests, random, json
from datetime import datetime
stations = {
    '竹科汙水廠':{'lat':'24.786846', 'lng':'121.006772'},
    '竹南汙水廠':{'lat':'24.710693', 'lng':'120.912398'},
    '龍潭汙水廠':{'lat':'24.887681', 'lng':'121.188066'},
    '臺南汙水廠01':{'lat':'23.108329', 'lng':'120.286136'},
    '臺南汙水廠02':{'lat':'23.089324', 'lng':'120.28017'},
    '高雄汙水廠':{'lat':'22.81926802', 'lng':'120.2829528'},
    '七星汙水廠':{'lat':'24.291202', 'lng':'120.725539'},
    '台中汙水廠':{'lat':'24.213917', 'lng':'120.6235'},
    '后里汙水廠':{'lat':'24.322179', 'lng':'120.724309'},
    '虎尾汙水廠':{'lat':'23.736972', 'lng':'120.395028'},
}
#ServerURL = 'http://IP:9999' #with no secure connection
ServerURL = 'http://localhost:9999' #with SSL connection
Reg_addr = 'ScienceParkWater' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='Sewage'
DAN.profile['df_list']=['COD-I', 'EC-I', 'SS-I', 'pH-I']
DAN.profile['d_name']= '1.Sewage' # None for autoNaming
DAN.device_registration_with_retry(ServerURL, Reg_addr)
def printing(lat=None,lng=None,station=None,data=None):
    print('COD-I', lat , lng ,  station , data['COD'] ,data['modify_time'])
    print('EC-I', lat , lng ,  station , data['EC'] ,data['modify_time'])
    print('SS-I', lat , lng ,  station , data['SS'] ,data['modify_time'])
    print('pH-I', lat , lng ,  station , data['pH'] ,data['modify_time'])
def pushing(lat=None,lng=None,station=None,data=None):
    DAN.push('COD-I', lat , lng ,  station , data['COD'] ,data['modify_time'])
    time.sleep(1)
    DAN.push('EC-I', lat , lng ,  station , data['EC'] ,data['modify_time'])
    time.sleep(1)
    DAN.push('SS-I', lat , lng ,  station , data['SS'] ,data['modify_time'])
    time.sleep(1)
    if data['pH'] == -2:
        data['pH'] = "維修中"
    DAN.push('pH-I', lat , lng ,  station , data['pH'] ,data['modify_time'])
    time.sleep(1)
def printing_central(lat=None,lng=None,station=None,data=None):
    print('COD-I', lat , lng ,  station , data['COD'] ,data['modify_time'])
    print('EC-I', lat , lng ,  station , data['EC'] ,data['modify_time'])
    print('SS-I', lat , lng ,  station , data['SS'] ,data['modify_time'])
    print('pH-I', lat , lng ,  station , data['Hydrogen_ion'] ,data['modify_time'])
def pushing_central(lat=None,lng=None,station=None,data=None):
    DAN.push('COD-I', lat , lng ,  station , data['COD'] ,data['modify_time'])
    time.sleep(1)
    DAN.push('EC-I', lat , lng ,  station , data['EC'] ,data['modify_time'])
    time.sleep(1)
    DAN.push('SS-I', lat , lng ,  station , data['SS'] ,data['modify_time'])
    time.sleep(1)
    DAN.push('pH-I', lat , lng ,  station , data['Hydrogen_ion'] ,data['modify_time'])
    time.sleep(1)
while True:
    url_hsinchu='https://www.twsp.org.tw/MOST/phpjson/sewage_hsinchu_json.php?year='+str(datetime.now().year-1911)+'&month='+str(datetime.now().strftime('%m'))
    url_south='https://www.twsp.org.tw/MOST/phpjson/sewage_south_json.php?year='+str(datetime.now().year-1911)+'&month='+str(datetime.now().strftime('%m'))
    url_central='https://www.twsp.org.tw/MOST/phpjson/sewage_central_json.php?year='+str(datetime.now().year-1911)+'&month='+str(datetime.now().strftime('%m'))
    response_hsinchu = requests.get(url_hsinchu)
    data_hsinchu = json.loads(response_hsinchu.text)
    length_hsinchu=len(data_hsinchu['sewage_hsinchu'])
    response_south = requests.get(url_south)
    data_south = json.loads(response_south.text)
    length_south=len(data_south['sewage_south'])
    response_central = requests.get(url_central)
    data_central = json.loads(response_central.text)
    length_central=len(data_central['sewage_central'])
    printing(24.786846 , 121.006772 ,  '竹科汙水廠' , data_hsinchu['sewage_hsinchu'][length_hsinchu-3])
    printing(24.710693 , 120.912398 ,  '竹南汙水廠' , data_hsinchu['sewage_hsinchu'][length_hsinchu-2])
    printing(24.887681 , 121.188066 ,  '龍潭汙水廠' , data_hsinchu['sewage_hsinchu'][length_hsinchu-1])
    printing(23.108329 , 120.286136 ,  '臺南汙水廠01' , data_south['sewage_south'][length_south-3])
    printing(23.089324 , 120.28017 ,  '臺南汙水廠02' , data_south['sewage_south'][length_south-2])
    printing(22.81926802 , 120.2829528 ,  '高雄汙水廠' , data_south['sewage_south'][length_south-1])
    printing_central(24.291202, 120.725539 ,  '七星汙水廠' , data_central['sewage_central'][length_central-8])
    printing_central(24.213917, 120.6235 ,  '台中汙水廠' , data_central['sewage_central'][length_central-6])
    printing_central(24.322179, 120.724309 ,  '后里汙水廠' , data_central['sewage_central'][length_central-4])
    printing_central(23.736972, 120.395028 ,  '虎尾汙水廠' , data_central['sewage_central'][length_central-2])
    try:
        pushing(24.786846 , 121.006772 ,  '竹科汙水廠' , data_hsinchu['sewage_hsinchu'][length_hsinchu-3])
        pushing(24.710693 , 120.912398 ,  '竹南汙水廠' , data_hsinchu['sewage_hsinchu'][length_hsinchu-2])
        pushing(24.887681 , 121.188066 ,  '龍潭汙水廠' , data_hsinchu['sewage_hsinchu'][length_hsinchu-1])
        pushing(23.108329 , 120.286136 ,  '臺南汙水廠01' , data_south['sewage_south'][length_south-3])
        pushing(23.089324 , 120.28017 ,  '臺南汙水廠02' , data_south['sewage_south'][length_south-2])
        pushing(22.81926802 , 120.2829528 ,  '高雄汙水廠' , data_south['sewage_south'][length_south-1])
        pushing_central(24.291202, 120.725539 ,  '七星汙水廠' , data_central['sewage_central'][length_central-8])
        pushing_central(24.213917, 120.6235 ,  '台中汙水廠' , data_central['sewage_central'][length_central-6])
        pushing_central(24.322179, 120.724309 ,  '后里汙水廠' , data_central['sewage_central'][length_central-4])
        pushing_central(23.736972, 120.395028 ,  '虎尾汙水廠' , data_central['sewage_central'][length_central-2])
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)
    time.sleep(10*60)

