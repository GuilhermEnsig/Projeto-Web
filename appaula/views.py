import random
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Aluno, Grupo, MembroGrupo, Tema  # Adicionei Tema aqui
from .forms import AlocarAlunosForm, GrupoForm, AlunoForm, TemaForm
from datetime import datetime, timedelta
from .models import Grupo
import random

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
            return redirect('appaula:listar_alunos')
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
            return redirect('appaula:listar_temas')
    else:
        form = TemaForm()
    
    return render(request, 'appaula/form.html', {'form': form})

def editar_aluno(request, aluno_id):
    aluno = Aluno.objects.get(id=aluno_id)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno atualizado com sucesso!')
            return redirect('appaula:listar_alunos')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'appaula/form.html', {'form': form})

def excluir_aluno(request, aluno_id):
    aluno = Aluno.objects.get(id=aluno_id)
    aluno.delete()
    messages.success(request, 'Aluno excluído com sucesso!')
    return redirect('appaula:listar_alunos')

def editar_tema(request, tema_id):
    tema = Tema.objects.get(id=tema_id)
    if request.method == 'POST':
        form = TemaForm(request.POST, instance=tema)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tema atualizado com sucesso!')
            return redirect('appaula:listar_temas')
    else:
        form = TemaForm(instance=tema)
    return render(request, 'appaula/form.html', {'form': form})

def excluir_tema(request, tema_id):
    tema = Tema.objects.get(id=tema_id)
    tema.delete()
    messages.success(request, 'Tema excluído com sucesso!')
    return redirect('appaula:listar_temas')

def executar_grupos(request, tema_id):
    tema = get_object_or_404(Tema, id=tema_id)

    alunos = list(Aluno.objects.exclude(membrogrupo__isnull=False))
    random.shuffle(alunos)

    MembroGrupo.objects.filter(grupo__tema=tema).delete()
    Grupo.objects.filter(tema=tema).delete()

    grupos = []
    for i in range(1, tema.quantidade_grupos + 1):
        grupo = Grupo.objects.create(nome=f"Grupo {i}", tema=tema)
        grupos.append(grupo)

    # Distribuição dos alunos com limite por grupo
    grupo_index = 0
    for aluno in alunos:
        while grupo_index < len(grupos) and MembroGrupo.objects.filter(grupo=grupos[grupo_index]).count() >= tema.alunos_por_grupo:
            grupo_index += 1

        if grupo_index < len(grupos):
            MembroGrupo.objects.create(aluno=aluno, grupo=grupos[grupo_index])
        else:
            break  # Todos os grupos estão cheios

    # Sorteio e definição de horários
    random.shuffle(grupos)
    tempo_total = (
        datetime.combine(datetime.today(), tema.horario_fim) -
        datetime.combine(datetime.today(), tema.horario_inicio)
    ).seconds // 60
    tempo_por_grupo = max(15, tempo_total // tema.quantidade_grupos)
    horario_atual = datetime.combine(datetime.today(), tema.horario_inicio)

    for ordem, grupo in enumerate(grupos, start=1):
        grupo.ordem_apresentacao = ordem
        grupo.data_apresentacao = tema.data_apresentacao.strftime('%d/%m/%Y')
        grupo.hora_apresentacao = horario_atual.strftime('%H:%M')
        grupo.save()
        horario_atual += timedelta(minutes=tempo_por_grupo)

    messages.success(request, 'Grupos gerados com sucesso!')
    return redirect('appaula:listar_temas')

def editar_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    if request.method == 'POST':
        grupo.nome = request.POST.get('nome')
        grupo.save()
        messages.success(request, 'Grupo atualizado com sucesso!')
        return redirect('appaula:listar_grupos')
    return render(request, 'appaula/form_grupo.html', {'grupo': grupo})

def excluir_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    grupo.delete()
    messages.success(request, 'Grupo excluído com sucesso!')
    return redirect('appaula:listar_grupos')

def editar_membros_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    membros = MembroGrupo.objects.filter(grupo=grupo)
    alunos_disponiveis = Aluno.objects.exclude(membrogrupo__isnull=False)

    if request.method == 'POST':
        # Remove membros selecionados
        remover_ids = request.POST.getlist('remover')
        MembroGrupo.objects.filter(id__in=remover_ids).delete()

        # Adiciona novos alunos selecionados
        adicionar_ids = request.POST.getlist('adicionar')
        for aluno_id in adicionar_ids:
            if MembroGrupo.objects.filter(grupo=grupo).count() < grupo.tema.alunos_por_grupo:
                aluno = Aluno.objects.get(id=aluno_id)
                MembroGrupo.objects.create(aluno=aluno, grupo=grupo)

        messages.success(request, 'Membros atualizados com sucesso!')
        return redirect('appaula:listar_grupos')

    return render(request, 'appaula/editar_membros_grupo.html', {
        'grupo': grupo,
        'membros': membros,
        'alunos_disponiveis': alunos_disponiveis
    })
    
def completar_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    tema = grupo.tema
    alunos_disponiveis = Aluno.objects.exclude(membrogrupo__isnull=False)
    qtd_faltando = tema.alunos_por_grupo - grupo.membrogrupo_set.count()

    for aluno in alunos_disponiveis[:qtd_faltando]:
        MembroGrupo.objects.create(aluno=aluno, grupo=grupo)

    messages.success(request, 'Grupo completado automaticamente.')
    return redirect('appaula:listar_grupos')