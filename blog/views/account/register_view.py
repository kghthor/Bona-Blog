# Django imports.
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views.generic import View

# Blog app imports.
from blog.forms.account.register_forms import UserRegisterForm


class UserRegisterView(View):
    """
    View to let users register without email verification.
    """
    template_name = 'account/register.html'

    def get(self, request):
        return render(request, self.template_name, {'register_form': UserRegisterForm()})

    def post(self, request, *args, **kwargs):
        register_form = UserRegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = True  # Directly activate the user
            user.save()

            login(request, user)  # Auto-login the user

            messages.success(request, f"Welcome {user.username}! Your account was created successfully.")

            return redirect('blog:home')  # Change to your homepage or dashboard

        else:
            messages.error(request, "Please provide valid information.")
            return render(request, self.template_name, {'register_form': register_form})
