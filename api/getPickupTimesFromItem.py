import sys

itemNo = sys.argv[1]

with open('/tmp/sgcli-send', 'w') as send_fifo:
  send_fifo.write('--getPickupTimes ' + itemNo)
  send_fifo.flush()

with open('/tmp/sgcli-receive', 'r') as receive_fifo:
  print receive_fifo.read()