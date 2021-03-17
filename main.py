import threading

from Config import Config
from GUI import GUI
from WindowChangeListener import WindowChangeListener

from inkkeys import *  # Inkkeys module
from modes import *

import pprint

from serial import SerialException  # Serial functions
import serial.tools.list_ports  # Function to iterate over serial ports
import traceback  # Print tracebacks if an error is thrown and caught

VID = 0x1b4f  # USB Vendor ID for a Pro Micro
PID = 0x9206  # USB Product ID for a Pro Micro

DEBUG = True


# called when window change event occurs
def handleWindowChange(exePath):
    if exePath in config.config["applications"]:
        pprint.pprint(config.config["applications"][exePath])
        mode = ModeApplication()
        mode.activate(device, exePath, config.config["applications"][exePath])
    else:
        print("Application not recognized")


# Try connecting on the given port and work with it. Will return false if connection fails or an unknown device is
# present. If it succeeds, it will enter the main working loop forever. It will only return if an error occurs and
# return True to report that it was working with the correct device.
def tryUsingPort(port):
    try:
        if device.connect(port):
            return True
    except SerialException as e:
        print("Serial error: ", e)
    except:
        # Something entirely unexpected happened. We will catch it nevertheless, so the device keeps working as this
        # process will probably run in the background unsupervised. But we need to print a proper stacktrace,
        # so we can debug the problem.
        if DEBUG:
            print(traceback.format_exc())
            print("Error: ", sys.exc_info()[0])
    return False


def endEverything():
    # disconnect the device (without triggering callbacks)
    device.disconnect(True)

def connectToDevice():
    def doConnect():
        connected = False
        print("CTD called")
        while connected == False:
            print("CTD loop")
            for port in serial.tools.list_ports.comports():  # Iterate over all serial ports
                if port.vid != VID or port.pid != PID:
                    continue  # Skip if vendor or product ID do not match
                if tryUsingPort(port.device):  # Try connecting to this device
                    connected=True
                    gui.setConnected()
                    print("CTD connected")
                    connecting=False
                    break  # Connection was successful and inkkeys was found. If we reach this point, we do not need to search on
                    # another port. We got disconnected or some other kind of error, so skip the rest of the port list and start
                    # over.
            time.sleep(5)

    t = threading.Thread(target=doConnect)
    #t.setDaemon(True)
    t.start()


def disconnected():
    if gui.connected:
        gui.setDisconnected()
        connectToDevice()

#### main
config = Config("./config.json")
gui = GUI()
gui.setExitCallback(endEverything)
winListener = WindowChangeListener(handleWindowChange)
winListener.runThreaded()

# Instantiate the device
device = Device()
device.debug = DEBUG
device.setDisconnectionCallback(disconnected)

connecting = False
connectToDevice() # runs in another thread

gui.work(config) # blocks
