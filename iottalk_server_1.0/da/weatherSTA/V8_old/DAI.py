import time, DAN, requests 
from datetime import datetime
import get_weather as g
import Station_List as s

fetch_interval = 600

def ConvertToFloat(string_data):
    try: 
        return float(string_data)
    except: 
        return None

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
        data = g.getWeather(STA[1])
        if not data: 
            continue
        try:
            
            Temperature = ConvertToFloat(data['0']['Temperature']['C']['E'])
            DAs[index].push('Temperature',Temperature)
            print(STA[0], 'Temperature', Temperature)

            Humidity = ConvertToFloat(data['0']['Humidity']['E'])
            DAs[index].push('Humidity',Humidity)
            print(STA[0], 'Humidity', Humidity)

            Rain = ConvertToFloat(data['0']['Rain']['E'])
            DAs[index].push('RainMeter',Rain)
            print(STA[0], 'RainMeter', Rain)

            Wind = ConvertToFloat(data['0']['Wind']['MS']['E'])
            DAs[index].push('WindSpeed',Wind)
            print(STA[0], 'WindSpeed', Wind)

            Pressure = ConvertToFloat(data['0']['Pressure']['E'])
            DAs[index].push('AtPressure',Pressure)
            print(STA[0], 'AtPressure', Pressure)

            Sunshine = ConvertToFloat(data['0']['Sunshine'])
            DAs[index].push('Sunshine',Sunshine)
            print(STA[0], 'Sunshine', Sunshine)

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
