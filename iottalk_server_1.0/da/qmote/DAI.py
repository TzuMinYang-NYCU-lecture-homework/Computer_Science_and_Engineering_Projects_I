import time, DAN, requests, json   

ServerIP = '140.113.199.246' #Change to your IoTtalk IP or None for autoSearching
Reg_addr='Qmote-'+DAN.get_mac_addr() # if None, Reg_addr = MAC address

DAN.profile['dm_name']='Qmote'
DAN.profile['df_list']=['Button']
DAN.profile['d_name']= None # None for autoNaming
DAN.device_registration_with_retry(ServerIP, Reg_addr)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    event = json.loads(msg.payload.decode('utf-8'))
    
    try:
        DAN.push('Button', int(event["event_id"]), event["device_id"])
        print ('Push: {}, {}'.format(event["event_id"], event["device_id"]))
    except Exception as e:
        print (e)
        DAN.device_registration_with_retry(ServerIP, Reg_addr)

