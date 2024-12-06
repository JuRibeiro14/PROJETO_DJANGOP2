from django.db import models

# Create your models here.

class Usuario(models.Model):
    nome = models.CharField(max_length = 255)
    email = models.EmailField(unique = True)
    senha = models.CharField(max_length = 100)
    foto = models.ImageField(upload_to='fotos/', null=True, blank=True)
    
def __str__(self):
        return self.nome
    
class Curso(models.Model):
    nome = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    duracao = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    fotoCurso = models.ImageField(upload_to='fotos/', null=True, blank=True)
    estoque = models.PositiveIntegerField(default=0)  # Defina o estoque com valor padrão (0)

    def reduzir_estoque(self):
        if self.estoque >= 1:
            self.estoque -= 1
            self.save()
        else:
            raise ValueError("Estoque insuficiente")
class Login(models.Model):
    usuario = models.CharField(max_length=255)
    email = models.EmailField()
    senha = models.CharField(max_length=16)

class Foto(models.Model):
    nome = models.CharField(max_length = 255)
    foto = models.ImageField(upload_to = 'imagens/')

class Galeria(models.Model):
    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='galeria/')

class Venda(models.Model):
    id_curso = models.IntegerField() 
    nome_curso = models.CharField(max_length=255)  
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)  
    data_venda = models.DateTimeField(auto_now_add=True)