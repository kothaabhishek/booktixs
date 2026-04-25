from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Event, Category


def event_list(request):
    events = Event.objects.filter(is_active=True, date__gt=timezone.now())
    categories = Category.objects.all()

    city = request.GET.get('city', '')
    category = request.GET.get('category', '')
    search = request.GET.get('q', '')

    if city:
        events = events.filter(city__icontains=city)
    if category:
        events = events.filter(category__slug=category)
    if search:
        events = events.filter(name__icontains=search)

    featured = events.filter(is_featured=True)[:3]

    return render(request, 'events/event_list.html', {
        'events': events,
        'featured': featured,
        'categories': categories,
        'city': city,
        'selected_category': category,
        'search': search,
    })


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_active=True)
    related = Event.objects.filter(
        category=event.category,
        is_active=True,
        date__gt=timezone.now()
    ).exclude(pk=pk)[:3]
    return render(request, 'events/event_detail.html', {
        'event': event,
        'related': related,
    })
