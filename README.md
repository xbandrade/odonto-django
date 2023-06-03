# <img src="https://raw.githubusercontent.com/xbandrade/odonto-django/main/base_static/global/img/favicon.ico" width="4%">  Odonto Django

🗒️🇧🇷 [README pt-BR](https://github.com/xbandrade/odonto-django/blob/main/README-pt-BR.md)

🌐  Deploy: https://odontodj.onrender.com


➡️ A dental clinic website built with `Django` and `Django REST` frameworks, using the TDD methodology with `Django` and `Selenium` tests, and the `PostgreSQL` database.

## ⚙️ Setup 
To run the project in a local environment, follow these steps:

```python -m venv venv```

```pip install -r requirements.txt```

```cp .env-example .env```

```python -m main```

Make sure to fill in the new `.env` file.

## 💻 Application Features

❕Home Page and Header
- The `OdontoDj` logo redirects the user to the home page. 
- While not logged in, the user can access the `Services`, `About`, `Login` and `Register` pages.
- When the user logs in, the pages `Schedule`, `Dashboard` and `Logout` are granted access. 

❕Services
- Displays all available treatments and procedures as well as their respective prices. 

❕Register
- The user must provide valid and unique information to register.
- The required fields are `Username`, `First Name`, `Last Name`, `Email`, `CPF` and `Password`.

❕Schedule
- When the user is logged in, displays a scheduler form with all available procedures, dates and times for an appointment.
- If the desired treatment is not found, the user has the option to schedule a custom appointment.
- When a valid appointment form is submitted, an email will be sent to the logged user with a confirmation link.

❕Dashboard
- Displays all the user's appointments and treatment history, with details for each appointment.
- Options to update the user's information and change the password can also be found in the dashboard.

## 🖱️ REST API
#### ➡️ The API was built using `Django REST Framework`, with `JWT` authentication
❕JWT
- The user can create a new token using the URL `/users/api/token/`
- The token can be refreshed and verified via the URLs `/users/api/token/refresh/` and `/users/api/token/verify/`, respectively.

❕Users API
- This API lets you retrieve the logged user's data using the URL `/users/api/<int:pk>/` or `/users/api/me/`.
- The user's data can also be updated by sending a PATCH to the URL `/users/api/<int:pk>/`.
- A new user can be created by sending a POST to the URL `/users/api/`.
  
❕Schedule API
- This API allows you to retrieve the logged user's appointments and treatment history using the URL `/schedule/api/`.
- Details about a specific appointment can be retrieved using the URL `/schedule/api/<int:pk>/`.
- A new appointment can be scheduled by sending a POST to the URL `/schedule/api/`.
- A scheduled appointment can be canceled by sending a DELETE to the URL `/schedule/api/<int:pk>/`.

## ✔️ Tests
❕Functional tests using `Selenium` are located in the `/tests` directory, and `Django` unit and integration tests are stored within the `/tests` directory of each individual app folder.
