import requests
import json

LOCATIONS_URL = "https://order.sweetgreen.com/api/restaurants?zip_code="
MENU_URL = "https://order.sweetgreen.com/api/menus/"
ORDER_URL = "https://order.sweetgreen.com/api/line_items"
SIGNUP_URL = "https://order.sweetgreen.com/api/customers/login_or_register"
LOGIN_URL = "https://order.sweetgreen.com/api/customers/login_or_register"



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
    r = requests.get(MENU_URL + str(rest_id))
    j = r.json()
    products = j['products']
    d = [{i['name']:i['product_slug']} for i in products]
    return {'menu': d}


def create_user(first_name, last_name, email, phone_number, pwd):
    params = {"customer": {
        "olo_id": None,
        "email": email,
        "password": pwd,
        "password_confirmation": None,
        "first_name":first_name,
        "last_name": last_name,
        "contact_number":phone_number,
        "reference": None,
        "is_rewards_user":False,
        "has_opted_in": True,
        "reset_password": False,
        "last_completed_order_id": None,
        "billing_account_ids":[],
        "loyalty_id": None
    }}
    r = requests.post(SIGNUP_URL, data=params)
    return r.json()


def sign_in(inp):
    with requests.Session() as s:
        params = inp.get('customer')
        pwd = params.get('password')
        user = params.get('email')
        payload = 'customer[email]=' + user + '&customer[password]=' + pwd
        r = s.post(LOGIN_URL, data=payload)
        return r




# def place_order(quantity, order_id):
#     s = requests.session()
#     json_obj = {"line_item": {"quantity": 1, "calories": 590, "favorited": False, "is_custom": False, "custom_name": None,
#                    "permalink": None, "slug": None, "static_cost": None, "additions": None, "removals": None,
#                    "order_completed": False, "customer_name": None, "ignored_order_id": None, "product_id": "159",
#                    "order_id": None, "options": [], "restaurant_id": "7"}}
#     r = requests.post(ORDER_URL, data=json_obj)
#     print r
#     return False
#
#
#
#
# print place_order(1, 1)