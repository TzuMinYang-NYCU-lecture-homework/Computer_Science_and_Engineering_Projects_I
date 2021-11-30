import time, DAN, requests
from datetime import datetime
from sensor_const import GradDorm3_url
from sensor_const import GradDorm3_sensor_list

ServerIP = 'localhost' 
Reg_addr = 'GradDorm3DataFeatchNumberOne' #For the different DA in the same computer, the Reg_addr needs to be modified.

DAN.profile['dm_name']='GradDorm3Data'
DAN.profile['df_list']=['Dryer-I', 'WashingMachine-I']
DAN.profile['d_name']= None

DAN.Target_df_list = []
for IDF in DAN.profile['df_list']: DAN.Target_df_list.append(IDF[:-2])

DAN.device_registration_with_retry(ServerIP, Reg_addr)
while True:
    try:
        data = DAN.pull_GradDorm3(GradDorm3_url)     
        if data != None and data !=[]:
            for key in data.keys():
                if 'event' and 'building' and 'type' in data[key]:
                    check_state = (data[key]['event'] == 'READY' or data[key]['event'] == 'OFFLINE' or (data[key]['event'] == 'RUNNING' and (int(time.time())-int(data[key]['ts'])/1000 > 3600) ))
                    
                    if   check_state and data[key]['building'] == 'N' and data[key]['type'] == 'D':
                        GradDorm3_sensor_list[0]['COUNT'] = GradDorm3_sensor_list[0]['COUNT'] + 1
                    elif check_state and data[key]['building'] == 'N' and data[key]['type'] == 'W':
                        GradDorm3_sensor_list[1]['COUNT'] = GradDorm3_sensor_list[1]['COUNT'] + 1
                    elif check_state and data[key]['building'] == 'S' and data[key]['type'] == 'D':
                        GradDorm3_sensor_list[2]['COUNT'] = GradDorm3_sensor_list[2]['COUNT'] + 1
                    elif check_state and data[key]['building'] == 'S' and data[key]['type'] == 'W':
                        GradDorm3_sensor_list[3]['COUNT'] = GradDorm3_sensor_list[3]['COUNT'] + 1

            for devices in GradDorm3_sensor_list:
                print(devices['FEATURE_NAME'], devices['lat'], devices['lng'], devices['NAME_ON_MAP'], devices['COUNT'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                DAN.push(devices['FEATURE_NAME'], devices['lat'], devices['lng'], devices['NAME_ON_MAP'], devices['COUNT'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                devices['COUNT'] = 0
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
