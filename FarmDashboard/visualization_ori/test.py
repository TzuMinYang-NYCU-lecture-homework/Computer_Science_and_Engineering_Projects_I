import sys
sys.path.append("..")
from db import db

def main():
    db.connect()

    session = db.get_session()

    for field in (session.query(db.models.field).all()):
        profile = {'d_name': field.name + '_DataServer',
                   'dm_name': 'DataServer',
                   'df_list': ['Alert-I', 'history-I', 'realtime-I'],
                   'is_sim': False}
        alert_range = {}
        query_df = (session.query(db.models.field_sensor)
                           .select_from(db.models.field_sensor)
                           .join(db.models.sensor)
                           .filter(db.models.field_sensor.field == field.id)
                           .all())

        print(field.name)

        for df in query_df:
            profile['df_list'].append(df.df_name)
            alert_range[df.df_name] = {'min': df.alert_min,
                                       'max': df.alert_max}
            #print(df.df_name)

        if not profile['df_list']:
            continue

    session.close()

if __name__ == "__main__":
    main()
