import time, DAN, requests
from datetime import datetime
from sensor_const import NCTUBus_url
from sensor_const import NCTUBus_post_data
from sensor_const import NCTUBus_sensor_list

ServerIP = 'localhost' 
Reg_addr = 'NCTUBusDataFeatchNumberOne' #For the different DA in the same computer, the Reg_addr needs to be modified.

DAN.profile['dm_name']='NCTUBusData'
DAN.profile['df_list']=['BusGeoData-I']
DAN.profile['d_name']= '1.NCTUBusData'

DAN.Target_df_list = []
for IDF in DAN.profile['df_list']: DAN.Target_df_list.append(IDF[:-2])

DAN.device_registration_with_retry(ServerIP, Reg_addr)
while True:
    try:
        for index, row in enumerate(NCTUBus_sensor_list):
            if row['DeviceId'] in NCTUBus_post_data:
                data = DAN.pull_NCTUBus(NCTUBus_url, NCTUBus_post_data[row['DeviceId']])
                # data = {'CarStatus': '2', 'Car_Unicode': '110428', 'NextStation_ID': '8960', 'NextStationTime': 13, 'Log_Direct': 13, 'Log_GISX': 120.934333, 'Log_GISY': 24.789678}
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print('BusGeoData-I', data['Log_GISY'], data['Log_GISX'], row['NAME_ON_MAP'], index, now)
                DAN.push('BusGeoData-I', data['Log_GISY'], data['Log_GISX'], row['NAME_ON_MAP'], index, now)
                time.sleep(2)

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerIP, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(20)
