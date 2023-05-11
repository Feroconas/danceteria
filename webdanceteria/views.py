import locale
from django.utils import timezone
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Instrutor
from webdanceteria.forms import RegisterUserForm
from webdanceteria.models import Membro, NivelMembro, Evento, AulaDanca, BilheteEvento, BilheteAula
from .forms import RegisterUserForm
from django.contrib.auth.decorators import user_passes_test



def home(request):
    user_in_instrutores = request.user.groups.filter(name='Instrutores').exists()
    return render(request, 'webdanceteria/home.html', {'user_in_instrutores': user_in_instrutores})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            # user.user_permissions.add(Permission.objects.get(codename="home"))
            # Permission.objects.get(codename="view_opcao"),
            # Permission.objects.get(codename="change_opcao"))
            login(request, user)
            return redirect('webdanceteria:home')
        else:
            return HttpResponse("Parâmetros de login inválidos: " + str(username) + " " + str(password))
    else:
        return render(request, 'webdanceteria/login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password']
            )
            # Definindo os pontos iniciais do user
            pontos = 0
            nivel_iniciante = NivelMembro.objects.get(id_nivel=1)
            a = Membro(
                user=user,
                nome=form.cleaned_data['nome'],
                email=form.cleaned_data['email'],
                genero=form.cleaned_data['genero'],
                data_nascimento=form.cleaned_data['data_nascimento'],
                preferencias_musicais=form.cleaned_data['preferencias_musicais'],
                nivel_membro=nivel_iniciante,
                pontos=pontos
            )
            a.save()

            return redirect('webdanceteria:login_view')
    else:
        form = RegisterUserForm()
    return render(request, 'webdanceteria/register.html', {'form': form})

#@login_required
#def criar_instrutor(request):
 #   if request.method == 'POST':
  #      form = InstrutorForm(request.POST)
   #     if form.is_valid():
    #        instrutor = form.save(commit=False)
     #       instrutor.user = request.user
      #      instrutor.save()
       #     return redirect('home')
   # else:
    #    form = InstrutorForm()
    #return render(request, 'criar_instrutor.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('webdanceteria:home')


def profile_view(request):
    user_in_instrutores = request.user.groups.filter(name='Instrutores').exists()
    bilhetesEvento = BilheteEvento.objects.order_by(F('data_validade'))
    bilhetesAula = BilheteAula.objects.order_by(F('data_validade'))
    pontos = request.user.utilizador.pontos
    return render(request, 'webdanceteria/profile.html',  {'bilhetesEvento': bilhetesEvento,'bilhetesAula': bilhetesAula,
                                                           'pontos': pontos, 'user_in_instrutores': user_in_instrutores})


@csrf_exempt
def editUser_view(request):
    if request.method == 'POST':
        userDjango = request.user
        userDjango.username = request.POST.get('username')
        user = request.user.utilizador
        user.nome = request.POST.get('nome')
        user.email = request.POST.get('email')
        user.genero = request.POST.get('genero')
        user.descricao = request.POST.get('descricao')
        user.data_nascimento = request.POST.get('data_nascimento')
        user.preferencias_musicais = request.POST.get('preferencias_musicais')
        user.save()
        userDjango.save()
        return render(request, 'webdanceteria/profile.html')
    else:
        return HttpResponse("Parâmetros de login inválidos: ")
        return render(request, 'webdanceteria/profile.html')

def events_view(request):
    user_in_instrutores = request.user.groups.filter(name='Instrutores').exists()
    eventos = Evento.objects.exclude(data_hora__isnull=True).order_by(F('data_hora'))
    # Set the locale to a specific language and encoding
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    for evento in eventos:
        data_hora_formatada = evento.data_hora.strftime('%d de %B de %Y, %H:%M')
        evento.data_hora = data_hora_formatada
    aulas = AulaDanca.objects.order_by(F('data_hora'))
    for aula in aulas:
        data_hora_formatada = aula.data_hora.strftime('%d de %B de %Y, %H:%M')
        aula.data_hora = data_hora_formatada
    return render(request, 'webdanceteria/events.html', {'eventos': eventos, 'aulas': aulas, 'user_in_instrutores': user_in_instrutores})


@login_required()
def comprarBilheteEv_view(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    preco = evento.preco_bilhete
    comprador = request.user.utilizador
    data_compra = timezone.now()
    data_validade = evento.data_hora

    if evento.bilhetes_disponiveis > 0:
        evento.bilhetes_disponiveis -= 1
        evento.save()
        BilheteEvento.objects.create(comprador=comprador, evento=evento, data_compra=data_compra, data_validade=data_validade,
                               preco=preco)
        comprador.pontos += 7
        comprador.save()
        return JsonResponse({
            "mensagem": "Bilhete comprado com sucesso!",
            "bilhetes_disponiveis": evento.bilhetes_disponiveis,
            "pontos": comprador.pontos
        })
    else:
        return JsonResponse({"mensagem": "Não há mais bilhetes disponíveis para este evento."})

@login_required()
def apagarBilheteEv_view(request, bilhete_id):
    bilhete = get_object_or_404(BilheteEvento, id=bilhete_id)
    evento = bilhete.evento
    if request.user.utilizador == bilhete.comprador:
        bilhete.comprador.pontos -= 7
        bilhete.comprador.save()
        bilhete.delete()
        evento.bilhetes_disponiveis += 1
        evento.save()
        return JsonResponse({
            "mensagem": "Bilhete apagado com sucesso!",
            "bilhetes_disponiveis": evento.bilhetes_disponiveis,
            "pontos": bilhete.comprador.pontos
        })
    else:
        return JsonResponse({"mensagem": "Não tem permissão para apagar este bilhete."})



@login_required()
def comprarBilheteAula_view(request, aula_id):
    aulaDanca = get_object_or_404(AulaDanca, id=aula_id)
    preco = aulaDanca.preco_bilhete
    comprador = request.user.utilizador
    data_compra = timezone.now()
    data_validade = aulaDanca.data_hora

    if aulaDanca.bilhetes_disponiveis > 0:
        aulaDanca.bilhetes_disponiveis -= 1
        aulaDanca.participantes += 1
        aulaDanca.save()
        BilheteAula.objects.create(comprador=comprador, aula=aulaDanca, data_compra=data_compra, data_validade=data_validade,
                               preco=preco)
        comprador.pontos += 5
        comprador.save()
        return JsonResponse({
            "mensagem": "Bilhete comprado com sucesso!",
            "bilhetes_disponiveis": aulaDanca.bilhetes_disponiveis,
            "pontos": comprador.pontos
        })
    else:
        return JsonResponse({"mensagem": "Não há mais bilhetes disponíveis para este evento."})

@login_required()
def apagarBilheteAula_view(request, bilheteAula_id):
    bilhete = get_object_or_404(BilheteAula, id=bilheteAula_id)
    aula = bilhete.aula
    if request.user.utilizador == bilhete.comprador:
        bilhete.comprador.pontos -= 5
        bilhete.comprador.save()
        bilhete.delete()
        aula.bilhetes_disponiveis += 1
        aula.participantes -= 1
        aula.save()

        return JsonResponse({
            "mensagem": "Bilhete apagado com sucesso!",
            "bilhetes_disponiveis": aula.bilhetes_disponiveis,
            "pontos": bilhete.comprador.pontos
        })
    else:
        return JsonResponse({"mensagem": "Não tem permissão para apagar este bilhete."})



#@user_passes_test(is_instrutor)
#def criar_aula(request):
