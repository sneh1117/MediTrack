web: gunicorn config.wsgi --log-file -
worker: celery -A config worker --loglevel=info
beat: celery -A config beat --loglevel=info
web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi --log-file -