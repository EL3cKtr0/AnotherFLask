from flask import Flask, jsonify, abort, request, url_for
import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    },
    {
        'id': 3,
        'title': u'Learn C',
        'description': u'Find nice tutorial of C/C++',
        'done': False
    }
]


# This function update task's id with an automatic URI generated from library url_for
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('getall', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@api.route('/<name>', methods=['GET'])
class hi(Resource):
    def get(self, name):
        """
            Hi, dynamic URL with name

        :param name: string that you insert/n
        :return: return a string with 'Hi' and the name you have insert
        """
        return "Hi %s" % name


@api.route('/alltasks')
class getall(Resource):
    def get(self):
        """
            Get all the tasks ubt with no id, using the URI library

        :return: return a json with all the tasks with uri
        """
        return jsonify({'tasks': [make_public_task(task) for task in tasks]})

    def post(self):
        """
            This method insert a task in the tasks data structure with post method

        :return: return a json with the new tasks updated
        """
        if not request.json or not 'title' in request.json:
            abort(400)

        task = {
            'id': tasks[-1]['id'] + 1,
            'title': request.json['title'],
            'description': request.json.get('description', ""),
            'done': False
        }

        tasks.append(task)
        return jsonify({'task': task}), 201


@api.route('/alltasks/<int:task_id>')
class gettask(Resource):
    def get(self, task_id):
        """
            This method take 1 URI of my structure if present and return it in the page

        :param task_id: integer who specified what task show
        :return: return a json of task we specified
        """
        task = [task for task in tasks if task['id'] == task_id]
        if len(task) == 0:
            abort(404)
        return jsonify({'task': [make_public_task(task[0])]})

    def delete(self, task_id):
        """
            This method should remove a task from the data structure tasks

        :param task_id: integer who specified what task is deleted
        :return: return a json without the task deleted
        """
        task = [task for task in tasks if task['id'] == task_id]
        if len(task) == 0:
            abort(404)
        tasks.remove(task[0])
        return jsonify({'result': True})


if __name__ == "__main__":
    app.run(debug=True)
