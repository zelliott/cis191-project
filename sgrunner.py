import sys
import os
import json
import imp
import scrape
from sgorder import Order

saver = imp.load_source('saver', 'saver/secure_saver.py')

SGOrder = Order()

def getLocationsFromZipCode(zipCode):
    SGOrder.get_location(zipCode)

    return ' '.join(SGOrder.locations['name'])

def getMenuFromLocation(locationNo):
    rest_id = SGOrder.locations['id'][int(locationNo)]
    menu_items = SGOrder.get_menu(rest_id)
    options = [i.keys()[0] for i in menu_items['menu']]
    order_options = [i.replace(" ", "_") for i in options]

    return ' '.join(order_options)

def getPickupTimesFromItem(itemNo):

    # TODO:
    # Add API call

    return '5:00 5:30 6:00'

def confirmOrder(timeNo, password):
    try:
        SGSaver = saver.SecureSaver(password)
        data = SGSaver.getData(password)

        # TODO:
        # Add API call

        return '1'
    except Exception:
        return '0'

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

def startRunner():
    while True:
        with open('/tmp/sgcli-send', 'r') as send_fifo:
            data = send_fifo.read().split()

            if len(data) == 0:
                continue

            handleRead(data)

if __name__ == '__main__':
    startRunner()