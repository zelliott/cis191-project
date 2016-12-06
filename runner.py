import sys
import scrape

order = scrape.Order()

while True:
    with open('/tmp/sgcli-send', 'r') as send_fifo:
        data = send_fifo.read().split()

        if len(data) == 0:
            continue

        flag = data[0]

        if flag == '--getLocations':

            # Params: A zip code
            # Returns: A list of space-separated locations
            #   e.g. 'LocationA LocationB LocationC...'
            zipCode = data[1]

            order.get_location(zipCode)

            toSend = ' '.join(order.locations['name'])

        elif flag == '--getMenu':

            # Params: The index of one of the locations in the list
            # Returns: A list of space-separated menu items
            #   e.g. 'ItemA ItemB ItemC...'
            locationNo = data[1]

            rest_id = order.locations['id'][int(locationNo)]
            menu_items = order.get_menu(rest_id)
            options = [i.keys()[0] for i in menu_items['menu']]
            order_options = [i.replace(" ", "_") for i in options]

            toSend = ' '.join(order_options)

        elif flag == '--getPickupTimes':

            # Params: The index of one of the items in the list
            # Returns: A list of space-separated pickup times
            #   e.g. '5:00 5:30 6:00...'
            itemNo = data[1]
            toSend = '5:00 5:30 6:00'

        elif flag == '--confirmOrder':

            # Params: The index of one of the times in the list and a password
            # Returns: `0` upon failure, `1` upon success
            timeNo = data[1]
            password = data[2]
            toSend = '1'

        else:
            raise Exception('Do not recognize api call')

        with open('/tmp/sgcli-receive', 'w') as receive_fifo:
            receive_fifo.write(toSend)
            receive_fifo.flush()
