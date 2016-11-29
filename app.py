from platform import node
from flask import Flask, jsonify, request
from flask_restful import Api, fields, marshal, Resource
import logging


__author__ = 'Zack Elliot, Alessandro Portela, Raghav Joshi'
app = Flask(__name__)
api = Api(app)


class Test(Resource):
	def get(self):
		return jsonify(node=node())


api.add_resource(Test, '/', endpoint='test')


if __name__ == "__main__":
	app.run('0.0.0.0', debug=True)


