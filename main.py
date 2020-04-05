from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QTextEdit, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from config_reader import ConfigReader


class TerminalWindow:

  def __init__(self, config: ConfigReader):
    self.default_commands = {
      'change_directory': {'func': self.change_directory, 'args_num': 1},
      'show_directory': {'func': self.show_dir},
      'read_file': {'func': self.read_file, 'args_num': 1},
      'hack_file': {'func': self.hack_file, 'args_num': 1},
      'exit_file': {'func': self.exit_file},
      'exit_app': {'func': self.exit_app},
      'show_help': {'func': self.help_cmd},
    }
    self.app = QApplication([])
    self.config = config
    self.palette = QPalette()
    self.current_path = self.config.get('working_path')
    self.set_palette()
    self.create_view()
    self.actions = self.load_commands()

  def show(self):
    self.app.exec_()

  def set_palette(self):
    self.palette.setColor(QPalette.Background, self.config.get('bgcolor'))
    self.palette.setColor(QPalette.Foreground, self.config.get('color'))
    self.palette.setColor(QPalette.Active, QPalette.Text, self.config.get('color'))
    self.palette.setColor(QPalette.Active, QPalette.Base, self.config.get('bgcolor'))

  def create_view(self):
    self.window = QWidget()
    self.window.setGeometry(0, 0, self.config.get('width'), self.config.get('height'))
    self.create_command_line()
    self.create_text_area()
    self.layout = QVBoxLayout()

    self.layout.addWidget(self.text_area)
    self.layout.addLayout(self.horizont_layout)
    self.window.setLayout(self.layout)
    self.window.setPalette(self.palette)
    self.window.show()

  def create_command_line(self):
    self.horizont_layout = QHBoxLayout()
    self.horizont_layout.setContentsMargins(0, 0, 0, 0)
    self.placeholder = QLineEdit()
    self.placeholder.setFixedWidth(25)
    self.placeholder.setStyleSheet('border: false; background: black; color: green;')
    self.placeholder.setText('>>')
    self.placeholder.setFocusPolicy(Qt.NoFocus)

    self.command_line = QLineEdit()
    self.command_line.setStyleSheet('border: false; background: black; color: green;')
    self.command_line.returnPressed.connect(self.cmd_handler)

    self.horizont_layout.addWidget(self.placeholder)
    self.horizont_layout.addWidget(self.command_line)

  def create_text_area(self):
    self.text_area = QTextEdit()
    self.text_area.setFocusPolicy(Qt.NoFocus)
    self.text_area.setStyleSheet('border: false; background: black; color: green;')
    self.text_area.append("some example text")

  def show_on_screen(self, txts):
    self.text_area.clear()
    for txt in txts:
      self.text_area.append(txt)

  def cmd_handler(self):
    cmd = self.command_line.text().split(' ')
    self.command_line.clear()
    if cmd[0] in self.actions:
      call_func = self.actions[cmd[0]]
      if 'args_num' in call_func:
        call_func['func'](*cmd[1:call_func['args_num']+1])
      else:
        call_func['func']()
    else:
      self.unknown_cmd()

  def load_commands(self):
    output = {}
    new_cmds_map = self.config.get('commands')
    default_cmds = set(self.default_commands.keys())
    loaded_cmds = set(new_cmds_map.values())
    new_cmds = list(new_cmds_map.keys())
    new_cmds += list(default_cmds ^ loaded_cmds)

    for cmd in new_cmds_map:
      output[cmd] = self.default_commands.get(new_cmds_map[cmd], {'func': self.unknown_cmd})

    return output

  def unknown_cmd(self):
    self.show_on_screen(["Nieznane polecenie"])

  def help_cmd(self):
    self.show_on_screen(self.config.get('help_text', self.config.get_text('missing_help_text')))

  def change_directory(self):
    pass

  def read_file(self, filename):
    try:
      with open(self.current_path + filename) as file:
        lines = file.readlines()
        parsed_txt = []
        if 'hack_lvl' in lines[0]:
          start_position = lines.index("<-<without_hack>->")
          if not start_position:
            parsed_txt = self.config.get_text("access_denied")
          else:
            parsed_txt = lines[start_position+1:]
        else:
          parsed_txt = lines
        self.show_on_screen(parsed_txt)
    except FileNotFoundError:
      self.show_on_screen(self.config.get_text("file_corrupted"))

  def hack_file(self):
    pass

  def exit_file(self):
    pass

  def show_help(self):
    pass

  def exit_app(self):
    self.app.quit()

  def show_dir(self):
    try:
      with open(self.current_path + "dirfile", 'r', encoding='utf-8') as file:
        lines = file.readlines()
        dirs = [line.strip() for line in lines if line.startswith("> ")]
        dirs.sort()
        files = [line.strip() for line in lines if not line.startswith("> ")]
        files.sort()
        self.show_on_screen(self.config.get_text("directory_header") + dirs + files)
    except FileNotFoundError:
      self.show_on_screen(self.config.get_text("directory_corrupted"))


if __name__ == '__main__':
  config_reader = ConfigReader()
  app = TerminalWindow(config_reader)
  app.show()
