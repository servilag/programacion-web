from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='tasks_list'),
    path('create/', views.create_task, name='create_task'),
    path('update/<task_id>', views.update_task, name='update_task'),
    path('delete/<task_id>', views.delete_task, name='delete_task')
]
