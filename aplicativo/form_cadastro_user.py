from django import forms
from aplicativo.models import Usuario, Foto

class FormCadastroUser(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome', 'email', 'senha', 'foto')
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Nome do Usuário',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'  
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email do Usuário',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'
            }),
            'senha': forms.PasswordInput(attrs={
                'placeholder': 'Senha do Usuário',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'
            }),
            'foto':forms.FileInput(attrs={
                'accept':'image/*',
                'class': 'form-control-file', 
                'style': 'margin-bottom: 10px;'                         
            }),
        }

        error_messages = {
            'email': {
                'required': "Por favor, insira um e-mail.",
                'unique': "Já existe um usuário com este e-mail.", 
            },
            'senha': {
                'required': "Por favor, insira uma senha.",
            },
        }
