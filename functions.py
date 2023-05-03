# from app import db
from extensions import db
from flask import redirect, abort, session
from models import *
from slugify import slugify


# Uploading questions to database
def uploadQuestions(data):
    count = 0
    for i in data:
        # try:
        temp = i["subject"]
        subject = Subject.query.filter_by(name=temp).all()
        if not subject:  # without all() it gives object | with all() gives list[]
            subject = Subject(name=temp, slug=slugify(temp))
            db.session.add(subject)
            db.session.commit()
        else:
            subject = subject[0]

        chapter = Chapter.query.filter_by(name=i["chapter"]).all()
        if not chapter:
            chapter = Chapter(
                name=i["chapter"], subject_id=subject.id, slug=slugify(i["chapter"]))
            db.session.add(chapter)
            db.session.commit()
        else:
            chapter = chapter[0]

        question = Question.query.filter_by(question=i["question"]).all()
        if question:
            answerList = [ans.getAnswer().choice for ans in question]
        else:
            answerList = []
        if not question or i["answer"] not in answerList:
            # if not question:
            question = Question(question=i["question"], chapter_id=chapter.id,
                                explanation=i["explanation"] if i["explanation"] else None)
            db.session.add(question)
            db.session.commit()

            for j in i["choices"]:
                choice = Choice(choice=j, question_id=question.id,
                                is_correct=i["answer"] == j)
                db.session.add(choice)
                db.session.commit()
            count += 1

        # except KeyError as k:
        #     abort(404)

        # except Exception as e:
        #     abort(404)

    return f"{count}/{len(data)} questions saved to database!"



# login required decorator for delete questions
def loginRequired(func):
    def inner(*args, **kwargs):
        username = session.get("username")
        if username:
            return func(*args, **kwargs)
        else:
            return redirect("/admin/")
    return inner



