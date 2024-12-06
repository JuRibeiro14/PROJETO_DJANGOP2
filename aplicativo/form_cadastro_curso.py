# forms.py
from django import forms
from aplicativo.models import Curso

class FormCadastroCurso(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('nome', 'autor', 'duracao', 'preco', 'fotoCurso', 'estoque')  # Adicionando 'estoque'
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Nome do Curso',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'
            }),
            'autor': forms.TextInput(attrs={
                'placeholder': 'Autor do Curso',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'
            }),
            'duracao': forms.NumberInput(attrs={
                'placeholder': 'Duração (horas)',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'
            }),
            'preco': forms.NumberInput(attrs={
                'placeholder': 'Preço',
                'step': '0.01',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'
            }),
            'estoque': forms.NumberInput(attrs={
                'placeholder': 'Quantidade em Estoque',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;',
                'min': 0,  
            }),
            'fotoCurso': forms.FileInput(attrs={'accept': 'image/*'}),
        }
