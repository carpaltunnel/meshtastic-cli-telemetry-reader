# meshtastic-cli-telemetry-reader

## Usage
First check the `serial_port` variable on line 8 and ensure it matches the USB port that your device is attached to.  `/dev/ttyACM0` is the correct setting for my Linux configuration.


Assuming you setup your Python Mestastic CLI with a virtual environment like in the [documentation ](https://meshtastic.org/docs/software/python/cli/installation/) the command will be something like :

```
~/path/to/meshtastic-virtual/bin/python telemetry-printer.py 
```

If you did not use a Python virtual environment then you're better at Python than me and you should just be able to run `python telemetry-printer.py`

Output is done directly to the console in JSON format, one line per packet.  The `type` property indicates if the output is related to `device` telemetry (power, aitUtil, etc) or `environment` telemetry (temperature, humidity, etc).

Example below : 
```json
{"type": "device", "batteryLevel": 101, "voltage": 3.423, "channelUtilization": 0.0, "airUtilTx": 0.05927778, "uptimeSeconds": 175}
{"type": "environment", "temperature": 31.568457, "lux": 0, "relativeHumidity": 39.26428, "barometricPressure": 1005.43335, "gasResistance": 1565.2688, "airQuality": 50}

```