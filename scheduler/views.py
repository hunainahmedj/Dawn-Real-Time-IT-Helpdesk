from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib import messages

from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse

from ipware import get_client_ip


from . import models
from users.models import User, LoggedUser
from .forms import TicketForm, TicketTrackForm
from django.views.generic import (

    ListView,
    DetailView,
    CreateView,

)

from mailer.email import Email
from datetime import datetime, date
from django.utils import timezone
import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(message)s:%(asctime)s')

file_handler = logging.FileHandler('./logs/ticket.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def home_view(request):
    return render(request, "scheduler/home.html")


# Dashboard Logic

@login_required(login_url='/')
def dash_view(request):

    active_tickets  = models.Ticket.objects.filter(ticket_status=1, is_deleted=False)
    due_date_tickets = models.Ticket.objects.filter(date_due__date=date.today(), is_deleted=False).exclude(ticket_status=2)
    hold_tickets = models.Ticket.objects.filter(ticket_status=3, is_deleted=False)
    active_users = LoggedUser.objects.all()
    gen_note = models.Notification.objects.first()

    ticket_logs = open("./logs/ticket.log","r")
    admin_logs = open("./logs/admin.log", "r")

    if ticket_logs.mode == 'r':
        ticket_logs = ticket_logs.read()
    if admin_logs.mode == "r":
        admin_logs = admin_logs.read()


    context = {
        'title': 'Dashboard',
        'active_tickets': len(active_tickets),
        'hold_tickets': len(hold_tickets),
        'due_today': len(due_date_tickets),
        'gen_note': gen_note,
        'active_users': active_users,
        "ticket_logs": ticket_logs,
        "admin_logs": admin_logs,
    }

    return render(request, "scheduler/ticket_dash.html", context)

# ############################ #

class TicketCreateView(CreateView):

    model = models.Ticket
    template_name = 'scheduler/ticket_new.html'
    form_class = TicketForm

    def form_valid(self, form):

        username = self.request.POST.get('username')
        tickets = models.Ticket.objects.all()

        if not tickets:
            ticket_id = 1
        else:
            ticket_id = models.Ticket.objects.last().id + 1

        email = models.Email.objects.get(id=1)
        subject = email.subject
        subject = str(subject) + " Ticket tracking ID: " + str(ticket_id)
        user_ticket_desc = self.request.POST.get('ticket_description')
        body = email.body + " Your original request description: (" + str(user_ticket_desc) + ")"
        user_email = self.request.POST.get('email')

        # Emailing
        email = Email(
            user_email,
            subject,
            body)
        email.send_mail()

        messages.success(self.request, "Ticket has been submitted you will get a response soon.")
        logger.info(f'Ticket:{ticket_id} created by IP:{get_client_ip(self.request)}, User:{username}');

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TicketCreateView, self).get_context_data(**kwargs)
        context['knowledgebase'] = models.KnowledgeBase.objects.all()
        return context


def create_notification(request):

    notifications = models.Notification.objects.all().delete()
    new_notification_data = request.POST.get('notif')
    new_notification = models.Notification(notification=new_notification_data)
    new_notification.save()

    return redirect('dash')




class TicketListView(LoginRequiredMixin, ListView):
    login_url = '/'
    model = models.Ticket
    queryset = models.Ticket.objects.filter(is_deleted=False)
    template_name = "scheduler/tickets_list.html"
    context_object_name = "tickets"
    # ordering = ["date_created"]

    users = User.objects.all()
    dict = {}

    for user in users:
        for skill in user.skill_set.all():

            if skill.skill_type in dict:
                dict[skill.skill_type].append(user)
            else:
                dict[skill.skill_type] = [user]


    def get_context_data(self, **kwargs):
        context = super(TicketListView, self).get_context_data(**kwargs)
        context['priorities'] = models.Priority.objects.all()
        # context['skills'] = models.Skill.objects.all()
        # context['users'] = get_user_model().objects.all()
        context['title'] = 'Manage Tickets'
        context['skilled_set'] = self.dict
        return context


class TicketDetailView(DetailView):
    model = models.Ticket
    template_name = 'scheduler/ticket_detail.html'
    context_object_name = "ticket"

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        context['notes'] = models.Note.objects.filter(ticket=self.kwargs['pk'])
        context['title'] = "Ticket Detail"
        return context


def change_priority(request):

    ticket = models.Ticket.objects.get(id=request.GET.get('ticket_id'))
    priority = models.Priority.objects.get(id=request.GET.get('ticket_priority'))

    if ticket.ticket_status.status != "Close":
        ticket.ticket_priority = priority
        ticket.save()
        logger.info(f'Priority:[{priority.priority}] assigned by IP:{get_client_ip(request)}, Admin:[{request.user.first_name} {request.user.middle_name} {request.user.last_name}] to Ticket:[{ticket.id}]');
        data = {
            'success': 'Priority has been updated!'
        }
    else:
        data = {
            'warning': 'Ticket has already been closed!'
        }

    return JsonResponse(data)


