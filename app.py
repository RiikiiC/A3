from flask import Flask, render_template, request, session, redirect
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

cursor = conn.cursor(dictionary=True)

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

@app.route("/process-login", methods=['POST'])
def process_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor.execute('''SELECT * 
                       FROM `User` 
                       WHERE `email` = %s 
                       AND `password` = %s''',(email, password))
        
        user = cursor.fetchone()

        if user:
            session['userId'] = user['userId']
            session['username'] = user['username']
            session['role'] = user['role']

            if user['role'] == 'admin':
                return redirect("/admin")
            else:
                return redirect("/")
        else:
            return render_template("not-logged-in.html")
        

@app.route("/admin")
def admin_dashboard():
    if 'userId' not in session or session.get('role') != 'admin':
        return "NOPE! YOU CANNOT SEE THIS!"
    return render_template("admin/dashboard.html", role=session.get('role'))


@app.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")


@app.route("/article/<name>")
def article(name):
    return render_template("articles/" + name + ".html")


@app.route("/admin/articles")
def admin_articles():
    if 'userId' not in session or session.get('role') != 'admin':
        return "NOPE! YOU CANNOT SEE THIS!"

    cursor.execute("SELECT * FROM Articles")
    articles = cursor.fetchall()

    return render_template("admin/article-list-record.html", role=session.get('role'), articles=articles)

@app.route("/admin/article-add", methods=['GET', 'POST'])
def admin_article_add():
    if 'userId' not in session or session.get('role') != 'admin':
        return "NOPE! YOU CANNOT SEE THIS!"
    
    if request.method == 'GET':
        return render_template("admin/article-add.html", role=session.get('role'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        cursor.execute('''INSERT INTO `Articles` (title, content)
            VALUES (%s, %s)
                ''', (title, content))
        conn.commit()

        return redirect("/admin/articles")


@app.route("/admin/article-edit/<int:article_id>", methods=['GET', 'POST'])
def admin_article_edit(article_id):
    if 'userId' not in session or session.get('role') != 'admin':
        return "NOPE! YOU CANNOT SEE THIS!"
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Articles WHERE articleId = %s", (article_id,))
        article = cursor.fetchone()
        return render_template("admin/article-edit.html", role=session.get('role'), article=article)
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        cursor.execute(
            "UPDATE Articles SET title = %s, content = %s WHERE articleId = %s",
            (title, content, article_id)
        )            
        conn.commit()

        return redirect("/admin/articles")


@app.route("/admin/article-delete/<int:article_id>", methods=['GET', 'POST'])
def admin_article_delete(article_id):
    if 'userId' not in session or session.get('role') != 'admin':
        return "NOPE! YOU CANNOT SEE THIS!"
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Articles WHERE articleId = %s", (article_id,))
        article = cursor.fetchone()
        return render_template("admin/article-delete.html", role=session.get('role'), article=article)
    
    if request.method == 'POST':
        cursor.execute(
            "DELETE FROM Articles WHERE articleId = %s", 
            (article_id,)
        )            
        conn.commit()

        return redirect("/admin/articles")


@app.route("/admin/set-featured/<int:article_id>", methods=['GET', 'POST'])
def admin_set_featured(article_id):
    if 'userId' not in session or session.get('role') != 'admin':
        return "NOPE! YOU CANNOT SEE THIS!"
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Articles WHERE articleId = %s", (article_id,))
        article = cursor.fetchone()
        return render_template("admin/set-featured.html", role=session.get('role'), article=article)
    
    if request.method == 'POST':
        cursor.execute("UPDATE Articles SET Featured = 0")  
        cursor.execute(
            "UPDATE Articles SET Featured = 1 WHERE articleId = %s", 
            (article_id,)
        )            
        conn.commit()

        return redirect("/admin/articles")




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