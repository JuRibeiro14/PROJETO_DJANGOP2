from datetime import timedelta
from pyexpat.errors import messages
from django.http import HttpResponse
from django.template import loader
from aplicativo.form_cadastro_curso import FormCadastroCurso
from aplicativo.form_cadastro_user import FormCadastroUser
from aplicativo.form_login import FormLogin
from aplicativo.models import Curso, Usuario, Foto, Venda, Curso
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from aplicativo.form_upload import FormFoto
from aplicativo.form_upload import Foto
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from django.utils import timezone
import base64, urllib, io
from matplotlib import pyplot as plt
from datetime import datetime
from django.utils.timezone import now


def index(request):
    return render(request, 'index.html')


def cadastrar_user(request):
    novo_user = FormCadastroUser(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if novo_user.is_valid():
            email = novo_user.cleaned_data['email']

            if Usuario.objects.filter(email=email).exists():
                messages.error(request, "E-mail já está sendo utilizado!")
            else:
                usuario = novo_user.save(commit=False)
                usuario.senha = make_password(novo_user.cleaned_data['senha'])  
                usuario.save() 
                messages.success(request, "Usuário cadastrado com sucesso!")
                return redirect('index')
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")

    context = {
        'form': novo_user
    }
    return render(request, 'cadastro.html', context)
 
 
def exibir_user(request):
    users = Usuario.objects.all()  
    return render(request, 'usuarios.html', {'users': users})
 
 
def cadastrar_curso(request):
    novo_curso = FormCadastroCurso(request.POST or None, request.FILES or None)  

    if request.method == 'POST':  
        if novo_curso.is_valid():  
            novo_curso.save()  
            messages.success(request, 'Curso cadastrado com sucesso!')
            return redirect('index') 
        else:
            messages.error(request, 'Erro ao cadastrar o curso. Verifique os dados e tente novamente.')

    context = {
        'form': novo_curso
    }
    return render(request, 'cadastro_curso.html', context)
 
 
def exibir_curso(request):
    cursos1 = Curso.objects.all()  
    return render(request, 'cursos.html', {'cursos1': cursos1})
 
 
def fazer_login(request):
    formLogin = FormLogin(request.POST or None)
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(senha, usuario.senha):
                request.session.set_expiry(timedelta(seconds=60))
                request.session['email'] = email
                return redirect('dashboard')
            else:
                messages.error(request, "Senha incorreta.")
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
    context = {
        'form': formLogin
    }
    return render(request, 'login.html', context)
 
 
def dashboard(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, "Você precisa estar logado para acessar o dashboard!")
        return redirect('index')
    usuario = Usuario.objects.get(email=email)
    
    context = {
        'usuario': usuario  
    }
    return render(request, 'dashboard.html', context)
 
 
def editar_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, id=id_usuario)
    form = FormCadastroUser(request.POST or None, instance=usuario)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('exibir_user')
    context = {'form': form}
    return render(request, 'editar_usuario.html', context)
 
 
def excluir_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, id=id_usuario)
    usuario.delete()
    logout(request)
    return redirect('index')
 

def redefinir_senha(request):
    if request.method == 'POST':
        senha_atual = request.POST['senha_atual']
        nova_senha = request.POST['nova_senha']
        confirmacao_senha = request.POST['confirmacao_senha']

        email = request.session.get('email')
        usuario = Usuario.objects.get(email=email)

        if check_password(senha_atual, usuario.senha):
            if nova_senha == confirmacao_senha:
                if nova_senha != senha_atual:
                    usuario.senha = make_password(nova_senha)
                    usuario.save()

                    update_session_auth_hash(request, usuario)

                    messages.success(request, 'Senha alterada com sucesso.')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'A nova senha não pode ser igual à senha atual.')
            else:
                messages.error(request, 'A nova senha e a confirmação não coincidem.')
        else:
            messages.error(request, 'Senha atual incorreta.')

    return render(request, 'redefinir_senha.html')


def add_foto(request):
    if request.method == 'POST':
        form = FormFoto(request.POST, request.FILES)  
        if form.is_valid():
            form.save()  
            return redirect('galeria')  
    else:
        form = FormFoto()
    return render(request, 'add_foto.html', {'form': form})


def galeria(request):
    fotos = Foto.objects.all().values()

    context = {
        'galeria':fotos
    } 
    return render(request, 'galeria.html', context)
 
 
def excluir_foto(request, foto_id):
    foto = get_object_or_404(Foto, id=foto_id)  
    foto.delete()  
    return redirect('galeria')


def contato(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')

        messages.success(request, 'Mensagem enviada com sucesso! Entraremos em contato em breve.')
        
    return render(request, 'contato.html')  


def realizar_venda(request, id_curso):
    email = request.session.get('email')
    if not email:
        messages.error(request, "Você precisa estar logado para realizar uma compra!")
        return redirect('login')  
    curso = get_object_or_404(Curso, id=id_curso)

    try:
        curso.reduzir_estoque()

        Venda.objects.create(
            id_curso=curso.id, 
            nome_curso=curso.nome, 
            valor_total=curso.preco * 1  
        )

        messages.success(request, "Compra realizada com sucesso!")
        return redirect('exibir_curso')  
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('exibir_curso')


def relatorio_vendas(request):
    hoje = timezone.now()
    mes_atual = hoje.month
    ano_atual = hoje.year
 
    vendas_gerais = Venda.objects.filter(data_venda__month=mes_atual, data_venda__year=ano_atual).values('data_venda__month').annotate(total_vendas=Count('id'))
 
    meses = [venda['data_venda__month'] for venda in vendas_gerais]
    total_vendas = [venda['total_vendas'] for venda in vendas_gerais]
 
    fig_gerais, ax_gerais = plt.subplots()
    ax_gerais.bar(meses, total_vendas, label="Vendas Totais", color='blue')
    ax_gerais.set_title("Vendas Gerais Mensais")
    ax_gerais.set_xlabel("Mês")
    ax_gerais.set_ylabel("Quantidade de Vendas")
    ax_gerais.set_xticks(range(1, 13))  
    ax_gerais.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax_gerais.legend()
 
    buf_gerais = io.BytesIO()
    fig_gerais.savefig(buf_gerais, format='png')
    buf_gerais.seek(0)
    img_gerais = base64.b64encode(buf_gerais.getvalue()).decode('utf-8')
 
    vendas_por_curso = Venda.objects.filter(data_venda__month=mes_atual, data_venda__year=ano_atual).values('nome_curso').annotate(total_vendas=Count('id'))
 
    cursos = [venda['nome_curso'] for venda in vendas_por_curso]
    vendas_por_curso_vals = [venda['total_vendas'] for venda in vendas_por_curso]
 
    fig_curso, ax_curso = plt.subplots()
    ax_curso.bar(cursos, vendas_por_curso_vals, color='green')
    ax_curso.set_title("Vendas por Curso")
    ax_curso.set_xlabel("Curso")
    ax_curso.set_ylabel("Quantidade de Vendas")
 
    buf_curso = io.BytesIO()
    fig_curso.savefig(buf_curso, format='png')
    buf_curso.seek(0)
    img_curso = base64.b64encode(buf_curso.getvalue()).decode('utf-8')
 
    context = {
        'vendas_gerais': vendas_gerais,
        'vendas_por_curso': vendas_por_curso,
        'img_gerais': img_gerais,
        'img_curso': img_curso,
    }
    return render(request, 'relatorio_vendas.html', context)