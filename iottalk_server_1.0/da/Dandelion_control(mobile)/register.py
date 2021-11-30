import requests

ENDPOINT = 'http://localhost:9999'
TIMEOUT=10
IoTtalk = requests.Session()

class CSMError(Exception):
    pass

def register(mac_addr, profile, UsingSession=IoTtalk):
    r = UsingSession.post(
        ENDPOINT + '/' + mac_addr,
        json={'profile': profile}, timeout=TIMEOUT
    )
    if r.status_code != 200: raise CSMError(r.text)
    else: passwordKey = r.json().get('password')
    return True, passwordKey
