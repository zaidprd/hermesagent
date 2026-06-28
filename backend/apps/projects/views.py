from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectForm, ProjectThreadsForm, ProjectWPForm
from .models import Project


@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.tenant = request.user.tenant
            project.save()
            messages.success(request, f"Project “{project.name}” dibuat.")
            return redirect(project)
    else:
        form = ProjectForm()
    return render(request, "projects/form.html", {"form": form})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, tenant=request.user.tenant)
    keywords = project.keywords.prefetch_related("titles__article")
    return render(
        request,
        "projects/detail.html",
        {"project": project, "keywords": keywords},
    )


@login_required
def project_settings(request, pk):
    project = get_object_or_404(Project, pk=pk, tenant=request.user.tenant)
    if request.method == "POST":
        form = ProjectWPForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Pengaturan WordPress disimpan.")
            return redirect(project)
    else:
        form = ProjectWPForm(instance=project)
    return render(request, "projects/settings.html", {"project": project, "form": form})


@login_required
def project_threads_settings(request, pk):
    project = get_object_or_404(Project, pk=pk, tenant=request.user.tenant)
    if request.method == "POST":
        form = ProjectThreadsForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Pengaturan Threads disimpan.")
            return redirect(project)
    else:
        form = ProjectThreadsForm(instance=project)
    return render(request, "projects/threads_settings.html", {"project": project, "form": form})
