# Email Classification Service

The purpose of this app is to learn Django. This codes contais a server that loads a classification model, previously trained, and does inference in runtime.

## Installation

Verify the python version installed. This project was built using python 3.7
```
python --version
```

Create a virtualenv
```
pyenv virtualenv 3.7.5 app
```

Activate the virtualenv
```
pyenv activate app
```

Install project dependencies requirement.txt
```
pip install -r requirements.txt
```

## Usage

To run the app localy, execute the following command
```
python manage.py runserver
```

This will expose a local URL. To interact with it, we can send different request using, for example, postman or curl.

## Endpoints

- **GET** `admin/` It allow us to access the admin page provided by django.

- **POST** `api-token-auth/` It allows to get a JWT token to interact with the app.

- **GET** `history/<n_emails>/` It allows to filter the las user's n_emails.

- **GET** `get_data/` Only available for super users. It allows to access to alll the data from the data base (Usuarios, Predicciones, User_Quotas)

- **GET** `get_users/` Only available for super users. It allows to get a list of all the user's names that use the application

- **GET** `health/` Endpoint useful for health check validation. It checks that the app is working.

- **POST** `process_email/` It allows to inferr the class of an email by sending in the text parameter the email text.

- **GET** `quota_info/` Given a user, it allows to know the amount of predictions used by the user and how many are still available.

- **GET** `test_if_logged/` It allows to validate if the user is logged in or not.


# Streamlit Dashboard


Verify the python version installed. This project was built using python 3.7
```
python --version
```

Create a virtualenv
```
pyenv virtualenv 3.7.5 streamlitapp
```

Activate the virtualenv
```
pyenv activate streamlitapp
```

Instal project dependencies
```
pip install -r requirements.txt
```

Run the dashboard. Important: In order to run the dashboard, it's necessary that the django service is running as the dashboards needs to comunicate and consume the APIs exposed by the classification app.
```
streamlit run api_dashboard.py 
```

## Environment Variable Configuration

There aree 3 environment variables that could be configured (`SPAM_APP_URL`, `SPAM_APP_ADMIN_USER`, `SPAM_APP_ADMIN_PASSWORD`) but it's not compulsory to do it given that the variables have a default value. This variables are in the file `sample.env` inside `streamlit-app`. If you want, you can change the values to run the streamlit dashboard pointing to the django service deployed in AWS.

## Docker

To run the docker image:
```
docker build -f Dockerfile -t app:latest .
```

To run the container locally.
```
docker run -p 8501:8501 app:latest
```
