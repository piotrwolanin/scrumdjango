from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from accounts.forms import UserLogInForm, PwdChangeForm


class UserLogIn(LoginView):
    template_name = 'login.html'
    authentication_form = UserLogInForm


class UserLogOut(LogoutView):
    template_name = 'logged-out.html'


class UserPasswordChange(PasswordChangeView):
    template_name = 'password-change.html'
    form_class = PwdChangeForm
    success_url = reverse_lazy('scrumboard:current_sprint')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change password'
        context['btn_title'] = 'Change'
        context['btn_class'] = 'success'
        return context