from datetime import datetime

from flask import Flask, request, render_template, redirect, url_for
from flaskext.mongokit import MongoKit, Document

app = Flask(__name__)
app.debug = True

class Task(Document):
	__collection__ = 'tasks'
	structure = {
		'title': unicode,
		'text': unicode,
		'creation': datetime,
	}
	required_fields = ['title', 'creation']
	default_values = {'creation': datetime.utcnow}
	use_dot_notation = True

db = MongoKit(app)
db.register([Task])

@app.route('/')
def hello_world():
	return 'Hello World!'


@app.route('/new', methods=["GET", "POST"])
def new_task():
	if request.method == 'POST':
		task = db.Task()
		task.title = request.form['title']
		task.text = request.form['text']
		task.save()
		return redirect(url_for('show_all'))
	return render_template('new.html')
	
if __name__ == '__main__':
	app.run()
