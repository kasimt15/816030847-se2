[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/uwidcit/flaskmvc)
<a href="https://render.com/deploy?repo=https://github.com/uwidcit/flaskmvc">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>

![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Flask MVC Template
A template for flask applications structured in the Model View Controller pattern [Demo](https://dcit-flaskmvc.herokuapp.com/). [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)


# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing Dependencies
```bash
$ pip install -r requirements.txt
```

# Configuration Management


Configuration information such as the database url/port, credentials, API keys etc are to be supplied to the application. However, it is bad practice to stage production information in publicly visible repositories.
Instead, all config is provided by a config file or via [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/).

## In Development

When running the project in a development environment (such as gitpod) the app is configured via default_config.py file in the App folder. By default, the config for development uses a sqlite database.

default_config.py
```python
SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
```

These values would be imported and added to the app in load_config() function in config.py

config.py
```python
# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...
```

## In Production

When deploying your application to production/staging you must pass
in configuration information via environment tab of your render project's dashboard.

![perms](./images/fig1.png)

# Flask Commands

wsgi.py is a utility script for performing various tasks related to the project. You can use it to import and test any code in the project. 
You just need create a manager command function, for example:

```python
# inside wsgi.py

user_cli = AppGroup('user', help='User object commands')

@user_cli.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

app.cli.add_command(user_cli) # add the group to the cli

```

```python
@user_cli.command("create", help="Creates a user")
@click.argument("name", default="rob")
@click.argument("address", default="1440_johnson&johnson_st_hidden_leaf_village")
def create_user_command(name, address):
    new_user= create_user(name, address)

    if isinstance(new_user, User):
        print(f'{name} created!')
    else:
        print(new_user)

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())
Then execute the command invoking with flask cli with command name and the relevant parameters

```bash
$ flask user create bob bobpass
```
```python
@competition_cli.command("create", help= "create a competition")
@click.argument("name", default= "code4runners")
@click.argument("venue", default= "online")
@click.argument("date", default= "2024-09-27")
@click.argument("start_time", default= "09:00:00")
@click.argument("end_time", default= "13:00:00")
@click.argument("participant", default= 0)
def create_competition_command(name, venue, date, start_time, end_time, participant):
    startTime= datetime.strptime(start_time, "%H:%M:%S").time()
    endTime= datetime.strptime(end_time, "%H:%M:%S").time()
    
    create_competition(name, venue, date, startTime, endTime, participant)
    print(f"{name} was created!")

@competition_cli.command("list", help="Lists competitions in the database")
@click.argument("format", default="string")
def list_competition_command(format):
    if format == 'string':
        print(get_all_competitions())
    else:
        print(get_all_competitions_json())


```

# Running the Project

_For development run the serve command (what you execute):_
```bash
# Run the Flask application
$ flask run

# User Commands
# Create a user with default values
$ flask user create bob "1234 Elm Street"

# List all users in string format
$ flask user list

# List all users in JSON format
$ flask user list json

# Coordinator Commands
# Create a coordinator with default values
$ flask coordination create_user

# Create a coordinator with custom values
$ flask coordination create_user "Alice" "123 Wonderland Ave"

# List all coordinators in string format
$ flask coordination list_users

# List all coordinators in JSON format
$ flask coordination list_users json

# Coordination Commands
# Create a coordination relationship with default IDs
$ flask coordination create

# Create a coordination relationship with custom IDs
$ flask coordination create 1 2

# List all coordinations in string format
$ flask coordination list

# List all coordinations in JSON format
$ flask coordination list json

# Competition Commands
# Create a competition
$ flask competition create "New Competition" "Stadium" "2024-10-01" "10:00:00" "14:00:00" 5

# List all competitions in string format
$ flask competition list

# List all competitions in JSON format
$ flask competition list json

# Participant Commands
# Create a participation relationship
$ flask participant create 1 1

# List all participations in string format
$ flask participant list

# List all participations in JSON format
$ flask participant list json

# Delete a participation relationship
$ flask participant delete 1 1
```

_For production using gunicorn (what the production server executes):_
```bash
$ gunicorn wsgi:app
```

# Deploying
You can deploy your version of this app to render by clicking on the "Deploy to Render" link above.

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. This must also be executed once when running the app on heroku by opening the heroku console, executing bash and running the command in the dyno.

```bash
$ flask init
```

# Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```

# Testing

## Unit & Integration
Unit and Integration tests are created in the App/test. You can then create commands to run them. Look at the unit test command in wsgi.py for example

```python
@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))
```

You can then execute all user tests as follows

```bash
$ flask test user
```

You can also supply "unit" or "int" at the end of the comand to execute only unit or integration tests.

You can run all application tests with the following command

```bash
$ pytest
```

## Test Coverage

You can generate a report on your test coverage via the following command

```bash
$ coverage report
```

You can also generate a detailed html report in a directory named htmlcov with the following comand

```bash
$ coverage html
```

# Troubleshooting

## Views 404ing

If your newly created views are returning 404 ensure that they are added to the list in main.py.

```python
from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list
views = [
    user_views,
    index_views
]
```

## Cannot Update Workflow file

If you are running into errors in gitpod when updateding your github actions file, ensure your [github permissions](https://gitpod.io/integrations) in gitpod has workflow enabled ![perms](./images/gitperms.png)

## Database Issues

If you are adding models you may need to migrate the database with the commands given in the previous database migration section. Alternateively you can delete you database file.
