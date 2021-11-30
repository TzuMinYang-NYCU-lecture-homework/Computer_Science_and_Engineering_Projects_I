import time, csmapi, DAN, requests, random

ServerIP = 'farm.iottalk.tw' #Change to your IoTtalk IP or None for autoSearching

Reg_addr='agri_bao_01' # if None, Reg_addr = MAC address
DAN.profile['dm_name']='Agri'
DAN.profile['df_list']=['Temperature', 'Humidity', 'RainMeter', 'AtPressure', 'SoilMoisture', 'WindSpeed', 'SoilEC', 'UV', 'BugAmount', 'SoilTemperature']
DAN.profile['d_name']= 'Agri.Bao'
DAN.device_registration_with_retry(ServerIP, Reg_addr)


Reg_addr='agri_wufeng_01'
DAN.profile['d_name']= 'Agri.WuFeng'
DAN.device_registration_with_retry(ServerIP, Reg_addr)

