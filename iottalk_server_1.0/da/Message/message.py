import time, requests, subprocess, re, os.path, pickle
import DAN_modify as DAN

NumberOfList = 9

SMS_SERVER_IP = '202.39.54.130'
SMS_SERVER_LOGIN = '89945934'
SMS_SERVER_PWD = '?????????'

ServerURL = 'http://127.0.0.1:9999' #with no secure connection
Reg_addr = 'IoTtalk_Message'

DAN.profile['dm_name']='Message'
DAN.profile['d_name']= 'Message' # None for autoNaming
DAN.profile['df_list'] = []
for i in range(1,NumberOfList+1):
    DAN.profile['df_list'].append('Name%d' % i)
DAN.device_registration_with_retry(ServerURL, Reg_addr)
    

def send_SMS(msg, tel):
    current_path = os.path.dirname(__file__)    #You can not execute message.py in the same directory with message.py.
    #print (current_path)
    #print (os.path.join(current_path, os.path.join('SMS')))

    subprocess.Popen([
        os.path.join(current_path, os.path.join('SMS')),
        SMS_SERVER_IP,
        SMS_SERVER_LOGIN,
        SMS_SERVER_PWD,
        tel,
        msg
    ])
   

msg_list = None    
while 1:
    try:
        if len(DAN.SelectedDF) > 0: 
            msgList = DAN.pull('__Ctl_I__')
            if msgList:
                msg_list = msgList[0]
                print('Notification ContactList Update:', msg_list)

            if not msg_list:
                try:
                    msg_list = pickle.load(open("MsgContact", "rb" ))
                except  Exception as e:
                    #print(e)
                    pass
                if not msg_list: 
                    print('Message Contact List is empty. Sleep 30 seconds.')
                    time.sleep(30)
                    continue
                print('ContactList loaded from the file:', msg_list)

        for index in range(len(DAN.SelectedDF)):
            time.sleep(0.1)
            value=DAN.pull('Name'+str(index+1))
            if value != None:
                if value[0] != None:
                    if (re.match(r'09\d{8}$', msg_list['name'][index]) != None):  #is phone number
                        print ('Phone:'+ msg_list['name'][index] + ',    Text:'  + msg_list['message'][index] + ',    value:'+str(value[0]))
                        send_SMS( msg_list['message'][index]+' - value:'+str(value[0]), msg_list['name'][index] )

                    elif (re.match(r'.+@.+',msg_list['name'][index])  != None):   #is email address
                        print ('E-mail:'+  msg_list['name'][index] + ',    Text:'  + msg_list['message'][index]  + ',    value:'+ str(value[0]) )

                        mail_content =  msg_list['message'][index]+' - value:'+ str(value[0])
                        mail_title = '[IoTtalk] Message Notification'
                        subprocess.call('echo \'{0}\' | mail -s \'{1}\' {2}'.format(mail_content, mail_title, msg_list['name'][index]), shell=True)
                    else:
                        print ('Incorrect input in  Name'+str(index+1))
                else: print ('Message content is None.')

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1) 

    time.sleep(3)

            
