from flask import Flask, render_template
from models import *


@app.route('/')
def home():
    subject_chapter_mapping = {}
    sub = Subject.query.all()
    for subject in sub:
        chapter = Chapter.query.filter_by(subject_id = subject.id).all()
        # chapter = subject.chapters
        subject_chapter_mapping[subject] = chapter
    
    context = {
        "subject_chapter_mapping": subject_chapter_mapping

    }  
    return render_template("home.html", context = context)


@app.route('/<subject_slug>/<chapter_slug>/quiz')
def quiz(subject_slug,chapter_slug):
    subject = Subject.query.filter_by(slug = subject_slug).first()  # we use first() here to get first value from returned list[]
    chapter = Chapter.query.filter_by(slug = chapter_slug, subject_id = subject.id ).first()
    questions = chapter.questions
    # print("########", questions[0].get_answer())
    return render_template("quiz.html",context = questions)


# main driver function
if __name__ == '__main__':
    app.run(debug=True)
    # db.create_all() in terminal to create database and table
    # > python
    # > from app import db
    # > db.create_all()
    # with app.app_context():
    #     db.create_all()
