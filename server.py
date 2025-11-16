from flask import Flask, jsonify, request
import sqlite3
from datetime import date
from constants import (
  SQL_SELECT_ALL_USER,
  SQL_DELETE_USER, 
  SQL_SELECT_USER_BY_ID, 
  SQL_UPDATE_USER,
  SQL_INSERT_USER,
  SQL_DELETE_EXPENSES,
  SQL_INSERT_EXPENSES,
  SQL_SELECT_ALL_EXPENSES,
  SQL_SELECT_EXPENSES_BY_ID,
  SQL_UPDATE_EXPENSES)
from response import (
  success_response,
  not_found
  
)

app = Flask(__name__)

# constant
DB_NAME = "budget_manager.db"


def init_db():
  conn = sqlite3.connect(DB_NAME) # opens a connection to the database file named "budget_manager.db"
  cursor = conn.cursor() # creates a cursor/tool that lets us send commands (SELECT, INSERT, ...)

  # ----- users table -----
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL             
  )
  """)
  #------ expenses table -----
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS expenses (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT,
      description TEXT NOT NULL,
      amount TEXT NOT NULL,
      date TEXT NOT NULL,
      category TEXT NOT NULL,
      user_id INTEGER,
      FOREIGN KEY(user_id) REFERENCES users(id)   
) 
""")

  conn.commit() # Save changes to the database
  conn.close() # Close de connection to the database






@app.get("/api/health")
def health_check():
  return jsonify({"status": "OK"}), 200


@app.post("/api/register")
def register():
  data = request.get_json()
  username = data.get("username")
  password = data.get("password")

  conn = sqlite3.connect(DB_NAME) # opens the connection to the db
  cursor = conn.cursor() # creates a cursor/tool (SELECT, INSERT)

  cursor.execute(SQL_INSERT_USER, (username, password)) # Executes the SQL statement
  conn.commit() # Save changes to the database
  conn.close() # Close de connection to the database

  return jsonify({
    "success": True,
    "message": "User registered successfully"  
  }), 201

@app.post("/api/login")
def login():
  data = request.get_json()
  username = data.get("username")
  password = data.get("password")

  conn = sqlite3.connect(DB_NAME)
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
  user = cursor.fetchone()
  conn.close()

  if user and user["password"] == password:
   return success_response("USER LOGGED IN SUCCESSFULLY", dict(user))

@app.get("/api/users/<int:user_id>")
def get_user_by_id(user_id):
  conn = sqlite3.connect(DB_NAME)
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  cursor.execute(SQL_SELECT_USER_BY_ID, (user_id,))
  user = cursor.fetchone()
  conn.close()

  if user:
   return success_response("USER RETRIEVED SUCCESSFULLY",dict(user))
  
  return not_found("User")

@app.put("/api/users/<int:user_id>")
def update_user(user_id):

  data= request.get_json()
  username = data.get("username")
  password = data.get("password")

  conn = sqlite3.connect(DB_NAME)
  cusor = conn.cursor()

  cusor.execute(SQL_SELECT_USER_BY_ID, (user_id,))
  if not cusor.fetchone():# fetchone, retrieves a single row from the result
    conn.close()
    return not_found("User")

  cusor.execute(SQL_UPDATE_USER,(username, password, user_id,))
  conn.close()

  
  return success_response("User updated successfully") 

@app.delete("/api/users/<int:user_id>")
def delete_user(user_id):
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()

  cursor.execute(SQL_SELECT_USER_BY_ID, (user_id,))
  if not cursor.fetchone():
    conn.close()
    return not_found("User")
  cursor.execute(SQL_DELETE_USER, (user_id,))
  conn.commit()
  conn.close()



  return success_response("DELETED SUCCESSFULLY")

@app.get("/api/users")
def get_users():
  conn = sqlite3.connect(DB_NAME)
  conn. row_factory = sqlite3.Row
  cursor = conn.cursor()


  cursor.execute(SQL_SELECT_ALL_USER)
  rows = cursor.fetchall() # retrieves all rows from the result of a query
  conn.close()

  users =[]

  for row in rows:
    user = {
      "id": row["id"],
      "username": row["username"],
    
    }
    users.append(users)
  
  return success_response("USERS RETRIEVED SUCCESSFULLY")



# ---------Expenses--------

@app.post("/api/expenses")
def create_expense():
  data = request.get_json()
  title = data.get("title")
  description = data.get("description")
  amount = data.get("amount")
  date_str = date.today()
  category = data.get("category")
  user_id = data.get("user_id")
  
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()

  cursor.execute("""
    INSERT INTO expenses (title,description,amount,date,category,user_id)
    VALUES (?,?,?,?,?,?)
""", (title,description,amount,date_str,category,user_id))
  conn.commit()
  conn.close()
  return jsonify({
    "success":True,
    "message":"Expenses retrieved successfully"
  }),201

@app.get("/api/expenses/<int:user_id>")
def get_expenses_by_id(user_id):
  conn = sqlite3.connect(DB_NAME)
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  cursor.execute(SQL_SELECT_EXPENSES_BY_ID, (user_id,))
  user = cursor.fetchone()
  conn.close()

  if user:
   return success_response("expense RETRIEVED SUCCESSFULLY",dict(user))
  
  return not_found("expense")


@app.put("/api/expenses/<int:user_id>")
def update_expense(user_id):

  data= request.get_json()
  id = data.get("user_id")
  title = data.get("title")
  description = data.get("description")
  amount = data.get("amount")
  date = data.get("date"),
  category = data.get("catergory")

  conn = sqlite3.connect(DB_NAME)
  cusor = conn.cursor()

  cusor.execute(SQL_SELECT_EXPENSES_BY_ID, (user_id,))
  if not cusor.fetchone():# fetchone, retrieves a single row from the result
    conn.close()
    return not_found("Expense")

  cusor.execute(SQL_UPDATE_EXPENSES,( id, title, description, amount, date, category))
  conn.close()

  
  return success_response( "expense updated successfully")









if __name__ == "__main__":


  init_db()
  app.run(debug=True)