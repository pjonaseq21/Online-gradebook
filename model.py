from extensions import db



class Uczen(db.Model):
    __tablename__ = 'uczniowie'
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(80), nullable=False)
    nazwisko = db.Column(db.String(80), nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    haslo = db.Column(db.String(20), nullable=False)

    klasa_id = db.Column(db.Integer, db.ForeignKey('klasy.id'), nullable=False)

    def __repr__(self):
        return f'<Uczen {self.imie} {self.nazwisko}>'

nauczyciel_klasa = db.Table('nauczyciel_klasa',
    db.Column('nauczyciel_id', db.Integer, db.ForeignKey('nauczyciele.id'), primary_key=True),
    db.Column('klasa_id', db.Integer, db.ForeignKey('klasy.id'), primary_key=True)
)

class Nauczyciel(db.Model):
    __tablename__ = 'nauczyciele'
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(80), nullable=False)
    nazwisko = db.Column(db.String(80), nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    haslo = db.Column(db.String(20), nullable=False)

    klasy = db.relationship('Klasa', secondary='nauczyciel_klasa', backref='nauczyciele')

    def __repr__(self):
        return f'<Nauczyciel {self.imie} {self.nazwisko}>'


class Klasa(db.Model):
    __tablename__ = 'klasy'
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(20), nullable=False, unique=True)
    przedmioty = db.relationship('PlanLekcji', backref='klasa', lazy=True)
    uczniowie = db.relationship('Uczen', backref='klasa', lazy=True)

    def __repr__(self):
        return f'<Klasa {self.nazwa}>'

class Ogloszenia(db.Model):
    __tablename__ = 'ogloszenia'
    id = db.Column(db.Integer, primary_key=True)
    temat = db.Column(db.String(80), nullable=False)
    tresc = db.Column(db.String(120), nullable=False)
    def __repr__(self):
            return f'<Klasa {self.temat}>'

class Ocena(db.Model):
    __tablename__ = 'oceny'
    id = db.Column(db.Integer, primary_key=True)
    wartosc = db.Column(db.Float, nullable=False) 

    uczen_id = db.Column(db.Integer, db.ForeignKey('uczniowie.id'), nullable=False)
    klasa_id = db.Column(db.Integer, db.ForeignKey('klasy.id'), nullable=False)

    uczen = db.relationship('Uczen', backref=db.backref('oceny', lazy=True))
    klasa = db.relationship('Klasa', backref=db.backref('oceny', lazy=True))

    def __repr__(self):
        return f'<Ocena {self.wartosc} dla ucznia {self.uczen_id} w klasie {self.klasa_id}>'

from datetime import datetime

class Wiadomosc(db.Model):
    __tablename__ = 'wiadomosci'
    
    id = db.Column(db.Integer, primary_key=True)
    nadawca_id = db.Column(db.Integer, db.ForeignKey('nauczyciele.id'), nullable=False)
    odbiorca_id = db.Column(db.Integer, db.ForeignKey('uczniowie.id'), nullable=False)
    tresc = db.Column(db.Text, nullable=False)
    data_wyslania = db.Column(db.DateTime, default=datetime.utcnow)

    nadawca = db.relationship('Nauczyciel', backref='wiadomosci_nadawca')
    odbiorca = db.relationship('Uczen', backref='wiadomosci_odbiorca')

    def __repr__(self):
        return f'<Wiadomosc od {self.nadawca_id} do {self.odbiorca_id}: {self.tresc}>'

class Przedmiot(db.Model):
    __tablename__ = 'przedmioty'
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(50), nullable=False)

    plan_lekcji = db.relationship('PlanLekcji', backref='przedmiot', lazy=True)

    def __repr__(self):
        return f'<Przedmiot {self.nazwa}>'

class PlanLekcji(db.Model):
    __tablename__ = 'plan_lekcji'
    id = db.Column(db.Integer, primary_key=True)
    klasa_id = db.Column(db.Integer, db.ForeignKey('klasy.id'), nullable=False)
    przedmiot_id = db.Column(db.Integer, db.ForeignKey('przedmioty.id'), nullable=False)
    dzien_tygodnia = db.Column(db.String(20), nullable=False)
    godzina = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<PlanLekcji Klasa: {self.klasa_id}, Przedmiot: {self.przedmiot_id}, Dzień: {self.dzien_tygodnia}, Godzina: {self.godzina}>'
