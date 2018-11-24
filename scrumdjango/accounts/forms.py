from django.forms import CharField, TextInput, PasswordInput
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.password_validation import password_validators_help_text_html


class UserLogInForm(AuthenticationForm):
    username = CharField(
        widget=TextInput(attrs={'class': 'form-control', 'required': True})
    )
    password = CharField(
        widget=PasswordInput(attrs={'class': 'form-control', 'required': True})
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''


class PwdChangeForm(PasswordChangeForm):
    old_password = CharField(
        widget=PasswordInput(attrs={'class': 'form-control', 'required': True})
    )
    new_password1 = CharField(
        label='New password',
        widget=PasswordInput(attrs={'class': 'form-control', 'required': True}),
        help_text=password_validators_help_text_html(),
    )
    new_password2 = CharField(
        label='Confirm new password',
        widget=PasswordInput(attrs={'class': 'form-control', 'required': True}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
