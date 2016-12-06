import os
import errno
import json
import hashlib, uuid
import base64
from itertools import cycle, izip

class SecureSaver:

  def __init__(self, password=None):
    self.foldername = '.sgcli/'
    self.filename = 'data.json'
    self.path = self.foldername + self.filename
    self.password = password
    self.emptyData = {
      'email': 'None',
      'password': 'None',
      'salt': 'None'
    }

    if not os.path.exists(self.foldername):
      os.makedirs(self.foldername)

    if not os.path.exists(self.path):
      f = open(self.path, 'w')

      salt = uuid.uuid4().hex
      password = hashlib.sha512(password + salt).hexdigest()

      self.emptyData['salt'] = salt
      self.emptyData['password'] = password

      json.dump(self.emptyData, f)
      f.close()
    else:

      # Important note: If .sgcli/data.json has already been created,
      # then this new password is effectively ignored by then
      # SecureSaver.
      pass

  def encryptField(self, value):
    return ''.join(chr(ord(c)^ord(k)) for c,k in izip(value, cycle(self.password)))

  def encryptData(self, data):
    for field, value in data.iteritems():
      if field != 'salt' and field != 'password':
        data[field] = self.encryptField(value)

    return data

  def decryptField(self, value):
    return ''.join(chr(ord(c)^ord(k)) for c,k in izip(value, cycle(self.password)))

  def decryptData(self, data):
    for field, value in data.iteritems():
      if field != 'salt' and field != 'password':
        data[field] = self.decryptField(value)

    return data


  def confirmPassword(self, password):
    if os.path.exists(self.path):
      f = open(self.path, 'r')
      data = json.load(f)

      savedHashPass = data['password']
      salt = data['salt']
      hashPass = hashlib.sha512(password + salt).hexdigest()

      if hashPass != savedHashPass:
        raise Exception('Incorrect password')
      else:
        return True

    else:
      raise Exception('Not found: .sgcli/data.json')

  def saveField(self, field, value, password):
    self.confirmPassword(password)

    data = self.getData(password)
    data[field] = value

    self.saveData(data, password)

  def saveData(self, data, password):
    self.confirmPassword(password)

    savedData = self.getData(password)

    data['password'] = savedData['password']
    data['salt'] = savedData['salt']

    if os.path.exists(self.path):
      f = open(self.path, 'w')
      json.dump(self.encryptData(data), f)
      f.close()
    else:
      raise Exception('Not found: .sgcli/data.json')

  def getField(self, field, password):
    self.confirmPassword(password)

    data = self.getData(password)
    return data[field]

  def getData(self, password):
    self.confirmPassword(password)

    if os.path.exists(self.path):
      f = open(self.path, 'r')
      data = self.decryptData(json.load(f))
      f.close()

      return data
    else:
      raise Exception('Not found: .sgcli/data.json')

  def clearData(self, password):
    self.confirmPassword(password)

    self.saveData(self.emptyData)