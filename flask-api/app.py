from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json
import mysql.connector

app = Flask(__name__)
# show to human language
app.config["JSON_AS_ASCII"] = False
CORS(app)

# server mysql 
host = "localhost"
user = "root"
password = ""
db = "traveling"

def connectDatabase ():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        db = "traveling"
    )

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

# read by id
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


#create data in api
@app.route("/api/attractions", methods = ['POST'])
def crete():

    # connect database
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        db = "traveling"
    )

    # get json data from request
    data = request.get_json()


    mycursor = mydb.cursor(dictionary=True)
    sql = "INSERT INTO attractions (name, detail) VALUES (%s, %s)"
    val = (data["name"], data["detail"])
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({ "rowcount": mycursor.rowcount }), 200)


@app.route("/api/attractions/<id>" , methods = ['PUT'])
def update(id):
    # connect database
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        db = "traveling"
    )

    # get json data from request
    data = request.get_json()

    mycursor = mydb.cursor(dictionary=True)
    sql = "UPDATE attractions SET name = %s, detail = %s WHERE id = %s"
    val = (data['name'], data['detail'], id)
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({ "rowcount" : mycursor.rowcount }), 200)



@app.route("/api/attractions/<id>" , methods = ['DELETE'])
def delete(id):
    # connect database
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        db = "traveling"
    )

    mycursor = mydb.cursor(dictionary=True)
    sql = "DELETE FROM attractions WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({ "rowcount" : mycursor.rowcount }), 200)


if __name__ == "__main__":
    app.run(debug=True)

    #     # return by dict
    # myCursor = mydb.cursor(dictionary=True)

    # # get data for insert to api
    # sql = "INSERT INTO attractions (name, detail) VALUES (%s, %s)"
    # val = (data['name'], data['detail'])

    # # # set for insetrt
    # myCursor.execute(sql, val)
    # mydb.commit()

    # # show th effect when insert
    # return make_response(jsonify({"rowcount" : myCursor.rowcount}), 200)