from application import db


class UsedVacation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(30), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    reference = db.Column(db.String(30), nullable=True)

    def __ref__(self):
        return "<Used Vacation> Google id : %r,  Start date : %r,  End date : %r,  type : %r" % (self.google_id, self.start_date, self.end_date, self.type)