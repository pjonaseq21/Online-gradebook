from flask import Flask,render_template,request, redirect, url_for, session,Response
from flask_sqlalchemy import SQLAlchemy
from model import Uczen,Nauczyciel,Klasa,nauczyciel_klasa,Ogloszenia,Ocena,Wiadomosc,Przedmiot,PlanLekcji
from extensions import db 
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

import io

app = Flask(__name__)
app.secret_key = 'supersecretkey'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

import random

def generuj_plan_lekcji():
    dni_tygodnia = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek']
    godziny = ['08:00', '09:00', '10:00', '11:00', '12:00']

    klasy = Klasa.query.all()
    przedmioty = Przedmiot.query.all()

    for klasa in klasy:
        for dzien in dni_tygodnia:
            for godzina in godziny:
                przedmiot = random.choice(przedmioty)
                new_plan = PlanLekcji(klasa_id=klasa.id, przedmiot_id=przedmiot.id, dzien_tygodnia=dzien, godzina=godzina)
                db.session.add(new_plan)

    db.session.commit()

@app.route('/generuj_plan')
def generuj_plan():
    generuj_plan_lekcji()
    return "Plan lekcji został wygenerowany!", 200

with app.app_context():
    db.create_all()
    przedmioty = ['Matematyka', 'Programowanie', 'Bazy Danych', 'Sieci Komputerowe', 'Inżynieria Oprogramowania']
    for przedmiot in przedmioty:
        new_przedmiot = Przedmiot(nazwa=przedmiot)
        db.session.add(new_przedmiot)
    db.session.commit()   
@app.route('/dodaj_ocene/<string:uczen_id>/<string:klasa_id>', methods=['POST'])
def add_grade(uczen_id,klasa_id):
    wartosc = request.form['wartosc']
    nowa_ocena = Ocena(wartosc=wartosc, uczen_id=uczen_id, klasa_id=klasa_id)
    db.session.add(nowa_ocena)
    db.session.commit()

    return redirect(url_for('view_class',klasa_id=klasa_id))

@app.route('/dodaj_ocene/<string:uczen_id>/<string:klasa_id>')
def add_grade_landingpage(uczen_id,klasa_id):
    uczen = Uczen.query.get(uczen_id)
    oceny_ucznia = uczen.oceny
    for ocena in oceny_ucznia:
        print(ocena.wartosc)
    return render_template('add_grade.html',uczen_id=uczen_id,klasa_id=klasa_id,oceny=oceny_ucznia)
    
@app.route("/wyslij_wiadomosc/<int:uczen_id>")
def send_message(uczen_id):


    return render_template("send_message.html",uczen_id=uczen_id)
@app.route('/wykres_ocen/<string:klasa_id>')
def wykres_ocen(klasa_id):
    print(klasa_id)
    Oceny_uczniow = Ocena.query.filter_by(klasa_id=klasa_id).all()
    print(Oceny_uczniow)
    if Oceny_uczniow:
        oceny_lista = []
        for oceny in Oceny_uczniow:
            oceny_lista.append(oceny.wartosc)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(oceny_lista, bins=range(1, 7), align='left', rwidth=0.8)
        ax.yaxis.get_major_locator().set_params(integer=True)  
        ax.set_xlabel('Ocena')
        ax.set_ylabel('Liczba wystąpień')
        ax.set_title(f'Rozkład ocen w klasie {klasa_id}')

        output = io.BytesIO()
        plt.savefig(output, format='png')
        output.seek(0)
        return Response(output.getvalue(), mimetype='image/png')
@app.route('/klasa/<string:klasa_id>')
def view_class(klasa_id):
    klasa_solid = Klasa.query.filter_by(nazwa=klasa_id).first()
    uczniowie = Uczen.query.filter_by(klasa_id=klasa_solid.id).all()
    plan = PlanLekcji.query.filter_by(klasa_id=klasa_solid.id).all()
    print(plan, "@@@@")
    if uczniowie:
        return render_template('show_class.html',klasa=klasa_id, uczniowie=uczniowie,plan =plan)

    return render_template('show_class.html',klasa=klasa_id, plan =plan)

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

@app.route("/send/announcement")
def send_announcement():

    return render_template("send_announcement.html")

@app.route("/addannouncement", methods=['POST'])
def addannouncement():
    if request.method == "POST":
        temat = request.form['temat']
        tresc = request.form['tresc']
        new_ogloszenie = Ogloszenia(temat=temat, tresc=tresc)
        db.session.add(new_ogloszenie)
        db.session.commit()
        return redirect(url_for('home'))
@app.route("/sendmessage/<int:uczen_id>", methods=['POST'])
def sendmessage(uczen_id):
    if request.method == "POST":
        nadawca_id = session['id'] 
        tresc = request.form['tresc']
        odbiorca_id = uczen_id
        nowa_wiadomosc = Wiadomosc(nadawca_id=nadawca_id, odbiorca_id=odbiorca_id, tresc=tresc)
        db.session.add(nowa_wiadomosc)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/show_messages')
def show_messages():
    if 'logged_in' not in session:
        flash("Musisz być zalogowany, aby zobaczyć wiadomości.")
        return redirect(url_for('login'))

    odbiorca_id = session['id']
    wiadomosci = Wiadomosc.query.filter_by(odbiorca_id=odbiorca_id).all()
    
    return render_template('view_messages.html', wiadomosci=wiadomosci)
    
@app.route("/")
def home():
     #tworzenie nowego usera
    #new_user = Nauczyciel(imie="Jan", nazwisko="Kowalski", login="qwerty",haslo="qwerty")
    #db.session.add(new_user)
    #db.session.commit()

    if 'logged_in' in session:
        print("Witaj w domu!")
        nauczyciel = Nauczyciel.query.filter_by(id=session["id"]).first()
        uczen = Uczen.query.filter_by(id=session["id"]).first()
        if nauczyciel:
            klasy_nauczyciela = nauczyciel.klasy
            print(klasy_nauczyciela)
            ogloszenia = Ogloszenia.query.all()
            if ogloszenia:
                print(ogloszenia)
                return render_template("main.html",klasy=klasy_nauczyciela,ogloszenia=ogloszenia)
            else:
                return render_template("main.html",klasy=klasy_nauczyciela)
        if uczen:
            oceny_ucznia = uczen.oceny
            plan = PlanLekcji.query.filter_by(klasa_id=uczen.klasa_id)
            print(plan)
            return render_template("main.html",ogloszenia = Ogloszenia.query.all(), oceny=oceny_ucznia,plan=plan)

    else:
        return render_template("main.html")

   

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        login = request.form['login']
        haslo = request.form['haslo']
        nauczyciel = Nauczyciel.query.filter_by(login=login, haslo=haslo).first()
        uczen = Uczen.query.filter_by(login=login, haslo=haslo).first()
       
        if nauczyciel:
            session["id"] = nauczyciel.id
            session["imie"] = nauczyciel.imie
            session["nazwisko"] = nauczyciel.nazwisko
            session['logged_in'] = True
            session["uczen"] = False

            return redirect(url_for('home'))
        elif uczen:
            session["id"] = uczen.id
            session["imie"] = uczen.imie
            session["nazwisko"] = uczen.nazwisko
            session['logged_in'] = True
            session["uczen"] = True
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
        generuj_plan_lekcji()

        return redirect(url_for('home'))  




