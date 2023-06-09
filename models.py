from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def setup_db(app):
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()

class TransactionWrapper(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class Movie(TransactionWrapper):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genre = db.Column (db.ARRAY(db.String()), nullable=False, default=[])
    release_date = db.Column(db.DateTime)
    participances = db.relationship('Participance',backref='movie', lazy='joined', cascade="all, delete,save-update")

class Person(TransactionWrapper):    
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.DateTime)
    gender = db.Column(db.String)
    participances = db.relationship('Participance',backref='person', lazy='joined', cascade="all, delete,save-update")

class Mission(TransactionWrapper):
    __tablename__ = 'mission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)    
    participances = db.relationship('Participance',backref='mission', lazy='joined', cascade="all, delete,save-update")

class Participance(TransactionWrapper):
    __tablename__ ='participance'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.ForeignKey ('person.id') ,nullable=False)
    movie_id =  db.Column(db.ForeignKey ('movie.id') ,nullable=False)
    mission_id =  db.Column(db.ForeignKey ('mission.id') ,nullable=False)