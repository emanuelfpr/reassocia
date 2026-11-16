from django import forms

from .models import Projeto


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ["nome", "resumo", "descricao", "objetivos", "publico_atendido",
                  "acoes_realizadas", "cor", "destaque", "na_consulta"]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 3}),
            "objetivos": forms.Textarea(attrs={"rows": 3}),
            "acoes_realizadas": forms.Textarea(attrs={"rows": 3}),
        }
