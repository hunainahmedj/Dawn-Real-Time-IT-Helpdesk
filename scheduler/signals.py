from scheduler.models import Ticket
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Ticket)
def announce_new_ticket(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "gossip", {
                "type": "ticket.gossip",
                "event": "New Ticket",
                "ticket": {
                    'ticket_id': instance.id,
                    'ticket_subject': instance.subject,
                    'ticket_username': instance.username,
                    # 'ticket_status': instance.ticket_status,
                    'ticket_department': {
                        'department_id': instance.user_department.id,
                        'department_name': instance.user_department.department_name,
                    },
                }
            }
        )