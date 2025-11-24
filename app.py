from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import os
import mysql.connector

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

conn = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB'],
    port=8889
)

cursor = conn.cursor()

@app.route("/")
def hompage():
    return render_template("homepage.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/process-register", methods=['POST'])
def process_register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    role = "member"

    cursor.execute('''INSERT INTO `User` (username, email, password, role)
        VALUES (%s, %s, %s, %s)
            ''', (username, email, password, role))
    conn.commit()

    return render_template("login.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")



@app.route("/article/<name>")
def article(name):
    return render_template("articles/" + name + ".html")



@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/process-contact", methods=["POST"])
def process_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    role = request.form.get('role')

    industry = 1 if request.form.get("industry") else 0
    technical = 1 if request.form.get("technical") else 0
    career = 1 if request.form.get("career") else 0

    cursor.execute("""
        INSERT INTO Contacts (name, email, industry, technical, career, role)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, email, industry, technical, career, role))

    conn.commit()

    return render_template("submit-contact.html")