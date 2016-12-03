import requests
import json

LOCATIONS_URL = "https://order.sweetgreen.com/api/restaurants?zip_code="
MENU_URL = "https://order.sweetgreen.com/api/menus/"
LINE_URL = "https://order.sweetgreen.com/api/line_items"
SIGNUP_URL = "https://order.sweetgreen.com/api/customers/login_or_register"
LOGIN_URL = "https://order.sweetgreen.com/api/customers/login_or_register"
ORDER_URL = "https://order.sweetgreen.com/api/orders?id=1512498&ignored_product_id=159"


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
    d = [{i['name']: i['product_slug']} for i in products]
    return {'menu': d}


def create_user(first_name, last_name, email, phone_number, pwd):
    params = {"customer": {
        "olo_id": None,
        "email": email,
        "password": pwd,
        "password_confirmation": None,
        "first_name": first_name,
        "last_name": last_name,
        "contact_number": phone_number,
        "reference": None,
        "is_rewards_user": False,
        "has_opted_in": True,
        "reset_password": False,
        "last_completed_order_id": None,
        "billing_account_ids": [],
        "loyalty_id": None
    }}

    payload = 'customer[olo_id]=' + 'null' + '&customer[email]=' + str(email) + '&customer[password]=' + str(pwd)
    payload += '&customer[password_confirmation]=' + "null" + '&customer[first_name]=' + str(first_name) + '&customer[last_name]=' + str(last_name)
    payload += '&customer[contact_number]=' + str(phone_number) + '&customer[reference]=' + 'null' + '&customer[is_rewards_user]=' + str(False)
    payload += '&customer[has_opted_in]=' + str(True) + '&customer[reset_password]=' + str(False) + '&customer[last_completed_order_id]=' + 'null'
    payload += '&customer[billing_account_ids]=' + '[]' + '&customer[loyalty_id]=' + 'null'

    r = requests.post(SIGNUP_URL, data=params)
    return r.json()


def sign_in(inp):
    with requests.Session() as s:
        params = inp.get('customer')
        pwd = params.get('password')
        user = params.get('email')
        payload = 'customer[email]=' + user + '&customer[password]=' + pwd
        r = s.post(LOGIN_URL, data=payload, headers={"Accept": "application/json",
                                                     "Content-Type": "application/x-www-form-urlencoded"})
        resp = r.json()
        return resp, resp['session']['csrf']



def make_order(inp, rest_id, prod_id):
    with requests.session() as s:
        # Login
        params = inp.get('customer')
        pwd = params.get('password')
        user = params.get('email')
        payload = 'customer[email]=' + user + '&customer[password]=' + pwd
        r = s.post(LOGIN_URL, data=payload, headers={"Accept": "application/json",
                                                     "Content-Type": "application/x-www-form-urlencoded"})
        resp = r.json()
        print resp

        # Make Order
        payload = 'line_item[quantity]=' + '1' + '&line_item[product_id]=' + str(prod_id) + '&line_item[calories]=' + 'null'
        payload += '&line_item[favorited]=' + str(False) + '&line_item[is_custom]=' + str(False) + '&line_item[custom_name]=' + 'null'
        payload += '&line_item[permalink]=' + 'null' + '&line_item[slug]=' + 'null' + '&line_item[static_cost]=' + 'null'
        payload += '&line_item[additions]=' + 'null' + '&line_item[removals]=' + 'null' + '&line_item[order_completed]=' + 'null'
        payload += '&line_item[customer_name]=' + 'null' + '&line_item[ignored_order_id]=' + 'null' + '&line_item[order_id]=' + 'null'
        payload += '&line_item[options]=' + '[]' + '&line_item[restaurant_id]=' + str(rest_id)
        o = s.post(url=LINE_URL, data=payload, headers={"X-CSRF-TOKEN":resp['session']['csrf']})
        # o = s.post(url=ORDER_URL, data=payload, headers={"X-CSRF-TOKEN": resp['session']['csrf']})
        # return o.json()


# print make_order({"customer": {"email": "snowboarderwv@hotmail.com", "password": "pwdpwdpwd"}}, 7, 159)

# print sign_in({"customer": {"email": "snowboarderwv@hotmail.com", "password": "pwdpwdpwd"}})


print create_user("Lemon", "Juice", "lemonjuice@hotmail.com", "8379094434", "welcome")