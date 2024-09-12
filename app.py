import os
from flask import Flask, request, redirect, url_for, session
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Retrieve sensitive data from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# Index route
@app.route('/')
def home():
    return 'Welcome! <a href="/login">Login</a>'

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if username and password are correct
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('secret'))
        else:
            return 'Invalid credentials, try again!'
    
    # Show login form
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# Secret route (accessible only if logged in)
@app.route('/secret')
def secret():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return 'This is a secret page!'

# Logout route
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return 'Logged out! <a href="/">Home</a>'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
