from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .models import Livro, Login
from .forms import LivroForm, LoginForm, RegistroForm
import json


def login_registro_view(request):
    login_form = LoginForm()
    registro_form = RegistroForm()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                senha = login_form.cleaned_data['senha']
                try:
                    Login.objects.get(email=email, senha=senha)
                    return redirect('homepage')
                except Login.DoesNotExist:
                    messages.error(request, 'Email ou senha inválidos.')

        elif action == 'registro':
            registro_form = RegistroForm(request.POST)
            if registro_form.is_valid():
                registro_form.save()
                return redirect('login')

    return render(request, 'login.html', {
        'login_form': login_form,
        'registro_form': registro_form
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