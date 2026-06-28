from django.shortcuts import redirect


def landing(request):
    """Root URL: send authenticated users to the dashboard, others to login."""
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    return redirect("account_login")
