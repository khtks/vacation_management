from application import db


class RemainVacation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(30), db.ForeignKey('user.google_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('used_vacations', lazy=True))
    number_of_year = db.Column(db.Integer, nullable=False)
    total_vacation = db.Column(db.Float, nullable=False)
    remain_vacation = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "\n< Remain Vacation Google id : %r,  Number of year : %r,  Total vacation : %r,  Remain vacation : %r >" % (self.google_id, self.number_of_year, self.total_vacation, self.remain_vacation)

    def get_id(self):
        return self.id
