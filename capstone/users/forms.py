from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms as django_forms

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }

class SignUpForm(django_forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'username', 'password']
        labels = {
            'email': "",
            'name': '',
            'username': '',
            'password': '',
        }
        widgets = {
            'email': django_forms.TextInput(attrs={'placeholder':'이메일 주소'}),
            'name': django_forms.TextInput(attrs={'placeholder':'성명'}),
            'username': django_forms.TextInput(attrs={'placeholder':'사용자 이름'}),
            'password': django_forms.PasswordInput(attrs={'placeholder':'비밀번호'}),
        }           
        
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LogInForm(django_forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {'username': '', 'password': '',}
        widgets = {
            'username': django_forms.TextInput(attrs={'placeholder':'사용자 이름'}),
            'password': django_forms.PasswordInput(attrs={'placeholder':'비밀번호'}),
        }     

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserSearchForm(django_forms.Form):
    search_word = django_forms.CharField(label='Search Word')