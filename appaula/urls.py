from django.urls import path
from . import views

app_name = 'appaula'

urlpatterns = [
    path('', views.home, name='home'),
    path('alunos/', views.listar_alunos, name='listar_alunos'),
    path('alunos/novo/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('temas/', views.listar_temas, name='listar_temas'),
    path('temas/novo/', views.cadastrar_tema, name='cadastrar_tema'),
    path('grupos/', views.listar_grupos, name='listar_grupos'),
    path('grupos/criar/', views.criar_grupo_manual, name='criar_grupo'),
    path('alocar/', views.alocar_alunos, name='alocar_alunos'),
    path('sortear/', views.sortear_ordem, name='sortear_ordem'),
]
