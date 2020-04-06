import json
import logging
from PyQt5.QtGui import QColor

log = logging.Logger('pyf3os.config_read')

DEFAULT_CONFIG = {
  "fullscreen": False,
  "width": 1024,
  "height": 768,
  "fontsize": 14,
  "fontfamily": "Courier New",
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
    "directory_header": ["-----------Dirrectories-----------"],
    "directory_corrupted": ["Uszkodzony katalog..."],
    "directory_missing": ["Brak podanego katalogu..."],
    "unknown_command": ["Nieznane polecenie. Wpisz help, aby uzyskac liste polecen."],
    "file_corrupted": ["Brak lub uszkodzony plik"],
    "missing_help_text": ["Brak tekstu do pomocy..."],
    "access_denied": ["Brak dostepu..."],
    "app_header": [
      "# F3OS ZEAP (C)2073                              #",
      "# TERMINAL #1; NETWORK: ZSP_LOCAL; USER: UNKNOWN #",
      "##################################################"],
    "help": [
      "Lista polecen:",
      "cd nazwa_katalogu - zmienia obecny katalog na wybrany",
      "cd .. - zmien katalog na nadrzedny ",
      "open nazwa_pliku - otwiera plik w trybie odczytu",
      "bypass nazwa_pliku - ominiecie zabezpieczenia",
    ]
  },
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

  def get(self, key, alternative=None):
    return self._config.get(key, alternative)

  def set(self, key, value):
    if key == "commands":
      return False

    self._config[key] = value
    return True

  def get_text(self, key, alternative="Missing texts in config..."):
    return self._config.get('texts', {}).get(key, alternative)