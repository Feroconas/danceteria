from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('danceteria/', include('webdanceteria.urls')),
    path('admin/', admin.site.urls),
]

#quando o projeto for invocado num browser, reencaminha de danceteria/urls.py
# para webdanceteria/urls.py e inclui os urls que lá encontrar, segundo o padrao. A inclusão de URLs é feita através de include().

