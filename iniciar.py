import sqlite3

def criar_banco():
    conexao = sqlite3.connect('banco.db')
    with open('schema.sql') as f:
        conexao.executescript(f.read())
    conexao.close()
    print("Banco criado com sucesso!")

if __name__ == '__main__':
    criar_banco()
