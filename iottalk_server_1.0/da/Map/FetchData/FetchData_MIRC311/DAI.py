import time, DAN, requests
from sensor_const import iottalk_sensor_list

ServerIP = 'localhost' 
Reg_addr = 'MIRC311DataFeatchNumberOne' #For the different DA in the same computer, the Reg_addr needs to be modified.

DAN.profile['dm_name']='MIRC311Data'
DAN.profile['df_list']=['CO2-I', 'Humidity-I','PM2.5-I','Temperature-I']
DAN.profile['d_name']= None

DAN.Target_df_list = []
for IDF in DAN.profile['df_list']: DAN.Target_df_list.append(IDF[:-2])

DAN.device_registration_with_retry(ServerIP, Reg_addr)
while True:
    try:
        DAN.TargetENDPOINT = 'iottalk.tw'
        for sensor in iottalk_sensor_list:
            DAN.TargetMACaddr = sensor['MAC']
            print('\nThe data source is http://' + DAN.TargetENDPOINT + ':9999/' + DAN.TargetMACaddr)
            data=DAN.pullTarget(sensor['FEATURE_NAME'])
            if data != None and data !=[]:
                print(sensor['FEATURE_NAME'], sensor['LAT'], sensor['LNG'], sensor['NAME_ON_MAP'], round(data[1][0],1), data[0])
                DAN.push(sensor['FEATURE_NAME']+'-I', sensor['LAT'], sensor['LNG'], sensor['NAME_ON_MAP'], round(data[1][0],1), data[0])
            time.sleep(1)

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerIP, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(300)
