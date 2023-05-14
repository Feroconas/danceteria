import locale
from django.contrib.admin import ModelAdmin
from django.utils import timezone
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from webdanceteria.templatetags.registerfilters import *
from datetime import date, timedelta, datetime
from .forms import *
from django.contrib.auth.decorators import user_passes_test


def home(request):
    eventos = Evento.objects.order_by('-id')[:5]
    return render(request, 'webdanceteria/home.html', {'eventos': eventos})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('webdanceteria:home')
        else:
            return HttpResponse("Parâmetros de login inválidos: " + str(username) + " " + str(password))
    else:
        return render(request, 'webdanceteria/login.html')


def register_member_view(request):
    if request.method == 'POST':
        form = RegisterMemberForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password']
            )
            nivel_iniciante = NivelMembro.objects.get(id_nivel=1)
            membro = Membro(
                user=user,
                nome=form.cleaned_data['nome'],
                email=form.cleaned_data['email'],
                genero=form.cleaned_data['genero'],
                descricao=form.cleaned_data['descricao'],
                data_nascimento=form.cleaned_data['data_nascimento'],
                preferencias_musicais=form.cleaned_data['preferencias_musicais'],
                nivel_membro=nivel_iniciante,
            )
            membro.imagem_perfil.save(request.FILES['imagem_perfil'].name, request.FILES['imagem_perfil'])
            membro.save()

            return redirect('webdanceteria:login_view')
    else:
        form = RegisterMemberForm()
    return render(request, 'webdanceteria/registermember.html', {'form': form})


@permission_required('webdanceteria.add_instrutor')
@login_required()
def register_instrutor_view(request):
    if request.method == 'POST':
        form = RegisterInstrutorForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password']
            )
            instrutor = Instrutor(
                user=user,
                nome=form.cleaned_data['nome'],
                email=form.cleaned_data['email'],
                genero=form.cleaned_data['genero'],
                descricao=form.cleaned_data['descricao'],
                data_nascimento=form.cleaned_data['data_nascimento'],
                especializacao=form.cleaned_data['especializacao'],
            )
            instrutor.imagem_perfil.save(request.FILES['imagem_perfil'].name, request.FILES['imagem_perfil'])
            instrutor.save()
            return redirect('webdanceteria:home')
    else:
        form = RegisterInstrutorForm()
    return render(request, 'webdanceteria/registerinstrutor.html', {'form': form})


