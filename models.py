from  datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from slugify import slugify


app = Flask(__name__)

# db connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/flasksql'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)
app.app_context().push()

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable = False)
    slug = db.Column(db.String(255), unique=True, nullable = False)

    def __str__(self):
        return self.name


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable = False)
    slug = db.Column(db.String(256), nullable = False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    subject = db.relationship('Subject', backref=db.backref('chapters'))


    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Chapter, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable = False)
    explanation = db.Column(db.Text, nullable=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    chapter = db.relationship('Chapter', backref=db.backref('questions'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __str__(self):
        return self.question

    def get_answer(self):
        answer = Choice.objects.get(question=self, is_correct=True)
        return answer


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable = False)
    question = db.relationship('Question', backref=db.backref('choices'))
    choice = db.Column(db.Text, nullable = False)
    is_correct = db.Column(db.Boolean, default=False)

    def __str__(self):
        return str(self.choice)


# class ReportQuestion(db.Model):
#     question = db.ForeignKey(Question, ondelete="CASCADE")
#     issue = db.TextField()
#     fixed = db.BooleanField(default=False)
#     report_type = db.Column(max_length=100)
#     created_at = db.DateTimeField(auto_now_add=True)
#     updated_at = db.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.question.id} - {self.report_type}"
if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    print("!!!!!!!!! Success !!!!!!!")

