import requests

ENDPOINT = None
TIMEOUT=10
IoTtalk = requests.Session()
#print(IoTtalk)

class CSMError(Exception):
    pass

def register(mac_addr, profile, UsingSession=IoTtalk):
    r = UsingSession.post(
        ENDPOINT + '/' + mac_addr,
        json={'profile': profile}, timeout=TIMEOUT
    )
    if r.status_code != 200: raise CSMError(r.text)
    return True


def deregister(mac_addr, UsingSession=IoTtalk):
    r = UsingSession.delete(ENDPOINT + '/' + mac_addr)
    if r.status_code != 200: raise CSMError(r.text)
    return True


def push(mac_addr, df_name, data, UsingSession=IoTtalk):
    r = UsingSession.put(
        ENDPOINT + '/' + mac_addr + '/' + df_name,
        json={'data': data}, timeout=TIMEOUT
    )
    if r.status_code != 200: raise CSMError(r.text)
    return True


def pull(mac_addr, df_name, EP=ENDPOINT, UsingSession=IoTtalk):
    r = UsingSession.get(EP + '/' + mac_addr + '/' + df_name, timeout=TIMEOUT)
    if r.status_code != 200: raise CSMError(r.text)
    return r.json()['samples']


def get_alias(mac_addr, df_name, UsingSession=IoTtalk):
    r = UsingSession.get(ENDPOINT + '/get_alias/' + mac_addr + '/' + df_name, timeout=TIMEOUT)
    if r.status_code != 200: raise CSMError(r.text)
    return r.json()['alias_name']

	
def set_alias(mac_addr, df_name, s, UsingSession=IoTtalk):
    r = UsingSession.get(ENDPOINT + '/set_alias/' + mac_addr + '/' + df_name + '/alias?name=' + s, timeout=TIMEOUT)
    if r.status_code != 200: raise CSMError(r.text)
    return True

	
def tree(UsingSession=IoTtalk):
    r = UsingSession.get(ENDPOINT + '/tree')
    if r.status_code != 200: raise CSMError(r.text)
    return r.json()

	
def pull_airbox(url, UsingSession=IoTtalk):
    r = UsingSession.get(url, verify=False, timeout=TIMEOUT)
    if r.status_code != 200: raise CSMError(r.text)
    return r.json()['devices']