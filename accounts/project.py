#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from accounts.models import Project
from accounts.forms import ProjectForm
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import permission_required,login_required


@login_required
@permission_required('accounts.get_project',raise_exception=True)
def project_list(request):

    error = ''
    data = {}
    current_page = request.GET.get("page", 1)
    page_number = 15
    Projects = Project.objects.order_by('id')
    pages = Paginator(Projects, page_number)
    try:
        Projects = pages.page(current_page)
    except EmptyPage:
        Projects = pages.page(current_page)
    data["content"] = Projects
    data["form"] = []
    for  i in Projects:
        data["form"].append({"id":i.id,"name":i.name,"description":i.description})
    data["pages"] = pages
    data["request"] = request

    return render_to_response('fms/project.html', data)

@login_required
@permission_required('accounts.add_project',raise_exception=True)
def project_add(request):

    if request.method == "POST":
        form = ProjectForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
    else:
        form = ProjectForm()
    return HttpResponseRedirect(reverse('project_list'))

@login_required
@permission_required('accounts.del_project',raise_exception=True)
def project_del(request, id):

    if id:
        Project.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('project_list'))


@login_required
@permission_required('accounts.edit_project',raise_exception=True)
def project_edit(request):

    id = request.POST.get('id')
    project = Project.objects.get(id=id)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
    else:
        form = ProjectForm(instance=project)

    return HttpResponseRedirect(reverse('project_list'))

