from flask import Flask, request, render_template, redirect, session,jsonify, url_for
from mailer import Mailer
import random
import hashlib
import sqlite3
from datetime import date, datetime
daych = datetime.now().date()
import html
date_  = date.today()
 
app = Flask(__name__) 
app.secret_key = '552266226622784955163'





print('qq')




# encryption def
def encryption(prs):

    p1e = hashlib.md5(prs.encode()).hexdigest()
    p1d1 = p1e.translate({ord('b'): None})
    p1d2 = p1d1.translate({ord('8'): None})
    p1 = p1d2[0:9]


    p2e = hashlib.sha1(prs.encode()).hexdigest()
    p2d1 = p2e.translate({ord('e'): None})
    p2d2 = p2d1.translate({ord('6'): None})
    p2 = p2d2[0:6]


    p3e = hashlib.sha256(prs.encode()).hexdigest()
    p3d1 = p3e.translate({ord('1'): None})
    p3d2 = p3d1.translate({ord('l'): None})
    p3 = p3d2[0:10]


    return str(p1)+str(p2)+str(p3)

# login page code
@app.route('/', methods =["GET", "POST"])
def loginn():

    db = sqlite3.connect("mydatabase.db")
    mydb = db.cursor()

    if request.method == "POST":
        user = html.escape(request.form.get("usr").lower())
        pwd  = html.escape(request.form.get("pwd"))

        mydb.execute(f"SELECT * FROM users WHERE  user = '{user}' AND password = '{encryption(pwd)}'")
        dddd = mydb.fetchone()
        if dddd == None:
            return render_template("logins.html", mm = 'error email or password')
        else:
            if dddd[4] == 'False':
                session['vrcode'] = random.randint(100011,900019)
                session['user']   = dddd[0]
                return redirect('/veres')
            else:
                session['email'] = user
                return redirect('/veres')
    
    return render_template("logins.html")

#signup page code
@app.route('/signup', methods =["GET", "POST"])
def signup():
    db = sqlite3.connect("mydatabase.db")
    mydb = db.cursor()
    if request.method == "POST":

        user = html.escape(request.form.get("nusr").lower())
        npwd  = html.escape(request.form.get("npwd"))
        Fullnamm = html.escape(request.form.get("hname"))
        phone = html.escape(request.form.get("phone"))

        mydb.execute("SELECT user FROM users")
        results = mydb.fetchall()
        if (user,) in results:
            return redirect('/')

        session['email'] = user
        session['vrcode'] = random.randint(100011,900019)

        db = sqlite3.connect("mydatabase.db")
        mydb = db.cursor()
        mydb.execute(f"INSERT INTO users ( user, password, fullName, PhoneNumber, verificationCode, DateCreate  )  VALUES ('{user}','{encryption(npwd)}','{Fullnamm}','{phone}', '{'False'}', '{date_}')")
        db.commit()
        db.close()

        return redirect('/veres')
        

    return render_template("signup.html")

# verify page code 
@app.route('/veres', methods =["GET", "POST"])
def verecode():
    if session.get('email') == None:
        return redirect('/')
    db = sqlite3.connect("mydatabase.db")
    mydb = db.cursor()


    mzil = Mailer(email="example@gmail.com", password="your developer password") # you need gmail account to connect here (:
    mzil.send(receiver=str(session.get('user')),
            subject="THIS IS EMAIL FOR verify account",
            message=" your verify code is ("+str(session.get('vrcode'))+")" )


    if request.method == "POST":
        vrcode__ = request.form.get('verc')

        if str(vrcode__) == str(session.get('vrcode')):
            user__ = str(session.get('user'))
            mydb.execute("UPDATE users SET verificationCode = ? WHERE user = ?", ('True', user__))
            db.commit()
            db.close()
            return redirect('/')
        else:
            massgeErorr_ = 'the code is not correct'
            return render_template('vere.html', massgeErorr = massgeErorr_, emailhis = str(session.get('email')) )


    return render_template('vere.html', emailhis = str(session.get('email')) )



if __name__=='__main__':    
   app.run(debug=True)