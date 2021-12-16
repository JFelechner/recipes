
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.recipe_model import Recipe



@app.route('/add_recipe')
def add_recipe():
    if 'user_id' not in session:
        flash("This page is only available to logged in users.")
        return redirect('/')
    return render_template('add_recipe.html')




@app.route("/add_recipe/create", methods=['POST'])
def create_recipe():
    if Recipe.validate_recipe(request.form):
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instruction': request.form['instruction'],
            'prep_time': request.form['prep_time'],
            'date_created': request.form['date_created'],
            'creator_id': session['user_id']
        }
        Recipe.create_recipe(data)
        return redirect('/dashboard')
    else:
        return redirect('/add_recipe')




@app.route('/recipe/<int:recipe_id>')
def single_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)
    return render_template('recipe.html', recipe=recipe)





@app.route('/recipe/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    data = {
        'id' : recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)
    if recipe.creator.id != session['user_id']:
        return redirect ('/dashboard')
    return render_template('edit_recipe.html', recipe = recipe)





@app.route('/recipe/<int:recipe_id>/update', methods=['POST'])
def update_recipe(recipe_id):
    if Recipe.validate_recipe(request.form):
        data = {
        'id' : recipe_id
        }
        recipe = Recipe.get_recipe_by_id(data)
        if recipe.creator.id != session['user_id']:
            return redirect ('/dashboard')
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instruction': request.form['instruction'],
            'prep_time': request.form['prep_time'],
            'date_created': request.form['date_created'],
            'id' : recipe_id
        }
        Recipe.update_recipe(data)
        return redirect(f'/recipe/{recipe.id}')
    else:
        return redirect(f'/recipe/{recipe_id}/edit')






@app.route('/recipe/<int:recipe_id>/delete')
def confirm_recipe_delete(recipe_id):
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)
    if recipe.creator.id != session['user_id']:
        return redirect('/dashboard')
    return render_template('confirm_recipe_delete.html', recipe=recipe)





@app.route('/recipe/<int:recipe_id>/confirm_delete')
def delete_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)
    if recipe.creator.id == session['user_id']:
        Recipe.delete_recipe(data)
    return redirect('/dashboard')



