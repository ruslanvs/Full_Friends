from flask import Flask, render_template, request, redirect, session
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "MySecretSessionKey"

mysql = MySQLConnector( app, "full_friends" )

@app.route( "/" )
def front_page():
    
    friends_data = mysql.query_db( "SELECT full_name, age, DATE_FORMAT(created_at, '%M %d, %Y') AS friends_from FROM users" )
    
    data = {}
    data["full_name"] = "<div>"
    data["age"] = "<div>"
    data["friend_since"] = "<div>"

    for i in range ( 0, len( friends_data ) ):
        data["full_name"] += "<p class='cell'>" + str( friends_data[i]["full_name"] ) + "</p>"
        data["age"] += "<p class='cell'>" + str( friends_data[i]["age"] ) + "</p>"
        data["friend_since"] += "<p class='cell'>" + str( friends_data[i]["friends_from"] ) + "</p>"

    data["full_name"] += "</div>"
    data["age"] += "</div>"
    data["friend_since"] += "</div>"

    return render_template( "index.html", data = data )

@app.route( "/create_friend", methods = ['POST'] )
def c():
    query = "INSERT INTO users ( full_name, age, created_at, updated_at) VALUES( :full_name, :age, NOW(), NOW() )"
    print request.form['full_name']
    print request.form['age']

    new_data = {
        'full_name': request.form['full_name'],
        'age': request.form['age']
    }
    mysql.query_db( query, new_data )
    return redirect( "/" )
    
app.run( debug = True )