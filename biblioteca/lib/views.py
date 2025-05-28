from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .models import Livro
from .forms import LivroForm, CustomUserCreationForm, CustomAuthenticationForm
import json


def login_page(request):
    login_form = CustomAuthenticationForm(request, data=request.POST or None)
    register_form = CustomUserCreationForm(request.POST or None)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                return redirect('homepage')
            else:
                messages.error(request, 'Erro ao fazer login.')

        elif action == 'registro':
            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Conta criada com sucesso.')
                return redirect('login')
            else:
                messages.error(request, 'Erro ao criar conta.')

    return render(request, 'login.html', {
        'login': login_form,
        'form': register_form
    })


def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirecionar para evitar reenvio do formulário
            return redirect('homepage')
    else:
        form = LivroForm()
    return render(request, 'homepage.html', {'form': form})

def arquivo(request):
    livros = Livro.objects.all()
    context = {'livros': livros}
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
            'tradutor': livro.tradutor,
            'genero': livro.genero,
            'npaginas': livro.npaginas,
            'ano': livro.ano,
            'preco': livro.preco
        })
    else:
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

@csrf_exempt  # ou use token corretamente
def deletar_livro(request, livro_id):
    if request.method == 'POST':
        try:
            livro = Livro.objects.get(pk=livro_id)
            livro.delete()
            return JsonResponse({'status': 'ok'})
        except ObjectDoesNotExist:
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
            livro.anotacoes = request.POST.get('anotacoes', '')  # Usa string vazia como padrão
            livro.save()

            return JsonResponse({
                'status': 'ok',
                'livro_id': livro.id,
                'anotacoes': livro.anotacoes
            })

        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=500)

    return JsonResponse({'erro': 'Método não permitido'}, status=405)