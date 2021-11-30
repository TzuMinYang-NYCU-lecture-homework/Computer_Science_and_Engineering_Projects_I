import time, DAN, requests

ServerIP = 'localhost' 
Reg_addr = 'BaoDataFeatchNumberTwo' #For the different DA in the same computer, the Reg_addr needs to be modified.

DAN.profile['dm_name']='BaoData'
DAN.profile['df_list']=['AtPressure-I', 'Bugs-I', 'Humidity-I','RainMeter-I','Temperature-I','UV1-I', 'WindSpeed-I',]
DAN.profile['d_name']= None

DAN.Target_df_list = []
for IDF in DAN.profile['df_list']: DAN.Target_df_list.append(IDF[:-2])

DAN.device_registration_with_retry(ServerIP, Reg_addr)
while True:
    try:
        DAN.TargetENDPOINT = 'farm.iottalk.tw'
        DAN.TargetMACaddr = '90A2DAF84CEC'
        print('\nThe data source is http://' + DAN.TargetENDPOINT + ':9999/' + DAN.TargetMACaddr)        
        for IDF in DAN.Target_df_list:
            data=DAN.pullTarget(IDF)
            if data != None and data !=[]:
                if IDF == 'UV1': data[1][0] = data[1][0] / 1024*370/200
                print(IDF, 24.764278, 120.993806, 'BaoFarm_'+IDF, round(data[1][0],1), data[0])
                DAN.push(IDF+'-I', 24.764278, 120.993806, 'BaoFarm_'+IDF, round(data[1][0],1), data[0])
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
