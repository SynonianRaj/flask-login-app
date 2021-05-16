import sqlite3 as sql
from random import choice

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message

char = 'abcdefghijklmnopqrstuvwxyz0123456789'
otp = ''

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'aryaankitkumarsingh@gmail.com'
app.config['MAIL_PASSWORD'] = '8541078756'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'aryaankitkumarsingh@gmail.com'
app.secret_key = char
mail = Mail(app)


class SQL:
    def __init__(self, sq):
        with sq.connect('Mydata.db') as self.sql:
            self.db = self.sql.cursor()

    def execute_cmd(self, *args):
        a = self.db.execute(*args)
        self.sql.commit()
        # self.sql.close()
        return a


def request_data(*names):
    data = []
    for i in names:
        if request.method == 'POST':
            data.append(request.form.get(i))
            # print(f'heloo {request.form.get(i)}')
    return data


SQL(sql)


@app.route('/')
@app.route('/register')
def sign_up():
    if 'email1' in session:
        sq = SQL(sql)
        fname, lname = sq.execute_cmd("""SELECT firstName,lastName FROM persons WHERE email=?""",
                                      (session['email1'],)).fetchone()
        return render_template('login-success.html', name=f'{fname} {lname}')
    return render_template('sign-up-page.html')


@app.route('/verify-email', methods=['POST'])
def verify_email():
    global otp
    otp = ''
    sq = SQL(sql)
    # print(request_data('fname', 'lname', 'email', 'password'))
    fname, lname, email, password = request_data('fname', 'lname', 'email', 'password')
    session['fname'] = fname.strip().capitalize()
    session['lname'] = lname.strip().capitalize()
    session['email'] = email.strip()
    session['password'] = password.strip()
    le = sq.execute_cmd('''SELECT * FROM persons WHERE email = ?''', (email,)).fetchall()
    if len(le) > 0:
        return redirect('/sign-up-failed')
    else:
        for i in range(7):
            otp += choice(char)
        print(otp)
        print([email])
        msg = Message(subject="Verification Code", recipients=[email])
        msg.html = f"""
              <h1 style="font-family:sans-serif; text-align:center; padding:10px 0;">Hello {fname.strip().capitalize()} {lname.strip().capitalize()}</h1> <h2 
              style="font-family:sans-serif; text-align:center; padding:10px 0; font-weight:400; border:1px solid 
              red;">Your Verification Code  is <b>{otp}</b></h2> 
<p style="font-family:sans-serif; text-align:center; padding:10px 0; font-size:25px;">Thanks For Registration.</p>"""
        mail.send(msg)
    return render_template('verify-email.html')


@app.route('/login')
def login_page():
    sq = SQL(sql)
    if 'email1' in session:
        fname, lname = sq.execute_cmd("""SELECT firstName,lastName FROM persons WHERE email=?""",
                                      (session['email1'],)).fetchone()
        return render_template('login-success.html', name=f'{fname} {lname}')
    return render_template('login-page.html')


@app.route('/sign-up-successful', methods=['POST'])
def signUpSuccess():
    sq = SQL(sql)
    code = request_data('otp')[0]
    fname = session['fname']
    lname = session['lname']
    email = session['email']
    password = session['password']
    print(f'Enter OTP is {code}')
    if code == otp:
        pass_hash = bcrypt.generate_password_hash(password).decode('utf-8'
                                                                   '')
        sq.execute_cmd("""INSERT INTO persons (firstName,lastName,email,password) VALUES (?,?,?,?)""",
                       (fname, lname, email, pass_hash))
        print(code)
        session.clear()
        return render_template('greet.html', name=f'{fname} {lname}')
    else:
        return redirect('/verification-failed')


@app.route('/verification-failed')
def verification_failed():
    return render_template('verify-email.html', message="Verification Failed")


@app.route('/login-success', methods=['GET', 'POST'])
def login_success():
    sq = SQL(sql)
    print(request_data('email', 'password'))
    if not request_data('email', 'password'):
        return redirect(url_for('login_page'))

    email, password = request_data('email', 'password')
    try:
        fname, lname, p = sq.execute_cmd("""SELECT firstName,lastName,password FROM persons WHERE email=?""",
                                         (email.strip(),)).fetchone()
        print(fname)
        if bcrypt.check_password_hash(p, password):
            print(p)
            session['email1'] = email
            return render_template('login-success.html', name=f'{fname} {lname}')
        else:
            return redirect(url_for('login_failed'))
    except:
        return redirect(url_for('login_failed'))


@app.route('/login-failed', methods=['GET', 'POST'])
def login_failed():
    return render_template('login-page.html', message="Check email/password again")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'email1' in session:
        session.clear()
        # session.pop('email1')
        return render_template('login-page.html', message="logout successfully")
    return render_template('login-page.html')


@app.route('/sign-up-failed')
def signup_failed():
    return render_template('sign-up-page.html', message='You have already registered')


def convert_to_dict(cursor, row):
    dic = {}
    for rid, col in enumerate(cursor.description):
        dic[col[0]] = row[rid]
    return dic


@app.route('/api/json')
def api():
    with sql.connect('Mydata.db') as mydb:
        mydb.row_factory = convert_to_dict
        db = mydb.cursor()
        data = db.execute("""SELECT * FROM persons""").fetchall()
    return jsonify(data)


if __name__ == '__main__':
    app.debug = True
    app.run()
