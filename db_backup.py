#!/usr/bin/env python

import sys
import os
import string
import getopt

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

def main(argv):

  # Set default vals
  keep = 7
  databases = None
  user = None
  password = None
  host = None
  store = None

  opts, args = getopt.getopt(argv, "hn:k:d:t:u:p:s:", ["help", "keep=", "databases=", "store=", "user=", "password=", "host="])

  print opts
  print args

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


if __name__ == "__main__":
  main(sys.argv[1:])

