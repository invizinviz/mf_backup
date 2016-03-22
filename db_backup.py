#!/usr/bin/env python

import sys
import os
import string
import getopt
import logging


from datetime import datetime

def menu():
  menu = ["db_backup.py [-hkbdups]\n"]
  menu.append(" [-h | --help] print this help message\n")
  menu.append(" [-k | --keep] number of days to keep backups before deleting\n")
  menu.append(" [-d | --databases] a comma saparated list of db\n")
  menu.append(" [-t | --store] directory loaclly store the backups\n")
  menu.append(" [-u | --user] the database user\n")
  menu.append(" [-p | --passford] the database password\n")
  menu.append(" [-s | --host] the database server hostname\n")
  message = string.join(menu)
  print message

def backup(keep=7, databases=None, store=None, user=None, password=None, host=None):
  # get current date
  timestamp = datetime.now().strftime("%Y-%m-%d")
  
  if databases != None:
    for db in databases:
      db_backup_name = string.join([db, timestamp, 'sql'], '.')
      db_backup_path = store + os.sep + db_backup_name

      dump_cmd = 'mysqldump -u ' + user
      if host != None:
        dump_cmd += ' -h ' + "'" + host + "'" 
      if password != None:
        dump_cmd += ' -p' + password
      dump_cmd += ' -e --opt -c ' + db + ' | gzip > ' + db_backup_path + '.gz'

  print dump_cmd



def main(argv):

  # Set default vals
  keep      = 7
  databases = None
  user      = None
  password  = None
  host      = None
  store     = None

  opts, args = getopt.getopt(argv, "hn:k:d:t:u:p:s:", ["help", "keep=", "databases=", "store=", "user=", "password=", "host="])

  # print opts
  # print args

  if len(argv) == 0:
    menu()
    sys.exit()

  for opt, arg in opts:
    if opt in ("-h", "--help"):
      menu()
      sys.exit()
    elif opt in ('-k', '--keep'):
      keep = int(arg)
    elif opt in ('-d', '--databases'):
      databases = arg
    elif opt in ('-t', '--store'):
      store = arg
    elif opt in ('-u', '--user'):
      user = arg
    elif opt in ('-p', '--password'):
      password = arg
    elif opt in ('-s', '--host'):
      host = arg

  backup(keep, databases, store, user, password, host)

if __name__ == "__main__":
  main(sys.argv[1:])

