from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json
import mysql.connector
import requests

app = Flask(__name__)
# show to human language
app.config["JSON_AS_ASCII"] = False
CORS(app)

# server mysql 
def connectDatabase ():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        db = "traveling"
    )

# chcek the id for update and delete
response_API = requests.get('http://127.0.0.1:5000/api/attractions').text
data = json.loads(response_API)
print(data)

def filterId(id):
    for d in data:
        if d["id"] != id:
            return "A"
        else:
            return "B"
print(filterId(1))

# home page api
@app.route("/")
def home():
    return "Welcome to my api"

# create database 
@app.route("/api/attractions")
def read():
    
    # connect database
    mydb = connectDatabase()

    # return by dict
    myCursor = mydb.cursor(dictionary=True)
    myCursor.execute("SELECT * FROM attractions")

    # show data
    myResult = myCursor.fetchall()
    return  make_response(jsonify(myResult), 200)

# # read by id
@app.route("/api/attractions/<id>")
def readById(id):
    # connect database
    mydb = connectDatabase()

    # return by dict
    myCursor = mydb.cursor(dictionary=True)
    # choosing the data by id
    sql = "SELECT * FROM attractions WHERE id = %s"
    val = (id,)
    
    # set the data to show]
    myCursor.execute(sql, val)

    # show data
    myResult = myCursor.fetchall()
    return  make_response(jsonify(myResult), 200) 


# #create data in api
@app.route("/api/attractions", methods = ['POST'])
def create():

    # get json data from request
    data = request.get_json()

    # connect database
    mydb = connectDatabase()
    mycursor = mydb.cursor(dictionary=True)
    sql = "INSERT INTO attractions (name, detail) VALUES (%s, %s)"
    val = (data["name"], data["detail"])
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({ "rowcount": mycursor.rowcount }), 200)


# update data in api
@app.route("/api/attractions/<id>" , methods = ['PUT'])
def update(id):
    # get json data from request
    data = request.get_json()

    # connect database and show by dict
    mydb = connectDatabase()
    mycursor = mydb.cursor(dictionary=True)

    # select by id to update new data
    sql = "UPDATE attractions SET name = %s, detail = %s WHERE id = %s"
    val = (data['name'], data['detail'], id)
    mycursor.execute(sql, val)
    mydb.commit()

     # show the response after delete
    return make_response(jsonify({ "rowcount" : mycursor.rowcount }), 200)


# delete data in api
@app.route("/api/attractions/<id>" , methods = ['DELETE'])
def delete(id):
    # connect database
    mydb = connectDatabase()
    mycursor = mydb.cursor(dictionary=True)
    
    # select of the id to delete
    sql = "DELETE FROM attractions WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()

    # show the response after delete
    return make_response(jsonify({ "rowcount" : mycursor.rowcount }), 200)


if __name__ == "__main__":
    app.run(debug=True)