from django.urls import path
from django.views.generic.base import TemplateView
from . import views
app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('report/send/', views.upload_file, name='send'),
    path('report/edit/<int:pk>', views.edit_file, name='edit'),
    path('report/delete/<int:pk>', views.delete_file, name='delete'),
]
