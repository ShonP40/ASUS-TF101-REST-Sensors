# ASUS TF101 REST Sensors
A REST API for reporting the sensor values of rooted ASUS TF101 devices

## Installation

### Requirements
- Rooted ASUS TF101 tablet running CyanogenMod 10 (Android 4.1.2)
- Terminal/SSH access to your ASUS TF101 device
- WiFi configured to stay on during sleep
- HTTP web server which can host files

## Setup
1. Meet the requirements
2. Download this git repository as a ZIP file and upload it to your HTTP web server
3. Use Terminal/SSH to connect to your ASUS TF101 device
4. Gain root access by running `su`
5. Make a new directory by running `mkdir /data/local/bin && cd /data/local/bin`
6. Download the repository ZIP file to your device by running `wget http://<your web server>/ASUS-TF101-REST-Sensors-master.zip`
7. Unzip the file by running `unzip ASUS-TF101-REST-Sensors-master.zip`
8. cd into the `ASUS-TF101-REST-Sensors-master` directory
9. Move the `userinit.sh` file to `/data/local/` by running `mv userinit.sh /data/local/`
10. Make the script executable by running `chmod 755 /data/local/userinit.sh`

## Python Installation
1. Go back to the repo directory by running `cd /data/local/bin/ASUS-TF101-REST-Sensors-master/Python/system`
2. Remount the system partition as read/write by running `mount -o remount,rw /system`
3. Install Python by moving its exacutable to the system directory by running `mv bin/python3 /system/bin/`
4. Move the main Python directory to the system directory by running `mv python3.4.2 /system/`
5. Update the permissions of the Python executable by running `chmod 755 /system/bin/python3`
6. Update the permissions of the Python directory by running `chmod -R 755 /system/python3.4.2/*`
7. Remount the system partition as read-only by running `mount -o remount,ro /system`

## Running the script
Rebooting your device should automatically start the script

### Updating the script
1. Use Terminal/SSH to connect to your ASUS TF101 device
2. Gain root access by running `su`
3. Find the PID of the running script by running `ps | grep python3`
4. Kill the running script by running `kill <PID>`
5. Download the updated `script.py` file into the `/data/local/bin/ASUS-TF101-REST-Sensors-master/` directory
6. Restart your device to start the updated script

## Usage
If you are using this script to display the battery status of your ASUS TF101 on Home Assistant, you can use the following configuration as an example:

```yaml
sensor:
    - platform: rest
        name: Tablet battery status
        unique_id: tablet_battery_status
        resource: http://<Tablet IP>:8000/status/battery
        method: GET
        value_template: "{{ value_json.Battery }}"
        unit_of_measurement: "%"
        device_class: battery
        json_attributes:
            - Battery
            - Battery status
            - Battery temperature
            - Battery voltage
    - platform: rest
        name: Tablet light sensor
        unique_id: tablet_light_sensor
        resource: http://<Tablet IP>:8000/status/light
        method: GET
        value_template: "{{ value_json.Lux }}"
        unit_of_measurement: "lx"
        device_class: illuminance
    - platform: rest
        name: Tablet board temperature
        unique_id: tablet_board_temperature
        resource: http://<Tablet IP>:8000/status/temperature
        method: GET
        value_template: "{{ value_json.Board }}"
        unit_of_measurement: "°C"
        device_class: temperature
    - platform: rest
        name: Tablet screen brightness
        unique_id: tablet_screen_brightness
        resource: http://<Tablet IP>:8000/status/screen
        method: GET
        value_template: "{{ (value_json.Brightness | int / 255 * 100) | round(0) }}"
        unit_of_measurement: "%"
```