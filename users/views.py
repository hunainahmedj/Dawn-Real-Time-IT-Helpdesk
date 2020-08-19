from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from django.http import JsonResponse

import logging
from ipware import get_client_ip

# Models Import
from scheduler.models import Ticket, Department, Skill, ToDo, Email, EmailCreds

# Forms Import
from .forms import UserAdminCreationForm, DepartmentForm, SkillForm, SkillUpdateForm


# Handling Logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(message)s:%(asctime)s')

file_handler = logging.FileHandler('./logs/admin.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# ###################################### #

@login_required(login_url = '/')
def profile(request):

    User = get_user_model().objects.get(id=request.user.id)

    tickets = Ticket.objects.filter(staff_assigned = User)
    notes = ToDo.objects.filter(staff_user = User)

    context = {
        'tickets': tickets,
        'notes': notes,
        'title': 'Technician Profile'
    }

    return render(request, 'users/profile.html', context)

# Handling Super User Forms and Panel

def super_pannel(request):

    context = {}
    users = get_user_model().objects.all()
    skills = Skill.objects.all()
    departments = Department.objects.all()
    tickets = Ticket.objects.filter(is_deleted=False)
    new_email = Email.objects.get(id=1)
    update_email = Email.objects.get(id=2)
    close_email = Email.objects.get(id=3)
    email_settings = EmailCreds.objects.first()

    client_ip = get_client_ip(request)

    if request.method == 'POST':

        # print (request.POST)

        Userform = UserAdminCreationForm(request.POST)
        Departform = DepartmentForm(request.POST)
        SkForm = SkillForm(request.POST)
        SKUpdateForm = SkillUpdateForm(request.POST)

        context = {
            'title': 'Super Admin Panel',
            'users': users,
            'tickets': tickets,
            'skills': skills,
            'departments': departments,
            'new_email': new_email,
            'update_email': update_email,
            'close_email': close_email,
            'Userform': Userform,
            'DepartForm': Departform,
            'SkillForm': SkForm,
            'SkillUForm': SKUpdateForm,
            'emailSettings': email_settings,
        }

        if Userform.is_valid():
            Userform.save()
            email = Userform.cleaned_data.get('email')
            logger.info(f'New Technician [{email}] has been added by [{request.user.first_name} {request.user.middle_name} {request.user.last_name}] IP {client_ip}')
            messages.success(request, f'New user has been created they will be able to log in')
            return render(request, 'users/admin.html', context)

        if Departform.is_valid():
            Departform.save()
            departname = Departform.cleaned_data.get('department_name')
            logger.info(
                f'New Department [{departname}] has been added by [{request.user.first_name} {request.user.middle_name} {request.user.last_name}] IP {client_ip}')
            messages.success(request, f'New Department has been added')
            return render(request, 'users/admin.html', context)

        if SkForm.is_valid():
            SkForm.save()
            skilname = SkForm.cleaned_data.get('skill_type')
            logger.info(
                f'New Skill [{skilname}] has been added by [{request.user.first_name} {request.user.middle_name} {request.user.last_name}] IP {client_ip}')
            messages.success(request, f'New Skill has been added')
            context['SkillForm'] = SkillForm()
            context['SkillUForm'] = SkillUpdateForm()
            return render(request, 'users/admin.html', context)

        if SKUpdateForm.is_valid():
            skill = Skill.objects.get(id=request.POST.get('skillID'))
            skilled_staff_list = request.POST.getlist('skilled_staff')

            for user in skilled_staff_list:
                u = users.get(id=user)
                skill.skilled_staff.add(u)

            skill.save()
            context['SkillUForm'] = SkillUpdateForm()
            return render(request, 'users/admin.html', context)

        # If any admin form is not valid

        elif not Userform.is_valid():
            return render(request, 'users/admin.html', context)
        elif not Departform.is_valid():
            return render(request, 'users/admin.html', context)
        elif not SkForm.is_valid():
            return render(request, 'users/admin.html', context)

    else:

        Userform = UserAdminCreationForm()
        Departform = DepartmentForm()
        SkForm = SkillForm()
        SKUpdateForm = SkillUpdateForm()

        context = {
            'title': 'Super Admin Panel',
            'users': users,
            'tickets': tickets,
            'skills': skills,
            'departments': departments,
            'new_email': new_email,
            'update_email': update_email,
            'close_email': close_email,
            'Userform': Userform,
            'DepartForm': Departform,
            'SkillForm': SkForm,
            'SkillUForm': SkillUpdateForm,
            'emailSettings': email_settings,
        }

        return render(request, 'users/admin.html', context)

# ############################# #

# Ajax handling Email Forms

def update_emails(request):

    email_id = request.GET.get("id")
    email = Email.objects.get(id=email_id)
    email.subject = request.GET.get("subject")
    email.body = request.GET.get("body")
    email.save()

    return JsonResponse({"success": f'{email.email_name} has been updated'})

def email_settings(request):

    email_setting = EmailCreds.objects.first()
    email_setting.email = request.GET.get("email")
    email_setting.smtp_server = request.GET.get("smtp")
    email_setting.port = request.GET.get("port")
    email_setting.password = request.GET.get("password")
    email_setting.save()

    return JsonResponse({"success": "Settings have been updated."})