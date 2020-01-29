import datetime
from application import db
from application.models.category import Category


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post id : %r,  title : %r,  body : %r>' % (self.id, self.title, self.body)

    def get_title(self):
        return self.title

    def get_id(self):
        return self.id

    def get_info(self):
        return '<Post id : %r,  title : %r,  body : %r,  category : %r,  pub_date : %r>' % (self.id, self.title, self.body, self.category.get_name(), str(self.pub_date))
