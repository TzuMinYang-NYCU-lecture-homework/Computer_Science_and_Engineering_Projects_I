import time

from threading import Thread

from db import db

from config import CSM_HOST as host
from da.DAN import DAN, log

### add by myself
#from flask import g

def _run(profile, reg_addr, field, field_id, alert_range={}):
    dan = DAN()
    dan.device_registration_with_retry(profile, host, reg_addr)
    
    while True:
        try:
            ### add by myself
            realtime_data = {field: {}}
            ###

            # Pull data
            session = db.get_session()
            for df in dan.selected_DF:
                ### add by myself
                if df != 'history-I' and df != 'realtime-I':
                ###
                    data = dan.pull_with_timestamp(df)
                    if data:
                        log.debug(field, df, data)
                        timestamp = data[0]

                        try:
                            value = float(data[1][0])
                        except Exception as e:
                            log.warning(e, ', ignore this data.')
                            continue

                        new_model = getattr(db.models, df.replace('-O', ''))(timestamp=timestamp, field=field_id, value=value)
                        session.add(new_model)
                        session.commit()

                        ### add by myself
                        # 令時間格式和push history一樣
                        single_data = [{'timestamp':'{}'.format(data[0]), 
                                        'value': '{}'.format(data[1])}]
                        #realtime_data[field].update({df: data})
                        realtime_data[field].update({df: single_data})

                        #IDF_data.append(new_model.value)
                        #print(new_model.value)
                        ###

                        # alert
                        if df in alert_range:
                            alert_min = alert_range[df].get('min', 0)
                            alert_max = alert_range[df].get('max', 0)
                            if alert_min != alert_max and (value > alert_max or value < alert_min):
                                dan.push('Alert-I', '{} {}'.format(df, value))

            ### add by myself
            #dan.push ('history-I', IDF_data)
            #sensors = g.session.query(db.models.sensor).order_by(db.models.sensor.id).all()
            #print(sensors)
            #print(IDF_data)

            if(len(realtime_data[field]) > 0):  #避免剛開始執行時沒有抓到資料時送出空的東西出去
                dan.push('realtime-I', realtime_data)

            ###

            

            time.sleep(20)
        except KeyboardInterrupt:
            log.info(field, ': exit')
            break
        except Exception as e:
            log.error('[ERROR]:', e)
            if str(e).find('mac_addr not found:') != -1:
                log.error('Reg_addr is not found. Try to re-register...')
                dan.device_registration_with_retry(profile, host, reg_addr)
            else:
                log.error('Connection failed due to unknow reasons.')
                time.sleep(1)
        finally:
            session.close()

def main():
    db.connect()#!!!
    threads = []

    session = db.get_session()#!!!

    for field in (session.query(db.models.field).all()):#!!! 名字可能是field.name
        ### add by myself, I add history-I and realtime-I in df_list
        profile = {'d_name': field.name + '_DataServer',
                   'dm_name': 'DataServer',
                   'df_list': ['Alert-I', 'history-I', 'realtime-I'],
                   'is_sim': False}
        alert_range = {}
        query_df = (session.query(db.models.field_sensor)#!!!
                           .select_from(db.models.field_sensor)
                           .join(db.models.sensor)
                           .filter(db.models.field_sensor.field == field.id)
                           .all())

        for df in query_df:
            profile['df_list'].append(df.df_name)
            alert_range[df.df_name] = {'min': df.alert_min,
                                       'max': df.alert_max}

        if not profile['df_list']:
            continue

        thread = Thread(target=_run,
                        args=(profile,
                              profile['d_name'],
                              field.name,
                              field.id,
                              alert_range))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    session.close()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
