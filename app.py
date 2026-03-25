from flask import Flask, render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://blog_rdsv_user:hgZ7HLuyfnaLtHdcA99Gt88b3hWJELIW@dpg-d723nm75r7bs73f8k520-a.oregon-postgres.render.com/blog_rdsv"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

#postgresql://blog_rdsv_user:hgZ7HLuyfnaLtHdcA99Gt88b3hWJELIW@dpg-d723nm75r7bs73f8k520-a.oregon-postgres.render.com/blog_rdsv

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro= db.Column(db.String(300),nullable=False)
    text = db.Column(db.Text,nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id




@app.route('/')
def index():
    return  redirect(url_for('posts'))




@app.route('/create-article',methods=['GET','POST'])
def  create_article():
    if request.method == 'POST':
        title=request.form['title']
        intro=request.form['intro']
        text=request.form['text']

        article=Article(title=title,intro=intro,text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Something went wrong"
    else:
        return render_template('create-article.html')

@app.route('/posts/<int:id>/update',methods=['GET','POST'])
def  post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title=request.form['title']
        article.intro=request.form['intro']
        article.text=request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Something went wrong with updating"
    else:
        return render_template('post_update.html',article=article)

@app.route("/posts")
def posts():
    articles=Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html',articles=articles)

@app.route("/posts/<int:id>")
def posts_detail(id):
    article=Article.query.get(id)
    return render_template('posts_detail.html',article=article)

@app.route("/posts/<int:id>/del")
def posts_delete(id):
    article=Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Something went wrong with deleting"


if __name__=='__main__':
    app.run(debug=True)
