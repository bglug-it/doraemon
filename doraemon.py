#!/usr/bin/env python

"""Helps a client to join domain and maintain itself."""
__author__ = 'Enrico Bacis'
__email__ = 'enrico.bacis@gmail.com'

from contextlib import contextmanager, closing
from subprocess import Popen, PIPE
from sqlite3 import connect
from bottle import Bottle, request
from json import dumps
from ConfigParser import ConfigParser
from Crypto.Hash import MD5
from Crypto.Cipher import AES
import base64
import re
import os
import sys

class MyApp:
  def __init__(self, configfile = '/etc/mac2hostname.ini'):
    if not os.path.isfile(configfile):
      print "Cannot find main file, %s. Exiting." % configfile
      sys.exit(1)

    # Loads configurations
    config = ConfigParser()
    config.read(configfile)
    # Populates private properties with configuration
    self.__dbfile = config.get('Daemon', 'Database') if config.has_option('Daemon', 'Database') else '/var/lib/doraemon/doraemon.db'
    self.__logdir = config.get('Daemon', 'LogFile') if config.has_option('Daemon', 'LogFile') else '/var/log/doraemon.log'
    self.__pidfile = config.get('Daemon', 'PIDFile') if config.has_option('Daemon', 'PIDFile') else '/var/run/doraemon.pid'
    self.__bindaddress = config.get('Daemon', 'BindAddress') if config.has_option('Daemon', 'BindAddress') else '127.0.0.1'
    self.__port = config.getint('Daemon', 'Port') if config.has_option('Daemon',
    'Port') else 8080
    self.__defaultbase = config.get('NameSettings', 'Base') if config.has_option('NameSettings', 'Base') else 'client'
    self.__defaultrole = config.get('NameSettings', 'Role') if config.has_option('NameSettings', 'Role') else 'client'
    self.__namedigits = config.get('NameSettings', 'Digits') if config.has_option('NameSettings', 'Digits') else '2'
    self.__domainfile = config.get('Files', 'Domain') if config.has_option('Files', 'Domain') else None
    self.__mgmtfile = config.get('Files', 'MgmtKey') if config.has_option('Files', 'MgmtKey') else None
    self.__vaultpassfile = config.get('Files', 'VaultPassFile') if config.has_option('Files', 'VaultPassFile') else None
    self.__app = Bottle()
    # Applies routes
    self.__route()
    # Assures table creation
    self.__init_tables()

  # Private methods
  def __route(self):
    self.__app.get('/mac2hostname', callback=self.mac2hostname)
    self.__app.get('/whatsmyhostname', callback=self.whatsmyhostname)
    self.__app.get('/hosts', callback=self.hosts)
    self.__app.get('/domain', callback=self.domain)
    self.__app.get('/mgmtkey', callback=self.mgmtkey)
    self.__app.get('/vaultpass', callback=self.vaultpass)

  def __init_tables(self):
    with self.__getcursor() as cursor:
      cursor.execute('CREATE TABLE IF NOT EXISTS client (id INT PRIMARY KEY,'
                       'hostname TEXT NOT NULL UNIQUE, mac TEXT UNIQUE, role TEXT)')
      cursor.execute('CREATE INDEX IF NOT EXISTS idxmac ON client(mac)')

  def __getmac(self, ip):
    Popen(['ping', '-c1', '-t2', ip], stdout=PIPE).communicate()
    arp = Popen(['arp', '-n', ip], stdout=PIPE).communicate()[0]
    return re.search(r'(([\da-fA-F]{1,2}\:){5}[\da-fA-F]{1,2})', arp).group(1).lower()
    
  def __normalizemac(self, mac):
    return ':'.join(x.zfill(2) for x in mac.split('_')).lower()

  def __gethostname(self, mac):
    # At this point, the mac is set.
    with self.__getcursor() as cursor:
      (newid,) = cursor.execute('SELECT COALESCE(MAX(id) + 1, 1) FROM client').fetchone()
      # Constucts the hostname format
      formatstring = '%s-%0' + self.__namedigits + 'd'
      data = (newid, formatstring % (self.__defaultbase, newid), mac, self.__role)
      # Since MAC is Unique, this fails with the same MAC address
      cursor.execute('INSERT OR IGNORE INTO client VALUES (?, ?, ?, ?)', data)
      (hostname,) = cursor.execute('SELECT hostname FROM client WHERE mac = "%s"' % mac).fetchone()
      return hostname

  @contextmanager
  def __getcursor(self):
    with connect(self.__dbfile) as connection:
      with closing(connection.cursor()) as cursor:
        yield cursor

  # Instance methods AKA routes
  def mac2hostname(self):
    # Ensure required parameters have been passed
    if not request.query.mac:
      return "Usage: GET /mac2hostname?mac=XX_XX_XX_XX_XX_XX[&base=YYY][&role=ZZZ]"
    # Sets up variables for possible parameters
    mac = self.__normalizemac(request.query.mac)
    self.__base = request.query.base or self.__defaultbase
    self.__role = request.query.role or self.__defaultrole
    return self.__gethostname(mac)

  def whatsmyhostname(self):
    # No required parameters
    ip = request.query.ip or request['REMOTE_ADDR']
    self.__role = request.query.role or self.__defaultrole
    return self.__gethostname(self.__getmac(ip))

  def hosts(self):
    # Default where clause: no where specifications
    where = ''
    # If a role parameter is passed, list the hosts for that role
    if request.query.role: 
      where = "WHERE role = '%s'" % request.query.role
    with self.__getcursor() as cursor:
      return dumps([dict((meta[0], data)
        for meta, data in zip(cursor.description, row))
          for row in cursor.execute('SELECT role, hostname, mac FROM client '
              + where + 'ORDER BY role ASC, hostname ASC')], indent=4)

  def domain(self):
    with open(self.__domainfile, 'r') as f:
      return f.read()

  def mgmtkey(self):
    with open(self.__mgmtfile, 'r') as f:
      return f.read()

  def vaultpass(self):
    with open(self.__vaultpassfile) as f:
      ip = request.query.ip or request['REMOTE_ADDR']
      hostname = self.__gethostname(self.__getmac(ip))
      # Chiave
      key = MD5.new(hostname).digest()
      # Segreto da crittare
      secret = f.read().strip()
      # Rendo il segreto lungo un multiplo di 16 byte
      i = 16 - (len(secret) % 16)
      lenghty_secret = secret + i * 'x'
      cipher = AES.new(key, AES.MODE_ECB)
      crypted = cipher.encrypt(lenghty_secret)

      # Devo ritornare un base64 perché la stringa criptata è UTF-8 e non è
      # sempre visibile.
      return base64.b64encode(crypted)

  def start(self):
    # Opens up a PID file
    pid = os.getpid()
    pidfile = open(self.__pidfile, 'w')
    pidfile.write('%s' % pid)
    pidfile.close()

    # Runs Bottle, at last.
    self.__app.run(host=self.__bindaddress, port=self.__port)

# Main body
if __name__ == '__main__':
  cfgfile = '/etc/mac2hostname.ini'
  if len(sys.argv) > 1:
    cfgfile = sys.argv[1]
  app = MyApp(cfgfile)
  app.start()
