import time, DAN, requests
from sensor_const import iottalk_sensor_list

ServerIP = 'localhost' 
Reg_addr = 'ParkingLotDataFeatchNumberOne' #For the different DA in the same computer, the Reg_addr needs to be modified.

DAN.profile['dm_name']='ParkingLotData'
DAN.profile['df_list']=['CountGeoData-I']
DAN.profile['d_name']= None

DAN.Target_df_list = []
for IDF in DAN.profile['df_list']: DAN.Target_df_list.append(IDF[:-2])

DAN.device_registration_with_retry(ServerIP, Reg_addr)
while True:
    try:
        DAN.TargetENDPOINT = 'iot.iottalk.tw'
        for sensor in iottalk_sensor_list:
            DAN.TargetMACaddr = sensor['MAC']
            print('\nThe data source is http://' + DAN.TargetENDPOINT + ':9999/' + DAN.TargetMACaddr)
            data=DAN.pullTarget(sensor['FEATURE_NAME'], sensor['FEATURE'])
            if data != None and data !=[]:
                print(sensor['FEATURE'], sensor['LAT'], sensor['LNG'], sensor['NAME_ON_MAP'], data[1][3], data[1][4])
                DAN.push(sensor['FEATURE']+'-I', sensor['LAT'], sensor['LNG'], sensor['NAME_ON_MAP'], data[1][3], data[1][4])
            time.sleep(1)

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerIP, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(60)
