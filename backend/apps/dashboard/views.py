from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.projects.models import Project


@login_required
def home(request):
    projects = Project.objects.filter(tenant=request.user.tenant)
    return render(request, "dashboard/home.html", {"projects": projects})
