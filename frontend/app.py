import os
import requests
from dotenv import load_dotenv   # type: ignore
from flask import Flask, render_template, request, redirect, session, \
    flash, url_for
from model import User
from werkzeug.exceptions import HTTPException


# TODO: Connect backend to users (with hash password)
list_users = [
    User('Luiza', 'Lu', '1234'),
    User('Leone', 'Leo', '1235'),
    User('Laura', 'Laurita', '1236')
]

users = {user.nickname: user for user in list_users}

load_dotenv()
app = Flask(__name__)

secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise RuntimeError(
        "SECRET_KEY environment variable is not set. \
            Please check your .env file.")
app.secret_key = secret_key
FILAMENT_URL = 'http://filament-api:8000/filaments_stock'


@app.route('/')
def index():
    try:
        response = requests.get(FILAMENT_URL)
        response.raise_for_status()
        filaments = response.json()
        print("--------->", filaments)
        return render_template(
            'lista.html',
            title='Filaments 3D Silveira',
            Filaments=filaments)
    except Exception as e:
        print("--------->", e)
        raise HTTPException(description="OUT OF SERVICE") from e


@app.route('/create', methods=['POST',])
def create():
    try:
        color = request.form['color']
        brand = request.form['brand']
        filament_name = request.form['filament_name']
        quantity = request.form['quantity']
        data = {
            "filament_name": filament_name,
            "color": color,
            "brand": brand,
            "quantity": float(quantity),
            "activate": True
        }
        create_response = requests.post(FILAMENT_URL, json=data)
        create_response.raise_for_status()
        print('create_response', create_response.json())
        flash("Created successfully", "success")
    except requests.RequestException as e:
        print(e.response.text)
        flash(f"Erro ao criar filamento: {e}", "error")
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
    try:
        inactivate_filament_response = requests.put(
            f'{FILAMENT_URL}/{id}/False')
        inactivate_filament_response.raise_for_status()
        flash("Filament deleted", 'success')
    except requests.RequestException as e:
        flash(f"Error deleting filament: {e}", 'error')
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id=None):
    if 'user_logged_in' not in session:
        return redirect(url_for('login', following=request.url))
    # connect with backend router filament_stock/read_filament
    get_filament_per_id = requests.get(f'{FILAMENT_URL}/{id}')
    get_filament_per_id.raise_for_status()
    filament = get_filament_per_id.json()
    if request.method == 'POST':
        color = request.form['color']
        supplier = request.form['brand']
        description = request.form['filament_name']
        amount = request.form['quantity']
        activate = filament['activate']
        data = {
            "filament_name": description,
            "color": color,
            "brand": supplier,
            "quantity": float(amount),
            "activate": activate,
        }
        update_filament_per_id = requests.put(
            f'{FILAMENT_URL}/{id}', json=data)
        if (update_filament_per_id.status_code == 200):
            flash("Filament updated", "success")
            return redirect(url_for('index'))
        else:
            flash("Filament could not be updated", 'error')
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
            flash(f'{user.nickname} logged in', "success")
            return redirect(following or url_for('index'))
    flash("User or password invalid", 'error')

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['user_logged_in'] = None
    flash('Logout', "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv(
        'FLASK_ENV') == 'development')
