# Lighthouse: Centralized Buoy client directory
Lighthouse will serve as an entry point to finding Buoy-enabled websites. See: [Project Proposal Lighthouse](https://github.com/betterangels/better-angels/wiki/Project-Proposal-Lighthouse) for details.

## Development
### Getting Started
First, install requirements using pip (ideally in a virtualenv).
`pip install -r requirements.txt`

Then, set up the django project:
```
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
```

To test: `python manage.py test lantern`

To run (on localhost:8000): `python manage.py runserver`
