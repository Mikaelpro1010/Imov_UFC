# Generated by Django 4.2.5 on 2023-10-08 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartments',
            fields=[
                ('id_apartment', models.AutoField(primary_key=True, serialize=False)),
                ('preco', models.FloatField()),
                ('endereco', models.TextField(max_length=255)),
                ('descricao', models.TextField(max_length=300)),
            ],
        ),
    ]
