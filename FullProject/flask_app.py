from flask import Flask,render_template
from data import article

app = Flask(__name__)

article = article()


@app.route("/")
def index():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/articles')
def articles():
    return render_template("articles.html",articles=article)

@app.route('/test/<string:num>')
def test(num):
    return render_template("test.html", num=num)



if __name__== '__main__':
    app.run(debug=True)