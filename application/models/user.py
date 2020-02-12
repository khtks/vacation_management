from application import db
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(30), nullable=False, unique=True)
    ko_name = db.Column(db.String(10), default="None")
    en_name = db.Column(db.String(10), nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    admin = db.Column(db.Integer, default=False)

    def __repr__(self):
        return "\n< USER INFO  Id : %r,   Google id : %r,  Name : %r,  Entry date : %r,  Admin : %r >" % (self.id, self.google_id, self.en_name, str(self.entry_date), self.admin)

    def get_id(self):
        return self.id

    def get_google_id(self):
        return self.google_id

    def get_en_name(self):
        return self.en_name
