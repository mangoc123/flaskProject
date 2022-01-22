from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, DateTime

from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), nullable=False)
    time_created = db.Column(DateTime(timezone=True))

    def __init__(self, name, time_created):
        self.name = name
        self.time_created = time_created


db.create_all()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', status=request.args.get('status'), user=request.args.get('user'))


@app.route('/users', methods=['GET'])
def users():
    return render_template('users.html', users=User.query.all())


@app.route('/add_user', methods=['POST'])
def add_user():
    user = request.form['name']
    time_created = func.now()

    exists = db.session.query(db.exists().where(User.name == user)).scalar()
    if exists:
        return redirect(url_for('index', status="Вже бачилися", user=user))

    db.session.add(User(user, time_created))
    db.session.commit()

    return redirect(url_for('index', status="Привіт", user=user))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
