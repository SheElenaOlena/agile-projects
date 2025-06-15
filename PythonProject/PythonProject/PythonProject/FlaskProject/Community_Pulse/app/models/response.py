from app.models import db


class Response(db.Model):
    tablename = 'responses'

    # creating some columns
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='NO ACTION'), nullable=True)
    is_agree = db.Column(db.Boolean, nullable=False)  # True if agree, False if disagree
    text = db.Column(db.String(250), nullable=True)


    # creating a relationships to other models
    user = db.relationship('User', back_populates='responses', lazy=True, cascade='none')
    question = db.relationship('Question', back_populates='responses', lazy=True)

    def repr(self):
        return f'For questioin with id {self.question_id} response is: {self.is_agree}'