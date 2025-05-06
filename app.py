from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.orm import sessionmaker
from models.base import  engine
from models.model import Usuario, VideoGameSale
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import jsonify
app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "dev_key_fallback")

# Crear sesión SQLAlchemy
Session = sessionmaker(bind=engine)
db_session = Session()

# Setup de LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'

@login_manager.user_loader
def load_user(user_id):
    return db_session.query(Usuario).get(int(user_id))

# Ruta principal
@app.route('/')
def home():
    return render_template('auth.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form.get('action')  # Obtienes el valor del campo hidden 'action'
        username = request.form.get('username')
        password = request.form.get('password')
        if action == 'register':
            # Verificamos si el usuario ya existe
            if db_session.query(Usuario).filter_by(username=username).first():
                flash('El usuario ya existe.', 'danger')
            else:
                new_user = Usuario(
                    username=username,
                    password=generate_password_hash(password)  # Encriptamos la contraseña
                )
                print(new_user)
                db_session.add(new_user)
                db_session.commit()
                flash('Usuario registrado. Ahora puedes iniciar sesión.', 'success')
                return redirect(url_for('auth'))  # Redirigimos al formulario de login

        elif action == 'login':
            user = db_session.query(Usuario).filter_by(username=username).first()
            if user and check_password_hash(user.password, password):  # Verificamos las credenciales
                login_user(user)
                return redirect(url_for('dashboard'))  # Redirigimos al dashboard si el login es exitoso
            else:
                flash('Credenciales inválidas', 'danger')

    return render_template('auth.html')  # Renderizamos el formulario

# Ruta de dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth'))




@app.route('/api/video_games')
def api_video_games():
    data = db_session.query(VideoGameSale).all()
    
    juegos = []
    for juego in data:
        juegos.append({
            "Name": juego.name,
            "Platform": juego.platform,
            "Year": juego.year,
            "Genre": juego.genre,
            "Publisher": juego.publisher,
            "NA_Sales": juego.na_sales,
            "EU_Sales": juego.eu_sales,
            "JP_Sales": juego.jp_sales,
            "Other_Sales": juego.other_sales,
            "Global_Sales": juego.global_sales
        })

    return jsonify(juegos)


@app.route('/api/filtros', methods=['GET'])
def obtener_filtros():
    plataforma = request.args.getlist('plataforma')
    genero = request.args.getlist('genero')
    anio = request.args.getlist('anio')
    editor = request.args.getlist('editor')

    query = db_session.query(VideoGameSale)
    print(plataforma)
    if plataforma:
        query = query.filter(VideoGameSale.platform.in_(plataforma))
    if genero:
        query = query.filter(VideoGameSale.genre.in_(genero))
    if anio:
        query = query.filter(VideoGameSale.year.in_(anio))
    if editor:
        query = query.filter(VideoGameSale.publisher.in_(editor))

    data = query.all()

    plataformas = sorted({v.platform for v in data if v.platform})
    print(plataformas)
    generos = sorted({v.genre for v in data if v.genre})
    print(generos)
    anios = sorted({v.year for v in data if v.year})
    print(anios)
    editores = sorted({v.publisher for v in data if v.publisher})
    print(editores)
    return jsonify({
        'plataformas': plataformas,
        'generos': generos,
        'anios': anios,
        'editores': editores
    })

if __name__ == '__main__':
    app.run(debug=True)
