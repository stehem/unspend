from flask import Flask, render_template, request, redirect, url_for
from mongokit import Connection, Document
import datetime


# configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017


app = Flask(__name__)
app.config.from_object(__name__)

# connect to the database
connection = Connection(app.config['MONGODB_HOST'],
								        app.config['MONGODB_PORT'])


@connection.register
class Spend(Document):
	__collection__ = 'expenses'
	__database__ = 'dev'
	structure = {
		'amount': int,
		'date': datetime.datetime
	}
	use_dot_notation = True



@app.route('/expenses/new')
def new():
	return render_template('new.html')

@app.route('/expenses', methods=['POST'])
def create():
	expense =  connection.Spend({'amount': int(request.form['amount']), 'date': datetime.datetime.today()})
	expense.save()
	return redirect(url_for('index'))

@app.route('/expenses', methods=['GET'])
def index():
	expenses = connection.Spend.find()
	return render_template('index.html', expenses=expenses)


if __name__ == '__main__':
	app.run(debug=True)
