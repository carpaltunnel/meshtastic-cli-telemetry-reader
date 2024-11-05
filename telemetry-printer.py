import time
import sys
import json
from pubsub import pub
from meshtastic.serial_interface import SerialInterface
from meshtastic import portnums_pb2

serial_port = '/dev/ttyACM0'  # Replace with your Meshtastic device's serial port

def build_environment_dict(envData):
    #TODO: Update this to support humidity, pressure, etc from BME280
    jsonPrep = {
        'type': 'environment',
        'temperature': envData['temperature'],
        'lux': envData['lux']
    }
    return jsonPrep

def build_device_dict(deviceData):
    jsonPrep = {
        'type': 'device',
        'batteryLevel': deviceData['batteryLevel'],
        'voltage': deviceData['voltage'],
        'channelUtilization': deviceData['channelUtilization'],
        'airUtilTx': deviceData['airUtilTx'],
        'uptimeSeconds': deviceData['uptimeSeconds']
    }
    return jsonPrep

def on_receive(packet, interface):
    try:
        if packet['decoded']['portnum'] == 'TELEMETRY_APP':
            # Device metrics parse :
            if "deviceMetrics" in packet['decoded']['telemetry']:
                #print('----- FOUND DEVICE METRICS!!!')
                parsedDevice = build_device_dict(packet['decoded']['telemetry']['deviceMetrics'])
                print(json.dumps(parsedDevice))

            # Environment parse:
            if "environmentMetrics" in packet['decoded']['telemetry']:
                #print('----- FOUND ENVIRONMENT METRICS!!!')
                parsedEnv = build_environment_dict(packet['decoded']['telemetry']['environmentMetrics'])
                print(json.dumps(parsedEnv))
            
            
    except KeyError:
        pass  # Ignore KeyError silently
    except UnicodeDecodeError:
        pass  # Ignore UnicodeDecodeError silently

def main():
    print(f"Using serial port: {serial_port}")

    # Subscribe the callback function to message reception
    def on_receive_wrapper(packet, interface):
        on_receive(packet, interface)#, node_list)

    pub.subscribe(on_receive_wrapper, "meshtastic.receive")
    print("Subscribed to meshtastic.receive")

    # Set up the SerialInterface for message listening
    local = SerialInterface(serial_port)
    print("SerialInterface setup for listening.")

    # Keep the script running to listen for messages
    try:
        while True:
            sys.stdout.flush()
            time.sleep(1)  # Sleep to reduce CPU usage
    except KeyboardInterrupt:
        print("Script terminated by user")
        local.close()

if __name__ == "__main__":
    main()
