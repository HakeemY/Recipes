from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import recipe
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)  


@app.route('/')
def index():
  return render_template('index.html')


# route that creates a user

@app.route('/users/registration', methods=['POST'])
def registration():

    if not User.validate_user(request.form):
      return redirect('/')
    

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
   
    new_user = {
      'first_name' : request.form['first_name'],
      'last_name' : request.form['last_name'],
      'email' : request.form['email'],
      'password' : pw_hash
    }
    
    user_id = User.create_user(new_user)
    
    session['user_id'] = user_id
    
    return redirect('/recipes')

# route that redirects us to our dashborad.html

@app.route('/recipes')
def dashboard():
  if 'user_id' in session:
    user_id = session['user_id']
  
    data = {
      'user_id': user_id
    }
    # we need to refrence here a method call that gets data by that one user id, and then save that value to a variable
    current_user = User.get_user_by_id(data)
    recipes = recipe.read_all_recipes()
    return render_template("dashboard.html", current_user = current_user, recipes = recipes)
  else:
    return redirect('/')

# this route is for Loggin in

@app.route('/users/login', methods=["POST"])
def login():
  data = {
    'email' : request.form['email']
  }
  user_in_db = User.read_one_user_by_email(data) 
  
  if not user_in_db:
    flash("invalid email or password", "login")
    return redirect('/')
  
  if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
    flash("invalid email or password", "login")
    return redirect('/')
  session['user_id'] = user_in_db.id
  return redirect('/recipes')
  
@app.route('/logout')
def destroy_session():
  session.clear()
  print("session is now cleared")
  return redirect('/')