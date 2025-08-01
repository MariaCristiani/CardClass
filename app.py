from flask import Flask, render_template, request, redirect, url_for, flash, session
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

            login_user(user_obj)
            return redirect(url_for('dash'))  
        
        flash('Email ou senha incorretos!', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')

from flask import flash

@app.route('/criar', methods=['GET', 'POST'])
@login_required
def criar_flashcard():
    if request.method == 'POST':
        materia = request.form['materia']
        outra_materia = request.form.get('outra_materia', '').strip()
        pergunta = request.form['pergunta']
        resposta = request.form['resposta']
        usuario_id = current_user.id

        if materia == "Outra" and outra_materia:
            materia = outra_materia

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO flashcards (pergunta, resposta, materia, id_usuario)
            VALUES (?, ?, ?, ?)
        ''', (pergunta, resposta, materia, usuario_id))
        conn.commit()
        conn.close()

        flash('Flashcard criado com sucesso!', 'success')
        return redirect(url_for('meus_flashcards'))  # redireciona para página dos flashcards

    return render_template('criar.html')

@app.route('/excluir', methods=['POST'])
@login_required
def excluir_flashcard():
    flashcard_id = request.form.get('id')
    
    if not flashcard_id:
        flash('ID do flashcard não fornecido', 'error')
        return redirect(url_for('meus_flashcards'))

    conn = get_db_connection()
    flashcard = conn.execute(
        'SELECT * FROM flashcards WHERE id = ? AND id_usuario = ?',
        (flashcard_id, current_user.id)
    ).fetchone()

    if flashcard is None:
        flash('Flashcard não encontrado ou você não tem permissão para excluí-lo', 'error')
        return redirect(url_for('meus_flashcards'))

    conn.execute('DELETE FROM flashcards WHERE id = ?', (flashcard_id,))
    conn.commit()
    conn.close()

    flash('Flashcard excluído com sucesso!', 'success')
    return redirect(url_for('meus_flashcards'))

@app.route('/editar', methods=['POST'])
@login_required
def editar_flashcard():
    flashcard_id = request.form.get('id')

    if not flashcard_id:
        flash('ID do flashcard não fornecido', 'error')
        return redirect(url_for('meus_flashcards'))

    conn = get_db_connection()
    flashcard = conn.execute(
        'SELECT * FROM flashcards WHERE id = ? AND id_usuario = ?',
        (flashcard_id, current_user.id)
    ).fetchone()
    conn.close()

    if flashcard is None:
        flash('Flashcard não encontrado ou você não tem permissão para editá-lo', 'error')
        return redirect(url_for('meus_flashcards'))

    return render_template('editar.html', flashcard=flashcard)

@app.route('/atualizar', methods=['POST'])
@login_required
def atualizar_flashcard():
    id = request.form['id']
    materia = request.form['materia']
    pergunta = request.form['pergunta']
    resposta = request.form['resposta']

    conn = get_db_connection()
    flashcard = conn.execute(
        'SELECT * FROM flashcards WHERE id = ? AND id_usuario = ?',
        (id, current_user.id)
    ).fetchone()

    if flashcard is None:
        flash('Flashcard não encontrado ou você não tem permissão para atualizá-lo', 'error')
        conn.close()
        return redirect(url_for('meus_flashcards'))

    conn.execute('UPDATE flashcards SET materia = ?, pergunta = ?, resposta = ? WHERE id = ?', (materia, pergunta, resposta, id))
    conn.commit()
    conn.close()

    flash('Flashcard atualizado com sucesso!', 'success')
    return redirect(url_for('meus_flashcards'))

@app.route('/meus_flashcards')
@login_required
def meus_flashcards():
    conn = get_db_connection()
    flashcards = conn.execute(
        "SELECT * FROM flashcards WHERE id_usuario = ?", 
        (current_user.id,)
    ).fetchall()
    conn.close()

    ultimo_flashcard_id = request.cookies.get('ultimo_flashcard')

    return render_template('meus_flashcards.html', flashcards=flashcards, ultimo_flashcard_id=ultimo_flashcard_id)

@app.route('/marcar_flashcard/<int:flashcard_id>')
@login_required
def marcar_flashcard(flashcard_id):
    response = make_response(redirect(url_for('meus_flashcards')))
    response.set_cookie('ultimo_flashcard', str(flashcard_id), max_age=3600)  
    return response

@app.route('/dash')
@login_required
def dash():
    ultima_materia = request.cookies.get('ultima_materia')
    ultimo_flashcard_id = request.cookies.get('ultimo_flashcard')

    ultimo_flashcard = None
    if ultimo_flashcard_id:
        conn = get_db_connection()
        ultimo_flashcard = conn.execute(
            "SELECT * FROM flashcards WHERE id = ? AND id_usuario = ?",
            (ultimo_flashcard_id, current_user.id)
        ).fetchone()
        conn.close()

    return render_template('dash.html', ultima_materia=ultima_materia, ultimo_flashcard=ultimo_flashcard)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/perfil')
@login_required
def perfil():
    conn = get_db_connection()
    historico = conn.execute('''
        SELECT f.pergunta, h.data_utilizacao, h.acerto
        FROM flashcard_historico h
        JOIN flashcards f ON f.id = h.flashcard_id
        WHERE h.usuario_id = ?
        ORDER BY h.data_utilizacao DESC
    ''', (current_user.id,)).fetchall()
    conn.close()
    
    return render_template('perfil.html', user=current_user, historico=historico)

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def erro_do_servidor(e):
    return render_template("500.html"), 500

conn = get_db_connection()
conn.execute('''
    CREATE TABLE IF NOT EXISTS flashcard_historico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        flashcard_id INTEGER NOT NULL,
        data_utilizacao TEXT DEFAULT CURRENT_TIMESTAMP,
        acerto BOOLEAN,
        FOREIGN KEY (usuario_id) REFERENCES users(id),
        FOREIGN KEY (flashcard_id) REFERENCES flashcards(id)
    )
''')
conn.commit()
conn.close()

if __name__ == '__main__':
    app.run(debug=True)
