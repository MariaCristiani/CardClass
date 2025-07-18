from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_super_secreta'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

def get_db_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

class User(UserMixin):
    def __init__(self, id, nome, email, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        conexao = get_db_connection()
        sql = "SELECT * FROM users WHERE email = ?"
        existente = conexao.execute(sql, (user_id,)).fetchone()
        conexao.close()

        if not existente:
            return None

        return cls(
            id=existente['id'],
            email=existente['email'],
            senha=existente['senha']
        )


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()

    if user:
        return User(id=user['id'], nome=user['nome'], email=user['email'], senha=user['senha'])
    return None
    # return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('name')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not nome or not email or not senha:
            flash('Preencha todos os campos!', 'error')
            return redirect(url_for('cadastro'))

        senha_hash = generate_password_hash(senha)

        conn = get_db_connection()
        existente = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone() # Retorna uma linha só (como um dicionário ou tupla)

        if existente:
            flash('Email já cadastrado!', 'error')
            conn.close()
            return redirect(url_for('cadastro'))

        conn.execute("INSERT INTO users (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha_hash))
        conn.commit()
        conn.close()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            flash('Preencha todos os campos!', 'error')
            return redirect(url_for('login'))

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['senha'], senha):
            user_obj = User( id=user['id'], nome=user['nome'], email=user['email'], senha=user['senha'])
            # user_obj.id = user['email'] 
            login_user(user_obj)
            flash(f'Login bem-sucedido! Bem-vindo, {user["email"]}', 'success')
            return redirect(url_for('dash'))  # Volta pra página Inicial (por enquanto)
        
        flash('Email ou senha incorretos!', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dash')
@login_required
def dash():
    return render_template('dash.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', user=current_user)

if __name__ == '__main__':
    app.run(debug=True)
