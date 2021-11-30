import time, DAN, requests, random, json
import main
from datetime import datetime
from ServerConfig import IoTtalkIP, MapServerPort

ServerIP = IoTtalkIP #Change to your IoTtalk IP or None for autoSearching
Reg_addr='MAP_DEFAULT_SERVER' #None # if None, Reg_addr = MAC address

DAN.profile['dm_name']='Map'
DAN.profile['df_list']=[]
DAN.profile['d_name']= None # None for autoNaming

all_app_list = []
all_app_num = []

def iottalk_device_feature_update():
    global all_app_list
    global all_app_num

    c = main.db.session.query(main.icon_define_table).all()
    DAN.profile['dm_name']='Map'
    DAN.profile['df_list']=[]
    DAN.profile['d_name']= None
    all_app_list = []
    all_app_num = []
    for row in c:
        DAN.profile['df_list'].append('GeoData_O'+ str(c.index(row)+1))
        all_app_list.append(row.app)
        all_app_num.append(row.number)

    print (DAN.profile['df_list'])
    DAN.device_registration_with_retry(ServerIP, Reg_addr)


def dai():
    global all_app_list
    global all_app_num
    while True:
        try:
        #Pull data from device features called "'GeoData_O'+ str(num)"
            for num in range(1, len(all_app_list)+1):
                value = DAN.pull('GeoData_O'+ str(num))
                if value != None:
                    post_data = {
                        'app_num': all_app_num[num-1],
                        'lat': value[0],
                        'lng': value[1],
                        'name': value[2],
                        'value': value[3],
                        'time': value[4]
                    }
                    main.requests.post('http://localhost:'+MapServerPort+'/secure/endpoint/pull', data=post_data)

        except Exception as e:
            print(e)
            DAN.device_registration_with_retry(ServerIP, Reg_addr)

        time.sleep(0.2)
