from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, F, Q, Sum, DecimalField, ExpressionWrapper
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LivroForm, MovimentoEstoqueForm
from .models import Livro


def _stats():
    valor_expr = ExpressionWrapper(F('preco') * F('estoque'), output_field=DecimalField(max_digits=12, decimal_places=2))
    stats = Livro.objects.aggregate(
        total_livros=Count('id'),
        estoque_total=Sum('estoque'),
        valor_total=Sum(valor_expr),
    )
    return {
        'total_livros': stats['total_livros'] or 0,
        'estoque_total': stats['estoque_total'] or 0,
        'valor_total': stats['valor_total'] or Decimal('0.00'),
        'estoque_baixo': Livro.objects.filter(estoque__lt=5).count(),
    }


@login_required
def dashboard(request):
    livros_estoque_baixo = Livro.objects.filter(estoque__lt=5).order_by('estoque', 'titulo')[:5]
    livros_recentes = Livro.objects.order_by('-data_atualizacao')[:6]
    context = {
        **_stats(),
        'livros_estoque_baixo': livros_estoque_baixo,
        'livros_recentes': livros_recentes,
    }
    return render(request, 'dashboard.html', context)


@login_required
def lista_livros(request):
    busca = request.GET.get('q', '').strip()
    livros = Livro.objects.all()

    if busca:
        livros = livros.filter(
            Q(titulo__icontains=busca)
            | Q(autor__icontains=busca)
            | Q(isbn__icontains=busca)
            | Q(categoria__icontains=busca)
        )

    paginator = Paginator(livros, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'busca': busca,
        **_stats(),
    }
    return render(request, 'livros.html', context)


@login_required
def gestao_estoque(request):
    form = MovimentoEstoqueForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        livro = form.cleaned_data['livro']
        quantidade = form.cleaned_data['quantidade']
        operacao = form.cleaned_data['operacao']

        if operacao == 'entrada':
            livro.estoque += quantidade
            messages.success(request, f'Foram adicionadas {quantidade} unidade(s) ao estoque de "{livro.titulo}".')
        else:
            livro.estoque -= quantidade
            messages.success(request, f'Foram retiradas {quantidade} unidade(s) do estoque de "{livro.titulo}".')
        livro.save()
        return redirect('gestao_estoque')

    livros = Livro.objects.order_by('titulo')
    context = {
        'form': form,
        'livros': livros,
        **_stats(),
    }
    return render(request, 'gestao_estoque.html', context)


@login_required
def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro cadastrado com sucesso.')
            return redirect('lista_livros')
    else:
        form = LivroForm()
    return render(request, 'form_livro.html', {'form': form, 'titulo_pagina': 'Cadastrar Livro', 'texto_botao': 'Salvar Livro'})


@login_required
def editar_livro(request, id):
    livro = get_object_or_404(Livro, id=id)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro atualizado com sucesso.')
            return redirect('lista_livros')
    else:
        form = LivroForm(instance=livro)
    return render(request, 'form_livro.html', {'form': form, 'titulo_pagina': 'Editar Livro', 'texto_botao': 'Salvar Alterações'})


@login_required
def excluir_livro(request, id):
    livro = get_object_or_404(Livro, id=id)
    if request.method == 'POST':
        livro.delete()
        messages.success(request, 'Livro excluído com sucesso.')
        return redirect('lista_livros')
    return render(request, 'confirmar_exclusao.html', {'livro': livro})
