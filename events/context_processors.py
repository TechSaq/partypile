from .models import Item, EventType


def get_featured_items(request):

    featured_items = Item.objects.filter(is_featured=True)

    return {"featured_items": featured_items}


def get_event_types(request):

    event_types = EventType.objects.all()

    return {"event_types": event_types}
