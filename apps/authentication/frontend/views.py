from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

def login_view(request):
    if request.user.is_authenticated:
     return redirect("authentication:dashboard")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("authentication:dashboard")

    return render(
        request,
        "authentication/login.html",
        {"form": form},
    )

@login_required
def dashboard_view(request):
    return render(
    request,
    "authentication/dashboard.html",
    )
