from flask import Flask
app = Flask(__name__)

###
import sys
sys.path.append("..")
from db import db
###

@app.route("/<string:field>") #用parent.document.getElementsByClassName('tab-pane active').id取得想要跳轉的網址後，可以用變數接在後面嗎?
def get_sensor_list(field):
    ###
    db.connect()
    session = db.get_session()
    ans = ""

    for field_attr in (session.query(db.models.field).all()):
        #field_attr = session.query(db.models.field).filter(db.models.field.name == field) 不知道為什麼不能這樣用，下面的id會有問題
        if field_attr.name == field:
            query_df = (session.query(db.models.field_sensor)
                                .select_from(db.models.field_sensor)
                                .join(db.models.sensor)
                                .filter(db.models.field_sensor.field == field_attr.id)
                                .all())
            ans = field + "'s sensors:<br><br>"
            for sensor in query_df:
                ans = ans + sensor.df_name + "<br>"

            break
    
    #ans += """<a href="#" onclick="window.open(' http://tw.yahoo.com ', 'Yahoo', config='height=750,width=1500');">開新視窗</a>"""
    ans += """<a href="#" onclick="alert('test');">開新視窗</a>"""

    session.close()
    return ans.strip("<br>")

@app.route("/")
def hello():
    """
    db.connect()

    session = db.get_session()

    ans = ""

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

        ans = ans + "<br>" + field.name

        for df in query_df:
            profile['df_list'].append(df.df_name)
            alert_range[df.df_name] = {'min': df.alert_min,
                                       'max': df.alert_max}
            #print(df.df_name)

        if not profile['df_list']:
            continue

    session.close()
    """
    return "test"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True) # host 參數可以指定允許訪問的主機IP，0.0.0.0 為所有主機的意思，而後面則是自訂網路埠號的參數