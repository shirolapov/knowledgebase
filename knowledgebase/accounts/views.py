from accounts.forms import UserForm
from django.urls import reverse
from django.template import loader
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User



# Create your views here.
@login_required
def logout_page(request):
    logout(request)
    return redirect("/articles/")


def login_page(request):
    error_login = False
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET.get("next", "/"))
        else:
            error_login = True

    context = {
        "error_login": error_login
    }
    template = loader.get_template('accounts/loginpage.html')
    return HttpResponse(template.render(context, request))


@login_required
def operators_list(request):
    is_login = True
    user = request.user
    users = User.objects.filter(is_superuser=False)
    if user.is_staff:
        context = {
            "is_login": is_login,
            "user": user,
            "users": users
        }
        template = loader.get_template('accounts/operatorslist.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseForbidden("Доступ только для сотрудников")


@login_required
def add_operator(request):
    is_login = True
    user = request.user
    form = UserForm()
    if user.is_staff:
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                new_user = User.objects.create_user(
                    username = form.cleaned_data['username'],
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name'],
                    email = form.cleaned_data['email'],
                    password = form.cleaned_data['password'],
                )
                return redirect("/accounts/operatorslist/")

        context = {
            "header": {
                "title": "Добавить оператора"
            },
            "is_login": is_login,
            "user": user,
            "form": form
        }
        template = loader.get_template('accounts/addaccount.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseForbidden("Доступ только для сотрудников")
