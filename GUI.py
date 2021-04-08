import pprint

import PySimpleGUI as psg
import PySimpleGUIWx as sg

import os

class GUI:
  def __init__(self):
    sg.theme('LightGrey1')
    psg.theme('LightGrey1')
    self.connected = False;

    # simple tray icon and menu
    self.menu_def = ['BLANK', ['!Disconnected', '&Settings', '---', 'E&xit']]
    self.tray = sg.SystemTray(menu=self.menu_def, filename=r'default_icon.ico')

  def setConnected(self):
    self.connected=True;
    self.menu_def = ['BLANK', ['!Connected', '&Settings', '---', 'E&xit']]
    self.tray.update(menu=self.menu_def)

  def setDisconnected(self):
    self.connected = False;
    self.menu_def = ['BLANK', ['!Disconnected', '&Settings', '---', 'E&xit']]
    self.tray.update(menu=self.menu_def)


  def work(self,config):
    # Event Loop to process "events"
    while True:
      menu_item = self.tray.read()
      print(menu_item)
      if menu_item == 'Exit':
        self.tray.close()
        self.exitCallback()
        break
      elif menu_item == 'Settings':
        self.settingsWindow(config)
        config.reLoadConfig()

        print("settings done")

  def updateForm(self, appConfig, exePath, settingsWindow):
    # print(newConfig)
    # print(appConfig)
    settingsWindow.Element('application_exe').Update(exePath)
    settingsWindow.Element('button1_icon').Update(appConfig['button1']['icon'])
    settingsWindow.Element('button1_data').Update(appConfig['button1']['data'])
    settingsWindow.Element('button2_icon').Update(appConfig['button2']['icon'])
    settingsWindow.Element('button2_data').Update(appConfig['button2']['data'])
    settingsWindow.Element('button3_icon').Update(appConfig['button3']['icon'])
    settingsWindow.Element('button3_data').Update(appConfig['button3']['data'])
    settingsWindow.Element('button4_icon').Update(appConfig['button4']['icon'])
    settingsWindow.Element('button4_data').Update(appConfig['button4']['data'])
    settingsWindow.Element('button5_icon').Update(appConfig['button5']['icon'])
    settingsWindow.Element('button5_data').Update(appConfig['button5']['data'])
    settingsWindow.Element('button6_icon').Update(appConfig['button6']['icon'])
    settingsWindow.Element('button6_data').Update(appConfig['button6']['data'])
    settingsWindow.Element('button7_icon').Update(appConfig['button7']['icon'])
    settingsWindow.Element('button7_data').Update(appConfig['button7']['data'])
    settingsWindow.Element('button8_icon').Update(appConfig['button8']['icon'])
    settingsWindow.Element('button8_data').Update(appConfig['button8']['data'])
    settingsWindow.Element('dial_left_data').Update(appConfig['dial_left']['data'])
    settingsWindow.Element('dial_right_data').Update(appConfig['dial_right']['data'])

  def settingsWindow(self, config):
    # All the stuff inside your window.
    # settingsLayout = [
    #   [sg.Text('First setting'), sg.InputText(key='first', default_text=config['first'])],
    #   [sg.Text('Second setting'), sg.InputCombo(('like biscuits', 'like horses'), size=(20, 1), key='second', default_value=config['second'])],
    #   [sg.Checkbox('Checkbox!!!', default=config['third'], key='third')],
    #   [sg.Button('Ok'), sg.Button('Cancel')]
    # ]
    icons = os.listdir('icons/.')
    apps = ('Code.exe', 'thunderbird.exe', 'msedge.exe', 'Discord.exe', 'WhatsApp.exe')
    firstAppConfig = config.config["applications"][apps[0]]

    # Column layout
    col = [
      [psg.Text('Application'), psg.Input(key='application_exe', default_text=apps[0])],
      [
        psg.Text('Button 1'),
        psg.Combo(icons, size=(20, 20), key='button1_icon', default_value=firstAppConfig['button1']['icon']),
        psg.Input(key='button1_data', size=(15, 1), default_text=firstAppConfig['button1']['data']),
        psg.Input(key='button5_data', size=(15, 1), default_text=firstAppConfig['button5']['data']),
        psg.Combo(icons, size=(20, 20), key='button5_icon', default_value=firstAppConfig['button5']['icon']),
        psg.Text('Button 5')
      ], [
        psg.Text('Button 2'),
        psg.Combo(icons, size=(20, 20), key='button2_icon', default_value=firstAppConfig['button2']['icon']),
        psg.Input(key='button2_data', size=(15, 1), default_text=firstAppConfig['button2']['data']),
        psg.Input(key='button6_data', size=(15, 1), default_text=firstAppConfig['button6']['data']),
        psg.Combo(icons, size=(20, 20), key='button6_icon', default_value=firstAppConfig['button6']['icon']),
        psg.Text('Button 6')
      ], [
        psg.Text('Button 3'),
        psg.Combo(icons, size=(20, 20), key='button3_icon', default_value=firstAppConfig['button3']['icon']),
        psg.Input(key='button3_data', size=(15, 1), default_text=firstAppConfig['button3']['data']),
        psg.Input(key='button7_data', size=(15, 1), default_text=firstAppConfig['button7']['data']),
        psg.Combo(icons, size=(20, 20), key='button7_icon', default_value=firstAppConfig['button7']['icon']),
        psg.Text('Button 7')
      ], [
        psg.Text('Button 4'),
        psg.Combo(icons, size=(20, 20), key='button4_icon', default_value=firstAppConfig['button4']['icon']),
        psg.Input(key='button4_data', size=(15, 1), default_text=firstAppConfig['button4']['data']),
        psg.Input(key='button8_data', size=(15, 1), default_text=firstAppConfig['button8']['data']),
        psg.Combo(icons, size=(20, 20), key='button8_icon', default_value=firstAppConfig['button8']['icon']),
        psg.Text('Button 8')
      ],
      [
        psg.Text('Wheel ACW'),
        psg.Input(key='dial_left_data', size=(15, 1), default_text=firstAppConfig['dial_left']['data']),
        psg.Input(key='dial_right_data', size=(15, 1), default_text=firstAppConfig['dial_right']['data']),
        psg.Text('Wheel CW')
      ],
      [
        psg.Button('Save')
      ]
    ]

    settingsLayout = [
        [
            psg.Listbox(apps,
                        select_mode=psg.LISTBOX_SELECT_MODE_SINGLE, size=(20, 20), enable_events=True,
                        key='_APPLICATION_',
                        default_values=apps[0]),
            psg.Column(col)
        ],
        [
          psg.Button('New', button_color=('white', 'green')),
          psg.Button('Delete', button_color=('white', 'red'))
        ],
        [
            psg.Button('Close')

        ]
    ]

    # open window
    settingsWindow = psg.Window('Macro Keyboard Settings', settingsLayout)

    loop = True
    while loop:
        # read from window on event
        settingsEvent, newConfig = settingsWindow.read()

        pprint.pprint(settingsEvent)

        if settingsEvent == '_APPLICATION_':
            applicationExe = newConfig['_APPLICATION_'][0]
            print("Settings:  " + applicationExe + " selected . . . ") 
            self.updateForm(config.config["applications"][applicationExe], applicationExe, settingsWindow)
        if settingsEvent == psg.WIN_CLOSED or settingsEvent == 'Close':
            loop = False
            settingsWindow.close()
        if settingsEvent == 'Save':
            #pprint.pprint(newConfig)
            newAppConfig = {
              "button1": {
                "icon": newConfig["button1_icon"],
                "mode": "keystroke",
                "data": newConfig["button1_data"]
              },
              "button2": {
                "icon": newConfig["button2_icon"],
                "mode": "keystroke",
                "data": newConfig["button2_data"]
              },
              "button3": {
                "icon": newConfig["button3_icon"],
                "mode": "keystroke",
                "data": newConfig["button3_data"]
              },
              "button4": {
                "icon": newConfig["button4_icon"],
                "mode": "keystroke",
                "data": newConfig["button4_data"]
              },
              "button5": {
                "icon": newConfig["button5_icon"],
                "mode": "keystroke",
                "data": newConfig["button5_data"]
              },
              "button6": {
                "icon": newConfig["button6_icon"],
                "mode": "keystroke",
                "data": newConfig["button6_data"]
              },
              "button7": {
                "icon": newConfig["button7_icon"],
                "mode": "keystroke",
                "data": newConfig["button7_data"]
              },
              "button8": {
                "icon": newConfig["button8_icon"],
                "mode": "keystroke",
                "data": newConfig["button8_data"]
              },
              "dial_right": {
                "mode": "keystroke",
                "data": newConfig["dial_right_data"]
              },
              "dial_left": {
                "mode": "keystroke",
                "data": newConfig["dial_left_data"]
              }
            }
            config.config["applications"][newConfig["application_exe"]] = newAppConfig
            config.saveConfig()

  def setExitCallback(self, exitCallback):
      self.exitCallback = exitCallback
