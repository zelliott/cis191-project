import sys

timeNo = sys.argv[1]
password = sys.argv[2]

with open('/tmp/sgcli-send', 'w') as send_fifo:
  send_fifo.write('--confirmOrder ' + timeNo + ' ' + password)
  send_fifo.flush()

with open('/tmp/sgcli-receive', 'r') as receive_fifo:
  print receive_fifo.read()