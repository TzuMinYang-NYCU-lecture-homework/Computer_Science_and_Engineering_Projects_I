#!/bin/sh

python3="python3"

cd $(dirname $0)
cd ../
ProjectPath=$(pwd)
ProjectName=$(echo $ProjectPath | tr "/" "\n" | tail -n 1)
echo "ProjectPath: $ProjectPath"
echo "ProjectName: $ProjectName"

cd $ProjectPath

export PYTHONPATH="$PYTHONPATH:$ProjectPath/lib"
LOG=$ProjectPath/log/startup.log
if [ ! -d $ProjectPath/log ]; then
    mkdir $ProjectPath/log
fi
if [ ! -d $ProjectPath/sqlite ]; then
    mkdir $ProjectPath/sqlite
fi
if [ ! -f $ProjectPath/sqlite/ec_db.db ]; then
    ./setup/reset_db.sh
fi

echo --------------------------------------- >> $LOG
date >> $LOG
echo --------------------------------------- >> $LOG

myIP=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*'| grep -v '127.0.0.1')

screen -dmS $ProjectName >> $LOG 2>&1
add_to_screen() {
    TITLE=$1
    CMD=$2
    screen -S $ProjectName -X screen -t "$TITLE" bash -c \
        "\
        while [ 1 ]; do \
            $CMD; echo ========== restart ==========; sleep 1; \
        done"
}

# wait for screen.
while [ 1 ]; do
    ps aux | grep -v grep | grep SCREEN | grep $ProjectName > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        break
    fi
    sleep 1
done


#add_to_screen CSM "./bin/csm $python3" 
add_to_screen CSM "sudo uwsgi ./lib/wsgi_csm.ini"
echo "Sleep 20 seconds for waitting CSM bootup."

sleep 20

add_to_screen SIM "./bin/ecsim $python3" 
#add_to_screen CCM "./bin/ccm $python3" 
add_to_screen CCM "sudo uwsgi ./lib/ccm/wsgi_ccm.ini"
add_to_screen ESM "./bin/esm $python3" 
#add_to_screen WEB "sudo $python3 ./da/web.py" 
add_to_screen Msg "$python3 ./da/Message/message.py"
add_to_screen Timer "$python3 ./da/Timer/timer.py" 
#add_to_screen MusicBox "cd ./da/MusicBox;npm install;nodejs Server.js $myIP:9999" 
#add_to_screen MorSocket "cd ./da/MorSocket-Server;npm install;nodejs MorSocketServer.js $myIP:9999" 
#add_to_screen Broadcast "$python3 ./bin/broadcast.py" 
#add_to_screen SmartMeter "$python3 ./da/SmartMeter/DAI.py"
#add_to_screen Weather "$python3 ./da/weatherSTA/DAI.py"
#add_to_screen Map "$python3 ./da/Map/start.py"
#add_to_screen Airbox "$python3 ./da/Map/FetchData/FetchData_Airbox/DAI.py"
#add_to_screen BaoFarm "$python3 ./da/Map/FetchData/FetchData_BaoFarm/DAI.py"
#add_to_screen MIRC311 "$python3 ./da/Map/FetchData/FetchData_MIRC311/DAI.py"
#add_to_screen GradDorm3 "$python3 ./da/Map/FetchData/FetchData_GradDorm3/DAI.py"
#add_to_screen NCTUBus "$python3 ./da/Map/FetchData/FetchData_NCTUBus/DAI.py"
#add_to_screen MIRC610 "$python3 ./da/Map/FetchData/FetchData_MIRC610/DAI.py"
#add_to_screen ParkingLot "$python3 ./da/Map/FetchData/FetchData_ParkingLot/DAI.py"
#add_to_screen OrchidHouse "$python3 ./da/Map/FetchData/OrchidHouse/DAI.py"
#add_to_screen SP_kAir "$python3 ./da/Map/FetchData_ScienceParkAir/DAI.py"
#add_to_screen SP_Water "$python3 ./da/Map/FetchData_ScienceParkWater/DAI.py"
#add_to_screen Weather "$python3 ./da/Map/FetchData_Weather/DAI.py"


$python3 ./da/Remote_control/startup_panel.py
#$python3 "./da/Dandelion_control(mobile)/startup.py"
#$python3 ./da/agri_startup/DAI.py


#echo "Waiting for CHT Pirius booting. (2 mintues.)"
#sleep 120
#add_to_screen CHT "nodejs ./da/IoTtalk-CHT-master/index.js" >> $LOG 2>&1

