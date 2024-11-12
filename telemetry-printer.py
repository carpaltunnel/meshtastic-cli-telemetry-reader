import time
import sys
import json
from pubsub import pub
from meshtastic.serial_interface import SerialInterface
from meshtastic import portnums_pb2

serial_port = '/dev/ttyACM0'  # Replace with your Meshtastic device's serial port

def build_environment_dict(envData):
    #TODO: Update this to support humidity, pressure, etc from BME280
    try:
        jsonPrep = {
            'type': 'environment',
            'temperature': envData['temperature'],
            'lux': envData.get('lux', 0),
            'relativeHumidity': envData.get('relativeHumidity', 0),
            'barometricPressure': envData.get('barometricPressure', 0),
            'gasResistance': envData.get('gasResistance', 0),
            'airQuality': envData.get('iaq', 0)
        }
        return jsonPrep
    except Exception as ex:
        print('Environment telemetry decoding failed!!')
        print(ex)


def build_device_dict(deviceData):
    try:
        jsonPrep = {
            'type': 'device',
            'batteryLevel': deviceData.get('batteryLevel', 0),
            'voltage': deviceData.get('voltage', 0),
            'channelUtilization': deviceData.get('channelUtilization', 0),
            'airUtilTx': deviceData.get('airUtilTx', 0),
            'uptimeSeconds': deviceData.get('uptimeSeconds', 0)
        }
        return jsonPrep
    except Exception as ex:
        print('Device telemetry decoding failed!!')
        print(ex)

def on_receive(packet, interface):
    try:
        #print(packet)
        #print('Trying to print telemetry....')
        #print(packet['decoded']['telemetry'])
        if packet['decoded']['portnum'] == 'TELEMETRY_APP':
            #print(packet['decoded']['telemetry']
            # Power info
            #print(packet['decoded']['telemetry']['deviceMetrics'])
            # Environment info
            #print(packet['decoded']['telemetry']['environmentMetrics'])

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
    #print(f"Using serial port: {serial_port}")

    # Subscribe the callback function to message reception
    def on_receive_wrapper(packet, interface):
        on_receive(packet, interface)#, node_list)

    pub.subscribe(on_receive_wrapper, "meshtastic.receive")
    #print("Subscribed to meshtastic.receive")

    # Set up the SerialInterface for message listening
    local = SerialInterface(serial_port)
    #print("SerialInterface setup for listening.")

    # Keep the script running to listen for messages
    try:
        while True:
            sys.stdout.flush()
            time.sleep(1)  # Sleep to reduce CPU usage
    except KeyboardInterrupt:
        #print("Script terminated by user")
        local.close()

if __name__ == "__main__":
    main()
