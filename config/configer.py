#/usr/env/
#encoding = "utf-8"

############################################################
from sys import version_info
if version_info.major == 3:
  if version_info.minor < 3:
    FileNotFoundError = Exception
else:
  raise Exception("Please update your python to 3+ version")
############################################################

from configparser import ConfigParser
from os.path import isfile, isdir, abspath

class Configer(object):
  """Class for configuration file's management"""
  def __init__(self, profile=""):
    """Configer instance initialization"""
    if len(profile) > 0:
      if not isdir(abspath(profile)):
        raise FileNotFoundError(
          "Cannot find specified profile directory: '%s'" %
          abspath(profile))

      self.profile_path = abspath(profile)
      
      #getting config file path
      self.config_path = profile + "/Configuration.ini"

      if not isfile(self.config_path):
        raise FileNotFoundError(
          "Cannot find configuration file in profile directory: '%s'" %
          self.config_path)

    self.config = ConfigParser()

  def read(self):
    """Reads configuration file"""
    try:
      self.config.read(self.config_path)
    except:
      print("Some error during reading of the configuration file")

    try:
      self.check_tomita_binary()
      self.check_parse_dir()
      return self
    except FileNotFoundError:
      raise

  def check_tomita_binary(self):
    """Checks tomitaparser executable"""
    if not isfile(self.get_tomita_path()):
      raise FileNotFoundError(
        "Cannot find specified tomita binary file: '%s'" %
        self.get_tomita_path())
    
  def check_parse_dir(self):
    """Checks directory which contain documents to parse"""
    self.parse_dir = self.config['GLOBAL']['parse_dir']
    if not len(self.parse_dir):
      self.parse_dir = self.profile_path + '/parse'

    if not isdir(self.parse_dir):
      raise FileNotFoundError(
        "Cannot find directory to parse documents: '%s'" % self.parse_dir)
    
  def get_workers_num(self):
    """Returns number of workers"""
    return self.config.getint('GLOBAL', 'workers_num')
  
  def get_queries_num(self):
    """Returns number of queries to print"""
    return self.config.getint('GLOBAL', 'queries_num')
    
  def get_parse_dir(self):
    """Returns path to parse directory"""
    return self.parse_dir
    
  def get_tomita_path(self):
    """Returns path to tomitaparser executable"""
    return self.config['TOMITA']['tomita_path']
    
  
  