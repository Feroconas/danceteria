import os.path

from django import template
from django.conf import settings
from webdanceteria.models import Membro, Instrutor, Diretor, Utilizador

register = template.Library()


@register.filter
def isMembro(user):
    return user.groups.filter(name='Membros').exists()


@register.filter
def isInstrutor(user):
    return user.groups.filter(name='Instrutores').exists()

@register.filter
def isSuperUser(user):
    return user.is_superuser

@register.filter
def getUtilizador(user):
    if isMembro(user):
        return Membro.objects.get(user_id=user)
    if isInstrutor(user):
        return Instrutor.objects.get(user_id=user)
    if user.is_superuser:
        return Diretor.objects.get(user_id=user)
    return None


@register.filter
def getNome(user):
    return getUtilizador(user).nome


@register.filter
def getEmail(user):
    return getUtilizador(user).email


@register.filter
def getGenero(user):
    return getUtilizador(user).genero


@register.filter
def getImagemPerfil(user):
    if getUtilizador(user).imagem_perfil:
        return f"{settings.MEDIA_URL}{getUtilizador(user).imagem_perfil}"
    else:
        return None


@register.filter
def getDescricao(user):
    return getUtilizador(user).descricao


@register.filter
def getDataNascimento(user):

    return getUtilizador(user).data_nascimento

@register.filter
def getDataNascimentoFormatted(user):
    date = getUtilizador(user).data_nascimento
    return date.strftime('%Y-%m-%d')
