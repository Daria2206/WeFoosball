# Foosball
A mock web application written with Flask + sqlite3 + SQLAlchemy.
For security resons client_secret.json is not stored in GitHub but it's
necessery for the app to work.

To install required packages type:
pip install -r requirements.txt

To create db run:
python manage.py shell
db.create_all()
quit()

To run app type:
python manage.py runserver
