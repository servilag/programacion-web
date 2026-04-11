from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

#C.R.U.D#
#listar tareas
def task_list(request):
    tasks = Task.objects.all().order_by("updated_at")
    return render(request, 'tasks/index.html', {'tasks':tasks})

#crear tareas
def create_task(request):
    
    form = TaskForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        return redirect('tasks_list')
        
    return render(request, 'tasks/create.html',{'form':form,'creando':True})

#update
def update_task(request,task_id):
    
    task = Task.objects.get(id=task_id)
    
    form = TaskForm(request.POST or None,instance=task)
    
    if form.is_valid():
        form.save()
        return redirect('tasks_list')
        
    return render(request, 'tasks/create.html',{'form':form,'creando':False})

#eliminar
def delete_task(request,task_id):
    task= Task.objects.get(id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks_list')
    
    return render(request, 'tasks/delete.html',{'task':task})