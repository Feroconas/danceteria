from django.db.models.signals import post_save
from django.dispatch import receiver
from webdanceteria.models import Instrutor
from django.contrib.auth.models import Group, Permission


#acionado sempre que um objeto Instrutor for criado - é adicionado ao grupo Instrutores
@receiver(post_save, sender=Instrutor)
def adicionarInstrutorGrupo(sender, instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name='Instrutores')
        permission1, created = Permission.objects.get_or_create(codename='add_auladanca')
        permission2, created = Permission.objects.get_or_create(codename='delete_auladanca')
        if permission1 not in group.permissions.all():
            group.permissions.add(permission1)
        if permission2 not in group.permissions.all():
            group.permissions.add(permission2)
        instance.user.groups.add(group)
