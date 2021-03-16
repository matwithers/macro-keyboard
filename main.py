
VID = 0x1b4f      #USB Vendor ID for a Pro Micro
PID = 0x9206      #USB Product ID for a Pro Micro

DEBUG = True

from inkkeys import *        #Inkkeys module
from modes import *  

import PySimpleGUIWx as sg
import PySimpleGUI as psg
import json
from pathlib import Path
import pprint
import os

from serial import SerialException  #Serial functions
import serial.tools.list_ports      #Function to iterate over serial ports
import traceback                    #Print tracebacks if an error is thrown and caught

import win32process
import win32api
import win32con

import ctypes
import ctypes.wintypes
import threading

config_file = "./config.json"

def loadConfig():
  my_file = Path(config_file)
  if my_file.is_file():
    with open(config_file) as json_file:
      config = json.load(json_file)
  else:
    config = initConfig()
    saveConfig(config)
  print("Config loaded . . .")
  pprint.pprint(config)
  print("-------------------")
  return config

def saveConfig(newConfig):
  with open(config_file, 'w') as json_file:
    json.dump(newConfig, json_file)
  print ("Config saved . . .")
  pprint.pprint(newConfig)
  print("-------------------")
  return

def initConfig():

  newConfig = {
    'first': 'aaabbbbxx',
    'second': 'like horses',
    'third': True
  }

  print("Config initialized . . .")
  pprint.pprint(newConfig)
  print("-------------------")
  return newConfig

def settingsWindow(config):
    # All the stuff inside your window.
    # settingsLayout = [
    #   [sg.Text('First setting'), sg.InputText(key='first', default_text=config['first'])],
    #   [sg.Text('Second setting'), sg.InputCombo(('like biscuits', 'like horses'), size=(20, 1), key='second', default_value=config['second'])],
    #   [sg.Checkbox('Checkbox!!!', default=config['third'], key='third')],
    #   [sg.Button('Ok'), sg.Button('Cancel')]
    # ]    
    # Column layout      
    col = [[psg.Text('col Row 1')],
           [psg.Text('col Row 2'),psg.Input('col input 1')],
           [psg.Text('col Row 3'), psg.Input('col input 2')]]

    settingsLayout = [
      [
        psg.Listbox(values=('Code.exe', 'thunderbird.exe', 'msedge.exe', 'Discord.exe', 'WhatsApp.exe'), select_mode=psg.LISTBOX_SELECT_MODE_SINGLE , size=(20,20), enable_events=True, key='_APPLICATION_'),
        psg.Column(col)
      ],
      [
        psg.Button('Ok'),
        psg.Button('Cancel')
      ]
    ]

    #open window
    settingsWindow = psg.Window('Macro Keyboard Settings', settingsLayout)    

    loop = True
    while loop:
      # read from window on event
      settingsEvent, newConfig = settingsWindow.read()    

      pprint.pprint(settingsEvent)

      if settingsEvent == '_APPLICATION_':
        print(newConfig)

      if settingsEvent == psg.WIN_CLOSED or settingsEvent == 'Cancel':
        loop = False
        settingsWindow.close()
      if settingsEvent == 'Ok':
        loop = False
        saveConfig(newConfig)
        settingsWindow.close()



# called when window change event occurs
def handleWindowChange(exePath):
  if exePath in config["applications"]:
    pprint.pprint(config["applications"][exePath])
    mode = ModeApplication()
    mode.activate(device, exePath, config["applications"][exePath])
  else:
    print("Application not recognized")

# main handler to trigger changes to current active window
# largely copied from:
# https://github.com/Danesprite/windows-fun
def windowChangeEventListener():

  # Look here for DWORD event constants:
  # http://stackoverflow.com/questions/15927262/convert-dword-event-constant-from-wineventproc-to-name-in-c-sharp
  # Don't worry, they work for python too.

  WINEVENT_OUTOFCONTEXT = 0x0000
  EVENT_SYSTEM_FOREGROUND = 0x0003
  WINEVENT_SKIPOWNPROCESS = 0x0002

  user32 = ctypes.windll.user32
  ole32 = ctypes.windll.ole32

  WinEventProcType = ctypes.WINFUNCTYPE(
    None,
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.HWND,
    ctypes.wintypes.LONG,
    ctypes.wintypes.LONG,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.DWORD
  )

  def callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION|win32con.PROCESS_VM_READ,0,pid)
    #exePath = win32process.GetModuleFileNameEx(handle, 0)
    head, exePath = os.path.split(win32process.GetModuleFileNameEx(handle, 0))
    handleWindowChange(exePath)

  WinEventProc = WinEventProcType(callback)

  user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
  hook = user32.SetWinEventHook(
    EVENT_SYSTEM_FOREGROUND,
    EVENT_SYSTEM_FOREGROUND,
    0,
    WinEventProc,
    0,
    0,
    WINEVENT_OUTOFCONTEXT | WINEVENT_SKIPOWNPROCESS
  )

  if hook == 0:
    print('SetWinEventHook failed')
    exit(1)

  msg = ctypes.wintypes.MSG()
  while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
    #user32.TranslateMessageW(msg)
    user32.DispatchMessageW(msg)

  # Stopped receiving events, so clear up the winevent hook and uninitialise.
  print('Stopped receiving new window change events. Exiting...')
  user32.UnhookWinEvent(hook)
  ole32.CoUninitialize()

def work():
  # Start the 'run' method in a daemonized thread.
  t = threading.Thread(target=windowChangeEventListener)
  t.setDaemon(True)
  t.start()

  # Event Loop to process "events"
  while True:
    menu_item = tray.read()
    print(menu_item)
    if menu_item == 'Exit':
      tray.close()
      break
    elif menu_item == 'Settings':
      settingsWindow(config)
      config = loadConfig()
      print("settings done")

#Try connecting on the given port and work with it.
#Will return false if connection fails or an unknown device is present.
#If it succeeds, it will enter the main working loop forever. It will only return if an error occurs and return True to report that it was working with the correct device.
def tryUsingPort(port):
  try:
    if device.connect(port):
      work()  #Success, enter main loop
      device.disconnect()
      return True
  except SerialException as e:
    print("Serial error: ", e)
  except:
    #Something entirely unexpected happened. We will catch it nevertheless, so the device keeps working as this process will probably run in the background unsupervised. But we need to print a proper stacktrace, so we can debug the problem.
    if DEBUG:
      print(traceback.format_exc())
      print("Error: ", sys.exc_info()[0])
  return False

#### main 

sg.theme('LightGrey1')
psg.theme('LightGrey1')
config = loadConfig()

# simple tray icon and menu
menu_def = ['BLANK', ['&Settings', '---','E&xit']]
tray = sg.SystemTray(menu=menu_def, filename=r'default_icon.ico')

# Instantiate the device
device = Device()
device.debug = DEBUG

for port in serial.tools.list_ports.comports(): #Iterate over all serial ports
  if port.vid != VID or port.pid != PID:
    continue                                #Skip if vendor or product ID do not match
  if tryUsingPort(port.device):             #Try connecting to this device
    break                                   #Connection was successful and inkkeys was found. If we reach this point, we do not need to search on another port. We got disconnected or some other kind of error, so skip the rest of the port list and start over.


