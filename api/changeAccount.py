import sys
import os
import json
import imp

saver = imp.load_source('saver', 'saver/secureSaver.py')

flag = sys.argv[1][2:]
value = sys.argv[2]
password = sys.argv[3]

SGSaver = saver.SecureSaver(password)
SGSaver.saveField(flag, value, password)

print '1'