from flask import Flask, jsonify, request
from flask_restful import Api, fields, marshal, Resource
import scrape

__author__ = 'Zack Elliot, Alessandro Portela, Raghav Joshi'
app = Flask(__name__)
api = Api(app)


class Location(Resource):
    def get(self):
        zip_code = request.args.get('zipcode')
        restaurants_list = scrape.get_location(zip_code)
        return jsonify(restaurants=restaurants_list)

class Menu(Resource):
    def get(self):
        rest_id = request.args.get('id')
        menu = scrape.get_menu(rest_id)
        return jsonify(menu)


api.add_resource(Location, '/location', endpoint='location')
api.add_resource(Menu, '/menu', endpoint='menu')

if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
