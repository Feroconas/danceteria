from django.db import models
from django.contrib.auth.models import User

class NivelMembro(models.Model):
    NIVEL_INICIANTE = 1
    NIVEL_INTERMEDIO = 2
    NIVEL_AVANCADO = 3
    NIVEL_PROFISSIONAL = 4

    NIVEL_CHOICES = (
        (NIVEL_INICIANTE, 'Iniciante'),
        (NIVEL_INTERMEDIO, 'Intermédio'),
        (NIVEL_AVANCADO, 'Avançado'),
        (NIVEL_PROFISSIONAL, 'Profissional'),
    )

    pontos_necessarios = models.IntegerField()
    recompensa = models.CharField(max_length=50, blank=True)
    id_nivel = models.IntegerField(primary_key=True, choices=NIVEL_CHOICES)

    def __str__(self):
        return self.get_id_nivel_display()

class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Membro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    nome = models.CharField(max_length=50)
    email = models.EmailField()
    genero_choices = [
        ('F', 'Feminino'),
        ('M', 'Masculino'),
        ('O', 'Outro')
    ]
    genero = models.CharField(max_length=1, choices=genero_choices)
    imagem_perfil = models.CharField(max_length=100, null=True, blank=True)
    descricao = models.CharField(max_length=500, null=True, blank=True)
    data_nascimento = models.DateField()
    preferencias_musicais = models.CharField(max_length=100, null=True)
    nivel_membro = models.ForeignKey(NivelMembro, on_delete=models.PROTECT)
    pontos = models.IntegerField(default=0)
    #amigos = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.nome

class Instrutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    nome = models.CharField(max_length=50)
    email = models.EmailField()
    genero_choices = [
        ('F', 'Feminino'),
        ('M', 'Masculino'),
        ('O', 'Outro')
    ]
    genero = models.CharField(max_length=1, choices=genero_choices)
    imagem_perfil = models.CharField(max_length=100, null=True, blank=True)
    descricao = models.CharField(max_length=500, null=True, blank=True)
    data_nascimento = models.DateField()
    especializacao = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True)


class Evento(models.Model):
    nome = models.CharField(max_length=100)
    data_hora = models.DateTimeField()
    descricao = models.CharField(max_length=500, null=True, blank=True)
    imagem = models.CharField(max_length=100, null=True, blank=True)
    preco_bilhete = models.DecimalField(max_digits=6, decimal_places=2)
    artistas = models.CharField(max_length=500, null=True, blank=True)
    bilhetes_disponiveis = models.IntegerField()

    def __str__(self):
        return self.nome


class AulaDanca(models.Model):
    nome = models.CharField(max_length=100, default=None)
    data_hora = models.DateTimeField(null=True)
    preco_bilhete = models.DecimalField(max_digits=6, decimal_places=2, default=None)
    bilhetes_disponiveis = models.IntegerField(default=10)
    participantes = models.IntegerField(default=0)
    instrutor_id = models.ForeignKey(Instrutor, on_delete=models.PROTECT)
    NIVEL_CHOICES = (
        (1, 'Iniciante'),
        (2, 'Intermediário'),
        (3, 'Avançado'),
        (4, 'Profissional'),
    )
    nivel_aconselhado = models.IntegerField(choices=NIVEL_CHOICES)

    def __str__(self):
        return self.nome


class BilheteEvento(models.Model):
    comprador = models.ForeignKey(Membro, on_delete=models.PROTECT)
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT)
    data_compra = models.DateTimeField()
    data_validade = models.DateTimeField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'Bilhete {self.numero_bilhete} para {self.evento.nome}'

class BilheteAula(models.Model):
    comprador = models.ForeignKey(Membro, on_delete=models.PROTECT)
    aula = models.ForeignKey(AulaDanca, on_delete=models.PROTECT)
    data_compra = models.DateTimeField()
    data_validade = models.DateTimeField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'Bilhete {self.numero_bilhete} para {self.evento.nome}'



#class HistoricoUtilizador(models.Model):
    #utilizador = models.ForeignKey(Utilizador, on_delete=models.PROTECT)
    #aula_evento = models.ForeignKey(Evento, on_delete=models.PROTECT)
    #data = models.DateTimeField()


#class Avaliacao(models.Model):
 #   utilizador = models.ForeignKey(Utilizador, on_delete=models.PROTECT)
  #  aula_evento = models.ForeignKey(Evento, on_delete=models.PROTECT)
