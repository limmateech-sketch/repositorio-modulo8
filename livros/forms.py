from django import forms
from .models import Livro


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'preco', 'categoria', 'isbn', 'estoque']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control afi-input', 'placeholder': 'Digite o título'}),
            'autor': forms.TextInput(attrs={'class': 'form-control afi-input', 'placeholder': 'Digite o autor'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control afi-input', 'step': '0.01', 'min': '0'}),
            'categoria': forms.Select(attrs={'class': 'form-select afi-input'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control afi-input', 'placeholder': 'Ex: 9780000000000'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-control afi-input', 'min': '0'}),
        }

    def clean_estoque(self):
        estoque = self.cleaned_data.get('estoque')
        if estoque is None:
            raise forms.ValidationError('Informe o estoque.')
        if estoque < 0:
            raise forms.ValidationError('O estoque não pode ser negativo.')
        return estoque


class MovimentoEstoqueForm(forms.Form):
    livro = forms.ModelChoiceField(
        queryset=Livro.objects.all().order_by('titulo'),
        empty_label='Selecione um livro',
        widget=forms.Select(attrs={'class': 'form-select afi-input'})
    )
    quantidade = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control afi-input', 'placeholder': 'Quantidade'})
    )
    operacao = forms.ChoiceField(
        choices=[('entrada', 'Adicionar ao estoque'), ('saida', 'Retirar do estoque')],
        widget=forms.RadioSelect(attrs={'class': 'afi-radio'})
    )

    def clean(self):
        cleaned_data = super().clean()
        livro = cleaned_data.get('livro')
        quantidade = cleaned_data.get('quantidade')
        operacao = cleaned_data.get('operacao')

        if livro and quantidade and operacao == 'saida' and quantidade > livro.estoque:
            raise forms.ValidationError('A quantidade de saída não pode ser maior que o estoque atual.')
        return cleaned_data
