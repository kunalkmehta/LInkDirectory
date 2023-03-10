from flask import Flask, render_template, request, redirect, jsonify
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
    category = db.Column(db.String, nullable = False)
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
        link_category = request.form['category']

        link_link = request.form['link']

        link_obj = link_class(title = link_title, link = link_link, category = link_category)
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

@app.route("/delete/<int:id>")
def delete(id):
    print(id)


    link_del = db.get_or_404(link_class, id)
    db.session.delete(link_del)
    db.session.commit()

    return redirect ('/')


@app.route("/update/<int:id>", methods = ['GET', 'POST'])
def update(id):
    if request.method == 'POST':

        link_update = db.get_or_404(link_class, id)
        link_update.title = request.form['title']
        link_update.category = request.form['category']

        link_update.link = request.form['link']

        db.session.commit()
        return redirect('/')


    print(id)
    link_update = db.get_or_404(link_class, id)
    return render_template('update.html', link_update = link_update)

@app.route("/gettitle/<string:strtitle>")
def gettitle(strtitle):
    #print(strtitle)

    get_title = link_class.query.filter_by(title = strtitle).all()
    if len(get_title) == 0:
        return "No Information Exist"
    else: 
    
        for i in range(len(get_title)):
            title = get_title[i].title
            category = get_title[i].category
            link = get_title[i].link

            result = {
                'Title': title, 
                'Category': category,
                'Link': link
            }
            return jsonify(result)
        

@app.route("/getcategory/<string:strtitle>")
def getcategory(strtitle):
    #print(strtitle)
    result_list = []
    get_category = link_class.query.filter_by(category = strtitle).all()
    if len(get_category) == 0:
        return "No Information Exist"
    else: 
    
        for i in range(len(get_category)):
            title = get_category[i].title
            category = get_category[i].category
            link = get_category[i].link

            result = {
                'Title': title, 
                'Category': category,
                'Link': link
            }
            result_list.append(result)
        return jsonify(result_list)
    #return "this is response"

if __name__ == '__main__':
    app.run(debug=True)

