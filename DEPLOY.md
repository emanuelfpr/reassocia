# Como colocar o site no ar

O projeto já está preparado para hospedagem: configurações lidas de variáveis de ambiente, WhiteNoise para o CSS/JS, gunicorn e as migrações incluídas.

Antes de tudo, gere uma chave secreta (guarde o resultado, é o `SECRET_KEY`):

```
py -c "import secrets; print(secrets.token_urlsafe(50))"
```

Suba o projeto para o GitHub (a pasta `venv` e o `db.sqlite3` já estão no `.gitignore`).

## Variáveis de ambiente que o site usa

| Variável | Para quê | Exemplo |
|---|---|---|
| `SECRET_KEY` | Chave secreta (obrigatória quando `DEBUG=False`) | a chave gerada acima |
| `DEBUG` | Use `False` na hospedagem | `False` |
| `ALLOWED_HOSTS` | Endereço do site | `usuario.pythonanywhere.com` |
| `CSRF_TRUSTED_ORIGINS` | Endereço do site com https | `https://usuario.pythonanywhere.com` |
| `DB_ENGINE` | `sqlite` para usar SQLite (sem MySQL) | `sqlite` |
| `MYSQLHOST`, `MYSQLPORT`, `MYSQLUSER`, `MYSQLPASSWORD`, `MYSQLDATABASE` | Dados do MySQL | do seu servidor MySQL |
| `DB_SSL_CA` | Caminho do certificado SSL do MySQL (Azure) | `/home/site/wwwroot/DigiCertGlobalRootG2.crt.pem` |

---

## Opção 0: Render (grátis, sem cartão)

O projeto já tem o `render.yaml`, o `build.sh` e o `start.sh` prontos.

1. Suba o projeto para o GitHub. A pasta `reassocia_site` precisa ser a raiz do repositório (onde ficam o `manage.py` e o `render.yaml`).
2. Crie a conta em render.com (pode entrar com o GitHub).
3. Clique em **New** e depois em **Blueprint**, escolha o repositório e confirme.
4. Quando ele pedir, informe `DJANGO_SUPERUSER_PASSWORD`: é a senha do login da administração (o usuário é `admin`).
5. Aguarde o deploy. O endereço aparece no topo do serviço, algo como `reassocia.onrender.com`.

Limites do plano grátis (confira na página de preços do Render antes):
- O site **dorme após 15 minutos sem acesso**, e o primeiro acesso depois disso demora cerca de 1 minuto.
- O disco é temporário: o SQLite volta ao estado inicial cada vez que o site liga. Projetos cadastrados na administração **somem** quando ele dorme. Serve para demonstrar, não para uso real.
- Para manter os dados, é preciso um banco externo (o Postgres grátis do Render expira em 30 dias).

---

## Opção 1: PythonAnywhere (grátis, com SQLite)

1. Crie a conta em pythonanywhere.com (o site ficará em `SEUUSUARIO.pythonanywhere.com`).
2. Abra um console **Bash** e rode (troque `SEUUSUARIO` e `SEUREPO`):
   ```bash
   git clone https://github.com/SEUUSUARIO/SEUREPO.git
   cd SEUREPO/reassocia_site
   mkvirtualenv venv --python=python3.13
   pip install -r requirements.txt
   ```
   Se o `python3.13` não existir, use a versão mais nova que aparecer.
3. Ainda no console, defina as variáveis só para estes comandos e prepare o banco:
   ```bash
   export DB_ENGINE=sqlite DEBUG=False SECRET_KEY="COLE_A_CHAVE" ALLOWED_HOSTS=SEUUSUARIO.pythonanywhere.com
   python manage.py migrate
   python manage.py loaddata projetos_iniciais
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```
4. Na aba **Web**: **Add a new web app**, **Manual configuration**, mesma versão de Python.
   - **Source code** e **Working directory**: `/home/SEUUSUARIO/SEUREPO/reassocia_site`
   - **Virtualenv**: `/home/SEUUSUARIO/.virtualenvs/venv`
   - **Static files**: URL `/static/` apontando para `/home/SEUUSUARIO/SEUREPO/reassocia_site/staticfiles`
5. Abra o arquivo WSGI (link na própria aba), apague tudo e deixe:
   ```python
   import os
   import sys

   caminho = "/home/SEUUSUARIO/SEUREPO/reassocia_site"
   if caminho not in sys.path:
       sys.path.append(caminho)

   os.environ["DB_ENGINE"] = "sqlite"
   os.environ["DEBUG"] = "False"
   os.environ["SECRET_KEY"] = "COLE_A_CHAVE"
   os.environ["ALLOWED_HOSTS"] = "SEUUSUARIO.pythonanywhere.com"
   os.environ["CSRF_TRUSTED_ORIGINS"] = "https://SEUUSUARIO.pythonanywhere.com"
   os.environ["DJANGO_SETTINGS_MODULE"] = "reassocia_site.settings"

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
6. Clique em **Reload** e abra o endereço.

Atualizar depois: `git pull` no console, `python manage.py collectstatic --noinput` se mexeu em CSS/JS, e **Reload**.
Na conta grátis, estenda o app na aba **Web** todo mês, senão ele expira.

---

## Opção 2: Azure for Students (MySQL de verdade)

1. **Região:** no portal, abra **Policy > Assignments > Allowed resource deployment regions** e anote as regiões liberadas para a sua conta. Use a mesma região para tudo.
2. **GitHub:** o `manage.py` e o `requirements.txt` precisam estar na raiz do repositório.
3. **MySQL:** crie **Azure Database for MySQL – Flexible Server** (Burstable, o menor; acesso público; marque permitir acesso de serviços do Azure). Em **Server parameters**, coloque `require_secure_transport` em `OFF`. Em **Databases**, crie `reassocia`.
4. **App Service:** crie um Web App (Linux, Python 3.13, plano mais barato). Em **Deployment Center**, conecte o repositório.
5. **Environment variables** do Web App: `SCM_DO_BUILD_DURING_DEPLOYMENT=1`, `SECRET_KEY`, `DEBUG=False`, `MYSQLHOST`, `MYSQLPORT=3306`, `MYSQLUSER`, `MYSQLPASSWORD`, `MYSQLDATABASE=reassocia`. (O endereço do site o projeto descobre sozinho.)
6. **Startup Command:** `python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn --bind=0.0.0.0 --timeout 600 reassocia_site.wsgi`
7. No **SSH** do Web App (uma vez só): `python manage.py loaddata projetos_iniciais` e `python manage.py createsuperuser`.

---

## Problemas comuns

- **Erro 500:** veja o **Error log** (PythonAnywhere) ou o **Log stream** (Azure). Costuma ser variável de ambiente faltando.
- **Site sem CSS:** falta rodar `collectstatic` ou mapear `/static/` (PythonAnywhere).
- **"CSRF verification failed" no login:** confira `CSRF_TRUSTED_ORIGINS` (com `https://`).
- **"Invalid HTTP_HOST":** confira `ALLOWED_HOSTS`.
- Troque o WhatsApp de exemplo (`5521999999999`) em `settings.py` antes de divulgar o link.
