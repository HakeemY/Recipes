from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
  def __init__(self, data):
    self.id = data['id']
    self.first_name = data['first_name']
    self.last_name = data['last_name']
    self.email = data['email']
    self.password = data['password']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    
    
    
    
# this is the method to create a user into our database

  @classmethod
  def create_user(cls,data):
      query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"  
      results = connectToMySQL(DB).query_db(query, data)
      
      return results
# create validation method

  @staticmethod
  def validate_user(user):
    is_valid = True
    
    if len(user['first_name']) < 3:
              flash("First Name must be at least 3 characters.", "registration")
              is_valid = False
    if len(user['last_name']) < 3:
              flash("Last Name must be at least 3 characters.", "registration")
              is_valid = False
              
    if len(user['email']) < 3:
              flash("Email must be at least 3 characters.", "registration")
              is_valid = False
              
              
    
    # checks to see if user has input valid email according to regex requirement
    if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "registration")
            print("We've reached this part of our regex if statement")
            is_valid = False
            
            
   
    # checks to see if email is already in use
    if (re.fullmatch(EMAIL_REGEX, user['email'])):
      this_user = {
        'email': user['email']
      }
      results = User.check_database(this_user)
      if len(results) != 0:
            flash('Email is already in use, please use a different email', "registration")
            is_valid = False
            
            
            
    # checks the password length          
    
    if len(user['password']) < 3:
              flash("Password must be at least 3 characters.", "registration")
              
              is_valid = False
    #check to see if the password has at least one digit
    if(re.search('[0-9]', user['password']) == None ):
              flash("Password requires at least one digit", "registration")
              is_valid = False
              
    #check to see if the password has at least one upper case letter          
    if(re.search('[A-Z]', user['password']) == None ):
              flash("Password requires at least one upper case letter", "registration")
              is_valid = False
              
    
    
    #checks if password and password confirmation match          
    if (user['password'] != user['password_confirmation']):
            flash("Passwords do not match!", "registration")
            
    return is_valid
  
  @staticmethod
  def validate_login(user):
    is_valid = True
    if len(user['email']) < 3:
              flash("Email must be at least 3 characters.", "login")
              is_valid = False
              
    if len(user['password']) < 3:
              flash("Password must be at least 3 characters.", "login")
              is_valid = False
              
  @classmethod
  def check_database(cls, data):
      query = "SELECT * FROM users WHERE email = %(email)s"
      
      results = connectToMySQL(DB).query_db(query, data)
      
      return results
    
  #Read One User from Database
  
  @classmethod
  def get_user_by_id(cls, data):
    query = "SELECT * FROM users WHERE id = %(user_id)s;"
    result = connectToMySQL(DB).query_db(query,data)
    return cls(result[0])
  

  # Read one User from the Database by the email
  @classmethod
  def read_one_user_by_email(cls,data):
    query = 'SELECT * FROM users WHERE email = %(email)s'
    results = connectToMySQL(DB).query_db(query,data)
    
    if not results:
      return None
    
    return User(results[0])