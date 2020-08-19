from django.db import models
from django.utils import timezone
from datetime import date
from users.models import User
from django.urls import reverse


class Skill(models.Model):

    skill_type = models.CharField(max_length=255)
    skilled_staff = models.ManyToManyField(User)

    def __str__(self):
        return self.skill_type


class StaffProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        self.user.username


class Department(models.Model):

    department_name = models.CharField(max_length=50)

    def __str__(self):
        return self.department_name


class Priority(models.Model):

    priority = models.CharField(max_length=50)

    def __str__(self):
        return self.priority


class Status(models.Model):

    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status


class Ticket(models.Model):

    subject = models.CharField(max_length=255)
    username = models.CharField("Your Name", max_length=255)
    email = models.EmailField(max_length=255)
    user_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    request_type = models.ForeignKey(Skill, on_delete=models.CASCADE)
    location_info = models.TextField(blank=True, null=True)
    ticket_priority = models.ForeignKey(Priority, on_delete=models.CASCADE, default=1)
    ticket_status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_due = models.DateTimeField(blank=True, null=True)
    ticket_description = models.TextField()
    staff_assigned = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.subject} ({self.user_department}) ({self.username})'

    def get_absolute_url(self):
        return reverse('ticket-detail', kwargs={'pk':self.pk})

    @property
    def is_due_date(self):
        return date.today() == self.date_due


class Note(models.Model):

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    staff_user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_note = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ticket} {self.staff_user} \n {self.date_created}'


class ToDo(models.Model):

    staff_user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_name = models.CharField(max_length=255)
    todo = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.todo}'


class Notification(models.Model):

    notification = models.CharField(max_length=255)

    def __str__(self):
        return self.notification


class KnowledgeBase(models.Model):

    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question


class EmailCreds(models.Model):

    email = models.EmailField(max_length=255)
    smtp_server = models.CharField(max_length=255)
    port = models.CharField(max_length=50)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email


class Email(models.Model):

    email_name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.email_name




    