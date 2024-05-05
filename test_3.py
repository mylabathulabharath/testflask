from flask import Flask,render_template,request
import sqlite3
app = Flask(__name__)


def create_connection():
    conn=sqlite3.connect('finaldb.db')
    return conn 

def create_table():
    conn=create_connection()
    conn.cursor().execute(''' CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
    conn.commit()
    conn.close

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        uname=request.form['username']
        pswd=request.form['password']
        print(uname)
        print(pswd)
        
        conn=create_connection()
        cur=conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ? AND password = ?',(uname, pswd))
        data=cur.fetchone()
        print(data)
        conn.close()
        if data:
            return render_template('home.html')
        else:
            return 'WRONG CREDENTIALS'
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        uname=request.form['username']
        pswd=request.form['password']

        conn=create_connection()
        conn.cursor().execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (uname, pswd))
        conn.commit()
        conn.close()
        return 'successfully pushed into database'
    return render_template('register.html')

if __name__ =='__main__':
    create_table()
    app.run(debug=True)