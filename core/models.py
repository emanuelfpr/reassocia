from django.db import models


class Projeto(models.Model):
    CORES = [
        ("roxo", "Roxo"),
        ("verde", "Verde"),
        ("laranja", "Laranja"),
        ("azul", "Azul"),
        ("rosa", "Rosa"),
    ]

    nome = models.CharField(max_length=150)
    resumo = models.CharField(max_length=120, blank=True)
    descricao = models.TextField()
    objetivos = models.TextField(blank=True)
    publico_atendido = models.CharField(max_length=255, blank=True)
    acoes_realizadas = models.TextField(blank=True)
    cor = models.CharField(max_length=10, choices=CORES, default="roxo")
    destaque = models.BooleanField(default=True)       # aparece na página inicial
    na_consulta = models.BooleanField(default=False)   # aparece na página de consulta
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nome
