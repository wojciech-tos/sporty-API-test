# Sporty.com task

## How to run PoetryAPI test:

- Clone this repository locally
- Enter main folder **sporty_WAP_task**
- Install, create and activate virtual environment
> pip install virtualenv

> virtualenv venv

> source venv/Scripts/activate
- Install requirements
> pip install -r requirements.txt
- Run all tests
> pytest --html=report.html

## Tests can be ran separately according to endpoints
- Run smoke tests
> pytest --html=report.html -m smoke
- Run author tests
> pytest --html=report.html -m author
- Run title tests
> pytest --html=report.html -m title
- Run combined tests
> pytest --html=report.html -m combined
- Run random tests
> pytest --html=report.html -m random

After test succeeds a report will be generated in main folder (**report.html**).
