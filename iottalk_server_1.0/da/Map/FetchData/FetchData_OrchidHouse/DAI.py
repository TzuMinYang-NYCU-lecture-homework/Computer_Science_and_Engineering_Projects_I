# -*- coding: UTF-8 -*-
import time, requests, datetime
import DAN, table, fetchData

ServerURL = 'http://localhost:9999' #with no secure connection
Reg_addr = 'TSMC_OrchidHouse_001'

DAN.profile['dm_name']='OrchidHouse'
DAN.profile['df_list']=['Temperature-I', 'Humidity-I', 'CO2-I', 'WindSpeed-I', 'RainMeter-I', 'AtPressure-I']
DAN.profile['d_name']= '1.OrchidHouse'

DAN.device_registration_with_retry(ServerURL, Reg_addr)

# 請勿在短時間內對同一個UUID發出request，第二次會拿到錯誤的值
idList = [
'705cd51992dc1faf544441c7dbb6e8bf',
'a9895e570f9fa4ee5a4a89ca76c7c435',
'b935c73cea07f16fdbfc5ec6665ee974', 
'd64482a4c9b0b050bf02a873725cf3a8', 
'97967e8a95078abf28ebc930f38c4ab5', 
'211d44826a4dbfabd92eb4a41a3fdce9', 
'176eda4efcc5df4204e6af17a7cc9417',
'dd6b762815f9b1cf33710a3ae9479aaf',
'406815839a93430b10e9a40142b38f6b',
'5603a1fa59dfd6cf306a614ce81ec71a',
'181347ab45ab2f9907e7f012369bc517',
'f164c6a8e45d6f5f697bf14e3a6a68dd',
'c164aec9fea2b4097a5a92bd479bbb3f',
'7a7422d65b2aa5da1d3c5a742ef97783',
'710fc079c41b1cdb815a90db273810c6',
'464ff43386ec498537143bd4b733884d',
'1e69be4fbbc322a61939b0e8e7964372',
'236f1e5f18488fa0fb4ae5185d1c5f2d',
'01edb4d035f6445f4b20b42af1ce0aa3',
'531184a6b5da90c19ca61c414fb79198',
'7204344eb66365fe28cdf7edf11265cf',
'29582aec4b7094249195204f6f895846'
]

