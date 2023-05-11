from django import forms
from django.contrib.auth.models import User

from .models import Membro
#Categoria


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = ['nome', 'email', 'genero', 'imagem_perfil', 'descricao', 'data_nascimento', 'preferencias_musicais', 'pontos']
        labels = []
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genero': forms.RadioSelect(choices=Membro.genero_choices, attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'imagem_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição'}),

            'preferencias_musicais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferências Musicais'}),

            'pontos': forms.HiddenInput(),
            #'amigos': forms.HiddenInput(),
        }
        label_suffix = ''
        attrs = {'class': 'login-form'}

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}))
    username = forms.CharField(
       widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))


#class InstrutorForm(forms.ModelForm):
    #especializacao = forms.ModelChoiceField(queryset=Categoria.objects.all())

    #class Meta:
        #model = Utilizador
        #fields = ['nome', 'email', 'genero', 'imagem_perfil', 'descricao', 'data_nascimento', 'preferencias_musicais', 'especializacao']
