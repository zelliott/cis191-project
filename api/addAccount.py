import sys
import os
import json
import imp

saver = imp.load_source('saver', 'saver/secure_saver.py')

email = sys.argv[1]
password = sys.argv[2]
cardNo = sys.argv[3]
expMo = sys.argv[4]
expYr = sys.argv[5]
cvv = sys.argv[6]
postalCode = sys.argv[7]
contactNum = sys.argv[8]

SGSaver = saver.SecureSaver(password)
salt = SGSaver.getField('salt', password)

data = {
  'email': email,
  'password': password,
  'salt': salt,
  'cardNo': cardNo,
  'expNo': expMo,
  'expYr': expYr,
  'cvv': cvv,
  'postalCode': postalCode,
  'contactNum': contactNum
}

SGSaver.saveData(data, password)

print '1'