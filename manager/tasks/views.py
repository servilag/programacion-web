from django.shortcuts import render
from .models import Task

def task_list(request):
    tasks = Task.objects.all().order_by("updated_at")
    return render(request, 'tasks/index.html', {'tasks':tasks})

