import pprint

import PySimpleGUI as psg
import PySimpleGUIWx as sg


class GUI:
  def __init__(self):
    sg.theme('LightGrey1')
    psg.theme('LightGrey1')

    # simple tray icon and menu
    menu_def = ['BLANK', ['&Settings', '---', 'E&xit']]
    self.tray = sg.SystemTray(menu=menu_def, filename=r'default_icon.ico')

  def work(self,config):
    # Event Loop to process "events"
    while True:
      menu_item = self.tray.read()
      print(menu_item)
      if menu_item == 'Exit':
        self.tray.close()
        break
      elif menu_item == 'Settings':
        self.settingsWindow(config)
        config.reLoadConfig()
        print("settings done")

  def settingsWindow(self,config):
    # All the stuff inside your window.
    # settingsLayout = [
    #   [sg.Text('First setting'), sg.InputText(key='first', default_text=config['first'])],
    #   [sg.Text('Second setting'), sg.InputCombo(('like biscuits', 'like horses'), size=(20, 1), key='second', default_value=config['second'])],
    #   [sg.Checkbox('Checkbox!!!', default=config['third'], key='third')],
    #   [sg.Button('Ok'), sg.Button('Cancel')]
    # ]
    # Column layout
    col = [[psg.Text('col Row 1')],
           [psg.Text('col Row 2'), psg.Input('col input 1')],
           [psg.Text('col Row 3'), psg.Input('col input 2')]]

    settingsLayout = [
        [
            psg.Listbox(values=('Code.exe', 'thunderbird.exe', 'msedge.exe', 'Discord.exe', 'WhatsApp.exe'),
                        select_mode=psg.LISTBOX_SELECT_MODE_SINGLE, size=(20, 20), enable_events=True,
                        key='_APPLICATION_'),
            psg.Column(col)
        ],
        [
            psg.Button('Ok'),
            psg.Button('Cancel')
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
            print(newConfig)

        if settingsEvent == psg.WIN_CLOSED or settingsEvent == 'Cancel':
            loop = False
            settingsWindow.close()
        if settingsEvent == 'Ok':
            loop = False
            config.saveConfig(newConfig)
            settingsWindow.close()