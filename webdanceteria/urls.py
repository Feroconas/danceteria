from django.urls import include, path
from . import views

# (. significa que importa views da mesma directoria)

app_name = 'webdanceteria'

urlpatterns = [
    # Isto é, quando for invocado o url "" o Django procura e executa a função index em views.py
    path("", views.home, name="home"),
    # login
    path('login/', views.login_view, name='login_view'),
    path('registermember/', views.register_member_view, name='register_member_view'),
    path('registerinstrutor/', views.register_instrutor_view, name='register_instrutor_view'),
    path("logout/", views.logout_view, name='logout_view'),
    path("perfil/", views.profile_view, name='profile_view'),
    path("perfil/editar/", views.editUser_view, name='editUser_view'),
    path("eventos/", views.events_view, name='events_view'),
    path('bilheteEvento/<int:evento_id>/', views.comprarBilheteEv_view, name='comprarBilheteEv_view'),
    path('bilheteEvento/eliminar/<int:bilhete_id>/', views.apagarBilheteEv_view, name='apagarBilheteEv_view'),
    path('bilheteAula/<int:aula_id>/', views.comprarBilheteAula_view, name='comprarBilheteAula_view'),
    path('bilheteAula/eliminar/<int:bilheteAula_id>/', views.apagarBilheteAula_view, name='apagarBilheteAula_view'),
    path('criar-aula/', views.criar_aula_view, name='criar_aula_view')
    ]
