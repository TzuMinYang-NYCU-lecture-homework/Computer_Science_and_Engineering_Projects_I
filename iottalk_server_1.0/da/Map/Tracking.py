import time, DAN, requests, random, json, csmapi, os
from datetime import datetime
from ServerConfig import IoTtalkIP

ServerIP = IoTtalkIP #Change to your IoTtalk IP or None for autoSearching
Reg_addr='TRACKING_DEFAULT' #None # if None, Reg_addr = MAC address

DAN.profile['dm_name']='Tracking'
DAN.profile['df_list']=['GeoData-I']
DAN.profile['d_name']= 'GPS_Tracking' # None for autoNaming



def dai():
    while True:
        try:
            DAN.device_registration_with_retry(ServerIP, Reg_addr)
            if csmapi.passwordKey != None:
	            passwd_file = open(r'/home/'+os.getlogin()+'/iottalk_server_1.0/da/Map/static/passwd_tracking', 'w+')
	            passwd_file.write(csmapi.passwordKey)
	            passwd_file.close()
	            print('passwordKey', csmapi.passwordKey)
	            break
                
        except Exception as e:
            print(e)
            DAN.device_registration_with_retry(ServerIP, Reg_addr)

        else:
            break

        time.sleep(1)
