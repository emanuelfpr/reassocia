from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjetoForm
from .models import Projeto


# ---------- Páginas públicas ----------
def index(request):
    busca = request.GET.get("q", "").strip()

    if busca:
        projetos = Projeto.objects.filter(
            Q(nome__icontains=busca) | Q(resumo__icontains=busca) | Q(descricao__icontains=busca)
        )
    else:
        projetos = Projeto.objects.filter(destaque=True)

    return render(request, "index.html", {"projetos": projetos, "busca": busca})


def projeto(request, id):
    p = get_object_or_404(Projeto, id=id)
    return render(request, "projeto.html", {"p": p})


def consulta(request):
    projetos = Projeto.objects.filter(na_consulta=True)
    return render(request, "consulta.html", {"projetos": projetos, "whatsapp": settings.WHATSAPP})


def contato(request):
    return render(request, "contato.html", {"whatsapp": settings.WHATSAPP})


def sobre(request):
    return render(request, "sobre.html")


# ---------- Login e logout ----------
def entrar(request):
    if request.user.is_authenticated:
        return redirect("admin_lista")

    usuario = ""

    if request.method == "POST":
        usuario = request.POST.get("usuario", "").strip()
        senha = request.POST.get("senha", "")

        if usuario == "" or senha == "":
            messages.error(request, "Preencha o usuário e a senha.")
        else:
            # o Django compara a senha com o hash guardado no banco
            user = authenticate(request, username=usuario, password=senha)
            if user is not None:
                login(request, user)
                return redirect("admin_lista")
            messages.error(request, "Usuário ou senha incorretos.")

    elif request.GET.get("next"):
        # chegou aqui porque tentou abrir uma página da administração sem login
        messages.error(request, "Faça login para acessar a administração.")

    return render(request, "login.html", {"usuario": usuario})


def sair(request):
    logout(request)
    messages.success(request, "Você saiu da administração.")
    return redirect("index")


# ---------- Administração (precisa de login) ----------
@login_required
def admin_lista(request):
    projetos = Projeto.objects.all()
    return render(request, "admin_lista.html", {"projetos": projetos})


@login_required
def admin_novo(request):
    if request.method == "POST":
        form = ProjetoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Projeto cadastrado com sucesso!")
            return redirect("admin_lista")
        messages.error(request, "Preencha o nome e a descrição do projeto.")
    else:
        form = ProjetoForm()

    return render(request, "admin_form.html", {"form": form, "editando": False})


@login_required
def admin_editar(request, id):
    p = get_object_or_404(Projeto, id=id)

    if request.method == "POST":
        form = ProjetoForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            messages.success(request, "Projeto atualizado com sucesso!")
            return redirect("admin_lista")
        messages.error(request, "Preencha o nome e a descrição do projeto.")
    else:
        form = ProjetoForm(instance=p)

    return render(request, "admin_form.html", {"form": form, "editando": True})
