
import json
import pymongo
from import_config import load_config
from pymongo import MongoClient
from flask import Flask, jsonify, request

app = Flask(__name__)

config = load_config()
client = MongoClient(config["database_mogodb"]["connection_url"])

db = client['basic_api']
collection = db['tasks']

url_root = '/todo/api/v2.0/'


@app.route(url_root+'tasks', methods=['GET', 'POST', 'PUT'])
def do_tasks():
	if request.method == 'GET':
		data = collection.find()
		return jsonify({'tasks': data})


	if request.method == 'POST':
		content = request.get_json(silent=True)
		result = collection.insert_one(content)
		return jsonify({'id': result.inserted_id})

	return jsonify({'status_code': '400'})

# RESTFUL operations related to a specific task

@app.route(url_root+'tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def do_task(task_id):
	if request.method == 'GET':
		data = collection.find({"_id": task_id})
		return jsonify({'task': data})

	if request.method == 'PUT':
		content = request.get_json(silent=True)
		result = collection.update_one(
			{"_id": task_id},
			{"$set": {"title": content["title"], "description": content["description"], "done": content["done"]}}
		)
		return jsonify({'status_code': 200})

	if request.method == 'DELETE':
		collection.delete_one({"_id": task_id})
		return jsonify({'status_code': 200})

	return jsonify({'status_code': '400'})


if __name__ == '__main__':
    app.run(debug=True)