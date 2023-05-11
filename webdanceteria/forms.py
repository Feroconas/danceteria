from django import forms
from .models import User
from .models import Membro


# Categoria


class RegisterMemberForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = ['nome', 'email', 'genero', 'descricao', 'data_nascimento', 'preferencias_musicais', 'imagem_perfil']
        labels = []
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'genero': forms.RadioSelect(choices=Membro.genero_choices, attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'preferencias_musicais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferências Musicais'}),
            'imagem_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
        label_suffix = ''
        attrs = {'class': 'register-form'}

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

# class InstrutorForm(forms.ModelForm):
# especializacao = forms.ModelChoiceField(queryset=Categoria.objects.all())

# class Meta:
# model = Utilizador
# fields = ['nome', 'email', 'genero', 'imagem_perfil', 'descricao', 'data_nascimento', 'preferencias_musicais', 'especializacao']
