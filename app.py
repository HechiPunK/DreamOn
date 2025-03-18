from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import jsonify

from config import config
from models.ModelUser import ModelUser
from models.entities.User import User
from models.ModelWordKey import ModelWordKey
from models.entities.WordKey import WordKey
from models.ModelPublication import ModelPublication
from models.entities.Publication import Publication

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

@app.route('/buscar_palabra', methods=['POST'])
def buscar_palabra():
    data = request.get_json()
    word = data.get("palabra", "").strip().lower()
    type = data.get("tipo", "jungian")  

    if not word:
        return jsonify({"error": "Palabra no proporcionada"}), 400

    significado = ModelWordKey.get_by_keyword(db, word, type)
    
    if significado:
        return jsonify({"significado": significado})
    else:
        return jsonify({"error": "Palabra no encontrada"}), 404
    
@app.route('/dashboard')
@login_required
def dashboard():
    user_id = current_user.id
    publications = ModelPublication.get_publications_by_user(db, user_id)
    return render_template('dashboard.html', publications=publications)

@app.route('/editar_publicacion/<int:id>', methods=['POST'])
@login_required
def editar_publicacion(id):
    if request.method == 'POST':
        nuevo_contenido = request.form['contenido']
        if ModelPublication.update_publication(db, id, nuevo_contenido):
            flash("Publicación actualizada con éxito", "success")
        else:
            flash("Error al actualizar la publicación", "danger")
    return redirect(url_for('dashboard'))

@app.route('/eliminar_publicacion/<int:id>')
@login_required
def eliminar_publicacion(id):
    publicacion = ModelPublication.get_publication_by_id(db, id)
    if publicacion and publicacion.username == current_user.id:
        if ModelPublication.delete_publication(db, id):
            flash("Publicación eliminada con éxito", "success")
        else:
            flash("Error al eliminar la publicación", "danger")
    else:
        flash("No tienes permiso para eliminar esta publicación", "danger")
    return redirect(url_for('dashboard'))

@app.route('/publicar', methods=['POST'])
def publicar():
    if request.method == 'POST':
        content = request.form['contenido']
        users_id = current_user.id if current_user.is_authenticated else None

        if ModelPublication.create_publication(db, content, users_id):
            flash("Publicación creada con éxito", "success")
        else:
            flash("Error al crear la publicación", "danger")

        return redirect(url_for('foro'))

@app.route('/agregar_significado', methods=['POST'])
@login_required
def agregar_significado():
    if request.method == 'POST':
        word = request.form['palabra']
        jungian_date = request.form['significado_jungian']
        modern_date = request.form['significado_moderno']
        user_id = current_user.id

        if ModelWordKey.agregar_significado(db, word, jungian_date, modern_date, user_id):
            flash("Significado agregado con éxito", "success")
        else:
            flash("Error al agregar el significado", "danger")
        return redirect(url_for('dashboard'))

@app.route('/foro')
def foro():
    publications = ModelPublication.get_publication(db)
    return render_template('foro.html', publications=publications)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('ruta_login'))

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True)
