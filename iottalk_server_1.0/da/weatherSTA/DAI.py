import time, DAN, requests 
from datetime import datetime
import get_weather as g
import Station_List as s

fetch_interval = 600

ServerIP = 'http://127.0.0.1:9999'
Reg_addr = 'Central_Weather_Bureau_V8_'

profile = {
    'dm_name': 'WeatherSTA',
    'df_list': ['AtPressure', 'Humidity', 'RainMeter', 'Temperature', 'WindSpeed', 'Sunshine'],
    'd_name': None # None for autoNaming
}

DAs = []
for STA in s.STAs:
    profile['d_name'] = STA[0]
    DAs.append(DAN.DAN(profile, ServerIP, Reg_addr+STA[0]))
    DAs[-1].device_registration_with_retry()
  
while True:
    
    print('\n     ', datetime.now())
    for index, STA in list(enumerate(s.STAs)):
        data = g.fetch_data(STA[1])
        if not data: 
            continue
        try:
            DAs[index].push('Temperature', data.get('Temp'))
            print(STA[0], 'Temperature', data.get('Temp'))

            DAs[index].push('Humidity',data.get('Humidity'))
            print(STA[0], 'Humidity', data.get('Humidity'))

            DAs[index].push('RainMeter',data.get('Rain'))
            print(STA[0], 'RainMeter', data.get('Rain'))

            DAs[index].push('WindSpeed',data.get('Wind'))
            print(STA[0], 'WindSpeed', data.get('Wind'))

            DAs[index].push('AtPressure',data.get('AtPressure'))
            print(STA[0], 'AtPressure', data.get('AtPressure'))

            DAs[index].push('Sunshine',data.get('Sunshine'))
            print(STA[0], 'Sunshine', data.get('Sunshine'))

        except Exception as e:
            print(e)
            if str(e).find('mac_addr not found:') != -1:
                print('Reg_addr is not found. Try to re-register...')
                DAs[index].device_registration_with_retry(ServerURL, Reg_addr)
            else:
                print('Connection failed due to unknow reasons.')
                time.sleep(1)    

        time.sleep(5)

    time.sleep(fetch_interval)
