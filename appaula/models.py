from django.db import models
from django.utils import timezone

class Aluno(models.Model):
    nome = models.CharField('Nome Completo', max_length=100)
    matricula = models.CharField('Matrícula', max_length=20, unique=True)
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    
    def __str__(self):
        return f"{self.nome} ({self.matricula})"

class Grupo(models.Model):
    tema = models.ForeignKey('Tema', on_delete=models.CASCADE, null=True, blank=True)  # <-- ADICIONE ISSO
    nome = models.CharField('Nome do Grupo', max_length=50)
    data_apresentacao = models.CharField('Data (DD/MM/AAAA)', max_length=10, blank=True)
    hora_apresentacao = models.CharField('Hora (HH:MM)', max_length=5, blank=True)
    ordem_apresentacao = models.PositiveIntegerField('Ordem', null=True, blank=True)

    class Meta:
        ordering = ['ordem_apresentacao']

    def __str__(self):
        return f"{self.nome} - Ordem: {self.ordem_apresentacao}"

class MembroGrupo(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    lider = models.BooleanField('Líder', default=False)
    
    def __str__(self):
        return f"{self.aluno.nome} no {self.grupo.nome}"
        
class Tema(models.Model):
    titulo = models.CharField('Título do Tema', max_length=200)
    quantidade_grupos = models.PositiveIntegerField('Quantidade de Grupos')
    alunos_por_grupo = models.PositiveIntegerField('Alunos por Grupo')
    data_apresentacao = models.DateField('Data da Apresentação')
    horario_inicio = models.TimeField('Horário de Início')
    horario_fim = models.TimeField('Horário de Fim')

    def __str__(self):
        return self.titulo

