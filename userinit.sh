#!/system/bin/sh
sleep 15
nohup /system/bin/python3 /data/local/bin/ASUS-TF101-REST-Sensors-master/script.py > /data/local/tmp/sensors.log 2>&1 &
exit 0