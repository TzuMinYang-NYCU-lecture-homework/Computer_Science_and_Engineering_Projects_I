import time, re, datetime, threading, requests 
import csmapi, DAN

alert_times = 1 # the number of alert times when the time is hitted.

ServerIP = 'http://127.0.0.1:9999' #Change to your IoTtalk IP or None for autoSearching
Reg_addr='Timer2-I-Default' # if None, Reg_addr = MAC address

DAN.profile['dm_name']='Timer2'
DAN.profile['df_list']=['Time1', 'Time2', 'Time3','Time4','Time5','Time6','Time7','Time8','Time9','Time10','Time11','Time12','Time13','Time14','Time15','Time16','Time17','Time18','Time19','Time20', ]
#DAN.profile['d_name']= None # None for autoNaming

def activate_control_channel():
    print ('Create control threading')
    DAN.thx=threading.Thread(target=DAN.ControlChannel) 
    DAN.thx.daemon = True                               
    DAN.thx.start()                                     

try:
    csmapi.ENDPOINT = ServerIP
    DAN.MAC = Reg_addr
    csmapi.pull(Reg_addr, 'profile')
except Exception as e:
    print('Try:', e)
    if str(e).find('mac_addr not found:') != -1:
        DAN.device_registration_with_retry(ServerIP, Reg_addr)
        print('Register Timer device.')
else:
    print('Timer device is existed, will not re-register.')
    activate_control_channel()

timeStartList=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
timeEndList  =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
alerted = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
disabled = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
while True:
    try:
        #if DAN.SelectedDF == []: print('SelectedDF is empty. Waiting...')
        for index in range(len(DAN.SelectedDF)):
            t_str = DAN.get_alias('Time'+str(index+1))
            if t_str != []: 
                t_str = t_str[0]
                #print(t_str)
            else: 
                print('Time'+str(index+1),'alias list is empty,', t_str)
                continue

            try:
                tStr = t_str.split('~')
                timeStartList[index] = datetime.datetime.strptime(tStr[0],'%H:%M')
                timeEndList[index] = datetime.datetime.strptime(tStr[1],'%H:%M')
                #print(index, timeStartList[index], timeEndList[index])
                 
                if timeStartList[index].hour == datetime.datetime.now().hour:
                    if timeStartList[index].minute == datetime.datetime.now().minute:
                        if alerted[index] < alert_times:
                            DAN.push('Time'+str(index+1), 1)
                            print ('Timer'+str(index+1)+' Alert')
                            alerted[index] += 1
                    else: alerted[index] = 0

                if timeEndList[index].hour == datetime.datetime.now().hour:
                    if timeEndList[index].minute == datetime.datetime.now().minute:
                        if disabled[index] < alert_times:
                            DAN.push('Time'+str(index+1), 0)
                            print ('Timer'+str(index+1)+' Disable')
                            disabled[index] += 1
                    else: disabled[index] = 0
                    
            except:
                print ('Time'+str(index+1) +': ' + t_str,'is not correct timer format, ignore.')
            time.sleep(0.2)

    except Exception as e:
        print(e)
        #DAN.device_registration_with_retry(ServerIP, Reg_addr)

    time.sleep(30)
