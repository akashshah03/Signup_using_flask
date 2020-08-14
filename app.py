from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

from passlib.hash import sha256_crypt

engine = create_engine("mysql+pymysql://root:1234567@localhost/register")
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

#register form

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        secure_password = sha256_crypt.encrypt(str(password))

        if password == confirm:
            db.execute("INSERT INTO user(name,username,password) VALUES(:name, :username, :password)",{"name":name,"username":username,"password":secure_password})
            db.commit()
            flash("you are registered and can login","success")
            return redirect(url_for('login'))
        else:
            flash("password does not match","danger")
            return render_template('register.html')

    return render_template("register.html")

#login

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("name")
        password = request.form.get("password")

        usernamedata = db.execute("SELECT username FROM user WHERE username=:username",{"username":username}).fetchone()
        passworddata = db.execute("SELECT password FROM user WHERE username=:username",{"username":username}).fetchone()

        if usernamedata is None:
            flash("No user name","danger")
            return render_template("login.html")
        else:
            for passwor_data in passworddata:
                if sha256_crypt.verify(password,passwor_data):
                    session["log"] = True
                    flash("You are now login","success")
                    return redirect(url_for('profile'))
                
            else:
                flash("incorrect password","danger")
                return render_template("login.html")

    return render_template("login.html")

#photo
@app.route("/profile")
def profile():
    return render_template("photo.html")

#logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You are now loged out","sucsess")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key="1234567akash"
    app.run(debug=True)