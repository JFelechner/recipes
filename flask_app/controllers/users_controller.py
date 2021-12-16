
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/users/register", methods=['POST'])
def register_user():
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'confirm_password' : request.form['confirm_password']
    }
    if User.validate_new_user(data):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        new_user_data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password' : pw_hash
        }
        User.create_new_user(new_user_data)
        flash("User created! log in with that account now.")
        return redirect('/')
    
    else: 
        print ('user DOES NOT pass validation')
        return redirect('/')



@app.route('/users/login', methods=['POST'])
def login_user():
    #first: get user from DB
    user = User.get_user_by_email(request.form)
    if user == None:
        flash("No user with that email found.")
        return redirect('/')
    #then: hash input password and compare against DB
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect password.")
        return redirect('/')
    #finally: user is 'logged in'
    print('user passes validation')
    session['user_id']=user.id
    session['user_first_name'] = user.first_name
    session['user_email'] = user.email
    return redirect('/dashboard')



@app.route('/dashboard')
def success():
    if 'user_id' not in session:
        flash("This page is only available to logged in users.")
        return redirect('/')
    recipes = Recipe.get_all_recipes()
    return render_template('dashboard.html', recipes = recipes)



@app.route('/users/logout')
def logout():
    session.clear()
    flash("You've successfully logged out!")
    return redirect('/')