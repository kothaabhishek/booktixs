import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booktix.settings')
application = get_wsgi_application()

if os.environ.get('VERCEL'):
    from booktix.startup import prepare_serverless_database

    prepare_serverless_database()
