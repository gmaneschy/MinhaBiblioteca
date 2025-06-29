"""
URL configuration for biblioteca project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from lib import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.cadastrar_livro, name="homepage"),
    path('homepage/', views.cadastrar_livro, name="homepage"),
    path('arquivo/', views.arquivo, name="arquivo"),
    path('editar/<int:livro_id>/', views.editar_livro, name='editar_livro'),
    path('deletar/<int:livro_id>/', views.deletar_livro, name='deletar_livro'),
    path('editar-anotacoes/', views.editar_anotacoes, name='editar_anotacoes'),
    path('login/', views.login_page, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('usuario/', views.usuario, name='usuario'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
