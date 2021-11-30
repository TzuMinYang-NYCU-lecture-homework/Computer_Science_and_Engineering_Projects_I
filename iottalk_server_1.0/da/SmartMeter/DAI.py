import time, DAN, requests, EMeter

ServerIP = 'https://farm.iottalk.tw' #Change to your IoTtalk IP or None for autoSearching
Reg_addr = 'ElectorSmartMeter' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='BaoEMeter'
DAN.profile['df_list']=['Volt', 'Current', 'Power', 'KWh']
DAN.profile['d_name']= 'EMeter' #None # None for autoNaming
DAN.device_registration_with_retry(ServerIP, Reg_addr)

while True:
    try:
        data = EMeter.gatherData()
        if data == None: 
            print('No smart meter data.')
            time.sleep(10)
            continue
        
        DAN.push('Volt', data['V'][0], data['V'][1], data['V'][2], data['V'][3])
        print('Volt', data['V'][0], data['V'][1], data['V'][2], data['V'][3])

        DAN.push('Current', data['A'][0], data['A'][1], data['A'][2], data['A'][3])
        print('Current', data['A'][0], data['A'][1], data['A'][2], data['A'][3])
        
        DAN.push('Power', data['W'][0], data['W'][1], data['W'][2], data['W'][3])
        print('Power', data['W'][0], data['W'][1], data['W'][2], data['W'][3])

        DAN.push('KWh', data['kWh'][0])
        print('KWh', data['kWh'][0])
        
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerIP, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(10)    

    time.sleep(20)
