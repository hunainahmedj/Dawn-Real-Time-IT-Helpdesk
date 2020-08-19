from .models import Ticket
from datetime import datetime, timezone


def recent_tickets(request):

    now = datetime.now(timezone.utc)
    all_tickets = Ticket.objects.filter(is_deleted=False)
    recent_tickets = []

    # 28800 = 8 hours

    for t in all_tickets:

        diff = t.date_created - now
        if diff.seconds <= 88800:
            recent_tickets.append(t)

    data = {
        'recent_tickets': recent_tickets
    }

    return data

