from threading import Thread

from main import map_server
import DAI, Tracking

t = Thread(target=map_server)
t.daemon = True
t.start()

Tracking.dai()

DAI.iottalk_device_feature_update()
DAI.dai()

