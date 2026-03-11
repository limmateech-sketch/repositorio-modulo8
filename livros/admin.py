from django.contrib import admin
from .models import Livro


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'categoria', 'preco', 'isbn', 'estoque', 'data_cadastro')
    search_fields = ('titulo', 'autor', 'isbn')
    list_filter = ('categoria',)
