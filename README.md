## Introduction

BBQ Planner is a small Django app that allows an event organizer to sign up, create an event, share a link, and have visitors sign up and enter record their guest count and meal preferences.

To start the dev environment for the first time, make sure you have Docker installed, open init_admin.py and enter credentials of your choice. After the first run, you must comment the line. Then run:
```
docker-compose -f docker-compose.dev.yml up --build
```
From then on, you can ommit --build

Visit: [http://localhost:8000/](http://localhost:8000/)

You can then create an account, login, create event(s), share them, etc. To access the admin panel visit [http://localhost:8000/admin/](http://localhost:8000/admin/) and enter the credentials from init_admin.py. Take precautions not to commit this file to a repo for security reasons. The same applies to the secrets in the docker-compose files.

A preliminary production environment is available:
```
docker-compose -f docker-compose.prod.yml up --build
```
**Note**: It does not include a static file server or a WSGI server such as nginx (yet) + gunicorn, nor are secrets such as DB passwords kept properly. Therefore, it is not actually suitable for production yet.

To run test suite excluding migrations:
```
docker-compose -f docker-compose.dev.yml exec web coverage run --source=app --omit=*/migrations/*  manage.py test -v 2
```
-v is the verbosity factor

Generate a coverage report:
```
docker-compose -f docker-compose.dev.yml exec web coverage html
```

# Concepts applied

### SOLID principles
Single responsibility, open for extension, LSP, etc.

### Loosely coupled
Separation of views, models, templates ensures high cohesion. Views were split into separate classes/files. 

### Use Django for as much as possible*
Django has a lot of features that I had not known of previously, but tried to use as many as possible to avoid reinventing the wheel.

### DRY
Keep as much as possible within models to avoid repeating common operations.

### Fat models
Keep as much domain logic as possible within models.

### Testable
Through fat models, most of the logic is testable. Although I did not write enough tests for 100% coverage of the views, the models are 98% covered.

### Clean & Readable
Clear method and variable names, tried to keep code smells as low as possible.

# Reflection
As my first Django app, I found the framework more feature rich than I was expecting, having previously (in Python) only used Flask for REST APIs. There are plenty of things I could have done better. A major non-source code improvement would've been to use commits more logically i.e. create a commit for each feature/class/etc with a good description rather than this god awful everything in one commit I'm about to make.

# TODO
* Use more Django features, particularly in regards to forms.
* Nothing needs to be edited once it has been created.
* Events have simple auto incremented ints as their id, not randomly generated slugs
* A user can resubmit any of the forms as many times as they want. They could fill the database with as many visitors/guests and meat choices as they want.
* Very little form validation
* Only one time zone
* Could improve database operations with some transactions
* Improve tests, also use Selenium
* The URL on the events list is hard coded
* The meat options input (comma separated) isn't great
* CI/CD pipeline e.g. Travis

# Assumptions made
* Visitors don't need an account to register for an event
* While visitors have a name, their guests are nameless
* An event organiser can create multiple events
* Each event has its own set of meat choices i.e. Choices need to be recreated for each event. This is because (in the future) events may update choices last minute e.g. Steak 200g to Steak 100g, but other events may not want the same change
* A visitor sums up the amount of meats for his guests