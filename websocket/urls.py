from django.urls import path, include
from . import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path('conncet/', views.connect, name='connect'),
    path('disconnect/', views.disconnect, name='disconnect'),
]