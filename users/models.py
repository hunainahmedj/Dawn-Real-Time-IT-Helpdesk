from django.db import models
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager


class LoggedUser(models.Model):

    name = models.CharField(max_length=30)
    email = models.EmailField(primary_key=True)
    last_login = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.email

    def login_user(sender, request, user, **kwargs):
        logged_in_users = LoggedUser.objects.filter(email=user.email)
        if not logged_in_users:
            LoggedUser(name=str(user.first_name + " " + " " + user.last_name), email=user.email).save()

    def logout_user(sender, request, user, **kwargs):
        try:
            u = LoggedUser.objects.get(pk=user.email)
            u.delete()
        except LoggedUser.DoesNotExist:
            pass

    user_logged_in.connect(login_user)
    user_logged_out.connect(logout_user)

class UserManager(BaseUserManager):

    def create_user(self, email, first_name, middle_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("Please provide a password for authentication")
        if not first_name:
            raise ValueError("First name is required")
        if not last_name:
            raise ValueError("Last name is required")
        email = self.normalize_email(email)
        user_obj = self.model(
            email=email, **extra_fields
        )

        user_obj.set_password(password)
        user_obj.first_name = first_name
        user_obj.middle_name = middle_name
        user_obj.last_name = last_name
        # user_obj.is_staff = is_staff
        # user_obj.is_admin = is_admin
        # user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    # def create_staffuser(self, email, first_name, middle_name, last_name, password=None):
    #     user = self.create_user(
    #         email,
    #         first_name,
    #         middle_name,
    #         last_name,
    #         password = password,
    #         is_staff = True
    #     )
    #     return user

    def create_superuser(self, email, first_name, middle_name, last_name, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)


        user = self.create_user(
            email,
            first_name,
            middle_name,
            last_name,
            password = password,
            **extra_fields
        )
        print(user.is_superuser)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)  # is the account active or not
    is_staff = models.BooleanField(default=True)   # is a staff or an admin
    # is_admin = models.BooleanField(default=False)  # is a superuser/admin

    USERNAME_FIELD = 'email'  # username and password are required by default

    REQUIRED_FIELDS = ['first_name', 'middle_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return "{} {} {}".format(self.first_name, self.middle_name, self.last_name)

    def get_email(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     return True

    # @property
    # def is_staff(self):
    #     return self.staff
    #
    # @property
    # def is_admin(self):
    #     return self.admin
    #
    # @property
    # def is_active(self):
    #     return self.active