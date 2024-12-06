from django import forms
from aplicativo.models import Foto

class FormFoto(forms.ModelForm):
    class Meta:
        model = Foto
        fields = ['nome', 'foto']
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Nome da Foto',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;',
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*',
            }),
        }
