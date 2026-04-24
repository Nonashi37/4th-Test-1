from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView

from users.forms import EditProfileForm, LoginForm, RegisterForm


# ✅ FBV → View (GET + POST in one class)
class RegisterView(View):
    template_name = "users/register.html"

    def get(self, request):
        return render(request, self.template_name, {"form": RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            login(request, user)
            return redirect("home")
        return render(request, self.template_name, {"form": form})


# ✅ FBV → View (custom auth logic, FormView won't fit cleanly here)
class LoginView(View):
    template_name = "users/login.html"

    def get(self, request):
        return render(request, self.template_name, {"form": LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                return redirect("home")
            form.add_error(None, "Wrong username or password!")
        return render(request, self.template_name, {"form": form})


# ✅ stays a simple View, logout needs no form or template
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")


# ✅ FBV → UpdateView (LoginRequiredMixin replaces @login_required)
class EditProfileView(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy("profile_edit")
    login_url = "/users/login/"

    def get_object(self):
        return self.request.user  # no pk lookup needed, same as before
# superuser:
# Admin, Admin@Geeksemail.com, lengadoc