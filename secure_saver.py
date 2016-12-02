import os
import errno
import json

class SecureSaver:
  def __init__(self):

    self.path = '.sgcli/'
    self.filename = 'data.json'
    self.emptyData = {
      'email': 'None',
      'password': 'None'
    }

    if not os.path.exists(self.path):
      os.makedirs(self.path)

    if not os.path.exists(self.path + self.filename):
      f = open(self.path + self.filename, 'w')
      json.dump(self.emptyData, f)
      f.close()

  def saveField(self, field, value, password):
    data = self.getData(password)
    data[field] = value
    self.saveData(data)

  def saveData(self, data):
    if os.path.exists(self.path + self.filename):
      f = open(self.path + self.filename, 'w')
      json.dump(data, f)
      f.close()
    else:
      raise Exception('Not found: .sgcli/data.json')

  def getField(self, field, password):
    data = self.getData(password)
    return data[field]

  def getData(self, password):
    if os.path.exists(self.path + self.filename):
      f = open(self.path + self.filename, 'r')
      data = json.load(f)
      f.close()

      return data
    else:
      raise Exception('Not found: .sgcli/data.json')

  def clearData(self):
    self.saveData(self.emptyData)