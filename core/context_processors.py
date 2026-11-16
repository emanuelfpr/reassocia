# Dados que ficam disponíveis em todas as páginas (rodapé)
from django.conf import settings


def dados_gerais(request):
    return {
        "endereco": settings.ENDERECO,
        "instagram": settings.INSTAGRAM,
        "facebook": settings.FACEBOOK,
    }
