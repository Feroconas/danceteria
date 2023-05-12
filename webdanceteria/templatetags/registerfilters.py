from django import template
from django.conf import settings
from webdanceteria.models import Membro, Instrutor, Diretor

register = template.Library()


@register.filter
def isMembro(user):
    return Membro.objects.filter(user=user).exists()


@register.filter
def isInstrutor(user):
    return Instrutor.objects.filter(user=user).exists()


@register.filter
def isDiretor(user):
    return Diretor.objects.filter(user=user).exists()


@register.filter
def getUtilizador(user):
    if isMembro(user):
        return Membro.objects.get(user_id=user)
    if isInstrutor(user):
        return Instrutor.objects.get(user_id=user)
    if isDiretor(user):
        return Diretor.objects.get(user_id=user)
    return None


@register.filter
def getDataNascimento(user):
    return user.utilizador.data_nascimento


@register.filter
def getNome(user):
    return user.nome


@register.filter
def getEmail(user):
    return user.email


@register.filter
def getGenero(user):
    return user.genero


@register.filter
def getImagemPerfil(user):
    return f"{settings.MEDIA_URL}{user.imagem_perfil}"


@register.filter
def getDescricao(user):
    return user.descricao


@register.filter
def getDataNascimento(user):
    return user.data_nascimento
