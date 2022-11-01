const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const mysql = require('mysql');

// for use json to data add url
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended : true}));


// homepage route
app.get("/", (req, res)=>{
    return res.send({
        error : false, 
        message : "Welcome to RESTful CRUD API with Nodejs, Express, MYSQL.",
        written_by : "Kongphop"
    })
})

// connect to mysql database
let dbCon = mysql.createConnection({
    host : "localhost",
    user : "root",
    database : "nodejs_api"
})
dbCon.connect()


// retrieve all books
app.get("/books", (req, res)=>{
    // show the book in databse
    dbCon.query('SELECT * FROM books', (error, results, fields)=>{
        if (error) throw error;

        let  message = "";
        if (results === undefined || results.length === 0){
            message = "Books table is empty.";
        }

        else {
            message = "Successfully retrieved all books.";
        }

        return res.send({error : false, data : results,  message : message});
    })
})


// add a new book
app.post("/book", (req ,res)=>{
    
    // get name and author
    let name = req.body.name;
    let author = req.body.author;

    // validation before set to database
    if(!name || !author){
        return res.status(400).send({error : true, message : "Please provide book name and author."})
    }
    else{
        // set data to database
        dbCon.query("INSERT INTO books (name, author) VALUES(?, ?)", [name, author], (error, results, fields)=>{
            if (error) throw error;

            return res.send({error : false, data : results,  message : "Booka scuccessfully added"});
        })
    }
})


// access specific by id
app.get("/book/:id", (req, res)=>{
    // get id of book to show each book
    let id = req.params.id;

    if (!id) {
        return res.status(400).send({error : true, message : "Please provide book id."})
    }

    // find id to show book
    else {
        dbCon.query("SELECT * FROM books WHERE id = ?", id, (error, results, fields)=>{
            if (error) throw error;

            let message = ""
            if (results === undefined || results.length === 0){
                message = "Book not found";
            }
            else{
                message = "Successfully retrieved book data";
            }

            return res.send({error : false, data : results[0], message : message});
        })
    }
})


// update book by id
app.put("/book", (req, res)=>{
    // get data for changing 
    let id = req.body.id;
    let name = req.body.name;
    let author = req.body.author;

    // validation
    if(!id || !name || !author){
        return res.status(400).send({error : true, message : "Please provide book id, name and author"});
    }

    // find to update
    else {
        dbCon.query("UPDATE books SET name = ?, author = ? WHERE id = ?", [name, author, id], (error, results, fields)=>{
            if (error) throw error;
            
            let message = "";
            if (results.changedRows === 0) {
                message = "Book not found or data are same"
            }
            else{
                message = "Book successfully updates"
            }

            return res.send({error : false, data : results, message : message});
        })
    }
})

// delete data 
app.delete("/book", (req, res)=>{
    // get id to delete
    let id = req.body.id;

    if (!id){
        return res.status(400).send({error : true, message : "Please provide book id"});
    }

    // find to delete
    else{
        dbCon.query("DELETE FROM books WHERE id = ?", [id], (error, results, fields)=>{
            if (error) throw error;

            let message = "";
            if(results.affectedRows === 0){
                message = "Book not found";
            }
            else{
                message = "Books successfully deleted";
            }

            return res.send({error : false, data : results, messagec : message});
        })
    }
})


app.listen(3000, ()=>{
    console.log("Node app is running on port 3000");
})
