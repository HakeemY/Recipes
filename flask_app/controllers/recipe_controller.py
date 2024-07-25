from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.recipe_model import recipe
from flask_app.models.user_model import User


#routes  that leads to create recipe page

@app.route('/recipes/new')
def create_new_recipe_page():
    print("hello")
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')

    return render_template("create_recipes.html")

#routes that receives form from create recipes page.

@app.route("/recipes/create", methods=["POST"])
def create_new_recipe():
    data ={
        'user_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date': request.form['date'],
        'time': request.form['time']
    }
    
    if not recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    recipe.create_recipes(data)
    return redirect('/recipes/new')


@app.route('/recipes/<int:id>')
def show_one_recipe(id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        session.clear()
        return redirect('/')
    data = {
        'id':id
    }
    
    current_user = User.get_user_by_id({'user_id': session['user_id']})
    session['user_id']
    
    # recipe_data = recipe.read_one_recipe(data)
    return render_template('read_one_recipes.html', recipe_data = recipe.read_one_recipe(data), current_user = current_user)
    
    #route to edit one recipe page
@app.route('/recipes/edit/<int:id>')
def edit_one_page(id):
    if 'user_id' not in session:
        flash('You must be logged in to view this page')
        session.clear()
        return redirect('/')
    
    
    data ={
        "id":id
    }
    # recipe = recipe.read_one_recipe(data)
    return render_template('edit_recipes.html',recipe_data = recipe.read_one_recipe(data))

    
    # route to edit one recipe we currently viewing
@app.route("/recipes/update", methods=['POST'])
def edit_recipe():
    data ={
        'id':request.form['id'],
        'user_id': session['user_id'],
        'name' : request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date' : request.form['date'],
        'time' : request.form['time'],

    }

    id = request.form['id']
    if not recipe.validate_recipe(request.form):
    
        return redirect(f'/recipes/edit/{id}')
    
    recipe.update_recipe(data)
    return redirect('/recipes')
    
@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        flash('You must be logged in')
        session.clear()
        return redirect('/')
    this_recipe  = {
    'id': recipe_id
    }
    recipe.delete_recipe(this_recipe)

    return redirect('/recipes')