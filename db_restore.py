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
  menu.append(" [-s | --host] the database server hostname\n")
  menu.append(" [-t | --store] directory stored backups\n")
  menu.append(" [-u | --user] the database user\n")
  menu.append(" [-p | --passford] the database password\n")
  message = string.join(menu)
  print message

def main(argv):
  # set default vals
  databases = None
  store = None
  user = 'backup'
  password = None
  host = None

  # set logging configs
  logging.basicConfig(filename='restore.log', level=logging.DEBUG)

  opts, args = getopt.getopt(argv, 'hd:s:t:u:p:', ['help', 'databases=', 'host=', 'user=', 'store=', 'password='])

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
    elif opt in ('-s', '--host'):
      host = arg
    elif opt in ('-t', '--store'):
      store = arg
    elif opt in ('-u', '--user'):
      user = arg
    elif opt in ('-p', '--password'):
      password = arg

  print password

if __name__ == '__main__':
  main(sys.argv[1:])

