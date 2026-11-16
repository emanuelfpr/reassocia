# Configurações do projeto Reassocia
import os
from pathlib import Path

from django.contrib.messages import constants as tipos_mensagem
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Os valores abaixo vêm de variáveis de ambiente (usadas na hospedagem).
# No seu computador, sem configurar nada, valem os valores padrão.
CHAVE_PADRAO = "chave-so-para-desenvolvimento"
SECRET_KEY = os.environ.get("SECRET_KEY", CHAVE_PADRAO)
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = [h for h in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h]
CSRF_TRUSTED_ORIGINS = [o for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if o]

# O Render informa o endereço do site nesta variável
HOST_RENDER = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if HOST_RENDER:
    ALLOWED_HOSTS.append(HOST_RENDER)
    CSRF_TRUSTED_ORIGINS.append("https://" + HOST_RENDER)

# O Azure informa o endereço do site nesta variável
HOST_AZURE = os.environ.get("WEBSITE_HOSTNAME")
if HOST_AZURE:
    ALLOWED_HOSTS.append(HOST_AZURE)
    CSRF_TRUSTED_ORIGINS.append("https://" + HOST_AZURE)

# Na hospedagem o site fica atrás de um proxy HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if not DEBUG and SECRET_KEY == CHAVE_PADRAO:
    raise ImproperlyConfigured("Defina a variável de ambiente SECRET_KEY antes de publicar o site.")

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # entrega o CSS/JS na hospedagem
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "reassocia_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.dados_gerais",
            ],
        },
    },
]

WSGI_APPLICATION = "reassocia_site.wsgi.application"

# Banco de dados: MySQL (padrão). Na hospedagem grátis sem MySQL, use DB_ENGINE=sqlite.
# Crie o banco antes no MySQL: veja criar_banco.sql
DB_ENGINE = os.environ.get(
    "DB_ENGINE",
    "sqlite" if os.environ.get("RENDER") or os.environ.get("RENDER_EXTERNAL_HOSTNAME") else "mysql",
)

if DB_ENGINE == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("MYSQLDATABASE", "reassocia"),
            "USER": os.environ.get("MYSQLUSER", "admin"),
            "PASSWORD": os.environ.get("MYSQLPASSWORD", "admin@123"),
            "HOST": os.environ.get("MYSQLHOST", "localhost"),
            "PORT": os.environ.get("MYSQLPORT", "3306"),
            "OPTIONS": {"charset": "utf8mb4"},
        }
    }
    # Alguns serviços (como o Azure) exigem SSL: informe o caminho do certificado
    if os.environ.get("DB_SSL_CA"):
        DATABASES["default"]["OPTIONS"]["ssl"] = {"ca": os.environ["DB_SSL_CA"]}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # pasta criada pelo collectstatic

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login
LOGIN_URL = "login"

# As mensagens usam as classes "ok" e "erro" do CSS
MESSAGE_TAGS = {
    tipos_mensagem.SUCCESS: "ok",
    tipos_mensagem.ERROR: "erro",
}

# Dados da ONG (WhatsApp com DDI + DDD, só números: troque pelo número real)
WHATSAPP = "5521999999999"
INSTAGRAM = "https://www.instagram.com/"
FACEBOOK = "https://www.facebook.com/"
ENDERECO = "ONG Reassocia, Lote 02, Quadra 35, R. Américo Miranda, S/N - Jardim Catarina, São Gonçalo - RJ, 24716-455"
