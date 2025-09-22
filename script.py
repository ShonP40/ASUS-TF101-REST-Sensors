from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import json
from collections import OrderedDict

################################################################################## Battery
def get_battery_percentage():
    output = subprocess.Popen(
        ['cat /sys/class/power_supply/battery/capacity'],
        shell=True, stdout=subprocess.PIPE
    ).communicate()[0]
    return output.decode('utf-8').strip()

def get_battery_charging_status():
    output = subprocess.Popen(
        ['cat /sys/class/power_supply/battery/status | grep "Charging"'],
        shell=True, stdout=subprocess.PIPE
    ).communicate()[0]
    status = output.decode('utf-8').strip()
    return "Charging" if status == '1' else "NotCharging"

def get_battery_temperature():
    output = subprocess.Popen(
        ['cat /sys/class/power_supply/battery/temp'],
        shell=True, stdout=subprocess.PIPE
    ).communicate()[0]
    return float(output.decode('utf-8').strip()) / 10.0

def get_battery_voltage():
    output = subprocess.Popen(
        ['cat /sys/class/power_supply/battery/voltage_now'],
        shell=True, stdout=subprocess.PIPE
    ).communicate()[0]
    return output.decode('utf-8').strip()
################################################################################## Light Sensor
def get_lux_level():
    output = subprocess.Popen(
        ['cat /sys/bus/i2c/devices/2-001c/show_lux'],
        shell=True, stdout=subprocess.PIPE
    ).communicate()[0]
    return output.decode('utf-8').strip()
################################################################################## Temperature Sensor
def get_board_temperature():
    output = subprocess.Popen(
        ['cat /sys/bus/i2c/devices/4-004c/ext_temperature'],
        shell=True, stdout=subprocess.PIPE
    ).communicate()[0]
    return output.decode('utf-8').strip()
##################################################################################

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status/battery':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = OrderedDict([
                ('Battery', get_battery_percentage()),
                ('Battery status', get_battery_charging_status()),
                ('Battery temperature', get_battery_temperature()),
                ('Battery voltage', get_battery_voltage())
            ])
            self.wfile.write(json.dumps(data).encode('utf-8'))
        elif self.path == '/status/light':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = OrderedDict([
                ('Lux', get_lux_level())
            ])
            self.wfile.write(json.dumps(data).encode('utf-8'))
        elif self.path == '/status/temperature':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = OrderedDict([
                ('Board temperature', get_board_temperature())
            ])
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            self.send_error(404)

def main():
    server = HTTPServer(('0.0.0.0', 8000), ServerHandler)
    print("Starting server, use <Ctrl-C> to stop")
    server.serve_forever()

if __name__ == '__main__':
    main()