# Documento de Requisitos Funcionais  
## Projeto: StudyCards  
**Tema:** Plataforma para registro e estudo de conteúdos por meio de flashcards organizados por matérias e temas personalizados.

## 1. Cadastro e Autenticação

- **RF01:** O usuário poderá criar uma conta com e-mail e senha
- **RF02:** O usuário poderá realizar login e logout
- **RF03:** As senhas serão armazenadas utilizando hash seguro 

## 2. Gerenciamento de Matérias e Flashcards

- **RF04:** O sistema disponibilizará algumas matérias com flashcards prontos, criados pela equipe da plataforma
- **RF05:** O usuário poderá visualizar os flashcards por matéria e tema
- **RF06:** O usuário poderá criar novas matérias personalizadas
- **RF07:** O usuário poderá adicionar flashcards personalizados dentro de qualquer matéria, informando termo/pergunta e definição/resposta
- **RF08:** O usuário poderá editar ou excluir seus próprios flashcards
- **RF09:** O usuário poderá marcar flashcards como “difícil” ou “para revisar depois”
- **RF10:** O sistema deve garantir que cada usuário possa visualizar, editar e excluir apenas seus próprios dados
- **RF11:** O sistema não permite interação entre usuários — é uma plataforma de uso individual

## 3. Gerenciamento de Perfil do Usuário

- **RF12:** O sistema deve exibir ao usuário um painel de progresso contendo:
  - A matéria/tema que está sendo revisada no momento
  - Número de flashcards visualizados
  - Flashcards marcados como “difícil” ou “favorito”  
  - Um histórico geral de estudo por matéria

- **RF13:** O usuário poderá editar informações do seu perfil, como nome, foto e outros dados pessoais  
- **RF14:** O usuário poderá visualizar seu perfil com todas as informações atualizadas

## 4. Modelos e Navegação

- **RF15:** O sistema deve utilizar `extends` e `includes` nos templates para estrutura de layout base (navbar, footer, etc)
- **RF16:** A página inicial (homepage) apresentará a proposta da plataforma, com opções de login e cadastro
- **RF17:** O sistema deve conter uma área pessoal do usuário com lista de matérias criadas e acesso aos flashcards  
- **RF18:** As páginas de criação e edição de flashcards devem conter formulários simples e intuitivos
- **RF19:** O sistema deve exibir páginas personalizadas para erros 404 (não encontrado) e 500 (erro interno)


## 5. Requisitos Técnicos

- **RF20:** O sistema deve utilizar `request` para processar dados de formulários (login, cadastro, criação de flashcards, etc)
- **RF21:** O sistema deve utilizar `redirect` e `url_for` para redirecionamento entre rotas
- **RF22:** O sistema deve utilizar `make_response` quando necessário, para cookies ou cabeçalhos personalizados
- **RF23:** O código-fonte deve ser versionado no GitHub com entregas semanais seguindo o cronograma do projeto  
- **RF24:** O repositório deve conter um `README.md` detalhado com instruções de instalação, dependências utilizadas e capturas de tela da aplicação

