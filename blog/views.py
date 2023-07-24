from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginUserForm
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    return render(request, "blog/index.html")


class RegisterUser(CreateView):
    """Register user"""
    form_class = CreateUserForm
    template_name = "blog/create_user.html"

    def form_valid(self, form):
        try:
            user = form.save()
            messages.success(self.request, message=f"{user.username} Successfully created")
            login(self.request, user)
            return redirect("home")
        except Exception as ex:
            messages.error(self.request, message=f"{ex} Error creating user")
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["register_user"] = True
        return context


class LoginUser(LoginView):
    """Login user"""
    form_class = LoginUserForm
    template_name = "blog/create_user.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, message=f"{form.cleaned_data['username']} Successfully logged in")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, message=f"{form.cleaned_data['username']}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_user"] = True
        return context

    def get_success_url(self):
        return self.success_url


def user_logout(request):
    """Logout User"""
    logout(request)
    return redirect("login_user")


class UpdateUser(LoginRequiredMixin, UpdateView):
    """Update User"""
    model = User
    form_class = CreateUserForm
    template_name = "blog/create_user.html"
    success_url = reverse_lazy("home")

    def form_invalid(self, form):
        try:
            user = form.save()
            messages.success(self.request, message=f"{self.object.username} Success update")
            login(self.request, user)
        except Exception as ex:
            messages.error(self.request, message=f"{ex} Error user updte")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update_user"] = True
        return context


class DeleteUser(LoginRequiredMixin, DeleteView):
    """Delete user"""
    model = User
    template_name = "blog/delete_user.html"
    success_url = reverse_lazy("register_user")

    def delete(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            messages.success(self.request, message=f"{user.username} Successfully deleted")
        except Exception as ex:
            messages.error(self.request, message=f"{ex} Error deleting user")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delete_user"] = True
        return context
