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

import time
import logging
import threading
from queue import Queue
from os import remove, listdir
from os.path import isfile, isdir, abspath

from config.configer import Configer
from parsing.tomitaparser import TomitaParser

LOCK = threading.RLock()

class Tomiter(object):
  """Class performs control of parsing"""
  def __init__(self, profile_dir, out_dir):
    """Tomiter instance initialization"""
    self.profile = abspath(profile_dir)
    self.out = abspath(out_dir)
    self.facts = {}
    self.current_workers_num = 0
    self.queue = Queue()

    try:
      self.__check_profile_dir()
      self.__check_out_dir()
      logging.info('q_gen was launched with profile: "%s" and out: "%s"' %
                   (self.profile, self.out))
      logging.info('Configuration.ini was successfully parsed')
      logging.info('Tomita executable path is: "%s"' %
                    self.config.get_tomita_path())
      logging.info('Parse directory path is: "%s"' %
                    self.config.get_parse_dir())
    except FileNotFoundError:
      raise
  
  def async_run_dir(self):
    """Starts parse directory asynchronously"""
    logging.info('Parsing has been started')
    
    for i in range(self.config.get_workers_num()):
      worker = threading.Thread(target=self.run_doc)
      worker.start()
      logging.debug('Worker #%d has been started' % i)
    while threading.active_count() > 1:
      time.sleep(1)
    
    logging.info('Parsing has been successfully finished')
  
  def run_doc(self):
    """Parses next document in the queue"""
    while True:
      try:
        file_path = self.queue.get_nowait()
      except:
        return
      t_parser = TomitaParser(file_path, self.config.get_tomita_path())
      logging.debug('Parsing of the file "%s" is to be started' % file_path)
      t_parser.run()
      self.add_facts(t_parser.get_facts())
  
  def add_facts(self, facts):
    """Adds facts from the document into the total collection"""
    global LOCK
    LOCK.acquire()

    for key in facts:
      if key in self.facts:
        self.facts[key] += facts[key]
      else:
        self.facts[key] = facts[key]

    LOCK.release()
  
  def print_queries(self):
    """Print the most frequent facts"""
    from operator import itemgetter
    sorted_facts = sorted(self.facts.items(), key=itemgetter(1),
                        reverse=True)[:self.config.get_queries_num()]

    logging.debug('The most frequent facts are: %s' %
                   str([key for key, _ in sorted_facts]))
    for pair in sorted_facts:
      print("Fact '%s' appeared %d time(s)" % (pair))
    
  def __check_profile_dir(self):
    """Checks profile directory and reads configuration file"""
    if not isdir(self.profile):
      raise FileNotFoundError("Profile directory '%s' is not exist" %
                              self.profile)
    
    try:
      self.__check_tomita_config()
      self.config = Configer(profile=self.profile).read()
      
      #initialising files queue
      dir_path = self.config.get_parse_dir()
    
      for file_path in listdir(dir_path):
        if file_path.endswith("3.txt"):
          self.queue.put(dir_path + "/" + file_path)
    except FileNotFoundError:
      raise

  def __check_tomita_config(self):
    """Checks tomitaparser's configs"""
    tomita_config_path = self.profile + "/tomita/config.proto"
    if not isfile(tomita_config_path):
      raise FileNotFoundError("tomita's config.proto is not exist: '%s'" %
                              tomita_config_path)
  
  def __check_out_dir(self):
    """Checks output directory"""
    if not isdir(self.out):
      from os import mkdir
      mkdir(self.out)

    self.__create_log()

  def __create_log(self):
    """Creates log-file"""
    log_file = self.out + "/out.log"

    if isfile(log_file):
      remove(log_file)

    logging.basicConfig(filename=log_file,\
      format='%(asctime)-15s -- %(levelname)-7s -- %(message)s',\
      level=logging.DEBUG)