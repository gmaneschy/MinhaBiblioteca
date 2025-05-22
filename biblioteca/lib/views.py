from django.shortcuts import render, redirect
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
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro atualizado com sucesso!")
            return redirect('arquivo')
    else:
        form = LivroForm(instance=livro)
    return render(request, 'editar_livro.html', {'form': form, 'livro': livro})

def deletar_livro(request, livro_id):
    livro = Livro.objects.get(id=livro_id)
    livro.delete()
    messages.success(request, "Livro deletado com sucesso!")
    return redirect('arquivo')