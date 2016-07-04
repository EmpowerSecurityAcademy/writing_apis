import json
import pymongo
from import_config import load_config
from pymongo import MongoClient
from flask import Flask, jsonify, request
from bson.json_util import dumps
from bson.objectid import ObjectId 

app = Flask(__name__)

config = load_config()
client = MongoClient(config["database_mongodb"]["connection_url"])

db = client[config['database_mongodb']['database_name']]
collection = db[config['database_mongodb']['collection_name']]

url_root = '/todo/api/v2.0/'

@app.route(url_root+'tasks', methods=['GET', 'POST', 'PUT'])
def do_tasks():
	if request.method == 'GET':
		data = collection.find()
		return make_response(dumps(data), 200)

	if request.method == 'POST':
		content = request.get_json(silent=True)
		result = collection.insert_one(content)
		return jsonify({'id': str(result.inserted_id)})

	return make_response(jsonify({'status_code': 500}), 500)

# RESTFUL operations related to a specific task

@app.route(url_root+'tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def do_task(task_id):
	if request.method == 'GET':
		data = collection.find_one({"_id": ObjectId(task_id)})
		return make_response(dumps(data), 200)

	if request.method == 'PUT':
		content = request.get_json(silent=True)
		result = collection.update_one(
			{"_id": task_id},
			{"$set": {"title": content["title"], 
						"description": content["description"], 
						"done": content["done"]}}
		)
		data = collection.find_one({"_id": ObjectId(task_id)})
		return make_response(dumps(data), 200)

	if request.method == 'DELETE':
		result = collection.delete_one({"_id": task_id})
		return make_response(jsonify({'status_code': 200}), 200)

	return make_response(jsonify({'status_code': 500}), 500)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)