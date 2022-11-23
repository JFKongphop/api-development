from flask_cors import CORS
from flask import Flask, jsonify, render_template, redirect, request
import mysql.connector

app = Flask(__name__, template_folder="templates")
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
    
    myDb = connectDatabase()

    myCursor = myDb.cursor(dictionary=True)
    myCursor.execute("SELECT * FROM history")

    myResult = myCursor.fetchall()

    return render_template(
        "index.html", 
        myResult = myResult
    )

# route to addForm page
@app.route("/addForm")
def addForm():
    return render_template("addForm.html")

# actions addStatement in addForm page
@app.route("/addStatement", methods=["POST"])
def addStatement():
    date = request.form["date"]
    name = request.form["name"]
    amount = request.form["amount"]
    category = request.form["category"]

    myDb = connectDatabase()
    myCursor = myDb.cursor(dictionary=True)

    sql = "INSERT INTO transactions (name, date, amount, category) VALUES (%s, %s, %s, %s)"
    val = (name, date, amount, category)

    myCursor.execute(sql, val)
    myDb.commit()

    return redirect("/")

# click edit form that will direact to each transaction and render transaction by id
@app.route("/edit/<int:id>")
def editStatement(id):
    myDb = connectDatabase()
    myCursor = myDb.cursor(dictionary=True)

    sql = "SELECT * FROM transactions WHERE id = %s"
    val = (id,)

    myCursor.execute(sql, val)
    myResult = myCursor.fetchall()

    return render_template("editForm.html", myResult = myResult)

# actions addStatement in addForm page
@app.route("/updateStatement", methods=['PUT'])
def updateStatement():
    id = request.form["id"]
    date = request.form["date"]
    name = request.form["name"]
    amount = request.form["amount"]
    category = request.form["category"]


    myDb = connectDatabase()

    mycursor = myDb.cursor(dictionary=True)
    sql = "UPDATE history SET name = %s, amount = %s, date = %s, category = %s WHERE id = %s"
    val = (name, amount, date, category, id)
    
    mycursor.execute(sql, val)
    myDb.commit()
    
    return redirect("/")

# click delete  form that will delate this transaction in databse
@app.route("/delete/<int:id>")
def deleteStatement(id):
    myDb = connectDatabase()
    myCursor = myDb.cursor(dictionary=True)
    
    # select of the id to delete
    sql = "DELETE FROM data WHERE id = %s"
    val = (id,)
    myCursor.execute(sql, val)
    myDb.commit()

    return redirect("/")


if  __name__ == "__main__":
    app.run(host="localhost", port=8001, debug=True)
