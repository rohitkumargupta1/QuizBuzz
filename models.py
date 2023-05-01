# from app import db
from extensions import db
from datetime import datetime

# Subject Table
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable = False)
    slug = db.Column(db.String(255), unique=True, nullable = False)

    def __str__(self):
        return self.name

# Chapter Table
class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable = False)
    slug = db.Column(db.String(256), nullable = False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    subject = db.relationship('Subject', backref=db.backref('chapters'))

    def __str__(self):
        return self.name

# Question Table
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable = False)
    explanation = db.Column(db.Text, nullable=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id', ondelete='CASCADE'), nullable=False)
    chapter = db.relationship('Chapter', backref=db.backref('questions'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __str__(self):
        return self.question
    

    def getAnswer(self):
        answer = Choice.query.filter_by(question = self, is_correct = True).first()
        return answer


# Choice Table
class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable = False)
    question = db.relationship('Question', backref=db.backref('choices'))
    choice = db.Column(db.Text, nullable = False)
    is_correct = db.Column(db.Boolean, default=False)

    def __str__(self):
        return str(self.choice)


# Admin Table 
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __str__(self):
        return f"Admin('{self.username}')"

