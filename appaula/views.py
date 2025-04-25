import random
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Aluno, Grupo, MembroGrupo, Tema  # Adicionei Tema aqui
from .forms import AlocarAlunosForm, GrupoForm

def home(request):
    """Página inicial do sistema"""
    return render(request, 'appaula/home.html')

def listar_alunos(request):
    """Listagem de todos os alunos"""
    alunos = Aluno.objects.all()
    return render(request, 'appaula/listar_alunos.html', {'alunos': alunos})

def listar_temas(request):
    """Listagem de todos os temas (se estiver usando)"""
    temas = Tema.objects.all() if hasattr(Tema, 'objects') else []
    return render(request, 'appaula/listar_temas.html', {'temas': temas})

def alocar_alunos(request):
    """Alocação automática de alunos em grupos"""
    if request.method == 'POST':
        form = AlocarAlunosForm(request.POST)
        if form.is_valid():
            # Limpar grupos existentes
            Grupo.objects.all().delete()
            
            # Obter alunos e embaralhar
            alunos = list(Aluno.objects.all())
            random.shuffle(alunos)
            
            tamanho_grupo = int(form.cleaned_data['tamanho_grupo'])
            data_apresentacao = form.cleaned_data['data_apresentacao']
            
            # Criar grupos
            for i in range(0, len(alunos), tamanho_grupo):
                grupo_alunos = alunos[i:i + tamanho_grupo]
                grupo = Grupo.objects.create(
                    nome=f"Grupo {i//tamanho_grupo + 1}",
                    data_apresentacao=data_apresentacao
                )
                
                # Adicionar alunos ao grupo
                for j, aluno in enumerate(grupo_alunos):
                    MembroGrupo.objects.create(
                        aluno=aluno,
                        grupo=grupo,
                        lider=(j == 0)  # Primeiro aluno é o líder
                    )
            
            messages.success(request, 'Alunos alocados em grupos com sucesso!')
            return redirect('appaula:sortear_ordem')
    else:
        form = AlocarAlunosForm()
    
    return render(request, 'appaula/alocar_alunos.html', {'form': form})

def sortear_ordem(request):
    """Sorteio da ordem de apresentação"""
    grupos = Grupo.objects.all()
    
    if request.method == 'POST':
        # Embaralhar a ordem de apresentação
        grupos_list = list(grupos)
        random.shuffle(grupos_list)
        
        for ordem, grupo in enumerate(grupos_list, start=1):
            grupo.ordem_apresentacao = ordem
            grupo.save()
        
        messages.success(request, 'Ordem de apresentação sorteada com sucesso!')
        return redirect('appaula:listar_grupos')
    
    return render(request, 'appaula/sortear_ordem.html', {'grupos': grupos})

def listar_grupos(request):
    """Listagem de todos os grupos"""
    grupos = Grupo.objects.all().order_by('ordem_apresentacao')
    return render(request, 'appaula/listar_grupos.html', {'grupos': grupos})

def criar_grupo_manual(request):
    """Criação manual de grupos"""
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo criado com sucesso!')
            return redirect('appaula:listar_grupos')
    else:
        form = GrupoForm()
    
    return render(request, 'appaula/criar_grupo.html', {'form': form})

def cadastrar_aluno(request):
    """Cadastro de novo aluno"""
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno cadastrado com sucesso!')
            return redirect('listar_alunos')
    else:
        form = AlunoForm()
    
    return render(request, 'appaula/form.html', {'form': form})


def cadastrar_tema(request):
    """Cadastro de novo tema"""
    if request.method == 'POST':
        form = TemaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tema cadastrado com sucesso!')
            return redirect('listar_temas')
    else:
        form = TemaForm()
    
    return render(request, 'appaula/form.html', {'form': form})

    