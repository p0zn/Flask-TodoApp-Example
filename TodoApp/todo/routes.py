from flask import render_template, url_for,redirect,request,flash
from todo import app, db , bcrypt
from todo.forms import RegistrationForm,LoginForm
from todo.models import User,Todo
from flask_login import login_user, current_user, login_user, logout_user, login_required



@app.route("/")
@login_required
def index():
    all_todos = current_user.todos

    return render_template("index.html",all_todos = all_todos)

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data, password= hashed_password )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for("login"))

    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods = ["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for("index"))
        else:    
            flash("Username or password is wrong!")
    return render_template("login.html", title="Login", form=form)

@app.route("/add", methods=["POST"])
def addTodo():
    title = request.form.get("title")
    content = request.form.get("content")
    user_id = current_user.id
    n_todo = Todo(title = title , content = content, user_id = user_id, done = False)
    db.session.add(n_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/complete/<string:id>")
def compTodo(id):
    todo = Todo.query.filter_by(id=id).first()

    if todo.done == False:
        todo.done = True 
    else :
        todo.done = False 
    
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def delTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))