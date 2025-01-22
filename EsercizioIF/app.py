from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models import db, Utente  # Importa db e Utente

app = Flask(__name__)
app.secret_key = 'key_sessione_user'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

bcrypt = Bcrypt(app)
db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Utente.query.get(int(user_id))  # Usa il campo `id` (o `id_user` se scegli la soluzione 2)

with app.app_context():
    db.create_all()  # Crea le tabelle nel database

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        if Utente.query.filter_by(username=username).first():
            return render_template('register.html', error="Questo username è già in uso.")

        new_user = Utente(username=username, hashed_password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)


        return redirect(url_for('home'))
    return render_template('register.html', error=None)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = Utente.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.hashed_password, password):
            login_user(user)
            return redirect(url_for('home'))
        return render_template('login.html', error="Credenziali non valide.")
    return render_template('login.html', error=None)

@app.route('/home')
@login_required
def home():
    return render_template('home.html', username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
