from django.db import models


class Livro(models.Model):
    CATEGORIAS = (
        ('Ficção', 'Ficção'),
        ('Não-Ficção', 'Não-Ficção'),
        ('Tecnologia', 'Tecnologia'),
        ('Humor', 'Humor'),
        ('Infantil', 'Infantil'),
        ('Biografia', 'Biografia'),
    )

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    isbn = models.CharField(max_length=20, unique=True)
    estoque = models.PositiveIntegerField(default=0)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['titulo']
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'


    @property
    def valor_em_estoque(self):
        return self.preco * self.estoque

    def __str__(self):
        return f'{self.titulo} - {self.autor}'
