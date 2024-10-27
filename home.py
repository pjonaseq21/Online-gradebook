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


@app.route('/klasa/<string:klasa_id>')
def view_class(klasa_id):
    klasa_solid = Klasa.query.filter_by(nazwa=klasa_id).first()
    uczniowie = Uczen.query.filter_by(klasa_id=klasa_solid.id).all()
    if uczniowie:
        return render_template('show_class.html',klasa=klasa_id, uczniowie=uczniowie)

    return render_template('show_class.html',klasa=klasa_id)

@app.route('/klasa/<string:klasa_id>/add_student')
def add_student_form(klasa_id):
    print(klasa_id)
    return render_template('addstudent_view.html',klasa=klasa_id)

@app.route('/add_uczen/<string:klasa_id>', methods=['POST'])
def add_uczen(klasa_id):
    if request.method == 'POST':
        imie = request.form['imie']
        nazwisko = request.form['nazwisko']
        login = request.form['login']
        haslo = request.form['haslo']
        klasa_id = klasa_id
        klasa = Klasa.query.filter_by(nazwa=klasa_id).first()

        if klasa:
            nowy_uczen = Uczen(imie=imie, nazwisko=nazwisko, login=login, haslo=haslo, klasa_id=klasa.id)
            db.session.add(nowy_uczen)
            db.session.commit()
            print(klasa_id, "@@@@")
            return redirect(url_for('view_class', klasa_id=klasa_id))
        else:
            return "Klasa nie istnieje!"

    return render_template('add_student.html')



@app.route("/")
def home():
     #tworzenie nowego usera
    #new_user = Nauczyciel(imie="Jan", nazwisko="Kowalski", login="qwerty",haslo="qwerty")
    #db.session.add(new_user)
    #db.session.commit()

    if 'logged_in' in session:
        print("Witaj w domu!")
        nauczyciel = Nauczyciel.query.filter_by(id=session["id"]).first()

        klasy_nauczyciela = nauczyciel.klasy
        print(klasy_nauczyciela)
        return render_template("main.html",klasy=klasy_nauczyciela)
    else:
        return render_template("main.html")

   

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



