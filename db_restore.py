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

def is_db_file_exist(databases, restore_day, store):
  tested_dbs = []
  suffix = '.' + restore_day + '.sql.gz'
  all_dbs = os.listdir(store)

  for db_from_request in databases:
    if db_from_request + suffix in all_dbs:
      exist = True
    else:
      exist = False
    tested_dbs.append({'exist': exist, 'db_path': store + os.sep + db_from_request + suffix, 'db_name': db_from_request })

  # will return list of dics
  return tested_dbs



def restore(databases=None, restore_day=None, store=None, user=None, password=None, host=None):
  tested_dbs = is_db_file_exist(databases, restore_day, store)
  for db_for_restore in tested_dbs:
    if db_for_restore['exist'] == True:
      restore_cmd = 'zcat ' + db_for_restore['db_path'] + ' | ' + 'mysql -u ' + user + ' -p' + password + ' -h ' + "'" + host + "'" + ' ' + db_for_restore['db_name']
      # os.popen(restore_cmd)
      print restore_cmd
    else:
      msg = 'The %s file is not exist.' % db_for_restore['db_path']
      logging.warning(msg)


def main(argv):
  # create pid file
  pid = str(os.getpid())
  pidfile = '/tmp/db_restore.pid'

  # set default vals
  databases = None
  store = None
  user = 'backup'
  password = None
  host = None

  # set logging configs, you can uncomment this line to save all logs in file
  # logging.basicConfig(filename='restore.log', level=logging.DEBUG)

  opts, args = getopt.getopt(argv, 'hd:y:s:t:u:p:', ['help', 'databases=', 'day=', 'host=', 'user=', 'store=', 'password='])

  # if no args exit and print menu
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

  # check is process running
  if os.path.isfile(pidfile):
    print '%s file exist. Probably restore is already running' % pidfile
    sys.exit()
  file(pidfile, 'w').write(pid)

  try:
    restore(databases, restore_day, store, user, password, host)
  except(Exception):
    logging.exception('Restore failed!!!\n')
  finally:
    os.unlink(pidfile)

if __name__ == '__main__':
  main(sys.argv[1:])

