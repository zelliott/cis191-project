import sys
import os
import json
import imp

saver = imp.load_source('saver', 'saver/secureSaver.py')

timeNo = sys.argv[1]
password = sys.argv[2]

SGSaver = saver.SecureSaver(password)

with open('/tmp/sgcli-send', 'w') as send_fifo:
  send_fifo.write('--confirmOrder ' + timeNo + ' ' + password)
  send_fifo.flush()

while True:
  with open('/tmp/sgcli-receive', 'r') as receive_fifo:
    data = receive_fifo.read()

    if not data == '':
      print data
      break