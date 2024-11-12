# meshtastic-cli-telemetry-reader

## Usage
First check the `serial_port` variable on line 8 and ensure it matches the USB port that your device is attached to.  `/dev/ttyACM0` is the correct setting for my Linux configuration.


Assuming you setup your Python Mestastic CLI with a virtual environment like in the [documentation ](https://meshtastic.org/docs/software/python/cli/installation/) the command will be something like :

```
~/path/to/meshtastic-virtual/bin/python telemetry-printer.py 
```

If you did not use a Python virtual environment then you're better at Python than me and you should just be able to run `python telemetry-printer.py`