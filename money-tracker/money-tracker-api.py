from flask_cors import CORS
from flask import Flask, jsonify, make_response, request
import mysql.connector

app = Flask(__name__)

app.config["JSON_AS_ASCII"] = False
CORS(app)

def connectDatabase ():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        db = "money-tracker"
    )

@app.route("/")
def index():
    return "Welcome to my api"


@app.route("/api/transactions")
def readAll():

    myDb = connectDatabase()

    myCursor = myDb.cursor(dictionary=True)
    myCursor.execute("SELECT * FROM history")

    myResult = myCursor.fetchall()

    return make_response(jsonify(myResult), 200)

@app.route("/api/transactions/<id>")
def readById(id):

    myDb = connectDatabase()

    myCursor = myDb.cursor(dictionary=True)

    sql = "SELECT * FROM history WHERE id = %s"
    val = (id,)

    myCursor.execute(sql, val)


    myResult = myCursor.fetchall()

    return make_response(jsonify(myResult), 200)

@app.route("/api/transactions/createStatement", methods = ['POST'])
def createStatement():

    data = request.get_json()

    myDb = connectDatabase()

    mycursor = myDb.cursor(dictionary=True)
    sql = "INSERT INTO history (name, amount, category) VALUES (%s, %s, %s)"
    val = (data["name"], data["amount"], data["category"])
    
    mycursor.execute(sql, val)
    myDb.commit()
    
    return make_response(jsonify({ "rowcount": mycursor.rowcount }), 200)

@app.route("/api/transactions/updateStatement/<id>", methods = ['PUT'])
def updateStatement(id):

    data = request.get_json()

    myDb = connectDatabase()

    mycursor = myDb.cursor(dictionary=True)
    sql = "UPDATE history SET name = %s, amount = %s, category = %s WHERE id = %s"
    val = (data["name"], data["amount"], data["category"], id)
    
    mycursor.execute(sql, val)
    myDb.commit()
    
    return make_response(jsonify({ "rowcount": mycursor.rowcount }), 200)

@app.route("/api/transactions/deleteStatement/<id>", methods = ['DELETE'])
def deleteStatement(id):

    myDb = connectDatabase()

    mycursor = myDb.cursor(dictionary=True)

    sql = "DELETE FROM history WHERE id = %s"
    val = (id,)

    mycursor.execute(sql, val)
    myDb.commit()
    
    return make_response(jsonify({ "rowcount" : mycursor.rowcount }), 200)


if  __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)