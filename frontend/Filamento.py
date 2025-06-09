import os
from dotenv import load_dotenv   # type: ignore
from flask import Flask, render_template, request, redirect, session, flash, url_for
from model import Filament, User


filament_list = [
    Filament(1, 'Vermelho', 'Volt', 'Vermelho', '1000', True),
    Filament(2, 'Azul piscina', 'National', 'Azul tiffany', '500', True),
    Filament(3, 'Branco', 'National', 'Branco gelo', '300', True)
]

list_users = [
    User('Luiza', 'Lu', '1234'),
    User('Leone', 'Leo', '1235'),
    User('Laura', 'Laurita', '1236')
]

users = {user.nickname: user for user in list_users}

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route('/')
def index():
    return render_template(
        'lista.html',
        title='Filaments 3D Silveira',
        Filaments=filament_list)


@app.route('/create', methods=['POST',])
def create():
    new_id = max(f.id for f in filament_list) + 1 if filament_list else 1
    color = request.form['color']
    supplier = request.form['supplier']
    description = request.form['description']
    amount = request.form['amount']
    Filament4 = Filament(new_id, color, supplier, description, amount, True)
    filament_list.append(Filament4)
    return redirect(url_for('index'))


@app.route('/new', methods=['GET', 'POST'])
def new():
    if 'user_logged_in' not in session or session['user_logged_in'] is None:
        return redirect(url_for('login', following=url_for('new')))
    return render_template('cadastro.html', title='Filament registration')


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id=None):
    if 'user_logged_in' not in session:
        return redirect(url_for('login', following=request.url))
    for filament in filament_list:
        if (filament.id == id):
            filament.activate = False
            flash("Filament deleted")
            return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id=None):
    if 'user_logged_in' not in session:
        return redirect(url_for('login', following=request.url))

    filament = next((f for f in filament_list if f.id == id), None)
    if not filament:
        flash("Filament not found")
        return redirect(url_for('index'))

    if request.method == 'POST':
        color = request.form['color']
        supplier = request.form['supplier']
        description = request.form['description']
        amount = request.form['amount']
        if filament:
            filament.color = color
            filament.supplier = supplier
            filament.description = description
            filament.amount = amount
            flash("Filament updated")
        return redirect(url_for('index'))
    return render_template('cadastro.html', filament=filament)


@app.route('/login')
def login():
    following = request.args.get('following')
    return render_template('login.html', following=following)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    user_input = request.form['user']
    password_input = request.form['password']

    following = request.form.get('following')
    if user_input in users:
        user = users[user_input]
        if password_input == user.password:
            session['user_logged_in'] = user.nickname
            flash(f'{user.nickname} logged in')
            return redirect(following or url_for('index'))
    flash('Usuário ou senha inválidos')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['user_logged_in'] = None
    flash('Logout ok')
    return redirect(url_for('index'))


app.run(debug=True, port=5002)

if __name__ == '__main__':
    app.run(debug=True)
