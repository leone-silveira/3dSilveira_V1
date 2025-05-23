import os
from dotenv import load_dotenv   # type: ignore
from flask import Flask, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()


class Filament:
    def __init__(self, color, supplier, description, amount):
        self.color = color
        self.supplier = supplier
        self.description = description
        self.amount = amount


Filament1 = Filament('Vermelho', 'Volt', 'Vermelho', '1000')
Filament2 = Filament('Azul piscina', 'National', 'Azul tiffany', '500')
Filament3 = Filament('Branco', 'National', 'Branco gelo', '300')
filament_list = [Filament1, Filament2, Filament3]


class User:
    def __init__(self, name, nickname, password):
        self.name = name
        self.nickname = nickname
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


list_users = [
    User('Luiza', 'Lu', '1234'),
    User('Leone', 'Leo', '1235'),
    User('Laura', 'Laurita', '1236')]

users = {user.nickname: user for user in list_users}

app = Flask(__name__)
secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise RuntimeError("SECRET_KEY environment variable is not set. Please check your .env file.")
app.secret_key = secret_key


@app.route('/')
def index():
    return render_template(
        'lista.html',
        title='Filaments 3D Silveira',
        Filaments=filament_list)


@app.route('/new')
def new():
    if 'user_logged_in' not in session or session['user_logged_in'] is None:
        return redirect(url_for('login', following=url_for('new')))
    return render_template('cadastro.html', title='Filament registration')


@app.route('/create', methods=['POST',])
def create():
    color = request.form['color']
    supplier = request.form['supplier']
    description = request.form['description']
    amount = request.form['amount']
    Filament4 = Filament(color, supplier, description, amount)
    filament_list.append(Filament4)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    following = request.args.get('following')
    return render_template('login.html', following=following)


@app.route('/authenticate', methods=['POST', ])
def authenticate():
    user_input = request.form['user']
    password_input = request.form['password']

    if user_input in users:
        user = users[user_input]
        if user.check_password(password_input):
            session['user_logged_in'] = user.nickname
            flash(user.nickname + ' logged in')
            return redirect(url_for('new'))
    flash('User not logged in')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['user_logged_in'] = None
    flash('Logout ok')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_ENV') == 'development', port=5002)
