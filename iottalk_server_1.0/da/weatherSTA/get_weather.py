import requests
import time
from bs4 import BeautifulSoup
fetch_gap = 10

ENDPOINT = 'https://www.cwb.gov.tw/'
TIMEOUT=10
CWB = requests.Session()

def getWeather(station_id, UsingSession=CWB):
    r = UsingSession.get(
#        ENDPOINT + '/Data/js/Observe/Stations/' + station_id + '.js',    #old version
        ENDPOINT + '/V8/C/W/Observe/MOD/24hr/' + station_id + '.html',
        timeout=TIMEOUT,
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    )
    if r.status_code != 200: return None
    r.encoding='utf-8'
    return r.text

def get_element(soup):
    data = []
    rows = soup.find_all('tr')
    for row in rows:
        first_col = row.find_all('th')
        if first_col == []: return
        cols = row.find_all('td')
        cols.insert(0, first_col[0])
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) 
    return data    

def C2f(string_data):
    try:
        return float(string_data)
    except Exception as e:
        #print(e)
        return None

def fetch_data(station_id):
    html_text = getWeather(station_id)
    soup = BeautifulSoup(html_text, "lxml")
    data = get_element(soup) 
    DIR={}
    if data:
        DIR['Temp']      = C2f(data[0][1])
        DIR['Wind']      = C2f(data[0][3])
        DIR['Humidity']  = C2f(data[0][6])
        DIR['AtPressure']= C2f(data[0][7])
        DIR['Rain']      = C2f(data[0][8])
        DIR['Sunshine']  = C2f(data[0][9])
    return DIR   

if __name__ == '__main__':

#    html_text = getWeather('46757')
#    soup = BeautifulSoup(html_text, "lxml")
#    data = get_element(soup)

    data = fetch_data('46757')
    print(data)
    data = fetch_data('C0D66')
    print(data)
    







