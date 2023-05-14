from django import forms
from .models import genero_choices, Membro, Instrutor, Categoria
from django.forms import SplitDateTimeWidget

from .models import *
from datetime import date, timedelta


class RegisterMemberForm(forms.ModelForm):
    username = forms.CharField(label='Nome de utilizador (único):',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password:',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}))
    genero = forms.ChoiceField(label='Género:', choices=genero_choices, widget=forms.RadioSelect)
    data_nascimento = forms.DateField(label='Data de nascimento', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Membro
        fields = ['username', 'password', 'nome', 'email', 'genero', 'descricao', 'data_nascimento', 'preferencias_musicais', 'imagem_perfil', ]
        labels = {
            'nome': 'Nome de perfil',
            'email': 'E-mail',
            'descricao': 'Sobre mim',
            'preferencias_musicais': 'Preferências Musicais',
            'imagem_perfil': 'Imagem de perfil'
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição'}),
            'preferencias_musicais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferências Musicais'}),
            'imagem_perfil': forms.ClearableFileInput(attrs={'class': 'form-control', 'enctype': 'multipart/form-data'}),
        }
        label_suffix = ':'
        attrs = {'class': 'login-form'}

    def clean_data_nascimento(self):
        data = self.cleaned_data['data_nascimento']
        idade = (date.today() - data) // timedelta(days=365.2425)
        if idade < 3 or idade > 100:
            raise forms.ValidationError("Deverá ter entre 3 a 100 anos de idade para se poder registar.")
        return data


class RegisterInstrutorForm(forms.ModelForm):
    username = forms.CharField(label='Nome de utilizador (único):',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password:',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}))
    genero = forms.ChoiceField(label='Género:', choices=genero_choices, widget=forms.RadioSelect)
    data_nascimento = forms.DateField(label='Data de nascimento', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    especializacao = forms.ModelChoiceField(queryset=Categoria.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Instrutor
        fields = ['username', 'password', 'nome', 'email', 'genero', 'descricao', 'data_nascimento', 'imagem_perfil', 'especializacao', ]
        labels = {
            'nome': 'Nome de perfil',
            'email': 'E-mail',
            'descricao': 'Sobre mim',
            'imagem_perfil': 'Imagem de perfil',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição'}),
            'imagem_perfil': forms.ClearableFileInput(attrs={'class': 'form-control', 'enctype': 'multipart/form-data'}),
        }
        label_suffix = ':'
        attrs = {'class': 'login-form'}

    def clean_data_nascimento(self):
        data = self.cleaned_data['data_nascimento']
        idade = (date.today() - data) // timedelta(days=365.2425)
        if idade < 3 or idade > 100:
            raise forms.ValidationError("Deverá ter entre 3 a 100 anos de idade para se poder registar.")
        return data


class CriarAulaForm(forms.ModelForm):
    data_hora = forms.DateTimeField(label='Data e Hora do evento', widget=SplitDateTimeWidget(attrs={'class': 'form-control'}))
    preco_bilhete = forms.DecimalField(label='Preço do bilhete (€):', max_digits=6, decimal_places=2, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Preço do bilhete (€)'}))
    instrutor_id = forms.ModelChoiceField(label='Instrutor:', queryset=Instrutor.objects.all(),
                                          widget=forms.Select(attrs={'class': 'form-control'}))

    nivel_aconselhado = forms.ModelChoiceField(label='Nível aconselhado:', queryset=NivelMembro.objects.all(),
                                               widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = AulaDanca
        fields = ['nome', 'data_hora', 'preco_bilhete', 'bilhetes_disponiveis', 'instrutor_id', 'nivel_aconselhado']
        labels = {
            'nome': 'Nome da aula',
            'bilhetes_disponiveis': 'Bilhetes disponíveis para venda',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da aula'}),
            'bilhetes_disponiveis': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bilhetes disponíveis para venda'}),
        }
        label_suffix = ':'
        attrs = {'class': 'login-form'}

    def hide_instrutor_id_field(self):
        del self.fields['instrutor_id']

class CriarAulaInstrutorForm(forms.ModelForm):
    data_hora = forms.CharField(label="Data e hora:", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AAAA-MM-DD hh:mm:ss'}))

    preco_bilhete = forms.DecimalField(label='Preço do bilhete (€):', max_digits=6, decimal_places=2, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Preço do bilhete (€)'}))

    nivel_aconselhado = forms.ModelChoiceField(label='Nível aconselhado:', queryset=NivelMembro.objects.all(), to_field_name='id_nivel',
                                               widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = AulaDanca
        fields = ['nome', 'data_hora', 'preco_bilhete', 'bilhetes_disponiveis', 'nivel_aconselhado']
        labels = {
            'nome': 'Nome da aula',
            'bilhetes_disponiveis': 'Bilhetes disponíveis para venda',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da aula'}),
            'bilhetes_disponiveis': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bilhetes disponíveis para venda'}),
        }
        label_suffix = ':'
        attrs = {'class': 'login-form'}


class CriarEventoForm(forms.ModelForm):
    data_hora = forms.CharField(label="Data e hora:", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AAAA-MM-DD hh:mm:ss'}))

    preco_bilhete = forms.DecimalField(label='Preço do bilhete (€):', max_digits=6, decimal_places=2, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Preço do bilhete (€)'}))

    class Meta:
        model = Evento
        fields = ['nome', 'data_hora', 'preco_bilhete', 'bilhetes_disponiveis', 'descricao', 'artistas']
        labels = {
            'nome': 'Nome do Evento',
            'bilhetes_disponiveis': 'Bilhetes disponíveis para venda',
            'descricao': 'Descrição',
            'artistas': 'Artistas'
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do evento'}),
            'bilhetes_disponiveis': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bilhetes disponíveis para venda'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição'}),
            'artistas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Artistas'}),
        }
        label_suffix = ':'
        attrs = {'class': 'login-form'}

class CriarAvaliacaoForm(forms.ModelForm):

    RATING_CHOICES = [(1, '1 estrela'), (2, '2 estrelas'), (3, '3 estrelas'), (4, '4 estrelas'), (5, '5 estrelas')]

    rating = forms.IntegerField(widget=forms.Select(choices=RATING_CHOICES))

    class Meta:
        model = Avaliacao
        fields = ['titulo','descricao', 'rating']
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'rating': 'Avaliação (1 a 5 estrelas)'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Descrição'}),
        }
        label_suffix = ':'
        attrs = {'class': 'login-form'}