while True:
    fetchData.fetchAllData(idList)
    # for node in table.node.keys():
    #     print(table.node[node])
    try:
        humidity = (float(table.node[idList[0]][0]))
        temperature = (float(table.node[idList[1]][0]))
        co2 = (float(table.node[idList[2]][0]))
        humidity_COS01 = (float(table.node[idList[3]][0]))
        temperature_COS01 = (float(table.node[idList[4]][0]))
        humidity_TH01 = (float(table.node[idList[5]][0]))
        temperature_TH01 = (float(table.node[idList[6]][0]))
        temperature_TH02 = (float(table.node[idList[7]][0]))
        humidity_TH02 = (float(table.node[idList[8]][0]))
        temperature_TH03 = (float(table.node[idList[9]][0]))
        humidity_TH03 = (float(table.node[idList[10]][0]))
        temperature_TH04 = (float(table.node[idList[11]][0]))
        humidity_TH04 = (float(table.node[idList[12]][0]))
        temperature_TH05 = (float(table.node[idList[13]][0]))
        humidity_TH05 = (float(table.node[idList[14]][0]))
        temperature_TH06 = (float(table.node[idList[15]][0]))
        humidity_TH06 = (float(table.node[idList[16]][0]))
        temperature_TH07 = (float(table.node[idList[17]][0]))
        humidity_TH07 = (float(table.node[idList[18]][0]))
        windspeed = (float(table.node[idList[19]][0]))
        pressure = (float(table.node[idList[20]][0]))
        rainmeter = (float(table.node[idList[21]][0]))
    except ValueError as e:
        time.sleep(10)
        continue
    
    try:
        DAN.push('Humidity-I', 24.772946, 121.011238, 'OrchidHouse_Humidity_WS-01智慧氣象站', humidity, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Humidity-I', 24.772946, 121.011238, 'OrchidHouse_Humidity_WS-01智慧氣象站', humidity, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Temperature-I', 24.772946, 121.011238, 'OrchidHouse_Temperature_WS-01智慧氣象站', temperature, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Temperature-I', 24.772946, 121.011238, 'OrchidHouse_Temperature_WS-01智慧氣象站', temperature, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('CO2-I', 24.772946,  121.011238, 'OrchidHouse_CO2', co2, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('CO2-I', 24.772946,  121.011238, 'OrchidHouse_CO2', co2, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('WindSpeed-I', 24.772946,  121.011238, 'OrchidHouse_WindSpeed', windspeed, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('WindSpeed-I', 24.772946,  121.011238, 'OrchidHouse_WindSpeed', windspeed, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('AtPressure-I', 24.772946,  121.011238, 'OrchidHouse_AtPressure', pressure, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('AtPressure-I', 24.772946,  121.011238, 'OrchidHouse_AtPressure', pressure, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('RainMeter-I', 24.772946,  121.011238, 'OrchidHouse_Rainmeter', rainmeter, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('RainMeter-I', 24.772946,  121.011238, 'OrchidHouse_Rainmeter', rainmeter, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Humidity-I', 24.77282, 121.011238, 'OrchidHouse_Humidity_COS-01空氣品質', humidity_COS01, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Humidity-I', 24.77282, 121.011238, 'OrchidHouse_Humidity_COS-01空氣品質', humidity_COS01, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Temperature-I', 24.77282, 121.011238, 'OrchidHouse_Temperature_COS-01空氣品質', temperature_COS01, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Temperature-I', 24.77282, 121.011238, 'OrchidHouse_Temperature_COS-01空氣品質', temperature_COS01, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Humidity-I', 24.773072, 121.011238, 'OrchidHouse_Humidity_TH-01入口', humidity_TH01, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Humidity-I', 24.773072, 121.011238, 'OrchidHouse_Humidity_TH-01入口', humidity_TH01, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Temperature-I', 24.773072, 121.011238, 'OrchidHouse_Temperature_TH-01入口', temperature_TH01, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Temperature-I', 24.773072, 121.011238, 'OrchidHouse_Temperature_TH-01入口', temperature_TH01, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Humidity-I', 24.77282, 121.011112, 'OrchidHouse_Humidity_TH-02浴廁', humidity_TH02, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Humidity-I', 24.77282, 121.011112, 'OrchidHouse_Humidity_TH-02浴廁', humidity_TH02, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Temperature-I', 24.77282, 121.011112, 'OrchidHouse_Temperature_TH-02浴廁', temperature_TH02, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Temperature-I', 24.77282, 121.011112, 'OrchidHouse_Temperature_TH-02浴廁', temperature_TH02, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Humidity-I', 24.772946, 121.011112, 'OrchidHouse_Humidity_TH-03廚房', humidity_TH03, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Humidity-I', 24.772946, 121.011112, 'OrchidHouse_Humidity_TH-03廚房', humidity_TH03, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Temperature-I', 24.772946, 121.011112, 'OrchidHouse_Temperature_TH-03廚房', temperature_TH03, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Temperature-I', 24.772946, 121.011112, 'OrchidHouse_Temperature_TH-03廚房', temperature_TH03, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Humidity-I', 24.773072, 121.011112, 'OrchidHouse_Humidity_TH-04客廳', humidity_TH04, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Humidity-I', 24.773072, 121.011112, 'OrchidHouse_Humidity_TH-04客廳', humidity_TH04, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Temperature-I', 24.773072, 121.011112, 'OrchidHouse_Temperature_TH-04客廳', temperature_TH04, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Temperature-I', 24.773072, 121.011112, 'OrchidHouse_Temperature_TH-04客廳', temperature_TH04, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Humidity-I', 24.77282, 121.011364, 'OrchidHouse_Humidity_TH-05臥室', humidity_TH05, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Humidity-I', 24.77282, 121.011364, 'OrchidHouse_Humidity_TH-05臥室', humidity_TH05, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Temperature-I', 24.77282, 121.011364, 'OrchidHouse_Temperature_TH-05臥室', temperature_TH05, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Temperature-I', 24.77282, 121.011364, 'OrchidHouse_Temperature_TH-05臥室', temperature_TH05, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Humidity-I', 24.772946, 121.011364, 'OrchidHouse_Humidity_TH-06二樓儲藏室', humidity_TH06, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Humidity-I', 24.772946, 121.011364, 'OrchidHouse_Humidity_TH-06二樓儲藏室', humidity_TH06, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Temperature-I', 24.772946, 121.011364, 'OrchidHouse_Temperature_TH-06二樓儲藏室', temperature_TH06, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Temperature-I', 24.772946, 121.011364, 'OrchidHouse_Temperature_TH-06二樓儲藏室', temperature_TH06, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Humidity-I', 24.773072, 121.011364, 'OrchidHouse_Humidity_TH-07二樓水牆外側', humidity_TH07, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Humidity-I', 24.773072, 121.011364, 'OrchidHouse_Humidity_TH-07二樓水牆外側', humidity_TH07, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
        DAN.push('Temperature-I', 24.773072, 121.011364, 'OrchidHouse_Temperature_TH-07二樓水牆外側', temperature_TH07, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Temperature-I', 24.773072, 121.011364, 'OrchidHouse_Temperature_TH-07二樓水牆外側', temperature_TH07, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(0.1)
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(10)

    time.sleep(600)