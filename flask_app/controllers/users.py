from flask_app import app
from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)


@app.route('/')
def register(): 
    return render_template('register.html')

@app.route('/login')
def login(): 
    return render_template('login.html')

@app.route('/process_register', methods = ['POST'])
def process_register():
      # validate the form here ...
     # if there are errors:
    # We call the staticmethod on User model to validate
    if not User.validate_user(request.form):
        # redirect to the route where the user form is rendered.
        return redirect('/')

    #hashing user password using bcrypt
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hashed_pw
        
    }
    id = User.save(data)
    #save user id to session
    session['user_id'] = id
    return redirect('/home')

#process login
@app.route('/process_login', methods = ['POST'])
def process_login():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    return redirect('/login')








