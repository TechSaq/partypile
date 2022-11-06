from django.shortcuts import redirect, render
from django.contrib.auth import login

from .forms import CreateAuthUserForm


def register_view(request):
    if request.method == "POST":
        form = CreateAuthUserForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            login(request, user.user)
            # messages.success(request, "AuthUser registered successfully.")
            return redirect("events:events")
        else:
            pass
            # messages.error(request, "Invalid form, please check your data.")
    else:
        form = CreateAuthUserForm()

    context = {"form": form}
    return render(request, "authuser/register.html", context)
