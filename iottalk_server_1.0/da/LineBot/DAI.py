import time, DAN, config 

ServerURL = config.ServerURL
Reg_addr = config.Reg_addr 

DAN.profile['dm_name']= config.dm_name
DAN.profile['df_list']= config.df_list
DAN.profile['d_name'] = config.d_name

DAN.device_registration_with_retry(ServerURL, Reg_addr)


def errorHandler(e):
    print(e)
    if str(e).find('mac_addr not found:') != -1:
        print('Reg_addr is not found. Try to re-register...')
        DAN.device_registration_with_retry(ServerURL, Reg_addr)
    else:
        print('Connection failed due to unknow reasons.')
        time.sleep(1)


def pull():
    try:
        Msg = DAN.pull('Msg-O')
        if Msg and Msg[0]: return Msg[0]
        else: return None
    except Exception as e:
        errorHandler(e)       


def push(Msg):
    try:
        DAN.push('Msg-I', Msg)
    except Exception as e:
        errorHandler(e) 
