import requests

# Sweetgreen's various API endpoints declared as constants
LOCATIONS_URL = 'https://order.sweetgreen.com/api/restaurants?zip_code='
MENU_URL = 'https://order.sweetgreen.com/api/menus/'
LINE_URL = 'https://order.sweetgreen.com/api/line_items'
SIGNUP_URL = 'https://order.sweetgreen.com/api/customers/login_or_register'
LOGIN_URL = 'https://order.sweetgreen.com/api/customers/login_or_register'
ORDER_URL = 'https://order.sweetgreen.com/api/orders?'
CHECKOUT_URL = 'https://order.sweetgreen.com/api/orders/'

class Order(object):
    """docstring for Order"""

    def __init__(self):
        super(Order, self).__init__()
        self.locations = None
        self.rest_id = None
        self.menu = None
        self.zip = None
	self.hours = None

    def get_location(self, zip_code):
        self.zip = zip_code
        response = {}
        loc_url = LOCATIONS_URL + str(self.zip)
        r = requests.get(loc_url).json()
        restaurants = r['restaurants']
        response['name'] = [i['restaurant_slug'] for i in restaurants]
        response['id'] = [i['id'] for i in restaurants]
        response['merged'] = [{i['restaurant_slug']: i['id']} for i in restaurants]
        self.locations = response
        return self.locations

    def get_menu(self, rest_id):
        self.rest_id = rest_id
        r = requests.get(MENU_URL + str(rest_id))
        j = r.json()
        products = j['products']
        d = [{i['name']: i['product_slug']} for i in products]
        self.menu = {'menu': d}
        return self.menu

    ##SG allows for pickup times every half-hour the store is open up until close of the subsequent day.
    def get_times(self, rest_id):
	self.rest_id = rest_id
	r = requests.get(LOCATIONS_URL + str(self.zip)
	j = r.json()
	j = j['restaurants']
	for i in restaurants:
		if i['id'] == self.rest_id:
			restaurant_entry = i
			break
	hours = restaurant_entry['hours']
	print(hours) ## TODO-- test
	self.hours = hours
	return self.hours
		
    def sign_in(self, inp):
        with requests.Session() as s:
            params = inp.get('customer')
            pwd = params.get('password')
            user = params.get('email')
            payload = 'customer[email]=' + user + '&customer[password]=' + pwd
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            r = s.post(LOGIN_URL, data=payload, headers=headers)
            resp = r.json()
            return resp, resp['session']['csrf']

    def make_order(self, inp, rest_id, prod_id):
        with requests.session() as s:
            # Login
            params = inp.get('customer')
            pwd = params.get('password')
            user = params.get('email')
            payload = 'customer[email]=' + user + '&customer[password]=' + pwd
            r = s.post(LOGIN_URL, data=payload, headers=headers)
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            resp = r.json()  # to get session information (csrf token)

            # Add line-item
            payload = 'line_item[quantity]=' + '1' + '&line_item[product_id]=' + str(
                prod_id) + '&line_item[calories]=' + 'null'
            payload += '&line_item[favorited]=' + str(False) + '&line_item[is_custom]=' + str(
                False) + '&line_item[custom_name]=' + 'null'
            payload += '&line_item[permalink]=' + 'null' + '&line_item[slug]=' + 'null' + '&line_item[static_cost]=' + 'null'
            payload += '&line_item[additions]=' + 'null' + '&line_item[removals]=' + 'null' + '&line_item[order_completed]=' + 'null'
            payload += '&line_item[customer_name]=' + 'null' + '&line_item[ignored_order_id]=' + 'null' + '&line_item[order_id]=' + 'null'
            payload += '&line_item[options]=' + '[]' + '&line_item[restaurant_id]=' + str(rest_id)
            order = s.post(url=LINE_URL, data=payload, headers={'X-CSRF-TOKEN': resp['session']['csrf']}).json()

            # Create order
            full_url = ORDER_URL + 'id=' + str(order['line_item']['ignored_order_id']) + \
                       '&ignored_product_id=' + str(order['line_item']['product_id'])

            # Checkout
            session = s.get(url='https://order.sweetgreen.com/api/session').json()
            checkout = s.get(url=CHECKOUT_URL + str(session['session']['current_order_id']),
                             headers={'X-CSRF-TOKEN': session['session']['csrf']})

            # Payment
            # final_order = s.post()

            return checkout.json()
