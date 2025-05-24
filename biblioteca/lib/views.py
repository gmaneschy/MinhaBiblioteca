from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import Livro
from .forms import LivroFormSimples, LivroFormAvancado


def cadastrar_livro(request):
    template_name = 'homepage.html'
    form_simples = LivroFormSimples(request.POST or None)
    form_avancado = LivroFormAvancado(request.POST or None)

    if request.method == 'POST':
        if 'form_simples' in request.POST and form_simples.is_valid():
            form_simples.save()
            return redirect('lista_livros')
        elif 'form_avancado' in request.POST and form_avancado.is_valid():
            form_avancado.save()
            # Aqui você pode salvar as preferências de campos visíveis
            request.session['mostrar_npaginas'] = form_avancado.cleaned_data['mostrar_npaginas']
            request.session['mostrar_preco'] = form_avancado.cleaned_data['mostrar_preco']
            return redirect('lista_livros')

    return render(request, template_name, {
        'form_simples': form_simples,
        'form_avancado': form_avancado
    })

def arquivo(request):
    livros = Livro.objects.all()
    context = {'livros': livros}
    return render(request, 'arquivo.html', context)

def editar_livro(request, livro_id):
    livro = Livro.objects.get(id=livro_id)
    if request.method == 'POST':
        livro.titulo = request.POST.get('titulo')
        livro.autor = request.POST.get('autor')
        livro.editora = request.POST.get('editora')
        livro.save()
        return JsonResponse({
            'id': livro.id,
            'titulo': livro.titulo,
            'autor': livro.autor,
            'editora': livro.editora
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