from django import forms
from .models import genero_choices,  Membro, Instrutor, Categoria
from datetime import date, timedelta


class RegisterMemberForm(forms.ModelForm):
    username = forms.CharField(label='Nome de utilizador (único):', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}))
    genero = forms.ChoiceField(label='Género:', choices=genero_choices, widget=forms.RadioSelect)
    data_nascimento = forms.DateField(label='Data de nascimento', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Membro
        fields = ['username', 'password', 'nome', 'email', 'genero', 'descricao', 'data_nascimento', 'preferencias_musicais', 'imagem_perfil']
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
            'imagem_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        label_suffix = ':'
        attrs = {'class': 'register-form'}

    def clean_data_nascimento(self):
        data = self.cleaned_data['data_nascimento']
        idade = (date.today() - data) // timedelta(days=365.2425)
        if idade < 3 or idade > 100:
            raise forms.ValidationError("Deverá ter entre 3 a 100 anos de idade para se poder registar.")
        return data


class RegisterInstrutorForm(forms.ModelForm):
    username = forms.CharField(label='Nome de utilizador (único):', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}))
    genero = forms.ChoiceField(label='Género:', choices=genero_choices, widget=forms.RadioSelect)
    data_nascimento = forms.DateField(label='Data de nascimento', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    especializacao = forms.ModelChoiceField(queryset=Categoria.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Instrutor
        fields = ['username', 'password', 'nome', 'email', 'genero', 'descricao', 'data_nascimento', 'imagem_perfil', 'especializacao']
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
            'imagem_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        label_suffix = ':'
        attrs = {'class': 'register-form'}

    def clean_data_nascimento(self):
        data = self.cleaned_data['data_nascimento']
        idade = (date.today() - data) // timedelta(days=365.2425)
        if idade < 3 or idade > 100:
            raise forms.ValidationError("Deverá ter entre 3 a 100 anos de idade para se poder registar.")
        return data
