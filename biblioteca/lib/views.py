from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.html import escape
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Livro, Biblioteca
from .forms import LivroForm, CustomUserCreationForm, CustomAuthenticationForm
import json

User = get_user_model()

def login_page(request):
    """
    Gerencia a página de login/registro.
    Lida com requisições POST para login e registro de usuários.
    Redireciona para a página inicial após o login bem-sucedido.
    Exibe mensagens de sucesso/erro apropriadas.
    """
    active_tab = 'login'  # Aba padrão
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            login_form = CustomAuthenticationForm(request, data=request.POST)
            register_form = CustomUserCreationForm()  # Formulário vazio

            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                return redirect('homepage')
            active_tab = 'login'

        elif action == 'registro':
            login_form = CustomAuthenticationForm()  # Formulário vazio
            register_form = CustomUserCreationForm(request.POST)

            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Conta criada com sucesso.')
                return redirect('login')
            else:
                active_tab = 'registro'  # Fica na aba de registro se houver erros

    else:  # GET
        login_form = CustomAuthenticationForm()
        register_form = CustomUserCreationForm()

    return render(request, 'login.html', {
        'login': login_form,
        'form': register_form,
        'active_tab': active_tab,
    })


@login_required
def cadastrar_livro(request):
    """
    Requer autenticação (@login_required).
    Processa o formulário de cadastro de livros.
    Associa o livro ao usuário logado antes de salvar.
    Redireciona para a página inicial após o cadastro.
    """
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

@login_required
def arquivo(request):
    """
    Requer autenticação.
    Exibe a lista de livros do usuário.
    Cria automaticamente uma biblioteca para o usuário se não existir.
    Renderiza o template 'arquivo.html' com os livros e dados da biblioteca.
    """
    livros = Livro.objects.filter(usuario=request.user)
    biblioteca, created = Biblioteca.objects.get_or_create(usuario=request.user)
    context = {
        'livros': livros,
        'biblioteca': biblioteca  # Agora ambos estão no mesmo contexto
    }
    return render(request, 'arquivo.html', context)

@login_required
def editar_livro(request, livro_id):
    """
    Requer autenticação.
    Processa requisições AJAX para edição de livros.
    Atualiza os campos do livro com os dados recebidos.
    Retorna os dados atualizados em formato JSON.
    Inclui tratamento para campos numéricos e valores nulos.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        livro = Livro.objects.get(id=livro_id)

        # Tratar campos numéricos
        def parse_number(value, default=None):
            if value == '' or value is None:
                return default
            return value

        livro.titulo = data.get('titulo')
        livro.autor = data.get('autor')
        livro.editora = data.get('editora')
        livro.tradutor = data.get('tradutor') or None
        livro.genero = data.get('genero') or None
        livro.npaginas = parse_number(data.get('npaginas'), None)
        livro.ano = parse_number(data.get('ano'), None)
        livro.preco = parse_number(data.get('preco'), None)

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

@login_required
def deletar_livro(request, livro_id):
    """
    Requer autenticação.
    Remove um livro específico do banco de dados.
    Retorna uma resposta JSON indicando sucesso ou falha.
    Verifica se o livro existe antes de tentar deletar.
    """
    if request.method == 'POST':
        try:
            livro = Livro.objects.get(id=livro_id)
            livro.delete()
            return JsonResponse({'status': 'ok'})
        except Livro.DoesNotExist:
            return JsonResponse({'erro': 'Livro não encontrado'}, status=404)
    return JsonResponse({'erro': 'Método não permitido'}, status=405)

@login_required
@csrf_protect
def editar_anotacoes(request):
    """
    Requer autenticação e proteção CSRF.
    Atualiza as anotações de um livro específico.
    Valida a entrada e escapa HTML para segurança.
    Retorna uma resposta JSON com o status da operação.
    """
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
                'anotacoes': escape(livro.anotacoes)  # Escapa HTML perigoso
            })

        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=500)

    return JsonResponse({'erro': 'Método não permitido'}, status=405)

@login_required
def usuario(request):
    """
    Requer autenticação.
    Gerencia as informações do perfil do usuário.
    Permite atualizar o nome e descrição da biblioteca.
    Calcula e exibe estatísticas como total de livros, páginas e valor total.
    Renderiza o template 'usuario.html' com os dados do usuário e sua biblioteca.
    """
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
