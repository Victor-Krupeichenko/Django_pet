from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout


class CategoryMixin(LoginRequiredMixin):
    """Category create, update mixin"""
    dispath_redirect_url = None
    name_view = None
    redirect_success = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, message=f"{request.user.username} Not enough rights")
            logout(request)
            return redirect(self.dispath_redirect_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            category = form.save()
            tit = category.title
            messages.success(
                self.request,
                f"{tit} Success created" if self.name_view == "CreateCategory" else f"{category.title} Success Updated"
            )
            return redirect(self.redirect_success)
        except Exception as ex:
            messages.error(
                self.request,
                f"{ex} Error created category" if self.name_view == "CreateCategory" else f"{ex} Error updated category"
            )
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
