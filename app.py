from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# db connection 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/flasksql'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)
app.app_context().push()
# with app.app_context():
#     db.create_all()

# models
class People(db.Model):
    # __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(80), unique=True, nullable=False)
    color = db.Column(db.String(120), nullable=False)

    

    def __init__(self, pname, color):
        self.pname = pname
        self.color = color
        
	

@app.route('/')
def home():
    return '<a href="/addperson"><button> Click here </button></a>'


@app.route("/addperson")
def addperson():
    return render_template("index.html")


@app.route("/personadd", methods=['POST'])
def personadd():
    pname = request.form["pname"]
    color = request.form["color"]
    entry = People(pname, color)
    db.session.add(entry)
    db.session.commit()

    return render_template("index.html")




# @app.route('/')
# # ‘/’ URL is bound with hello_world() function.
# def hello_world():
# 	return render_template("base.html")

# @app.route('/signup')
# def signup():
# 	return render_template("signup2.html")

# main driver function
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)   
	# db.create_all() in terminal to create database and table 
		# > python
		# > from app import db
		# > db.create_all()
