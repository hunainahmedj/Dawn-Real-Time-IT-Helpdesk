from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from scheduler.models import Department, Skill


User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    is_staff = forms.BooleanField(label="Staff Status")
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    # first_name = forms.CharField(label='First Name')
    # middle_name = forms.CharField(label='Middle Name')
    # last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name', 'email', 'is_staff', 'is_superuser')  # 'full_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class DepartmentForm(forms.ModelForm):

    department_name = forms.CharField(label='Department Name')

    class Meta:
        model = Department
        fields = ('department_name',)


class SkillForm(forms.ModelForm):

    skill_type = forms.CharField(label='Skill Name', max_length=30)
    # skilled_staff = forms.ChoiceField()

    class Meta:
        model = Skill
        fields = ('skill_type', 'skilled_staff',)


class SkillUpdateForm(forms.ModelForm):

    class Meta:
        model = Skill
        fields = ('skilled_staff',)
