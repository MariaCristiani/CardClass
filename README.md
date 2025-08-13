# CardClass

## O que é o CardClass?
O CardClass é um projeto desenvolvido para a matéria de Programa de Sistemas para Internet (PSI) que consiste em uma aplicação web para estudo por meio de flashcards.
O sistema permite que o usuário crie, edite, exclua e pesquise flashcards, além de armazenar um histórico de utilização e salvar o último flashcard acessado por meio de cookies.

## Tecnologias Utilizadas
Python 3
Flask
SQLite
HTML / CSS

## Para rodar localmente este projeto você precisa:
O CardClass foi feito utilizando o framework ```Flask``` para fazer a aplicação. Então você precisa seguir os seguintes passos, caso tenha interesse em rodar esse projeto localmente:
1. Clone o repositório do projeto na sua máquina. Você pode fazer isso utilizando o comando:
```cmd
git clone https://github.com/MariaCristiana/CardClass.git
```

2. Crie e ative o ambiente virtual.

```cmd
# Crie
python -m venv venv
```

```cmd
# Para ativar no Windows:
venv\Scripts\activate
```

```cmd
# Para ativar no Linux/Mac:
source venv/bin/activate
```

3. Em seguida, instale as dependências do projeto. Para instalar todos os requerimentos, utilize o comando:
```cmd
pip install -r requirements.txt
```

4. Crie o banco de dados inicial

```cmd
python iniciar.py
```

5. Execute a aplicação para iniciar

```cmd
flask run --debug
```

## Equipe e suas Funções
## 👥 Equipe e suas Funções

- **[Cristiani](https://github.com/MariaCristiani)**  
  "Criou o repositório no GitHub e configurou o banco de dados SQLite com a tabela de usuários.  
  Implementou as páginas de registro e login de usuários, além das páginas personalizadas para erros 404 e 500."

- **[Amanda Alves](https://github.com/AmandaA6)**  
  "Definiu o tema do sistema junto ao grupo e elaborou o Documento de Requisitos Funcionais.  
  Implementou o recurso de senha com hash seguro, desenvolveu funcionalidades de criação e listagem no CRUD, e foi responsável pelo README do projeto."

- **[Fernanda](https://github.com/Fernanda-Erika)**  
  "Montou a estrutura inicial do projeto, incluindo ambiente virtual, `app.py` e `requirements.txt`.  
  Implementou a autenticação com Flask-Login/sessões, a funcionalidade de edição no CRUD e o uso de `make_response` para cookies ou headers customizados."

- **[Priscylla](https://github.com/pribeea)**  
  "Criou o sistema de logout e desenvolveu os templates com `extends`/`includes` para base e navbar.  
  Implementou a exclusão no CRUD e participou da criação das páginas personalizadas para erros 404 e 500."

- **Todas**  
  "Colaboraram na escolha do tema do sistema, realizaram testes manuais, aplicaram estilização básica com CSS/Bootstrap e participaram dos ajustes finais para entrega no GitHub."
 tema do sistema, realizaram testes manuais, aplicaram estilização básica com CSS/Bootstrap e participaram dos ajustes finais para entrega no GitHub.
