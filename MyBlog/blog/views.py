# En el archivo views.py de tu aplicación 'blog'

from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from .models import Article
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    articles = Article.objects.all()[:3]  # Obtiene los primeros 3 artículos
    return render(request, 'blog/home.html', {'articles': articles})

@login_required
def login_view(request):
    # Esta vista podría simplemente redirigir a la página de inicio después de iniciar sesión
    return redirect('home')


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    # Aquí puedes agregar la lógica para mostrar los detalles del artículo
    # y también mostrar los comentarios relacionados
    return render(request, 'blog/article_detail.html', {'article': article})

def add_comment_to_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article_detail', article_id=article_id)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_article.html', {'form': form})
