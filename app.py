from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_super_secreta'

def get_db_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

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
            flash(f'Login bem-sucedido! Bem-vindo, {user["nome"]}', 'success')
            return redirect(url_for('index'))  # Volta pra página Inicial (por enquanto)
        else:
            flash('Email ou senha incorretos!', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
