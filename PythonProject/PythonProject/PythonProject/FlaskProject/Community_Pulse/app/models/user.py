from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    # creating some columns
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    # creating a relationships to other models
    questions = db.relationship('Question', back_populates='user', lazy=True)
    responses = db.relationship('Response', back_populates='user', lazy=True)


    def __repr__(self):
        return f'ID: {self.id}\nNickname: {self.nickname}'