from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = 'smarttodo123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


# ------------------ DATABASE ------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text)

    priority = db.Column(db.String(20))

    due_date = db.Column(db.String(20))

    status = db.Column(db.String(20), default="Pending")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ------------------ HOME ------------------

@app.route('/')
def home():
    return redirect(url_for("login"))


# ------------------ REGISTER ------------------

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful")

        return redirect(url_for("login"))

    return render_template("register.html")
# ------------------ LOGIN ------------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password")

    return render_template("login.html")


# ------------------ DASHBOARD ------------------

@app.route('/dashboard')
@login_required
def dashboard():

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    total = len(tasks)
    completed = len([t for t in tasks if t.status == "Completed"])
    pending = len([t for t in tasks if t.status == "Pending"])

    return render_template(
        "dashboard.html",
        user=current_user,
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending
    )


# ------------------ ADD TASK ------------------

@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():

    if request.method == "POST":

        task = Task(
            title=request.form["title"],
            description=request.form["description"],
            priority=request.form["priority"],
            due_date=request.form["due_date"],
            user_id=current_user.id
        )

        db.session.add(task)
        db.session.commit()

        flash("Task Added Successfully!")

        return redirect(url_for("dashboard"))

    return render_template("add_task.html")


# ------------------ EDIT TASK ------------------

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):

    task = Task.query.get_or_404(id)

    if request.method == "POST":

        task.title = request.form["title"]
        task.description = request.form["description"]
        task.priority = request.form["priority"]
        task.due_date = request.form["due_date"]

        db.session.commit()

        flash("Task Updated Successfully!")

        return redirect(url_for("dashboard"))

    return render_template("edit_task.html", task=task)


# ------------------ DELETE TASK ------------------

@app.route('/delete/<int:id>')
@login_required
def delete_task(id):

    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    flash("Task Deleted Successfully!")

    return redirect(url_for("dashboard"))


# ------------------ COMPLETE TASK ------------------

@app.route('/complete/<int:id>')
@login_required
def complete_task(id):

    task = Task.query.get_or_404(id)

    task.status = "Completed"

    db.session.commit()

    flash("Task Completed!")

    return redirect(url_for("dashboard"))


# ------------------ LOGOUT ------------------

@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


# ------------------ MAIN ------------------

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)