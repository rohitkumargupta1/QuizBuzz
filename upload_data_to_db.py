import json
from models import *
from slugify import slugify
with open('static/lr.json', 'r') as f:
    data = json.load(f)

    
for i in data:

   
    # import pdb;
    # pdb.set_trace()

    try:

        temp = i["subject"]
        subject = Subject.query.filter_by(name=temp).all()
        if not subject:  # without all() it gives object | with all() gives list[]
            subject = Subject(name=temp, slug = slugify(temp))
            db.session.add(subject)
            db.session.commit()
        else:
            subject = subject[0]

        chapter = Chapter.query.filter_by(name=i["chapter"]).all()
        if not chapter:
            chapter = Chapter(name = i["chapter"], subject_id=subject.id, slug = slugify(i["chapter"]))
            db.session.add(chapter)
            db.session.commit()
        else:
            chapter = chapter[0]
        
        question = Question.query.filter_by(question=i["question"]).all()
        if not question:
            question = Question(question = i["question"], chapter_id = chapter.id, explanation =  i["explanation"] if i["explanation"] else None)
            db.session.add(question)
            db.session.commit()
        else:
            question = question[0]
        

        for j in i["choices"]:
            choice = Choice(choice = j, question_id = question.id, is_correct = i["answer"] == j)   
            db.session.add(choice)
            db.session.commit()
    
    except KeyError as k:
        print("Error!!!!!!!!!: " , k, "not found.")

    except Exception as e:
        print("Error!!!!!!!!! ", e)



    
    
