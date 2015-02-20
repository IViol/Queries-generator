#/usr/env/
#encoding = "utf-8"

import logging
from subprocess import Popen, PIPE
from re import sub

class TomitaParser(object):
  """Class for executing Tomita Parser and parsing it's output"""
  def __init__(self, filename, tomita_path):
    """TomitaParser instance initialization"""
    self.filename = filename
    self.binary = tomita_path
    self.facts = {}
  
  def run(self):
    """Executes tomitaparser process and receives it's output"""
    input_text = ""
    with open(self.filename) as f:
      for line in f:
        input_text += line

    input_text = sub(r'[^а-я\w\d\sё.]', ' ', input_text)
    input_text = sub(r'[\s\s+]', ' ', input_text)
    input_text = sub(' +', ' ', input_text)

    #getting tomita's config.proto file path
    parse_dir_path = self.filename[:self.filename.rfind('/')]
    tomita_config_path = parse_dir_path + '/../tomita/config.proto'
    
    logging.debug('Tomitaparser is to be launched with config "%s"' %
                 tomita_config_path)

    tomita_command = self.binary + " " + tomita_config_path
    p = Popen(tomita_command, stdin=PIPE, shell=True, stdout=PIPE, stderr=PIPE,
              universal_newlines=True)
    out, err = p.communicate(input=input_text)
    
    if p.returncode != 0:
      logging.error('Extracting from file "%s" was failed' % self.filename)
      raise Exception('Extracting from file "%s" was failed' % self.filename)
    
    text = out.split('\n')
    self.parse(text)
    
    logging.info('Extracting from file "%s" was successfully' % self.filename)
  
  def parse(self, text):
    """Parses of the tomita's output"""
    for line in text:
      if 'fact' in line or 'object' in line:
        length = len(line)
        pos = line.find('=') + 2

        if (pos == 1) and (pos >= length):
          logging.warning('Strange things have happened in the file "%s"' %
                          self.filename)
          continue

        fact = line[pos:].lower()
        self.add_fact(fact)
    
  def add_fact(self, fact):
    """Adds fact into the collection"""
    found = False
    for key in self.facts:
      if fact == key:
        found = True
        self.facts[fact] += 1

    if not found or not self.facts:
      self.facts[fact] = 1
  
  def get_facts(self):
    """Returns extracted facts"""
    return self.facts