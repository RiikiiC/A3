from flask import Flask, render_template
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
    database=app.config['MYSQL_DB']
)

cursor = conn.cursor()

@app.route("/")
def hompage():
    return render_template("homepage.html")

@app.route("/")
def about():
    return render_template("about.html")

@app.route("/")
def contact():
    return render_template("contact.html")