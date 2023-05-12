from django.db.models.signals import post_save
from django.dispatch import receiver
from webdanceteria.models import Instrutor, Membro, Diretor
from django.contrib.auth.models import Group, Permission


# acionado sempre que um objeto Instrutor for criado - é adicionado ao grupo Instrutores
@receiver(post_save, sender=Instrutor)
def adicionarInstrutorGrupo(sender, instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name='Instrutores')
        permission1, created = Permission.objects.get_or_create(codename='add_auladanca')
        permission2, created = Permission.objects.get_or_create(codename='delete_auladanca')
        permission3, created = Permission.objects.get_or_create(codename='add_evento')
        permission4, created = Permission.objects.get_or_create(codename='delete_evento')
        for permission in (permission1, permission2, permission3, permission4):
            if permission not in group.permissions.all():
                group.permissions.add(permission)
        instance.user.groups.add(group)


@receiver(post_save, sender=Membro)
def adicionarMembroGrupo(sender, instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name='Membros')
        instance.user.groups.add(group)




