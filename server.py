from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = 'SuperSecretKey'
mysql = MySQLConnector(app,'emailsdb')


@app.route('/')
def index():
    query = "SELECT * FROM emails"
    emails = mysql.query_db(query)                           # run query with query_db()
    return render_template('index.html', all_emails=emails) # pass data to our template


@app.route('/success')
def success():
    query = "SELECT email, DATE_FORMAT(created_at, '%m/%d/%y %H:%m:%S %p') AS time FROM emails ORDER BY created_at ASC"                           # define your query
    emails = mysql.query_db(query) 
    return render_template('success.html', all_emails=emails)


@app.route('/emails', methods=['POST'])
def create():
    is_valid = True
    # Validate that the field is not empty.
    if len(request.form['email']) < 1:
        flash("Email cannot be empty!") # just pass a string to the flash function
        is_valid = False
    else:
        # Validate that the email doesn't already exist in the database.
        getquery = "SELECT * FROM emails WHERE email = '{}'".format(
            request.form['email'])
        data = mysql.query_db(getquery)
        if len(data) > 0:
            flash("Email not valid!")
            is_valid = False
    if (is_valid):
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {
                'email': request.form['email'],
            }
        mysql.query_db(query, data)
        return redirect('/success')
    else:
        return redirect('/')
app.run(debug=True)
