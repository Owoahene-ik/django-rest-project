from flask import Flask,render_template,flash,request,  redirect, url_for, session, logging
from data import article 
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired
# from MySQLdb import escape_string as thwart
import mysql.connector

import gc







app = Flask(__name__)



#config sql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'demo'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'flask'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql= MySQL(app)


article = article()


# def connection():
#     conn = pymysql.connect(host="localhost",
#                            unix_socket='/tmp/mysql.sock',
#                            user = "root",
#                            passwd = "",
#                            db = "myflaskapp")
#     c = conn.cursor()

#     return c, conn
    


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


class MyForm(Form):
    name    = StringField('Name', [validators.length(min = 4, max=100)])
    user_name    = StringField('User Name', [ validators.length(min = 4, max=50)])
    email = TextAreaField('Mailing Address', [validators.optional(), validators.length(min =5,max=200)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message ='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    
    remember_me = BooleanField('Remember Me')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice.', [validators.Required()])
    

@app.route('/register/', methods=[ 'GET', 'POST'])
def register():
    form = MyForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        user_name = form.user_name.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        confirm = sha256_crypt.encrypt(str(form.confirm.data))
        
        cur = mysql.connection.cursor()
        x = cur.execute('''SELECT * FROM persons WHERE username = (%s)''',(user_name))
        if int(x) > 0:
            flash("Username already exists, please choose another")
            return render_template('register.html', form=form)
        else:
            cur.execute('''INSERT INTO persons (name,user_name, password, email, confirm) VALUES (%s, %s, %s, %s,%s)''',(name,user_name, password, email, confirm))
        
        mysql.connection.commit
        cur.close
     
        return redirect(url_for('index'))
        
    return render_template('register.html', form=form ) 
        
    
    



    
if __name__== '__main__':
    app.run(debug=True)
    
    
    