from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

class link_class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable = False)
    link_dt = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"

with app.app_context():
    db.create_all()

@app.route("/", methods = ['GET', 'POST'])
def home():

    if request.method == 'POST':
        link_title = request.form['title']
        link_link = request.form['link']
        link_obj = link_class(title = link_title, link = link_link)
        db.session.add(link_obj)
        db.session.commit()


    link_all = link_class.query.all()
    #link_obj = link_class(title = "test0", link = 'test0')
    #db.session.add(link_obj)
    #db.session.commit()

    return render_template('index.html', link_all = link_all)

@app.route("/about")
def about():
    return '<p>This is an About Page </p>'


if __name__ == '__main__':
    app.run(debug=True)

