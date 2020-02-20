from application import db


class UsedVacation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(30), nullable=False, unique=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    reference = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return "<Used Vacation> Google id : %r,  Start date : %r,  End date : %r,  type : %r" % (self.google_id, str(self.start_date), str(self.end_date), self.type)

    def get_period(self):
        period = self.end_date - self.start_date

        if period.days < 0:
            raise Exception("End date earlier than Start date")

        return period
