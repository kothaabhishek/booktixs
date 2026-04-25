import datetime
import os

from django.core.management import call_command
from django.db import connection
from django.utils import timezone


_prepared = False


def prepare_serverless_database():
    """Prepare an ephemeral SQLite database for Vercel demo deployments."""
    global _prepared
    if _prepared or os.environ.get('DATABASE_URL'):
        return

    existing_tables = connection.introspection.table_names()
    if 'events_event' not in existing_tables:
        call_command('migrate', interactive=False, verbosity=0)

    from events.models import Category, Event

    music, _ = Category.objects.get_or_create(
        slug='music',
        defaults={'name': 'Music', 'icon': 'M'}
    )
    sports, _ = Category.objects.get_or_create(
        slug='sports',
        defaults={'name': 'Sports', 'icon': 'S'}
    )

    sample_events = [
        {
            'name': 'BookTix Live Night',
            'description': 'A high-energy live music showcase with top local performers.',
            'date': timezone.now() + datetime.timedelta(days=21),
            'venue': 'HITEX Exhibition Centre',
            'city': 'Hyderabad',
            'category': music,
            'price_general': 1499,
            'price_vip': 2499,
            'price_platinum': 3999,
            'total_seats': 500,
            'available_seats': 500,
            'is_active': True,
            'is_featured': True,
        },
        {
            'name': 'Premier Match Screening',
            'description': 'A stadium-style fan screening with food courts and live commentary.',
            'date': timezone.now() + datetime.timedelta(days=35),
            'venue': 'Gachibowli Indoor Stadium',
            'city': 'Hyderabad',
            'category': sports,
            'price_general': 799,
            'price_vip': 1499,
            'price_platinum': 2499,
            'total_seats': 300,
            'available_seats': 300,
            'is_active': True,
            'is_featured': True,
        },
    ]

    for event in sample_events:
        Event.objects.get_or_create(name=event['name'], defaults=event)

    _prepared = True
