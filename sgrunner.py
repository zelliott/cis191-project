import sys
import os
import json
import imp
import scrape
from sgorder import Order

saver = imp.load_source('saver', 'saver/secureSaver.py')
SGOrder = Order()

# Helper function used to interface with sgorder.py
def getLocationsFromZipCode(zipCode):
    SGOrder.get_location(zipCode)

    return ' '.join(SGOrder.locations['name'])

# Helper function used to interface with sgorder.py
def getMenuFromLocation(locationNo):
    menuItems = SGOrder.get_menu(locationNo)
    options = [i.keys()[0] for i in menuItems['menu']]
    orderOptions = [i.replace(' ', '_') for i in options]

    return ' '.join(orderOptions)

# Helper function used to interface with sgorder.py
def getPickupTimesFromItem(itemNo):

    storeHours = SGOrder.get_times()

    # TODO:
    # Use store hours to print out half-hour intervals while store is open from
    # Current day/time to closing time of subsequent day

    return '3:00 3:30 4:00 4:30 5:00 5:30 6:00 6:30'

# Helper function used to interface with sgorder.py
def confirmOrder(timeNo, password):
    try:
        SGSaver = saver.SecureSaver(password)
        data = SGSaver.getData(password)

        # TODO:
        # Add API call

        return '1'
    except Exception:
        return '0'

# This function is called whenever data is sent to sgrunner.py via the
# sgcli.sh -> api/[some function] pipeline.
def handleRead(data):
    flag = data[0]

    if flag == '--getLocations':

        # Params: A zip code
        # Returns: A list of space-separated locations
        #   e.g. 'LocationA LocationB LocationC...'
        zipCode = data[1]
        toSend = getLocationsFromZipCode(zipCode)

    elif flag == '--getMenu':

        # Params: The index of one of the locations in the list
        # Returns: A list of space-separated menu items
        #   e.g. 'ItemA ItemB ItemC...'
        locationNo = data[1]
        toSend = getMenuFromLocation(locationNo)

    elif flag == '--getPickupTimes':

        # Params: The index of one of the items in the list
        # Returns: A list of space-separated pickup times
        #   e.g. '5:00 5:30 6:00...'
        itemNo = data[1]
        toSend = getPickupTimesFromItem(itemNo)

    elif flag == '--confirmOrder':

        # Params: The index of one of the times in the list and a password
        # Returns: `0` upon failure, `1` upon success
        timeNo = data[1]
        password = data[2]
        toSend = confirmOrder(timeNo, password)

    else:
        raise Exception('Do not recognize api call')

    with open('/tmp/sgcli-receive', 'w') as receive_fifo:
        receive_fifo.write(toSend)
        receive_fifo.flush()

# This is the central python runner that simply loops and reads from
# the opened fifo.  Whenever data has been sent to this function, it handles
# it.
def startRunner():
    while True:
        with open('/tmp/sgcli-send', 'r') as send_fifo:
            data = send_fifo.read().split()

            if len(data) == 0:
                continue

            handleRead(data)

if __name__ == '__main__':
    startRunner()
