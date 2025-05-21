from django.shortcuts import render, redirect
from .models import Livro
from .forms import LivroForm

def homepage(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')  # recarrega a página
    else:
        form = LivroForm()

    livros = Livro.objects.all()
    return render(request, 'homepage.html', {'livros': livros, 'form': form})