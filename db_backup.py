#!/usr/bin/env python

import sys
import os
import string
import getopt
import logging
import datetime

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

def backup(databases=None, store=None, user=None, password=None, host=None):
  # get current date
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d")

  if databases != None:
    for db in databases:
      db = db.strip() # remove leading and trailing whitespace
      db_backup_name = string.join([db, timestamp, 'sql'], '.')
      db_backup_path = store + os.sep + db_backup_name

      dump_cmd = 'mysqldump -u ' + user
      if host != None:
        dump_cmd += ' -h ' + "'" + host + "'"
      if password != None:
        dump_cmd += ' -p' + password
      dump_cmd += ' -e --opt -c ' + db + ' | gzip > ' + db_backup_path + '.gz'
      logging.info("Dump db, %s to %s." % (db, db_backup_path))
      os.popen(dump_cmd)

def delete_old_backups(keep=7, store=None):
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
  cut_date = datetime.datetime.now() - datetime.timedelta(days=keep)

  # converge cut_date from to proper fomat
  cut_date = datetime.datetime.strptime(cut_date.strftime("%Y-%m-%d"), "%Y-%m-%d")

  for dump_file in os.listdir(store):
    if dump_file.endswith('sql.gz'):
      dump_date = datetime.datetime.strptime(dump_file.split('.')[1], "%Y-%m-%d")
      if dump_date < cut_date:
        os.remove(os.path.join(store, dump_file))


"""
main method
"""
def main(argv):
  # create pid file
  pid = str(os.getpid())
  pidfile = '/tmp/db_backup.pid'

  # Set default vals
  keep      = 7
  databases = None
  user      = None
  password  = None
  host      = None
  store     = None

  # set logging configs, you can uncomment this line to save all logs in file
  # logging.basicConfig(filename='backups.log', level=logging.DEBUG)

  try:
    opts, args = getopt.getopt(argv, "hn:k:d:t:u:p:s:", ["help", "keep=", "databases=", "store=", "user=", "password=", "host="])

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
        databases = string.split(arg, ',')
      elif opt in ('-t', '--store'):
        store = arg
      elif opt in ('-u', '--user'):
        user = arg
      elif opt in ('-p', '--password'):
        password = arg
      elif opt in ('-s', '--host'):
        host = arg

  except getopt.GetoptError, msg:
    logging.warning(msg)
    menu()
    sys.exit()
  
  # chek if process is running
  if os.path.isfile(pidfile):
    print '%s file exist. Probably backup is already running.' % pidfile
    sys.exit()
  file(pidfile, 'w').write(pid)

  try:
    backup(databases, store, user, password, host)
    delete_old_backups(keep, store)
  except(Exception):
    logging.exception('Backups failed!!!\n')
  finally:
    os.unlink(pidfile)

if __name__ == "__main__":
  main(sys.argv[1:])

