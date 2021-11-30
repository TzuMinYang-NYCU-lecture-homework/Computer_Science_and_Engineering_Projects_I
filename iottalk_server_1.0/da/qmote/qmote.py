#!/usr/bin/env python3
import base64
import json
import os.path
import paho.mqtt.client as mqtt
import requests
import ssl
import DAI

user_email = 'User account'
user_password = 'User password'

client_id = '6292430aeb5084477f6e4ea9d6162dac2ab25c00b1150195e2c9a0b225ed2626'
client_secret = '238af1acaab12c87ebc5c3b3d28bb31e0810dc4c9411703daf4766eadb3c3fe0'

token_server = 'https://qcloud.qblinks.com/api/qmote/users/oauth/token'
list_server  = 'https://qcloud.qblinks.com/api/device/list'
cert_server = 'https://deviceauth.qblinks.com/deviceCertificate'
mqtt_server = ''

rootca_file = 'rootca.cert'
certificate_file = 'certificate.crt'
key_file = 'private.key'
mqtt_server_file = 'mqtt_server'

token = ''
userhash = ''

def create_cert():
    if not os.path.isfile(rootca_file) or not os.path.isfile(certificate_file) or not os.path.isfile(key_file) or not os.path.isfile(mqtt_server_file):
  
        auth_str = base64.b64encode(bytes(client_id + ":" + client_secret, 'utf-8')).decode('utf-8')

        # get token
        headers = {"Authorization": "Basic " + auth_str}
        data = {"user[email]": user_email, "user[password]": user_password}
        r = requests.post(token_server, data=data, headers=headers)
        token = r.json()["access_token"]

        # get certificate
        headers = {"Authorization": "Bearer " + token}
        r = requests.post(cert_server, headers=headers)
    
        userhash = r.json()["userhash"]
        certificate = r.json()["certificate"]
        mqtt_url = r.json()["mqtt_url"][8:-5]

        # save file
        with open(rootca_file, 'w') as f:
            f.write(certificate['rootca'])
        with open(certificate_file, 'w') as f:
            f.write(certificate['certificate'])
        with open(key_file, 'w') as f:
            f.write(certificate['private_key'])
        with open(mqtt_server_file, 'w') as f:
            f.write(token+';'+userhash+';'+mqtt_url)
            
def get_device_list():
    headers = {"Authorization": "Bearer " + token}
    r = requests.get(list_server, headers=headers)
    return r.json()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(rc))
    event_sub = 'qblinks/v1/{}/channel/qmote/triggered'.format(userhash)
    client.subscribe(event_sub)

create_cert()

with open(mqtt_server_file, 'r') as f:
    token, userhash, mqtt_server = (f.readline()).split(';')

# connect to mqtt server
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = DAI.on_message
client.tls_set(rootca_file,
               certfile=certificate_file,
               keyfile=key_file,
               cert_reqs=ssl.CERT_REQUIRED,
               tls_version=ssl.PROTOCOL_TLSv1_2,
               ciphers=None)
client.connect(mqtt_server, port=8883)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

