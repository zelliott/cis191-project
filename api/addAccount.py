import sys
import os
import json

from saver.secure_saver import SecureSaver

# I don't know why I made each of these a separate variable, ridiculous
# hoenstly but at least it's clear what everything is...

email = sys.argv[1]
password = sys.argv[2]
cardNo = sys.argv[3]
expMo = sys.argv[4]
expYr = sys.argv[5]
cvv = sys.argv[6]
postalCode = sys.argv[7]
contactNum = sys.argv[8]

saver = SecureSaver(password)
salt = saver.getField('salt', password)

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

saver.saveData(data, password)

print '1'