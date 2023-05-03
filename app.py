from flask import Flask
from routes import *
from extensions import db
import os

app = Flask(__name__)
app.secret_key = 'secret_key'


# db connection [Postgresql]
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/flasksql'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://quizbuzzflask_user:RnF4OyIy5KLOQnbmhQVQvfgbkZQr4TzZ@dpg-ch8bg0dgk4q7lmp1udfg-a.oregon-postgres.render.com/quizbuzzflask'

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"] # DATABASE_URL = render internal connection url 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# db = SQLAlchemy(app)
db.init_app(app)
app.app_context().push()


# Register routes defined in routes.py using Blueprint
app.register_blueprint(homeBp)
app.register_blueprint(quizBp)
app.register_blueprint(quizAnswersOnSubmitBp)
app.register_blueprint(adminLoginBp)
app.register_blueprint(adminLogoutBp)
app.register_blueprint(deleteQuestionsBp)
app.register_blueprint(updateAdminBp)
app.register_blueprint(adminPanelBp)


# main driver functions
if __name__ == '__main__':
    # uncomment for model changes
    # db.drop_all()
    # db.create_all()  
    # print("All good!!!!!!!!!")
    app.run(debug=True)
