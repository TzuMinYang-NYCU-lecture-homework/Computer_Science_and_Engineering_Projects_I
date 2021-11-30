import time
import requests
import threading

import DAN

ServerIP = '127.0.0.1'
Reg_addr = 'IoTtalk_Folder_I' # if None, Reg_addr = MAC address
FileThread = {}
timestamp = 0

''' IoTtalk part '''
DAN.profile = {
    'd_name': 'Folder_I',
    'dm_name': 'Folder_I',
    'u_name': 'yb',
    'is_sim': False,
    'df_list': [],
}
for i in range(1,10):
    DAN.profile['df_list'].append("File-I%d" % i)
DAN.device_registration_with_retry(ServerIP, Reg_addr)

class FileClass(threading.Thread):
    def __init__(self, df_name):
        threading.Thread.__init__(self)
        self.df_name = df_name
        self.filename = DAN.get_alias(self.df_name)
        self.fd = open(os.getcwd() + "/da/Folder/files/" + self.filename, 'r')
        self.timestamp_last = 0
        self.timestamp_next = 0
    def run(self):
        while True:
            if self.filename != DAN.get_alias(self.df_name):
                if DAN.get_alias(self.df_name) is None:
                    del FileThread[self.df_name]
                    self.fd.close()
                    break
                self.fd.close()
                self.filename = DAN.get_alias(self.df_name)
                self.fd = open(os.getcwd() + "/da/Folder/files/" + self.filename, 'r')
            self.timestamp_last = self.timestamp_next
            info = self.fd.readline()
            if not info:
                time.sleep(1)
                continue
            else:
                self.timestamp_next, value = info.split(" ")
            if value != None:
                time_gap = float(self.timestamp_next)-float(self.timestamp_last)
                time.sleep(time_gap)
                print("timestamp = "+self.timestamp_next)
                print("time gap = "+str(time_gap))
                print("value = "+value)
                DAN.push(self.df_name, value)

def folder_I_run():
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
    folder_I_run()
    DAN.deregister()

