import requests, json

ENDPOINT = 'https://www.cwb.gov.tw/'
TIMEOUT=10
CWB = requests.Session()

def getWeather(station_id, UsingSession=CWB):
    r = UsingSession.get(
        ENDPOINT + '/Data/js/Observe/Stations/' + station_id + '.js',    #old version
        timeout=TIMEOUT,
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    )
    if r.status_code != 200: return None
    r.encoding='utf-8'
    text = r.text.replace("'", '"')
    text = text.replace('var ST = ', '')
    text = text.replace('var OBS =', '')
    return json.loads(text.split(';')[1])





if __name__ == '__main__':
    
    data = getWeather('46757')
    if data:
        ST_Status = data['0']['ST_Status']
        Date = data['0']['Date']
        Time = data['0']['Time']
        StationName = data['0']['StationName']['E']
        Weather = data['0']['Weather']['E']
        Temperature = data['0']['Temperature']['C']['E']
        Humidity = data['0']['Humidity']['E']
        Rain = data['0']['Rain']['E']
        WindDir = data['0']['WindDir']['E']
        Wind = data['0']['Wind']['MS']['E']
        Gust = data['0']['Gust']['MS']['E']
        Visibility  = data['0']['Visibility']['E']
        Pressure = data['0']['Pressure']['E'] 
        Sunshine = data['0']['Sunshine']
        print(ST_Status, Date, Time, StationName, Weather, Temperature, Humidity, Rain, WindDir, Wind, Gust, Visibility, Pressure, Sunshine  )
    
