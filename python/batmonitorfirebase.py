#!/usr/bin/env python3

# batmonitorfirebase.py
import subprocess
import time
import pyrebase
import firebaseconfig

limit_min = 20               # %
limit_max = 100              # %
time_monitor = 30            # segundos
time_monitor_critical = 10   # segundos

def read_status_perc():
    command = "upower -i $(upower -e | grep BAT) | grep --color=never -E percentage|xargs|cut -d' ' -f2|sed s/%//"
    get_batterydata = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE)
    return int(get_batterydata.communicate()[0].decode("utf-8").replace("\n", ""))

def read_status_charging():
    # estudar melhor esta linha
    command = "upower -i $(upower -e | grep BAT) | grep --color=never -E state|xargs|cut -d' ' -f2|sed s/%//"
    get_batterydata = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE)

    # discharging = 0
    # charging = 1
    resp = get_batterydata.communicate()[0].decode("utf-8").replace("\n", "")
    #print(resp)
    if resp == "charging":
        return 1
    else:
        return 0

def bat_monitor():
    show = 0
    charging = 0
    charging_old = 0
    while True:
        charging = read_status_charging()

        if charging != charging_old:
            show = 0
            charging_old = charging

        charge = read_status_perc()

        if charge == 100:
            if charging == 1:
                # Se não quiser usar Firebase, comente esta linha
                info_network(0)
                show_notify_remove_charger()
            if show == 0:
                show_notify(charge, read_status_charging())
                show = 1
        elif charge > limit_min and show == 0:
            show_notify(charge, charging)
            show = 1
        elif charge <= limit_min and charging == 0:
            # Se não quiser usar Firebase, comente esta linha
            info_network(1)
            while (read_status_charging() == 0):
                show = 0
                show_notify_critical(read_status_perc())
                time.sleep(time_monitor_critical)
            show_notify(read_status_perc(), read_status_charging())
        
        time.sleep(time_monitor)

def show_notify(perc, charg):
    msg = "Bateria com {0}%".format(perc)
    if charg == 1:
        msg += "\nCarregando..."
    else:
        msg += "\nNão carregando..."
    command = "notify-send '{0}'".format(msg)
    subprocess.Popen(["/bin/bash", "-c", command])

def show_notify_critical(perc):
    msg = "Bateria em nível crítica com {0}%".format(perc)
    msg += "\nConectar carregador!"
    command = "notify-send '{0}'".format(msg)
    subprocess.Popen(["/bin/bash", "-c", command])

def show_notify_remove_charger():
    command = "notify-send 'Remova o carregador'"
    subprocess.Popen(["/bin/bash", "-c", command])

def info_network(on_off):
    firebase = pyrebase.initialize_app(firebaseconfig.config)
    db = firebase.database()
    db.child(firebaseconfig.path_control).set(on_off)

def main():
    bat_monitor()

##
main()
