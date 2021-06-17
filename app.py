from flask import Flask,render_template,request,url_for,redirect,session,flash,g, json, jsonify
from flask_mysqldb import MySQL,MySQLdb
from cryptography.fernet import Fernet
import bcrypt
import os
import re

app = Flask(__name__)
#--------------Tasks---------------------
#encryption,/sign upX, auto-detection of login, home page, styling
app.config['MYSQL_HOST'] ='pmanager.ci7cp0xr2b1f.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'Chic79!zoid'
app.config['MYSQL_DB'] = 'pmanager'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
# key = Fernet.generate_key()
key = '-nMTfmWwJd-PnYQkYLuw3TKP-52_TP4wKy730HkEphg='
f=Fernet(key)

@app.before_request
def before_request():
    g.username = None
    if 'username' in session:
        g.username = session['username']
        print(g.username)


@app.route('/')
def root():
    return render_template('login.html')


@app.route('/authentication',methods=['POST','GET'])
def authenticate():
    msg=''
    query=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #checking the hashed password in db against
        # hashed = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
        # newPassword = hashed.decode('utf8')
        # print(newPassword)
        # if(bcrypt.checkpw(password, newPassword.encode('utf8'))):
        #     print(True)
        # cur.execute("UPDATE pmanager.users SET password = %s WHERE username=%s", (newPassword, username,))
        # mysql.connection.commit()
        # print("Updated password")

        cur.execute("SELECT username FROM pmanager.users WHERE username=%s", (username,))
        uname = cur.fetchone()
        if not uname:
            msg = "A user with this username does not exist."
            return render_template('login.html', msg=msg)


        #getting password
        cur.execute("SELECT password FROM pmanager.users WHERE username=%s", (username,))

        passwordHashed = cur.fetchone()

        print(passwordHashed.get('password'))

        if not (bcrypt.checkpw(password.encode('utf8'), passwordHashed.get('password').encode('utf8'))):
            msg = "Incorrect password."
            return render_template('login.html', msg=msg)

        #logging in user and creating a session
        if(bcrypt.checkpw(password.encode('utf8'), passwordHashed.get('password').encode('utf8'))):
            print("Correct password")
            session['loggedin'] = True
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        return render_template('login.html',username=username, query=query)
    else:
        return render_template('login.html')


@app.route('/home')
def home():
    if g.username:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM pmanager.websites WHERE id = (SELECT id FROM pmanager.users WHERE username=%s)", (g.username,))
        query = cur.fetchall()
        print(query)

        for i in range(len(query)):
            password = f.decrypt(query[i]['password'].encode('utf8'))
            query[i]['password'] = password.decode('utf8')

        cur.execute("SELECT id FROM pmanager.users WHERE id = (SELECT id FROM pmanager.users WHERE username=%s)", (g.username,))
        id = cur.fetchone()
        print(id)

        return render_template('home.html', username=g.username, query=query, id=id)
    else:
        return render_template('login.html')


@app.route('/editpassword', methods=['POST'])
def editpassword():
    if request.method == 'POST':
        id = request.form['id']
        #print(pk)
        password = request.form['value']
        #print(password)
        username = request.form['username']
        #print(username)
        website = request.form['website']
        #print(website)
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        passwordEncrypt = f.encrypt(password.encode('utf8'))
        passwordDecode = passwordEncrypt.decode("utf8")
        cur.execute('UPDATE pmanager.websites SET password = %s WHERE id = %s AND website = %s AND username = %s', (passwordDecode,id,website,username,  ))
        mysql.connection.commit()
    return json.dumps({'status':'OK'})

@app.route('/deletepassword', methods=['POST'])
def deletepassword():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['value']
        username = request.form['username']
        website = request.form['website']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('DELETE FROM pmanager.websites WHERE id = %s AND website = %s AND username = %s AND password = %s', (id, website,username,password,  ))
        mysql.connection.commit()

        cur.execute("SELECT id FROM pmanager.users WHERE id = (SELECT id FROM pmanager.users WHERE username=%s)", (g.username,))
        id = cur.fetchone()
        cur.execute("SELECT * FROM pmanager.websites WHERE id = (SELECT id FROM pmanager.users WHERE username=%s)", (g.username,))
        query = cur.fetchall()
        print(query)

    return render_template('home.html', username=g.username, id=id, query=query)

@app.route('/addpassword', methods=['POST'])
def addpassword():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['value']
        username = request.form['username']
        website = request.form['website']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        passwordEncrypt = f.encrypt(password.encode('utf8'))
        passwordDecode = passwordEncrypt.decode('utf8')
        cur.execute('INSERT INTO pmanager.websites VALUES (% s, % s, % s, % s)', (id, website, username, passwordDecode, ))
        mysql.connection.commit()
        cur.execute("SELECT * FROM pmanager.websites WHERE id = (SELECT id FROM pmanager.users WHERE username=%s)", (g.username,))
        query = cur.fetchall()
        cur.execute("SELECT id FROM pmanager.users WHERE id = (SELECT id FROM pmanager.users WHERE username=%s)", (g.username,))
        id = cur.fetchone()
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    return render_template('home.html', username=g.username, query=query, id=id)



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    # session.pop('id', None)
    return render_template('login.html')

@app.route('/signup', methods =['GET', 'POST'])
def signup():
    msg=''
    if request.method == 'POST':

        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor = mysql.connection.cursor(mysql.cursors.DictCursor)
        cur.execute('SELECT * FROM pmanager.users WHERE username = % s', (username, ))
        user = cur.fetchone()
        cur.execute('SELECT * FROM pmanager.users WHERE email = % s', (email, ))
        useremail = cur.fetchone()
        cur.execute('SELECT * FROM pmanager.users WHERE phonenumber = % s', (phonenumber, ))
        userphone = cur.fetchone()
        if user:
            msg = 'An account with that username already exists.'
        elif useremail:
            msg ='An account with that email already exists.'
        elif userphone:
            msg = 'An account with that phone number already exists.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[0-9]{10}', phonenumber):
            msg = 'Phone number should contain only numbers!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif password1 != password2:
            msg = "Passwords do not match. Please try again."
        elif not username or not password1 or not email or not phonenumber:
            msg = 'Please fill out the form !'
        else:
            hashed = bcrypt.hashpw(password1.encode('utf8'),bcrypt.gensalt())
            newPassword = hashed.decode('utf8')
            cur.execute('INSERT INTO pmanager.users VALUES (NULL, % s, % s, % s, % s)', (username, newPassword, email, phonenumber, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('signup.html', msg = msg)

@app.route('/getdata', methods=['POST'])
def getdata():
    # content = request.get_json()
    # print(content)
    print("k")
    return "h"

if __name__ == '__main__':
  app.secret_key = os.urandom(24)
  app.run(host='127.0.0.1', port=8000, debug=True)
