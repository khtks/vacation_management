from application import db
from application.models.user import User


class RemainVacation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(30), db.ForeignKey('user.google_id'), unique=True, nullable=False)
    user = db.relationship('User', backref=db.backref('remain_vacation', cascade='all, delete', lazy=True))
    number_of_years = db.Column(db.Integer, nullable=False)
    total_vacation = db.Column(db.Float, nullable=False)
    remain_vacation = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "\n< Remain Vacation Google id : %r,  Number of years : %r,  Total vacation : %r,  Remain vacation : %r >" % (self.user.google_id, self.number_of_years, self.total_vacation, self.remain_vacation)

    def get_id(self):
        return self.id
