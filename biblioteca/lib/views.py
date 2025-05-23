from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import Livro
from .forms import LivroForm

def homepage(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro cadastrado!")
            return redirect('homepage')  # recarrega a página
    else:
        form = LivroForm()

    livros = Livro.objects.all()
    return render(request, 'homepage.html', {'livros': livros, 'form': form})

def arquivo(request):
    form = LivroForm(request.GET)
    livros = Livro.objects.all()
    return render(request, 'arquivo.html', {'livros': livros, 'form': form})

def editar_livro(request, livro_id):
    livro = Livro.objects.get(id=livro_id)
    if request.method == 'POST':
        livro.titulo = request.POST['titulo']
        livro.autor = request.POST['autor']
        livro.editora = request.POST['editora']
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