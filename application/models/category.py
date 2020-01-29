from application import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category id : %r,  name : %r>' % (self.id, self.name)

    def get_name(self):
        return self.name
