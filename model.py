from extensions import db



class Uczen(db.Model):
    __tablename__ = 'uczniowie'
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(80), nullable=False)
    nazwisko = db.Column(db.String(80), nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    haslo = db.Column(db.String(20), nullable=False)

    # Foreign key, aby powiązać ucznia z klasą
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
    
    # Relacja z uczniem - jedna klasa może mieć wielu uczniów
    uczniowie = db.relationship('Uczen', backref='klasa', lazy=True)

    def __repr__(self):
        return f'<Klasa {self.nazwa}>'