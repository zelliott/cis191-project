import requests

LOCATIONS_URL = "https://order.sweetgreen.com/api/restaurants?zip_code="
ORDER_URL = "https://order.sweetgreen.com/api/menus/"


"/api/menus/id"

def get_location(zip_code):
    response = {}
    loc_url = LOCATIONS_URL + str(zip_code)
    r = requests.get(loc_url).json()
    restaurants = r['restaurants']
    response['name'] = [i['restaurant_slug'] for i in restaurants]
    response['address'] = [i['address'] for i in restaurants]
    response['id'] = [i['id'] for i in restaurants]
    return response


def get_menu(rest_id):
    r = requests.get(ORDER_URL + str(rest_id))
    j = r.json()
    products = j['products']
    d = [{i['name']:i['product_slug']} for i in products]
    return {'menu': d}

# print get(7)