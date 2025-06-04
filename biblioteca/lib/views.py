from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.safestring import mark_safe
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib import messages
from .models import Livro, Biblioteca
from .forms import LivroForm, CustomUserCreationForm, CustomAuthenticationForm
import json

User = get_user_model()

def login_page(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            login_form = CustomAuthenticationForm(request, data=request.POST)
            register_form = CustomUserCreationForm()  # Formulário vazio

            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                return redirect('homepage')

        elif action == 'registro':
            login_form = CustomAuthenticationForm(request)  # Formulário vazio
            register_form = CustomUserCreationForm(request.POST)

            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Conta criada com sucesso.')
                return redirect('login')

    else:  # GET request
        login_form = CustomAuthenticationForm(request)
        register_form = CustomUserCreationForm()

    return render(request, 'login.html', {
        'login': login_form,
        'form': register_form,
    })

def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.usuario = request.user
            livro.save()
            return redirect('homepage')
    else:
        form = LivroForm()
    return render(request, 'homepage.html', {'form': form})

def arquivo(request):
    livros = Livro.objects.filter(usuario=request.user)
    biblioteca, created = Biblioteca.objects.get_or_create(usuario=request.user)
    context = {
        'livros': livros,
        'biblioteca': biblioteca  # Agora ambos estão no mesmo contexto
    }
    return render(request, 'arquivo.html', context)

def editar_livro(request, livro_id):
    if request.method == 'POST':
        data = json.loads(request.body)  # <- Aqui está a mudança
        livro = Livro.objects.get(id=livro_id)
        livro.titulo = data.get('titulo')
        livro.autor = data.get('autor')
        livro.editora = data.get('editora')
        livro.tradutor = data.get('tradutor')
        livro.genero = data.get('genero')
        livro.npaginas = data.get('npaginas')
        livro.ano = data.get('ano')
        livro.preco = data.get('preco')
        livro.save()
        return JsonResponse({
            'id': livro.id,
            'titulo': livro.titulo,
            'autor': livro.autor,
            'editora': livro.editora,
            'tradutor': livro.tradutor or '',
            'genero': livro.genero or '',
            'npaginas': livro.npaginas,
            'ano': livro.ano,
            'preco': livro.preco
        })
    else:
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

def deletar_livro(request, livro_id):
    if request.method == 'POST':
        try:
            livro = Livro.objects.get(id=livro_id)
            livro.delete()
            return JsonResponse({'status': 'ok'})
        except Livro.DoesNotExist:
            return JsonResponse({'erro': 'Livro não encontrado'}, status=404)
    return JsonResponse({'erro': 'Método não permitido'}, status=405)

@csrf_protect
def editar_anotacoes(request):
    if request.method == 'POST':
        try:
            livro_id = request.POST.get('livro_id')
            if not livro_id:
                return JsonResponse({'erro': 'ID do livro não fornecido'}, status=400)

            livro = get_object_or_404(Livro, id=livro_id)
            livro.anotacoes = request.POST.get('anotacoes', '')
            livro.save()

            return JsonResponse({
                'status': 'ok',
                'livro_id': livro.id,
                'anotacoes': mark_safe(livro.anotacoes)  # Marca como seguro
            })

        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=500)

    return JsonResponse({'erro': 'Método não permitido'}, status=405)


def usuario(request):
    biblioteca, created = Biblioteca.objects.get_or_create(usuario=request.user)

    if request.method == 'POST' and 'nome_biblioteca' in request.POST:
        biblioteca.nome = request.POST['nome_biblioteca'].strip() or "Minha biblioteca"
        biblioteca.save()
        return JsonResponse({'status': 'success'})

    if 'descricao_biblioteca' in request.POST:
        biblioteca.descricao = request.POST['descricao_biblioteca'].strip()
        biblioteca.save()
        return JsonResponse({'status': 'success'})

    livros = Livro.objects.filter(usuario=request.user)
    total_livros = livros.count()
    total_paginas = sum(livro.npaginas for livro in livros if livro.npaginas)
    preco_total = sum(livro.preco for livro in livros if livro.preco)

    return render(request, 'usuario.html', {
        'biblioteca': biblioteca,
        'total_livros': total_livros,
        'total_paginas': total_paginas,
        'preco_total': preco_total,
    })
