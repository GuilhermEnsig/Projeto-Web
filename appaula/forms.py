from django import forms
from .models import Grupo, Aluno, Tema

class DateInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({
            'placeholder': 'DD/MM/AAAA',
            'pattern': r'\d{2}/\d{2}/\d{4}',
            'title': 'Formato: DD/MM/AAAA'
        })
        super().__init__(*args, **kwargs)

class TimeInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({
            'placeholder': 'HH:MM',
            'pattern': r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$',
            'title': 'Formato: HH:MM (24 horas)'
        })
        super().__init__(*args, **kwargs)

class AlocarAlunosForm(forms.Form):
    TAMANHO_GRUPO_CHOICES = [
        (2, '2 alunos'),
        (3, '3 alunos'),
        (4, '4 alunos'),
        (5, '5 alunos'),
    ]

    tamanho_grupo = forms.ChoiceField(
        label='Tamanho do Grupo',
        choices=TAMANHO_GRUPO_CHOICES,
        initial=4
    )

    data_apresentacao = forms.DateField(
    label='Data de Apresentação',
    input_formats=['%d/%m/%Y'], 
    widget=DateInput(),
    required=True
)

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nome', 'data_apresentacao', 'hora_apresentacao']
        widgets = {
            'data_apresentacao': DateInput(),
            'hora_apresentacao': TimeInput(),
        }

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'matricula']

class TemaForm(forms.ModelForm):
    data_apresentacao = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=DateInput(),
        required=True
    )

    class Meta:
        model = Tema
        fields = [
            'titulo',
            'quantidade_grupos',
            'alunos_por_grupo',
            'data_apresentacao',
            'horario_inicio',
            'horario_fim'
        ]
        widgets = {
            'horario_inicio': TimeInput(),
            'horario_fim': TimeInput(),
        }