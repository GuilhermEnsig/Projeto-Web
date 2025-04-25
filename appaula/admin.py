# appaula/admin.py
from django.contrib import admin
from .models import Aluno, Grupo 
# Registre os modelos que você tem
admin.site.register(Aluno)
admin.site.register(Grupo)