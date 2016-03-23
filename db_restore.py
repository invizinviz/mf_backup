#!/usr/bin/env python

import sys
import os
import string
import getopt
import logging
import datetime

def menu():
  menu = ["db_restore.py [-hdtups]\n"]
  menu.append(" [-h | --help] print this help message\n")
  menu.append(" [-d | --databases] a comma saparated list of db\n")
  menu.append(" [-y | --day] date of day restore (year-month-day 2016-03-28)\n")
  menu.append(" [-s | --host] the database server hostname\n")
  menu.append(" [-t | --store] directory stored backups\n")
  menu.append(" [-u | --user] the database user\n")
  menu.append(" [-p | --passford] the database password\n")
  message = string.join(menu)
  print message

def restore(databases=None, restore_day=None, store=None, user=None, password=None, host=None):
  for db_name in databases:
    restore_cmd = 'zcat ' + store + os.sep + db_name + '.' + restore_day + '.sql.gz' + ' | ' + 'mysql -u ' + user + ' -p' + password + ' -h ' + "'" + host + "'" + ' ' + db_name

    print restore_cmd

def main(argv):
  # set default vals
  databases = None
  store = None
  user = 'backup'
  password = None
  host = None

  # set logging configs
  logging.basicConfig(filename='restore.log', level=logging.DEBUG)

  opts, args = getopt.getopt(argv, 'hd:y:s:t:u:p:', ['help', 'databases=', 'day=', 'host=', 'user=', 'store=', 'password='])

  if len(argv) == 0:
    menu()
    sys.exit()

  for opt, arg in opts:
    if opt in ('-h', '--help'):
      menu()
      sys.exit()
    elif opt in ('-d', '--databases'):
      # convert in list
      databases = string.split(arg, ',')
    elif opt in ('-y', '--day'):
      restore_day = arg
    elif opt in ('-s', '--host'):
      host = arg
    elif opt in ('-t', '--store'):
      store = arg
    elif opt in ('-u', '--user'):
      user = arg
    elif opt in ('-p', '--password'):
      password = arg

  # try:
  #   restore(databases, restore_day, store, user, password, host)
  # except(Exception):
  #   logging.exception('Restore failed!!!\n')
  
  restore(databases, restore_day, store, user, password, host)

if __name__ == '__main__':
  main(sys.argv[1:])

