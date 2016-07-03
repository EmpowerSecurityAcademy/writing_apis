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

@app.route('/todo/api/v1.0/tasks', methods=['GET', 'POST'])
def do_tasks():
	if request.method == 'GET':
		return jsonify({'tasks': tasks})



if __name__ == '__main__':
    app.run(debug=True)