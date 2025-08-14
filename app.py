from flask import Flask, render_template, request, redirect, url_for, flash, make_response, redirect, url_for
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
        existente = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone() 

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
            return redirect(url_for('index'))  
        
        flash('Email ou senha incorretos!', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')

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
        return redirect(url_for('meus_flashcards'))  
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
    
    # Pega todos os flashcards do usuário, já ordenando por matéria
    flashcards = conn.execute(
        "SELECT * FROM flashcards WHERE id_usuario = ? ORDER BY materia, id",
        (current_user.id,)
    ).fetchall()
    
    conn.close()

    # Agrupar por matéria
    flashcards_por_materia = {}
    for f in flashcards:
        materia = f['materia'] or 'Outros'
        if materia not in flashcards_por_materia:
            flashcards_por_materia[materia] = []
        flashcards_por_materia[materia].append(f)

    ultimo_flashcard = request.cookies.get('ultimo_flashcard')
    
    return render_template(
        'meus_flashcards.html',
        flashcards_por_materia=flashcards_por_materia,
        ultimo_flashcard=ultimo_flashcard
    )

@app.route('/marcar')
@login_required
def marcar_flashcard():
    flashcard_id = request.args.get('flashcard_id')
    if not flashcard_id:
        flash('ID não informado', 'error')
        return redirect(url_for('meus_flashcards'))

    conn = get_db_connection()
    
    flashcard = conn.execute('SELECT materia FROM flashcards WHERE id = ?', 
                           (flashcard_id,)).fetchone()
    
    conn.execute('''
        INSERT INTO flashcard_historico (usuario_id, flashcard_id, acerto)
        VALUES (?, ?, NULL)
    ''', (current_user.id, flashcard_id))
    
    conn.commit()
    conn.close()

    response = make_response(redirect(url_for('meus_flashcards')))
    response.set_cookie('ultimo_flashcard', flashcard_id, max_age=60*60*24*30)
    return response

@app.route('/dash')
@login_required
def dash():
    conn = get_db_connection()

    flashcard_id = request.cookies.get('ultimo_flashcard')
    ultimo_flashcard = None

    if flashcard_id:
        ultimo_flashcard = conn.execute(
            'SELECT * FROM flashcards WHERE id = ? AND id_usuario = ?',
            (flashcard_id, current_user.id)
        ).fetchone()

    conn.close()

    return render_template('dash.html', ultimo_flashcard=ultimo_flashcard)

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
        SELECT f.materia, f.pergunta
        FROM flashcard_historico h
        JOIN flashcards f ON f.id = h.flashcard_id
        WHERE h.usuario_id = ?
        ORDER BY h.data_utilizacao DESC
    ''', (current_user.id,)).fetchall()
    conn.close()
    
    return render_template('perfil.html', user=current_user, historico=historico)

@app.route('/buscar', methods=['GET'])
@login_required
def buscar_flashcards():
    termo = request.args.get('q', '').strip()
    
    if not termo:
        flash('Digite um termo para pesquisar', 'error')
        return redirect(url_for('meus_flashcards'))
    
    conn = get_db_connection()
    
    flashcards = conn.execute('''
        SELECT * FROM flashcards 
        WHERE id_usuario = ? 
        AND (pergunta LIKE ? OR resposta LIKE ? OR materia LIKE ?)
        ORDER BY materia
    ''', (current_user.id, f'%{termo}%', f'%{termo}%', f'%{termo}%')).fetchall()
    
    conn.close()

    flashcards_por_materia = {}
    for f in flashcards:
        materia = f['materia'] or 'Outros'
        if materia not in flashcards_por_materia:
            flashcards_por_materia[materia] = []
        flashcards_por_materia[materia].append(f)

    ultimo_flashcard = request.cookies.get('ultimo_flashcard')
    
    return render_template(
        'meus_flashcards.html',
        flashcards_por_materia=flashcards_por_materia,
        ultimo_flashcard=ultimo_flashcard,
        termo_busca=termo
    )

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def erro_do_servidor(e):
    return render_template("500.html"), 500

if __name__ == '__main__':
    app.run(debug=True)
