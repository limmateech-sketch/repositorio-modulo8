from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('livros/', views.lista_livros, name='lista_livros'),
    path('estoque/', views.gestao_estoque, name='gestao_estoque'),
    path('cadastrar/', views.cadastrar_livro, name='cadastrar_livro'),
    path('editar/<int:id>/', views.editar_livro, name='editar_livro'),
    path('excluir/<int:id>/', views.excluir_livro, name='excluir_livro'),
]
