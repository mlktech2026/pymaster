from django.shortcuts import render, get_object_or_404
from .models import Project

def project_list_view(request):
    projects = Project.objects.all()
    level = request.GET.get('level')
    if level in ['beginner', 'intermediate', 'advanced']:
        projects = projects.filter(level=level)

    beginner_projects = Project.objects.filter(level='beginner')
    intermediate_projects = Project.objects.filter(level='intermediate')
    advanced_projects = Project.objects.filter(level='advanced')

    context = {
        'projects': projects,
        'selected_level': level,
        'beginner_projects': beginner_projects,
        'intermediate_projects': intermediate_projects,
        'advanced_projects': advanced_projects,
    }
    return render(request, 'projects/project_list.html', context)

def project_detail_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.filter(level=project.level).exclude(id=project.id)[:3]
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'related_projects': related_projects,
    })
