from django.urls import path

from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('report/send/', views.upload_file, name='send'),
    path('report/edit/<int:pk>', views.edit_file, name='edit'),
    path('report/delete/<int:pk>', views.delete_file, name='delete'),
    path('data/uploads_reports/<int:pk>', views.get_file, name='get_file'),
    path('data/reports/<int:pk>', views.get_report, name='get_report'),
]
