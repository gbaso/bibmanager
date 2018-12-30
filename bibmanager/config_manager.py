# Copyright (c) 2018 Patricio Cubillos and contributors.
# bibmanager is open-source software under the MIT license (see LICENSE).

__all__ = ['reset']

import os
import shutil
import configparser
import textwrap
from pygments.styles import STYLE_MAP


# Set these as a unique constant in the pakage (in __init__?)
ROOT = os.path.dirname(os.path.realpath(__file__)) + '/'
HOME = os.path.expanduser("~") + "/.bibmanager/"

styles = textwrap.fill(", ".join(style for style in iter(STYLE_MAP)),
                       width=79, initial_indent="  ", subsequent_indent="  ")

def reset():
  """
  Reset the bibmanager configuration file.

  Simply, copy the default config file into bm.HOME/config,
  overwriting any pre-existing content.
  """
  shutil.copy(ROOT+'config', HOME+'config')


def set_key(key, value=None):
  """
  Set the value of a bibmanager config key.

  Parameters
  ----------
  key: String
     bibmanager config key to set.
  value: String
     Value to set for input key.
     If value is None, display the key's help information on the prompt.
  """
  config = configparser.ConfigParser()
  config.read(HOME+'config')
  if not config.has_option('BIBMANAGER', key):
      raise ValueError("'{:s}' is not a valid bibmanager config key."
                       "\nThe available keys are: {}".
                       format(key, config.options('BIBMANAGER')))

  # Set value:
  if value is not None:
      # Check for exceptions:
      if key == 'style' and value not in STYLE_MAP.keys():
          raise ValueError("'{:s}' is not a valid style option.  "
              "Available options are:\n{:s}".format(value, styles))
      # The code identifies invalid commands, but cannot assure that a
      # command actually applies to a text file.
      if key == 'text_editor' and shutil.which(value) is None:
          raise ValueError("'{:s}' is not a valid text editor.".format(value))

      config.set('BIBMANAGER', key, value)
      with open(HOME+'config', 'w') as configfile:
          config.write(configfile)
      return

  # Display helps (value is None):
  if key == 'style':
      print("The 'style' key sets the color-syntax style of displayed BibTeX "
            "entries.\nThe default style is 'autumn'.  "
            "The current style is '{:s}'.\n\n"
            "Available options are:\n{:s}\n"
            "See http://pygments.org/demo/6780986/ for a demo of the style "
            "options.".format(config.get('BIBMANAGER',key), styles))

  elif key == 'text_editor':
      print("The 'text_editor' key sets the text editor to use when editing "
            "the\nbibmanager manually (i.e., a call to: bibm edit).  By "
            "default, bibmanager\nuses the OS-default text editor.\n\n"
            "Typical text editors are: emacs, vim, gedit.\n"
            "To set the OS-default editor set text_editor to 'default'.\n"
            "Note that aliases defined in the .bash are not accessible.\n"
            "The current text editor is '{:s}'.".
            format(config.get('BIBMANAGER',key)))

  elif key == 'paper':
      print("The 'paper' key sets the default paper format for latex "
            "compilation outputs\n(not for pdflatex, which is automatic).  "
            "Typical options are 'letter'\n(e.g., for ApJ articles), or "
            "'A4' (e.g., for A&A).\n\nCurrent value is: '{:s}'.".
            format(config.get('BIBMANAGER',key)))

  elif key == 'adstoken':
      print("The 'adstoken' key sets the ADS token required for ADS requests.\n"
            "To obtain a token follow the two steps described here:\n"
            "  https://github.com/adsabs/adsabs-dev-api#access")

def get(key):
  """
  Get the value of a key in the bibmanager config file.

  Parameters
  ----------
  key: String
     The requested key.

  Returns
  -------
  value: String
     Value of the requested key.

  Examples
  --------
  >>> import config_manager as cm
  >>> cm.get('paper')
  'letter'
  >>> cm.get('style')
  'autumn'
  """
  config = configparser.ConfigParser()
  config.read(HOME+'config')
  if not config.has_option('BIBMANAGER', key):
      raise ValueError("No key '{:s}' in bibmanager config file."
                       "\nThe available keys are: {}".
                       format(key, config.options('BIBMANAGER')))
  return config.get('BIBMANAGER', key)


def display(key=None):
  """
  Display the value(s) of the bibmanager config file on the prompt.

  Parameters
  ----------
  key: String
     bibmanager config key to display.  Leave as None to display the
     values from all keys.

  Examples
  --------
  >>> import config_manager as cm
  >>> # Show all keys and values:
  >>> cm.display()
  bibmanager configuration file:
  KEY          VALUE
  -----------  -----
  style        autumn
  text_editor  default
  paper        letter
  adstoken     None

  >>> # Show an specific key:
  >>> cm.display('text_editor')
  text_editor: default
  """
  if key is not None:
      print("{:s}: {:s}".format(key, get(key)))
  else:
      config = configparser.ConfigParser()
      config.read(HOME+'config')
      print("\nbibmanager configuration file:"
            "\nKEY          VALUE"
            "\n-----------  -----")
      for key, value in config['BIBMANAGER'].items():
          print("{:11s}  {:s}".format(key, value))
