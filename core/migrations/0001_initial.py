from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Projeto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=150)),
                ("resumo", models.CharField(blank=True, max_length=120)),
                ("descricao", models.TextField()),
                ("objetivos", models.TextField(blank=True)),
                ("publico_atendido", models.CharField(blank=True, max_length=255)),
                ("acoes_realizadas", models.TextField(blank=True)),
                ("cor", models.CharField(choices=[("roxo", "Roxo"), ("verde", "Verde"), ("laranja", "Laranja"), ("azul", "Azul"), ("rosa", "Rosa")], default="roxo", max_length=10)),
                ("destaque", models.BooleanField(default=True)),
                ("na_consulta", models.BooleanField(default=False)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["id"],
            },
        ),
    ]
