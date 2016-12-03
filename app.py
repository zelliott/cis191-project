from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from werkzeug.datastructures import ImmutableMultiDict
import scrape

__author__ = 'Zack Elliot, Alessandro Portela, Raghav Joshi'
app = Flask(__name__)
api = Api(app)

SIGNUP_URL = "https://order.sweetgreen.com/api/customers/login_or_register"

class Location(Resource):
    def get(self):
        zip_code = request.args.get('zipcode')
        restaurants_list = scrape.get_location(zip_code)
        return jsonify(restaurants=restaurants_list)


class Login(Resource):
    def post(self):
        # customer = request.args
        inp = request.get_json(force=True)
        login = scrape.sign_in(inp)
        return jsonify(login)



class Menu(Resource):
    def get(self):
        rest_id = request.args.get('id')
        menu = scrape.get_menu(rest_id)
        return jsonify(menu)






api.add_resource(Location, '/location', endpoint='location')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Menu, '/menu', endpoint='menu')


if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
