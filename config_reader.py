import json
import logging
from PyQt5.QtGui import QColor

log = logging.Logger('pyf3os.config_read')

DEFAULT_CONFIG = {
  "fullscreen": False,
  "width": 1024,
  "height": 768,
  "bgcolor": "#000000",
  "color": "#00ff00",
  "working_path": "f:\\zakon\\f3os\\",
  "commands": {
    "cd": "change_directory",
    "dir": "show_directory",
    "open": "read_file",
    "bypass": "hack_file",
    "exit": "exit_file",
    "exitFromThisHell": "exit_app",
    "help": "show_help"
  },
  "texts": {
    "directory_header": ["______Dirrectory_______"],
    "directory_corrupted": ["Uszkodzony katalog..."],
    "unknown_command": ["Nieznane polecenie. Wpisz help, aby uzyskac liste polecen."],
    "file_corrupted": ["Brak lub uszkodzony plik"],
    "missing_help_text": ["Brak tekstu do pomocy..."],
    "access_denied": ["Brak dostepu..."]
  }
}


class ConfigReader:

  def __init__(self, filename='config.json'):
    self._config = DEFAULT_CONFIG
    self.read_config(filename)

  def read_config(self, filename):
    try:
      file = open(filename, 'rb')
      self._config = json.load(file)
    except FileNotFoundError:
      log.info('File %s not found, using default config.' % filename)

    for key in self._config.keys():
      if 'color' in key:
        self._config[key] = QColor(self._config[key])

  def get_config(self):
    return self._config

  def get(self, key):
    return self._config[key]

  def set(self, key, value):
    if key == "commands":
      return False

    self._config[key] = value
    return True

  def get_text(self, key):
    return self._config.get('texts', {}).get(key, "Missing texts in config...")