from django.db import models

class Apartment(models.Model):
    id_apartment = models.AutoField(primary_key=True)
    preco = models.FloatField()
    endereco = models.TextField(max_length=255)
    descricao = models.TextField(max_length=300)
    