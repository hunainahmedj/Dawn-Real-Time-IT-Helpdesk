from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (

    home_view,
    dash_view,
    TicketListView,
    TicketDetailView,
    TicketCreateView,
    create_notification,
    change_priority,
    assign_ticket,
    create_note,
    change_status,
    email_user,
    track_ticket,
    create_todo,
    delete_todo,
    ticket_delete,
    email_view,
    set_duedate,
    data_graphs,
)

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='scheduler/home.html'), name='home'),
    path('dash/', dash_view, name='dash'),
    path('notification/', create_notification, name='notification'),
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('ticket/new/', TicketCreateView.as_view(), name='ticket-create'),
    path('ticket/delete', ticket_delete, name='ticket-delete'),
    path('ticket/track', track_ticket, name='ticket-track'),
    path('ticket/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('ticket/change_priority/', change_priority, name='change-priority'),
    path('ticket/assign_ticket/', assign_ticket, name='ticket-assign'),
    path('ticket/set_duedate/', set_duedate, name='ticket-due'),
    path('ticket/add_note/', create_note, name='create-note'),
    path('create/todo', create_todo, name='create-todo'),
    path('delete/todo', delete_todo, name='delete-todo'),
    path('ticket/change_status/', change_status, name='ticket-change-status'),
    path('ticket/email/', email_user, name='email-user'),
    path('email/', email_view, name='email'),
    path('graphs/', data_graphs, name='data-graphs'),

]
