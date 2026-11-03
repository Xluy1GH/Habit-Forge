from django.shortcuts import render
from django.views.generic import CreateView

from accounts.forms import CustomUserCreationForm

class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup_form.html"
    success_url = "/"