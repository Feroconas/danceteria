from django.db import models
from django.contrib.auth.models import User

NIVEL_NOVATO = 1
NIVEL_INICIANTE = 2
NIVEL_INTERMEDIO = 3
NIVEL_AVANCADO = 4
NIVEL_PROFISSIONAL = 5

NIVEL_CHOICES = (
    (NIVEL_NOVATO, 'Novato'),
    (NIVEL_INICIANTE, 'Iniciante'),
    (NIVEL_INTERMEDIO, 'Intermédio'),
    (NIVEL_AVANCADO, 'Avançado'),
    (NIVEL_PROFISSIONAL, 'Profissional'),
)

genero_choices = [
    ('F', 'Feminino'),
    ('M', 'Masculino'),
    ('O', 'Outro')
]

class NivelMembro(models.Model):
    pontos_necessarios = models.IntegerField()
    recompensa = models.CharField(max_length=50, blank=True)
    id_nivel = models.IntegerField(primary_key=True, choices=NIVEL_CHOICES)

    def __str__(self):
        return self.get_id_nivel_display()


# samba, hip-hop, tango, etc
class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    nome = models.CharField(max_length=50)
    email = models.EmailField()
    genero = models.CharField(max_length=1, choices=genero_choices)
    imagem_perfil = models.FileField(upload_to='utilizadorImg', null=True)
    descricao = models.CharField(max_length=500, null=True, blank=True, default="")
    data_nascimento = models.DateField()
    n_aulas = models.IntegerField(default=0)
    n_eventos = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome


class Membro(Utilizador):
    preferencias_musicais = models.CharField(max_length=100, null=True)
    nivel_membro = models.ForeignKey(NivelMembro, on_delete=models.PROTECT)
    pontos = models.IntegerField(default=0)


class Instrutor(Utilizador):
    especializacao = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True)


class Diretor(Utilizador):
    pass


class Evento(models.Model):
    nome = models.CharField(max_length=100)
    data_hora = models.DateTimeField()
    preco_bilhete = models.DecimalField(max_digits=6, decimal_places=2, default=None)
    bilhetes_disponiveis = models.IntegerField()
    descricao = models.CharField(max_length=500, null=True, blank=True)
    artistas = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.nome


class AulaDanca(models.Model):
    nome = models.CharField(max_length=100, default="")
    data_hora = models.DateTimeField(null=True)
    preco_bilhete = models.DecimalField(max_digits=6, decimal_places=2, default=None)
    bilhetes_disponiveis = models.IntegerField(default=10)
    participantes = models.IntegerField(default=0)
    instrutor_id = models.ForeignKey(Instrutor, on_delete=models.PROTECT)
    nivel_aconselhado = models.ForeignKey(NivelMembro, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome


class Bilhete(models.Model):
    comprador = models.ForeignKey(User, on_delete=models.CASCADE)
    data_compra = models.DateTimeField()
    data_validade = models.DateTimeField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    especial = models.BooleanField(default=False)

    class Meta:
        abstract = True


class BilheteEvento(Bilhete):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    def __str__(self):
        return f'Bilhete {self.id} para {self.evento.nome}'


class BilheteAula(Bilhete):
    aula = models.ForeignKey(AulaDanca, on_delete=models.CASCADE)

    def __str__(self):
        return f'Bilhete {self.id} para {self.aula.nome}'


class Avaliacao(models.Model):
    avaliador = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, default="")
    descricao = models.CharField(max_length=1000, null=True, blank=True, default="")
    rating = models.IntegerField()  # 1 a 5 estrelas
    data_avaliacao = models.DateTimeField()
