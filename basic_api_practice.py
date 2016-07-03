from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
	{
		'id': 1,
		'title': 'Buy groceries',
		'description': 'Milk, Cheese, Pizza, Fruit, Tylenol',
		'done': False
	},
	{
		'id': 2,
		'title': 'Learn Python',
		'description': 'Need to find a good Python tutorial on the web',
		'done': False
	}
]

url_root = '/todo/api/v1.0/'

@app.route(url_root+'tasks', methods=['GET', 'POST'])
def do_tasks():
	if request.method == 'GET':
		return jsonify({'tasks': tasks})

	if request.method == 'POST':
		content = request.get_json(silent=True)
		content["id"] = tasks[-1]['id'] + 1
		tasks.append(content)
		return jsonify({'id': content["id"]})

	return jsonify({'status_code': 404})

@app.route(url_root+'tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def do_task(task_id):
	task_id = int(task_id)
	if request.method == 'GET':
		task_array = [t for t in tasks if t['id'] == task_id]
		if task != None:
			return jsonify({'task': task_array[0]})
		else:
			return jsonify({'status_code': 404}) 

	if request.method == 'PUT':
		content = request.get_json(silent=True)
		task_array = [t for t in tasks if t['id'] == task_id]
		task = task_array[0]
		if content["title"] != "":
			task["title"] = content["title"]
		if content["description"] != "":
			task["description"] = content["description"]
		if content["description"] != "":
			task["description"] = content["description"]	
		return jsonify({'task': task})	


	if request.method == 'DELETE':
		task_array = [t for t in tasks if t['id'] == task_id]
		if len(task_array) > 0:
			tasks.remove(task_array[0])
			return jsonify({'status_code': 200})
		else:
			return jsonify({'status_code': 404})

	return jsonify({'status_code': 404})



if __name__ == '__main__':
    app.run(debug=True)