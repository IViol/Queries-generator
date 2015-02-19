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

import traceback
from os import mkdir
from os.path import isdir
from sys import argv
from parsing.tomiter import Tomiter

def main():
  """Entry point of the application"""
  argc = len(argv)

  profile_dir = ""
  out_dir = ""
  
  if argc < 2 or argc > 3 or (argv[1] == '-h' or argv[1] == '--help'):
    print(usage())
  elif argc == 2:
    profile_dir = argv[1]
    try:
      out_dir = make_default_out(profile_dir)
    except Exception as e:
      print(e)
      #print(traceback.format_exc())
      return 1
  else:
    profile_dir = argv[1]
    out_dir = argv[2]

  try:
    m_tomiter = Tomiter(profile_dir, out_dir)
    m_tomiter.async_run_dir()
    m_tomiter.print_queries()
  except (Exception, FileNotFoundError) as err:
    print(err)
    print(traceback.format_exc())

def usage():
  """Returns help string about usage of the application"""
  return """Usage: python q_gen.py <profile> <output_dir>
<profile>    - profile directory which contains configuration files
<output_dir> - output directory, which contains log file"""

def make_default_out(profile_path):
  """Makes default output directory if one is absent and returns it's path"""
  out_path = profile_path + "/out"
  try:
    if isdir(out_path):
      from shutil import rmtree
      rmtree(out_path)
    
    mkdir(out_path)
  except (Exception, OSError) as err:
    raise Exception("Cannot delete/create output directory", err.strerror)
  
  return out_path

if __name__ == '__main__':
  main()
