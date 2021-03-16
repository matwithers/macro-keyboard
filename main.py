import PySimpleGUIWx as sg
import json
from pathlib import Path
import pprint

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
  newConfig = {'first': 'aaabbbbxx', 'second': 'like horses', 'third': True}
  print("Config initialized . . .")
  pprint.pprint(newConfig)
  print("-------------------")
  return newConfig

def settingsWindow(config):
    # All the stuff inside your window.
    settingsLayout = [
      [sg.Text('First setting'), sg.InputText(key='first', default_text=config['first'])],
      [sg.Text('Second setting'), sg.InputCombo(('like biscuits', 'like horses'), size=(20, 1), key='second', default_value=config['second'])],
      [sg.Checkbox('Checkbox!!!', default=config['third'], key='third')],
      [sg.Button('Ok'), sg.Button('Cancel')]
    ]    

    #open window
    settingsWindow = sg.Window('Macro Keyboard Settings', settingsLayout)    

    # read from window on event
    settingsEvent, newConfig = settingsWindow.read()    

    if settingsEvent == sg.WIN_CLOSED or settingsEvent == 'Cancel':
        settingsWindow.close()
    if settingsEvent == 'Ok':
        saveConfig(newConfig)
        settingsWindow.close()

# called when window change event occurs
def handleWindowChange(exePath):
  print(exePath)

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
    exePath = win32process.GetModuleFileNameEx(handle, 0)
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

#### main 

sg.theme('LightGrey1')
config = loadConfig()

# simple tray icon and menu
menu_def = ['BLANK', ['&Settings', '---','E&xit']]
tray = sg.SystemTray(menu=menu_def, filename=r'default_icon.ico')

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
