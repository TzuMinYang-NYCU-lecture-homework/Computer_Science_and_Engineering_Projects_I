import time
import requests
import threading
import os

import DAN

ServerIP = '127.0.0.1'
Reg_addr = 'IoTtalk_Folder_O' # if None, Reg_addr = MAC address
FileThread = {}
timestamp = 0

''' IoTtalk part '''
DAN.profile = {
    'd_name': 'Folder_O',
    'dm_name': 'Folder_O',
    'u_name': 'yb',
    'is_sim': False,
    'df_list': [],
}
for i in range(1,10):
    DAN.profile['df_list'].append("File-O%d" % i)
DAN.device_registration_with_retry(ServerIP, Reg_addr)

class FileClass(threading.Thread):
    def __init__(self, df_name):
        threading.Thread.__init__(self)
        self.df_name = df_name
        self.filename = DAN.get_alias(self.df_name)
        self.fd = open(os.getcwd() + "/da/Folder/files/" + self.filename, 'w+')
        self.timestamp_start = 0
        self.timestamp_now = 0
    def run(self):
        while True:
            if self.filename != DAN.get_alias(self.df_name):
                if DAN.get_alias(self.df_name) is None:
                    del FileThread[self.df_name]
                    self.fd.close()
                    break
                self.fd.close()
                self.filename = DAN.get_alias(self.df_name)
                self.fd = open(os.getcwd() + "/da/Folder/files/" + self.filename, 'w+')
            value = DAN.pull(self.df_name)
            if value != None:
                self.timestamp_now = time.time()
                if self.timestamp_start == 0:
                    self.timestamp_start = self.timestamp_now
                self.fd.write(str(self.timestamp_now-self.timestamp_start) + " " + str(value) + "\n")
                self.fd.flush()

def folder_O_run():
    global FileThread
    while True:
        if not DAN.SelectedDF:
            time.sleep(1)
            continue
        for df_name in DAN.SelectedDF:
            if FileThread.get(df_name) is None:
                FileThread[df_name] = FileClass(df_name)
                FileThread[df_name].daemon = True
                FileThread[df_name].start()
                FileThread[df_name].join()
        time.sleep(1)

if __name__ == '__main__':
    folder_O_run()
    DAN.deregister()

