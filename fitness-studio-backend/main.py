import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Database Connection (Using Replit's SQLite)
db = sqlite3.connect('fitness_data.db', check_same_thread=False)
cursor = db.cursor()

# Create Tables (If they don't exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT
    )
''')
db.commit()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plans.html')
def plans():
    return render_template('plans.html')

@app.route('/cart.html')
def cart():
    return render_template('cart.html')

@app.route('/about us.html')
def about():
    return render_template('about us.html')

@app.route('/Gallery.html')
def gallery():
    return render_template('Gallery.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if email:
        try:
            cursor.execute("INSERT OR IGNORE INTO emails (email) VALUES (?)", (email,))
            db.commit()
            return 'Subscribed!'
        except sqlite3.IntegrityError:
            return 'Email already exists in the list.'  # Handle duplicate emails
    return 'Invalid email.'

@app.route('/contact', methods=['POST'])
def contact_form():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    if name and email and message:
        try:
            cursor.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", (name, email, message))
            db.commit()
            return 'Message sent!'
        except Exception as e:
            return f'Error sending message: {e}'
    return 'Please fill out all the fields.'

if __name__ == '__main__':
    app.run(debug=True)