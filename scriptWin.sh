find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

rm db.sqlite3


python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminadmin')" | python manage.py shell
echo "import sifranti.naredi_bazo; sifranti.naredi_bazo.naredi_bazo(None)" | python manage.py shell
