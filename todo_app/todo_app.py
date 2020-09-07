import datetime

from flask import Flask, current_app
from flask import g
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from peewee import *

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version = '1.0', title = 'TodoMVC API',
    description = 'A simple TodoMVC API')

my_api = api.namespace('task', description = 'TODO operation my_api')

todo_list = api.model('Todo list', {
    'title': fields.String(required = True, description = 'The task title'),
    'created_at': fields.String(required = True, description = 'Created time')
})

todo = api.model('Todo', {
    'title': fields.String(required = True, description = 'The task title'),
    'content': fields.String(required = True, description = 'The task content')
})

todo_detail = api.model('Todo detail', {
    'title': fields.String(required = True, description = 'The task title'),
    'content': fields.String(required = True, description = 'The task content'),
    'created_at': fields.String(required = True, description = 'Created time')
})


database = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = database

now = datetime.datetime.now()

# the user model specifies its fields (or columns) declaratively, like django
class Task(BaseModel):
    title = CharField(max_length = 150)
    content = TextField()
    created_at = DateTimeField()

    def get_all_todos():
        return (list(Task
                        .select(Task.title, Task.created_at)
                        .dicts()))

    def get_todo(id):
        return (Task
                .select(Task.title, Task.content, Task.created_at)
                .where(Task.id == id)
                .dicts()
                .get())

    def create_todo(data):
        (Task.create(title = data.get('title'),
                     content = data.get('content'),
                     created_at = now))

    def update_todo(id, data):
        (Task
            .update(title = data.get('title'), content = data.get('content'))
            .where(Task.id == id)
            .execute())

    def delete_todo(id):
            return (Task
                    .delete()
                    .where(Task.id == id)
                    .execute())


# simple utility function to create tables
def create_tables():
    with database:
        database.create_tables([Task])

@app.before_request
def before_request():
    g.db = database
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@my_api.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @my_api.doc('list_todos')
    @my_api.marshal_list_with(todo_list)
    def get(self):
        '''List of all tasks'''
        return Task.get_all_todos()

    @my_api.doc('create_todo')
    @my_api.expect(todo)
    def post(self):
        '''Create a new task'''
        try:
            Task.create_todo(api.payload)
            return 'Success'
        except:
            return 'Error'


@my_api.route('/<int:id>')
@my_api.param('id', 'The task identifier')
class Todo(Resource):
    @my_api.doc('get_todo')
    @my_api.marshal_with(todo_detail, code = 201)
    @my_api.response(404, 'Todo not found')
    def get(self, id):
        '''Show a task given its identifier '''
        try:
            return Task.get_todo(id), 201
        except:
            return 'todo not found', 404


    @my_api.doc('delete_todo')
    @my_api.response(204, 'Todo deleted')
    @my_api.response(404, 'Todo not found')
    def delete(self, id):
        '''Delete a task given its identifier'''
        if Task.delete_todo(id):
            return '', 204
        else:
            return 'todo not found', 404

    @my_api.expect(todo)
    @my_api.marshal_with(todo_detail)
    @my_api.response(404, 'Todo not found')
    def put(self, id):
        '''Update a task given its identifier'''
        try:
            Task.update_todo(id, api.payload)
            return Task.get_todo(id)
        except:
            return '', 404


if __name__ == '__main__':
    database.init('todo.db')
    create_tables()
    app.run(debug = True)