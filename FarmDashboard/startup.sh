#!/bin/sh

path="/home/sam1248105/NYCU/交大/上課/大三上/'資訊工程專題(一)'/FarmDashboard"
venvfile="~/CS_project_env_and_script/venv_for_dashboard/bin/activate"

session_name="graphserver"

tmux kill-session -t $session_name 2>/dev/null

if [ $(tmux ls 2>/dev/null | grep $session_name | wc -l) -eq "0" ]
then
  ###原本的會開兩個window,dashboard執行在第二個window,不知道第一個window要幹嘛

  #tmux new-session -s $session_name -d;
  #sleep 1
  #tmux new-window -t $session_name -n Dashboard -d "source $venvfile; python3 $path/server.py; bash -i"
  #本來的版本不會自動執行server.py,好像是找不到在哪,但不確定
  #tmux new-window -t $session_name -n Dashboard -d "source $venvfile; python3 ./server.py; bash -i"

  ###我改成只會有一個window
  tmux new-session -s $session_name -n Dashboard -d "source $venvfile; python3 $path/server.py; bash -i"
else
  echo "Can't kill previous tmux session..."
fi
