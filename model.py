from extensions import db


class Uczen(db.Model):
    __tablename__ = 'Uczniowie'
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(80), unique=False, nullable=False)
    nazwisko = db.Column(db.String(80), unique=False, nullable=False)
    klasa = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Nauczyciel(db.Model):
    __tablename__ = 'Nauczyciel'
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(80), unique=False, nullable=False)
    nazwisko = db.Column(db.String(80), unique=False, nullable=False)
    login = db.Column(db.String(20), unique=False, nullable=False)
    haslo = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'