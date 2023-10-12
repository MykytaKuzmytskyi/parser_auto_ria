# ParserAutoRia

An application for parsing used cars on the website, 
filling the database and dumping data into a csv file. 
The script runs every day at 00:00. 
"https://auto.ria.com/uk/car/used/"

There are two ways to run the program

Install PostgresSQL and create db

### Local Run
1. Clone the source code:

```bash
git clone https://github.com/MykytaKuzmytskyi/parser_auto_ria.git
cd parser_auto_ria
```

2. Install PostgresSQL and create DB.
3. Install modules and dependencies:

```bash
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```

4. `.env_sample`
   This is a sample .env file for use in local development.
   Duplicate this file as .env in the root of the project
   and update the environment variables to match your
   desired config. You can use [djecrety.ir](https://djecrety.ir/)

5. Use the command to configure the database and tables:

```bash
python manage.py migrate
```

6. Run Redis server.

7. Run celery for tasks handling:

```bash
celery -A parser_auto_ria worker -l info
```
8. Run Celery beat for task scheduling:

```bash
celery -A parser_auto_ria beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

9. Start the app:

```bash
python manage.py runserver
```

### Run with docker
Copy .env_sample -> .env and populate with all required data

Docker should be installed

```commandline
docker-compose up --build
```

You can also run the script after starting the program using the link.
```commandline
http://127.0.0.1:8000/start_pars/
```