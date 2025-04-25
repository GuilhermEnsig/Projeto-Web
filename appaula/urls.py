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
    path('alunos/<int:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('alunos/<int:aluno_id>/excluir/', views.excluir_aluno, name='excluir_aluno'),
    path('temas/editar/<int:tema_id>/', views.editar_tema, name='editar_tema'),
    path('temas/excluir/<int:tema_id>/', views.excluir_tema, name='excluir_tema'),
    path('temas/<int:tema_id>/executar_grupos/', views.executar_grupos, name='executar_grupos'),
    path('grupos/<int:grupo_id>/editar/', views.editar_grupo, name='editar_grupo'),
    path('grupos/<int:grupo_id>/excluir/', views.excluir_grupo, name='excluir_grupo'),
    path('grupos/', views.listar_grupos, name='listar_grupos'),
    path('grupo/<int:grupo_id>/completar/', views.completar_grupo, name='completar_grupo'),
]
