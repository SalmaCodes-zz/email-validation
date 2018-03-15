from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'full_friends_db')
@app.route('/')

@app.route('/')
def index():
    query = "SELECT name, age, DATE_FORMAT(created_at, '%M %d, %Y') AS time FROM friends"                           # define your query
    friends = mysql.query_db(query)                           # run query with query_db()
    return render_template('index.html', all_friends=friends) # pass data to our template


@app.route('/friends', methods=['POST'])
def create():
    query = "INSERT INTO friends (name, age, created_at, updated_at) VALUES (:name, :age, NOW(), NOW())"
    data = {
             'name': request.form['name'],
             'age':  request.form['age'],
           }
    mysql.query_db(query, data)
    return redirect('/')
app.run(debug=True)
