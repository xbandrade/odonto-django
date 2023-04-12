# <img src="https://raw.githubusercontent.com/xbandrade/odonto-django/main/base_static/global/img/favicon.ico" width="4%">  Odonto Django

🌐  Deploy: https://odontodj.onrender.com

➡️ Um site de clínica odontológica criado com `Django` e `Django REST` frameworks, usando a metodologia TDD com testes com `Django` e `Selenium`, e usando o banco de dados `PostgreSQL`.

## ⚙️ Setup 
Para executar o projeto em um ambiente local, siga estes passos:

```python -m venv venv```

```pip install -r requirements.txt```

```cp .env-example .env```

```python -m main```

Não se esqueça de preencher o novo arquivo `.env`.

## 💻 Funcionalidades da Aplicação

❕Página Inicial e Header
- A logo `OdontoDj` redireciona o usuário para a página inicial.
- Enquanto não estiver logado, o usuário pode acessar as páginas `Serviços`, `Sobre`, `Login` e `Registrar`.
- Quando o usuário logar, as páginas `Agendar`, `Painel do Usuário` e `Logout` serão liberadas.

❕Serviços
- Exibe todos os tratamentos e procedimentos disponíveis, assim como seus respectivos preços.

❕Registrar
- O usuário deve fornecer informações válidas e únicas para se registrar.
- Os campos requeridos são `Nome de Usuário`, `Nome`, `Sobrenome`, `Email`, `CPF` e `Senha`.

❕Agendar
- Quando o usuário está logado, exibe um formulário de agendamento com todos os procedimentos, datas e horários disponíveis.
- Se o tratamento desejado não for encontrado, o usuário tem a opção de agendar uma consulta personalizada.
- Quando um formulário de consulta válido é submetido, um email será enviado para o usuário com um link de confirmação.

❕Painel de Usuário
- Exibe todas as consultas e o histórico de tratamento do usuário, com detalhes de cada consulta.
- Opções para atualizar as informações de usuário e alterar a senha também podem ser encontradas no painel do usuário.

## 🖱️ REST API
#### ➡️ A API foi criada usando Django REST Framework com autenticação JWT
❕JWT
- O usuário pode criar um novo token usando a URL `/users/api/token/`
- O token pode ser atualizado e verificado através das URLs `/users/api/token/refresh/` e `/users/api/token/verify/`, respectivamente.

❕API de Usuários
- Esta API permite obter dados do usuário logado através da URL `/users/api/<int:pk>/` ou `/users/api/me/`.
- Os dados do usuário também podem ser atualizados enviando um PATCH à URL `/users/api/<int:pk>/`.
- Um novo usuário pode ser criado enviando um POST à URL `/users/api/`.
  
❕API de Agendamento
- Esta API permite obter as consultas e o histórico de tratamento do usuário logado através da URL `/schedule/api/`.
- Detalhes sobre uma consulta específica podem ser obtidas através da URL `/schedule/api/<int:pk>/`.
- Uma nova consulta pode ser marcada enviando um POST à URL `/schedule/api/`.
- Uma consulta agendada pode ser cancelada enviando um DELETE à URL `/schedule/api/<int:pk>/`.

## ✔️ Testes
❕Testes funcionais usando `Selenium` estão localizados no diretório `/tests`, e testes unitários e de integração com `Django` estão armazenados dentro dos diretórios `/tests` na pasta de cada app.

