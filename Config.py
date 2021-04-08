import json
import pprint
from pathlib import Path


class Config:
  def __init__(self,config_file):
    self.config_file = config_file
    self.config = self.__loadConfig()

  def __loadConfig(self):
    my_file = Path(self.config_file)
    if my_file.is_file():
      with open(self.config_file) as json_file:
        config = json.load(json_file)
    else:
      config = self.initConfig()
      self.saveConfig(config)
    print("Config loaded . . .")
    #pprint.pprint(config)
    #print("-------------------")
    return config

  def __initConfig(self):
    newConfig = {
      'first': 'aaabbbbxx',
      'second': 'like horses',
      'third': True
    }
    print("Config initialized . . .")
    #pprint.pprint(newConfig)
    #print("-------------------")
    return newConfig

  def saveConfig(self):
    with open(self.config_file, 'w') as json_file:
      json.dump(self.config, json_file)
    print ("Config saved . . .")
    #pprint.pprint(newConfig)
    #print("-------------------")
    return

  def reLoadConfig(self):
    self.config = self.__loadConfig()