def assign_ticket(request):

    ticket = models.Ticket.objects.get(id=request.GET.get('ticket_id'))
    user = User.objects.get(id=request.GET.get('staffToAssign'))
    ticket.staff_assigned = user
    ticket.save()

    # Handling Email
    email = models.Email.objects.get(id=2)
    subject = email.subject
    subject = str(subject) + " Ticket tracking ID: " + str(ticket.id)
    body = f'{user.first_name} {user.middle_name} {user.last_name} has been assigned to your ticket. ' + email.body
    user_email = ticket.email

    # Emailing
    email = Email(
        user_email,
        subject,
        body)
    email.send_mail()



    logger.info(f'Technician:[{user.first_name} {user.middle_name} {user.last_name}] assigned to Ticket:[{ticket.id}] by IP:{get_client_ip(request)}, Admin:[{request.user.first_name} {request.user.middle_name} {request.user.last_name}]');

    data = {"success": 'Ticket has been assigned Assigned!'}

    return JsonResponse(data)


def change_status(request):

    ticket = models.Ticket.objects.get(id=request.GET.get('ticket_id'))

    if ticket.ticket_status.status != 'Close':
        status = models.Status.objects.get(status=request.GET.get('statusId'))
        ticket.ticket_status = status
        ticket.save()

        # Handling Email

        if status.status == 'Close':

            # Handling Email
            email = models.Email.objects.get(id=3)
            subject = email.subject
            subject = str(subject) + " Ticket tracking ID: " + str(ticket.id)
            body = email.body
            user_email = ticket.email

            # Emailing
            email = Email(
                user_email,
                subject,
                body)
            email.send_mail()

        logger.info(f'Status changed to [{status.status}] by IP:{get_client_ip(request)}, Admin:[{request.user.first_name} {request.user.middle_name} {request.user.last_name}] for Ticket:[{ticket.id}]');

        data = {
            'success': 'Status has been changed!'
        }

    else:
        data = {
            'warning': 'Ticket has already been closed!'
        }

    return JsonResponse(data)


def set_duedate(request):


    date = datetime.strptime(request.GET.get('due_date'), '%Y-%m-%d')
    today = datetime.today()

    if date.date() >= today.date():
        ticket = models.Ticket.objects.get(id=request.GET.get('ticket_id'))
        ticket.date_due = date
        ticket.save()
        context = { 'success': 'Due date has been assigned.'}
    else:
        context = { 'warning': 'Select a valid date.'}

    return JsonResponse(context)


def ticket_delete(request):

    ticket = models.Ticket.objects.get(id=request.GET.get('ticket_id'))
    ticket.is_deleted = True
    if ticket.ticket_status.status != "Close":
        ticket.ticket_status = models.Status.objects.get(status="Close")
    ticket.save()
    logger.info(f'Ticket:{ticket.id} deleted by IP:{get_client_ip(request)}, Admin:{request.user.first_name} {request.user.middle_name} {request.user.last_name}');
    return JsonResponse({'success': 'Ticket Deleted!'})


def track_ticket(request):

    title = 'Track Request'
    form = TicketTrackForm()

    if request.method == 'POST':
        form = TicketTrackForm(request.POST)

        if form.is_valid():

            ticket = form.cleaned_data['ticket_id']
            email = form.cleaned_data['email']

            found_ticket = models.Ticket.objects.filter(id=ticket, email=email)

            if found_ticket:
                return redirect('ticket-detail', pk=ticket)
            else:
                context = {
                    'title': title,
                    'form': form,
                }
                messages.warning(request, f'No such tickets exist')
                return render(request, "scheduler/ticket_search.html", context)

        else:

            form = TicketTrackForm()
            context = {'title': 'Track Ticket', 'form': form}
            return render(request, "scheduler/ticket_search.html", context)

    return render(request, "scheduler/ticket_search.html", {'title': 'Track Ticket', 'form': form})



def create_note(request):

    ticket = models.Ticket.objects.get(id=request.GET.get('ticket_id'))
    user = request.user
    note_data = request.GET.get('note')
    new_note = models.Note(ticket=ticket, staff_user=user, ticket_note=note_data)
    new_note.save()
    return JsonResponse({'msg':'Note has been added'})

def delete_todo(request):

    todo = models.ToDo.objects.get(id=request.GET.get('todo_id'))
    todo.delete()
    return JsonResponse({ 'success': 'Note Deleted!' })


def create_todo(request):

    user = request.user
    todo_name = request.GET.get('subject')
    todo_body = request.GET.get('body')
    new_todo = models.ToDo(staff_user=user, todo_name=todo_name, todo=todo_body)
    new_todo.save()
    return JsonResponse({'success': 'ToDo has been added!'})



def email_user(request):
    recip = request.GET.get('email')
    subject = request.GET.get('subject')
    body = request.GET.get('body')

    email = Email(
        recip,
        subject,
        body)

    email.send_mail()

    return JsonResponse({'msg': 'Email Sent'})

def email_view(request):

    if request.POST:
        subject = request.POST.get('subject')
        user_email = request.POST.get('userEmail')
        body = request.POST.get('body')
        messages.success(request, "Your email has been sent. A representative will get in touch soon.")

    return render(request, 'scheduler/email.html', { 'title': 'Email IT Admin'})


def data_graphs(request):

    departments = models.Department.objects.values()
    tickets = models.Ticket.objects.values('user_department', 'request_type', 'staff_assigned', 'ticket_status')
    skills = models.Skill.objects.values()
    users = User.objects.values()

    context = {
        "departments": list(departments),
        "skills": list(skills),
        "tickets": list(tickets),
        "users": list(users)
    }

    return JsonResponse(context, safe=False)