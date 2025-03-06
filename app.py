from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from config import config
from models.ModelUser import ModelUser
from models.entities.User import User

app = Flask(__name__)
db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def ruta_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(0, username, password)
        logged_user = ModelUser.login(db, user)
        if logged_user and logged_user.password:
            login_user(logged_user)
            return redirect(url_for('dashboard'))
        flash("Usuario o contraseña incorrectos", "danger")
    return render_template('login.html')

@app.route('/newaccount', methods=['GET', 'POST'])
def ruta_newaccount():
    if request.method == 'POST':
        username = request.form['username']
        mail = request.form['e-mail']
        password = request.form['password']
        user = User(0, username, password, mail)
        if ModelUser.register(db, user):
            flash("Usuario registrado con éxito")
            return redirect(url_for('index'))
        flash("Error al registrar usuario. Puede que ya exista.")
    return render_template('newaccount.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('ruta_login'))

@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('q', '').strip()
    significados = []
    if query:
        cursor = db.connection.cursor()
        sql = "SELECT palabra, significado FROM significados WHERE palabra LIKE %s LIMIT 3"
        cursor.execute(sql, ('%' + query + '%',))
        significados = cursor.fetchall()
    return render_template('index.html', resultados=significados)

@app.route('/agregar_palabra', methods=['POST'])
@login_required
def agregar_palabra():
    palabra = request.form['palabra'].strip()
    significado = request.form['significado'].strip()
    if palabra and significado:
        cursor = db.connection.cursor()
        sql = "INSERT INTO significados (palabra, significado, usuario_id) VALUES (%s, %s, %s)"
        cursor.execute(sql, (palabra, significado, current_user.id))
        db.connection.commit()
        flash("Palabra agregada con éxito", "success")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True)
