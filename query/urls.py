from django.urls import path

from . import views

urlpatterns = [
    path('createScript/', views.createScript, name='createScript'),
    path('getScript/<int:pk>/', views.getScript, name='getScript'),
    path('getScript/<str:script_name>/', views.getScriptByName, name='getScriptByName'),
    path('updateScript/<str:script_name>/', views.updateScript, name='updateScript'),
    path('deleteScript/<str:script_name>/', views.deleteScript, name='deleteScript'),
    path('authorizeScript/', views.authorizeScript, name='authorizeScript'),
    path('removeScriptPermission/', views.removeScriptPermission, name='removeScriptPermission'),
    path('sharedUser/', views.sharedUser, name='sharedUser'),
    path('sharedScripts/', views.sharedScripts, name='sharedScripts'),
    path('searchScript/', views.searchScript, name='searchScript')
]
