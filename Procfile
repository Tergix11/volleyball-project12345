web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn volleyball_site.wsgi --bind 0.0.0.0:$PORT
