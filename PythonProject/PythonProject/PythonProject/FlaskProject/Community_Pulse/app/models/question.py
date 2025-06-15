# from app.models import db
from app.extensions import db



class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='NO ACTION'), nullable=True)
    text = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    # creating relationships to other models
    user = db.relationship('User', back_populates='questions', lazy=True, cascade='none')
    responses = db.relationship('Response', back_populates='question',
                                lazy=True, cascade='all, delete-orphan')


    def repr(self):
        return f'Question: {self.text}'


class Statistic(db.Model):
    __tablename__ = 'statistics'

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)


    def repr(self):
        return (f'Statistic for Question {self.question_id}: {self.agree_count} agree, '
                f'{self.disagree_count} disagree')