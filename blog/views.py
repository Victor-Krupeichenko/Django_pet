from django.contrib.auth.models import User
from django.shortcuts import redirect
from .forms import CreateUserForm, LoginUserForm, CategoryForm, PostCreateForm
from django.views.generic import CreateView, ListView, DetailView
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Post
from .utils import CategoryMixin
from django.db.models import Count


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

    def form_valid(self, form):
        try:
            user = form.save()
            messages.success(self.request, message=f"{self.object.username} Success update")
            login(self.request, user)
        except Exception as ex:
            messages.error(self.request, message=f"{ex} Error user updte")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update_user"] = True
        return context


class DeleteUser(LoginRequiredMixin, DeleteView):
    """Delete user"""
    model = User
    template_name = "blog/delete.html"
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


class CreateCategory(CategoryMixin, CreateView):
    """Create category"""
    form_class = CategoryForm
    template_name = "blog/create_category.html"
    name_view = "CreateCategory"
    dispath_redirect_url = "login_user"
    redirect_success = "list_category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_category"] = True
        return context


class ListCategory(LoginRequiredMixin, ListView):
    """View all Category"""
    model = Category
    template_name = "blog/list_category.html"

    def get_queryset(self):
        return Category.objects.annotate(cnt=Count("post"))

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, message=f"{request.user.username} Not enough rights")
            logout(request)
            return redirect("login_user")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_category"] = True
        return context


class UpdateCategory(CategoryMixin, UpdateView):
    """Update Category"""
    model = Category
    form_class = CategoryForm
    template_name = "blog/create_category.html"
    name_view = "UpdateCategory"
    dispath_redirect_url = "login_user"
    redirect_success = "list_category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update_category"] = True
        return context


class DeleteCategory(LoginRequiredMixin, DeleteView):
    """Delete category"""
    model = Category
    success_url = reverse_lazy("list_category")
    template_name = "blog/delete.html"

    def delete(self, request, *args, **kwargs):
        try:
            category = self.get_object()
            messages.success(request, message=f"{category.title} Successfully deleted")
        except Exception as ex:
            messages.error(request, message=f"{ex} Error deleting user")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delete_category"] = True
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    """Create Post"""
    form_class = PostCreateForm
    template_name = "blog/create_post.html"

    def form_valid(self, form):
        try:
            post = form.save(commit=False)
            post.author_id = self.request.user.pk
            post.save()
            messages.success(self.request, message=f"{post.title} Successfully created")
            return redirect(post)
        except Exception as ex:
            messages.error(self.request, message=f"{ex} Error created post")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_post"] = True
        return context


class ListPostView(ListView):
    """View All Posts"""
    model = Post
    template_name = "blog/index.html"

    def get_queryset(self):
        return Post.objects.filter(is_publish=True).select_related("category")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "All Post"
        return context


class DetailPostView(DetailView):
    """Detail Post"""
    model = Post
    template_name = "blog/detail_post.html"


class UpdatePost(LoginRequiredMixin, UpdateView):
    """Update Post"""
    model = Post
    form_class = PostCreateForm
    template_name = "blog/create_post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update_post"] = True
        return context

    def form_valid(self, form):
        try:
            post = form.save()
            messages.success(self.request, message=f"{post.title} Successfully updated")
            return redirect(post)
        except Exception as ex:
            messages.error(self.request, message=f"{ex} Error updated")
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, DeleteView):
    """Delete Post"""
    model = Post
    template_name = "blog/delete.html"
    success_url = reverse_lazy("home")

    def delete(self, request, *args, **kwargs):
        try:
            post = self.get_object()
            messages.success(request, message=f"{post.title} Successfully deleted")
        except Exception as ex:
            messages.error(request, message=f"{ex} Error deleted")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delete_post"] = True
        return context
