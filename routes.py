from flask import Blueprint, abort, render_template, request, flash, session, redirect, url_for
from models import *
import math
import json
from functions import loginRequired, uploadQuestions


# Creating Blueprint to be accessed in app.py
homeBp = Blueprint('homeBp', __name__)
quizBp = Blueprint('quizBp', __name__)
quizAnswersOnSubmitBp = Blueprint('quizAnswersOnSubmitBp', __name__)
adminLoginBp = Blueprint('adminLoginBp', __name__)
adminLogoutBp = Blueprint('adminLogoutBp', __name__)
deleteQuestionsBp = Blueprint('deleteQuestionsBp', __name__)
updateAdminBp = Blueprint('updateAdminBp', __name__)


# Home Page [Default] | Listing all Subject & Chapter
@homeBp.route('/')
def home():
    subject_chapter_mapping = {}
    sub = Subject.query.all()
    for subject in sub:
        chapter = Chapter.query.filter_by(subject_id=subject.id).all()
        # chapter = subject.chapters
        subject_chapter_mapping[subject] = chapter

    context = {
        "subject_chapter_mapping": subject_chapter_mapping

    }
    return render_template("home.html", context=context)


# Quiz Page | 
@quizBp.route('/<subject_slug>/<chapter_slug>/quiz/', methods=['GET', 'POST'])
def quiz(subject_slug, chapter_slug):

    # we use first() here to get first value from returned list[]
    try:
        subject = Subject.query.filter_by(slug=subject_slug).first()
        # we use first() here to get first value from returned list[]
        chapter = Chapter.query.filter_by(
            slug=chapter_slug, subject_id=subject.id).first()
        questions = chapter.questions
        lengthOfQuestions = len(questions)
    except:
        abort(404)

    if lengthOfQuestions in range(15, 100):
        numberOfQuiz = math.ceil(lengthOfQuestions/10)
        questionsPerQuiz = 10

    elif lengthOfQuestions >= 100:
        numberOfQuiz = math.ceil(lengthOfQuestions/20)
        questionsPerQuiz = 20
    else:
        numberOfQuiz = 1
        questionsPerQuiz = 15

    # get quizNumber from GET request [default will be "Quiz1"]  
    quizNumber = request.args.get("quizNumber", "Quiz1")
    try:
        # convert to int form as value comes in string format
        quizNumber = int(quizNumber.strip("Quiz"))
    except Exception:
        quizNumber = 1

    # display questions in multiple quizes
    endIndex = quizNumber*questionsPerQuiz
    startIndex = endIndex-questionsPerQuiz
    questions = questions[startIndex:endIndex]
    quizNumber = f"?quizNumber={quizNumber}"

    return render_template("quiz.html", quizNumber=quizNumber, context=questions, subject_slug=subject_slug, chapter_slug=chapter_slug, numberOfQuiz=numberOfQuiz)


# Display and Calculate Result on Quiz Submit
@quizAnswersOnSubmitBp.route('/<subject_slug>/<chapter_slug>/quiz/answer/', methods=['GET', 'POST'])
def quizAnswersOnSubmit(subject_slug, chapter_slug):
    try:
        subject = Subject.query.filter_by(slug=subject_slug).first()
        chapter = Chapter.query.filter_by(
            slug=chapter_slug, subject_id=subject.id).first()
        questions = chapter.questions
        lengthOfQuestions = len(questions)
    except:
        abort(404)

    if lengthOfQuestions in range(15, 100):
        questionsPerQuiz = 10

    elif lengthOfQuestions >= 100:
        questionsPerQuiz = 20
    else:
        questionsPerQuiz = 15

    quizNumber = request.args.get("quizNumber", "Quiz1")
    try:
        quizNumber = int(quizNumber.strip("Quiz"))
    except Exception as e:
        quizNumber = 1
    endIndex = quizNumber*questionsPerQuiz
    startIndex = endIndex-questionsPerQuiz
    questions = questions[startIndex:endIndex]

    form = request.form  # form submitted all values in dict format

    usersChoicesId = [int(form[i]) for i in form] 
    usersQuestionsId = [int(i) for i in form]
    allQuestionsId = [ques.id for ques in questions] 
    unAttemptedQuestionsID = [
        i for i in allQuestionsId if i not in usersQuestionsId]

    rightAnswers = []
    questions = [ques for ques in questions]
    for question in questions:
        rightAnswers.append(question.getAnswer().id)

    score = 0
    for i in usersChoicesId:
        if i in rightAnswers:
            score += 1

    # data to plot pie chart
    data = [score, len(questions)-score -
            len(unAttemptedQuestionsID), len(unAttemptedQuestionsID)]

    context = {
        "questions": questions,
        "usersChoicesId": usersChoicesId,
        "score": f"{score} / {len(questions)}",
        "data": data,
        "unAttemptedQuestionsID": unAttemptedQuestionsID,
        "usersQuestionsId": usersQuestionsId,
    }

    return render_template("quizAnswersOnSubmit.html", context=context)



# Admin Login Page [with session]
@adminLoginBp.route('/admin/', methods=['GET', 'POST'])
def adminLogin():
    try:
        # if admin already in session 
        if "username" in session:
            # getting json file from adminPanel
            jsonFile = request.files.get("jsonFile")
            if jsonFile:
                jsonData = json.load(jsonFile)
                # calling uploadQuestions() in functions.py 
                result = uploadQuestions(jsonData)   
                flash(result)
            return render_template("adminPanel.html", username=session["username"])

        # if admin trying to login
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            admin = Admin.query.filter_by(
                username=username, password=password).first()
            if admin:
                session['username'] = admin.username
                return render_template("adminPanel.html", username=admin.username)
            else:
                flash('Invalid username or password')
                return render_template("adminLogin.html")
        else:
            return render_template("adminLogin.html")
    except Exception:
        abort(404)



# Admin Logout and clear Session
@adminLogoutBp.route('/admin/logout/')
def adminLogout():
    session.clear()
    return redirect(url_for("adminLoginBp.adminLogin"))



# Delete Questions from database
@deleteQuestionsBp.route('/admin/deleteQuestions/', methods=['GET', 'POST'])
# login required implemented using Decorators [functions.py file]
@loginRequired # === loginRequired(deleteQuestions)
def deleteQuestions():
    try:
        questions = Question.query.all()
    except:
        abort(404)

    if request.method == "POST":
        # get question id to be deleted
        questionId = int(request.form.get("questionId"))
        question = Question.query.get(questionId)

        for choice in question.choices:
            db.session.delete(choice)
            db.session.commit()

        db.session.delete(question)
        db.session.commit()
        questions = Question.query.all()

    return render_template("deleteQuestions.html", questions=questions)



# Update Admin data [within session]
@updateAdminBp.route('/admin/update/', methods=['GET', 'POST'])
def updateAdmin():
    try:
        username = session.get("username")
        if username:
            if request.method == "POST":
                newUsername = request.form.get("username")
                newPassword = request.form.get("newPassword")
                confirmPassword = request.form.get("confirmPassword")
                if newPassword == confirmPassword:
                    admin = Admin.query.filter_by(username=username).first()
                    admin.username = newUsername
                    admin.password = confirmPassword
                    session['username'] = admin.username
                    db.session.commit()
                    flash("Your Profile updated successfully")
                    return redirect("/admin/")
                else:
                    flash("Your password and confirmation password do not match")
            return render_template("updateAdmin.html", username=username)
        else:
            return redirect("/admin/")
    except:
        return redirect("/admin/")



