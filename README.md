# Reassocia ONG – Site do Projeto de Extensão

Site institucional da **Reassocia**, ONG de Jardim Catarina, São Gonçalo (RJ), com o lema **Acolher • Capacitar • Transformar**.

Divulga os cursos e as ações de saúde, permite agendar consultas e iniciar doações pelo WhatsApp e tem uma área administrativa (com **login**) para cadastrar e editar projetos.

## Funcionalidades

**Visitante**
- Página inicial com projetos em destaque e busca (nome, resumo ou descrição)
- Detalhes de cada projeto (descrição, objetivos, público atendido, ações realizadas)
- Consulta (agendamento pelo WhatsApp), Contato (endereço, WhatsApp, Instagram, doação) e Sobre

**Administrador (precisa estar logado)**
- Login e logout
- Listagem, cadastro e edição de projetos (cor do card, aparece no início e/ou na consulta)

## Tecnologias

Python, Django, MySQL (driver PyMySQL), HTML, CSS, JavaScript, Git e GitHub.

## Estrutura

```
reassocia_site/
├── manage.py
├── criar_banco.sql          # cria o banco "reassocia"
├── requirements.txt
├── reassocia_site/          # configurações do projeto
│   ├── settings.py
│   └── urls.py
├── core/                    # app principal
│   ├── models.py            # tabela Projeto
│   ├── forms.py             # formulário de projeto
│   ├── views.py             # páginas, login e administração
│   ├── urls.py
│   └── fixtures/projetos_iniciais.json
├── templates/               # páginas HTML (templates do Django)
└── static/                  # css e js
```

## Como executar

1. (Opcional) crie e ative um ambiente virtual: `py -m venv venv` e `venv\Scripts\activate`
2. Instale as dependências: `pip install -r requirements.txt`
3. Crie o banco: `mysql -u root -p < criar_banco.sql`
4. Confira usuário e senha do MySQL em `reassocia_site/settings.py` (`DATABASES`)
5. Crie as tabelas: `py manage.py migrate`
6. Carregue os projetos iniciais: `py manage.py loaddata projetos_iniciais`
7. Crie o usuário da administração: `py manage.py createsuperuser`
8. Rode o servidor: `py manage.py runserver`
9. Abra **http://127.0.0.1:8000**

## Publicar na internet

Veja o passo a passo no arquivo [DEPLOY.md](DEPLOY.md).

## Rotas

| Rota | Descrição | Login |
|---|---|---|
| `/` | Início e busca (`/?q=termo`) | não |
| `/projetos/<id>/` | Detalhes do projeto | não |
| `/consulta/`, `/contato/`, `/sobre/` | Páginas informativas | não |
| `/login/`, `/logout/` | Entrar e sair | não |
| `/admin/projetos/` | Lista de projetos | sim |
| `/admin/projetos/novo/` | Cadastro | sim |
| `/admin/projetos/<id>/editar/` | Edição | sim |

## Segurança

- O ORM do Django usa consultas parametrizadas (contra SQL Injection)
- Os templates escapam o texto automaticamente (contra XSS)
- Formulários protegidos com token CSRF
- Senhas guardadas com hash pelo sistema de autenticação do Django
- Páginas de administração protegidas com `@login_required`

## Licença

Distribuído sob a licença do arquivo [LICENSE](LICENSE).