@login_required()
@permission_required('webdanceteria.add_auladanca')
def criar_aula_view(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            form = CriarAulaAdminForm(request.POST)
        else:
            form = CriarAulaInstrutorForm(request.POST)
        if form.is_valid():
            data_hora_str = form.cleaned_data['data_hora']
            try:
                data_hora_obj = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return HttpResponse("Data e hora com formato errado: " + data_hora_str)

            if request.user.is_superuser:
                instrutor = form.cleaned_data['instrutor_id']
            else:
                instrutor = getUtilizador(request.user)
                instrutor.n_aulas += 1
                instrutor.save()

            aulaDanca = AulaDanca(
                nome=form.cleaned_data['nome'],
                data_hora=data_hora_obj,
                preco_bilhete=form.cleaned_data['preco_bilhete'],
                bilhetes_disponiveis=form.cleaned_data['bilhetes_disponiveis'],
                instrutor_id=instrutor,
                nivel_aconselhado=form.cleaned_data['nivel_aconselhado']
            )
            aulaDanca.save()

            return redirect('webdanceteria:events_view')
    else:
        if request.user.is_superuser:
            form = CriarAulaAdminForm()
        else:
            form = CriarAulaInstrutorForm()
    return render(request, 'webdanceteria/createAula.html', {'form': form})


@login_required()
@permission_required('webdanceteria.add_evento')
def criar_evento_view(request):
    if request.method == 'POST':
        form = CriarEventoForm(request.POST)
        if form.is_valid():
            data_hora_str = form.cleaned_data['data_hora']
            try:
                data_hora_obj = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return HttpResponse("Data e hora com formato errado: " + data_hora_str)
            evento = Evento(
                nome=form.cleaned_data['nome'],
                data_hora=data_hora_obj,
                preco_bilhete=form.cleaned_data['preco_bilhete'],
                bilhetes_disponiveis=form.cleaned_data['bilhetes_disponiveis'],
                descricao=form.cleaned_data['descricao'],
                artistas=form.cleaned_data['artistas']
            )
            evento.save()

            return redirect('webdanceteria:events_view')
    else:
        form = CriarEventoForm()
    return render(request, 'webdanceteria/createEvento.html', {'form': form})


@login_required()
def criar_avaliacao_view(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        form = CriarAvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = Avaliacao(
                avaliador=request.user,
                evento=evento,
                titulo=form.cleaned_data['titulo'],
                descricao=form.cleaned_data['descricao'],
                rating=form.cleaned_data['rating'],
                data_avaliacao=timezone.now(),
            )
            avaliacao.save()
            return redirect('webdanceteria:profile_view')
    else:
        form = CriarAvaliacaoForm()
    return render(request, 'webdanceteria/createAvaliacao.html', {'form': form})


@login_required()
def avaliacoes_view(request):
    avaliacoes = Avaliacao.objects.order_by('-data_avaliacao')
    return render(request, 'webdanceteria/avaliacoes.html', {'avaliacoes': avaliacoes})


@login_required()
def logout_view(request):
    logout(request)
    return redirect('webdanceteria:home')


@login_required()
def profile_view(request):
    bilhetesEvento = BilheteEvento.objects.filter(comprador=request.user).order_by(F('data_validade'))
    bilhetesAula = BilheteAula.objects.filter(comprador=request.user).order_by(F('data_validade'))
    nivel_nome = NIVEL_CHOICES[request.user.membro.nivel_membro.id_nivel - 1][1] if isMembro(request.user) else None

    return render(request, 'webdanceteria/profile.html',
                  {'bilhetesEvento': bilhetesEvento, 'bilhetesAula': bilhetesAula, 'genero_choices': genero_choices, 'nivel_nome': nivel_nome})


@csrf_exempt
@login_required()
def editUser_view(request):
    if request.method == 'POST':
        datanascimento = datetime.strptime(request.POST.get('data_nascimento'), '%Y-%m-%d').date()
        idade = (date.today() - datanascimento) // timedelta(days=365.2425)
        if idade < 3 or idade > 100:
            return render(request, 'webdanceteria/profile.html', {'genero_choices': genero_choices})
        userDjango = request.user
        userDjango.username = request.POST.get('username')
        user = getUtilizador(request.user)
        user.nome = request.POST.get('nome')
        user.email = request.POST.get('email')
        user.genero = request.POST.get('genero')
        user.descricao = request.POST.get('descricao')
        user.data_nascimento = datanascimento
        if isMembro(request.user):
            user.preferencias_musicais = request.POST.get('preferencias_musicais')
        if 'imagem_perfil' in request.FILES:
            user.imagem_perfil.save(request.FILES['imagem_perfil'].name, request.FILES['imagem_perfil'])
        user.save()
        userDjango.save()
        return render(request, 'webdanceteria/profile.html', {'genero_choices': genero_choices})
    else:
        return render(request, 'webdanceteria/profile.html', {'genero_choices': genero_choices})


def events_view(request):
    eventos = Evento.objects.exclude(data_hora__isnull=True).order_by(F('data_hora'))
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    for evento in eventos:
        data_hora_formatada = evento.data_hora.strftime('%d de %B de %Y, %H:%M')
        evento.data_hora = data_hora_formatada
    aulas = AulaDanca.objects.order_by(F('data_hora'))
    for aula in aulas:
        data_hora_formatada = aula.data_hora.strftime('%d de %B de %Y, %H:%M')
        aula.data_hora = data_hora_formatada
    return render(request, 'webdanceteria/events.html',
                  {'eventos': eventos, 'aulas': aulas})


@login_required()
def comprarBilheteEv_view(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    preco = evento.preco_bilhete
    comprador = request.user
    data_compra = timezone.now()
    data_validade = evento.data_hora

    if evento.bilhetes_disponiveis > 0:

        if BilheteEvento.objects.filter(comprador=request.user,
                                        evento_id=evento).exists():  # Ver se já comprou o bilhete
            return JsonResponse({
                "mensagem": "Já tens este bilhete, verifica no teu perfil...",
            })
        utilizador = getUtilizador(request.user)
        utilizador.n_eventos += 1
        utilizador.save()
        evento.bilhetes_disponiveis -= 1
        evento.save()

        BilheteEvento.objects.create(comprador=comprador, evento=evento, data_compra=data_compra,
                                     data_validade=data_validade,
                                     preco=preco)
        if isMembro(request.user):
            pontos_adicionados = int(preco)
            comprador.membro.pontos += pontos_adicionados
            comprador.membro.save()
            recompensa_obtida = atualizarNivelMembro(request.user)
            if recompensa_obtida is None:
                return JsonResponse({
                    "mensagem": "Bilhete comprado com sucesso!",
                    "bilhetes_disponiveis": evento.bilhetes_disponiveis,
                    "pontos": pontos_adicionados,
                })
            else:
                return JsonResponse({
                    "mensagem": "Bilhete comprado com sucesso!",
                    "bilhetes_disponiveis": evento.bilhetes_disponiveis,
                    "pontos": pontos_adicionados,
                    "recompensa": recompensa_obtida,
                    "nivel_membro": NIVEL_CHOICES[comprador.membro.nivel_membro.id_nivel - 1][1],
                })
        else:
            return JsonResponse({
                "mensagem": "Bilhete comprado com sucesso!",
                "bilhetes_disponiveis": evento.bilhetes_disponiveis,
            })
    else:
        return JsonResponse({
            "mensagem": "Não há mais bilhetes disponíveis para este evento."})


@login_required()
def comprarBilheteAula_view(request, aula_id):
    aulaDanca = get_object_or_404(AulaDanca, id=aula_id)
    preco = aulaDanca.preco_bilhete
    comprador = request.user
    data_compra = timezone.now()
    data_validade = aulaDanca.data_hora

    if aulaDanca.bilhetes_disponiveis > 0:

        if BilheteAula.objects.filter(comprador=request.user,
                                      aula_id=aulaDanca).exists():  # Ver se já comprou o bilhete
            return JsonResponse({
                "mensagem": "Já tens este bilhete, verifica no teu perfil...",
            })

        aulaDanca.bilhetes_disponiveis -= 1
        aulaDanca.participantes += 1
        aulaDanca.save()
        utilizador = getUtilizador(request.user)
        utilizador.n_aulas += 1
        utilizador.save()

        BilheteAula.objects.create(comprador=comprador, aula=aulaDanca, data_compra=data_compra,
                                   data_validade=data_validade,
                                   preco=preco)
        if isMembro(request.user):
            pontos_adicionados = int(preco)
            comprador.membro.pontos += pontos_adicionados
            comprador.membro.save()
            recompensa_obtida = atualizarNivelMembro(request.user)
            if recompensa_obtida is None:
                return JsonResponse({
                    "mensagem": "Bilhete comprado com sucesso!",
                    "bilhetes_disponiveis": aulaDanca.bilhetes_disponiveis,
                    "pontos": pontos_adicionados,
                })
            else:
                return JsonResponse({
                    "mensagem": "Bilhete comprado com sucesso!",
                    "bilhetes_disponiveis": aulaDanca.bilhetes_disponiveis,
                    "pontos": pontos_adicionados,
                    "recompensa": recompensa_obtida,
                    "nivel_membro": NIVEL_CHOICES[comprador.membro.nivel_membro.id_nivel - 1][1],
                })
        else:
            return JsonResponse({
                "mensagem": "Bilhete comprado com sucesso!",
                "bilhetes_disponiveis": aulaDanca.bilhetes_disponiveis,
            })
    else:
        return JsonResponse({
            "mensagem": "Não há mais bilhetes disponíveis para esta aula."})


@login_required()
def apagarBilheteEv_view(request, bilhete_id):
    bilhete = get_object_or_404(BilheteEvento, id=bilhete_id)
    evento = bilhete.evento
    if request.user == bilhete.comprador:
        if isMembro(request.user):
            bilhete.comprador.membro.pontos -= int(bilhete.preco)
            bilhete.comprador.membro.save()
        bilhete.delete()
        evento.bilhetes_disponiveis += 1
        evento.save()
        utilizador = getUtilizador(request.user)
        utilizador.n_eventos -= 1
        utilizador.save()

        return JsonResponse({
            "mensagem": "Bilhete apagado com sucesso!",
        })
    else:
        return JsonResponse({"mensagem": "Não tem permissão para apagar este bilhete."})


@login_required()
def apagarBilheteAula_view(request, bilhete_id):
    bilhete = get_object_or_404(BilheteAula, id=bilhete_id)
    aulaDanca = bilhete.aula
    if request.user == bilhete.comprador:
        if isMembro(request.user):
            bilhete.comprador.membro.pontos -= int(bilhete.preco)
            bilhete.comprador.membro.save()
        bilhete.delete()
        aulaDanca.bilhetes_disponiveis += 1
        aulaDanca.participantes -= 1
        aulaDanca.save()
        utilizador = getUtilizador(request.user)
        utilizador.n_aulas -= 1
        utilizador.save()
        return JsonResponse({
            "mensagem": "Bilhete apagado com sucesso!",
        })
    else:
        return JsonResponse({"mensagem": "Não tem permissão para apagar este bilhete."})


def atualizarNivelMembro(user):
    niveis_membro = NivelMembro.objects.all().order_by('id_nivel')
    for nivel_atual in niveis_membro:
        if user.membro.pontos >= nivel_atual.pontos_necessarios and user.membro.nivel_membro.id_nivel < nivel_atual.id_nivel:
            user.membro.nivel_membro = nivel_atual
            user.membro.save()
            if nivel_atual.id_nivel == NIVEL_INICIANTE:
                BilheteAula.objects.create(comprador=user, data_compra=timezone.now(),
                                           data_validade=(timezone.now() + timedelta(weeks=10)), preco=0, especial=0,
                                           aula=AulaDanca.objects.latest('id'))
            if nivel_atual.id_nivel == NIVEL_INTERMEDIO:
                BilheteEvento.objects.create(comprador=user, data_compra=timezone.now(),
                                             data_validade=(timezone.now() + timedelta(weeks=10)), preco=0, especial=0,
                                             evento=Evento.objects.latest('id'))
            if nivel_atual.id_nivel == NIVEL_AVANCADO:
                BilheteAula.objects.create(comprador=user, data_compra=timezone.now(),
                                           data_validade=(timezone.now() + timedelta(weeks=10)), preco=0, especial=1,
                                           aula=AulaDanca.objects.order_by('-preco_bilhete').first())
            if nivel_atual.id_nivel == NIVEL_PROFISSIONAL:
                BilheteEvento.objects.create(comprador=user, data_compra=timezone.now(),
                                             data_validade=(timezone.now() + timedelta(weeks=10)), preco=0,
                                             especial=1,
                                             evento=Evento.objects.order_by('-preco_bilhete').first())
            return nivel_atual.recompensa
    return None
