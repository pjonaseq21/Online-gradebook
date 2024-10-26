from flask import Flask,render_template,request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from model import Uczen,Nauczyciel
from extensions import db 

app = Flask(__name__)
app.secret_key = 'supersecretkey'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    if 'logged_in' in session:
        print("Witaj w domu!")
    #tworzenie nowego usera
    #new_user = Nauczyciel(imie="N", nazwisko="Drałus", login="qwerty",haslo="qwerty")
    #db.session.add(new_user)
    #db.session.commit()
    return render_template("main.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        login = request.form['login']
        haslo = request.form['haslo']
        nauczyciel = Nauczyciel.query.filter_by(login=login, haslo=haslo).first()
        if nauczyciel:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Nieprawidłowe dane logowania")
        
    return render_template("login.html")
    

