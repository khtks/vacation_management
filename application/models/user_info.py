from application import db
import datetime


class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(30), nullable=False)
    ko_name = db.Column(db.String(5), default="None")
    en_name = db.Column(db.String(10), nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<User Info> Id : %r,   Google id : %r,  Name : %r,  Entry date : %r,  Admin : %r" % (self.id, self.google_id, self.en_name, str(self.entry_date), self.admin)
