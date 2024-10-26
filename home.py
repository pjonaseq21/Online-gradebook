from flask import Flask,render_template,request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from model import Uczen,Nauczyciel,Klasa,nauczyciel_klasa
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
        nauczyciel = Nauczyciel.query.filter_by(id=session["id"]).first()

        klasy_nauczyciela = nauczyciel.klasy
        print(klasy_nauczyciela)
    #tworzenie nowego usera
    #new_user = Nauczyciel(imie="Jan", nazwisko="Kowalski", login="qwerty",haslo="qwerty")
    #db.session.add(new_user)
    #db.session.commit()
    return render_template("main.html",klasy=klasy_nauczyciela)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        login = request.form['login']
        haslo = request.form['haslo']
        nauczyciel = Nauczyciel.query.filter_by(login=login, haslo=haslo).first()

       
        if nauczyciel:
            session["id"] = nauczyciel.id
            session["imie"] = nauczyciel.imie
            session["nazwisko"] = nauczyciel.nazwisko
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Nieprawidłowe dane logowania")
        
    return render_template("login.html")
    
@app.route("/add_class", methods=[ 'POST'])
def add_class():
    if request.method == "POST":
        klasa_nazwa = request.form['class']
        print(klasa_nazwa)

        nauczyciel_id = session['id']
        nauczyciel = Nauczyciel.query.get(nauczyciel_id)

        klasa = Klasa.query.filter_by(nazwa=klasa_nazwa).first()

        if not klasa:
            klasa = Klasa(nazwa=klasa_nazwa)
            db.session.add(klasa)  #

        if klasa not in nauczyciel.klasy:
            nauczyciel.klasy.append(klasa)  

        db.session.commit()

        return redirect(url_for('home'))  

        return redirect(url_for('home'))



