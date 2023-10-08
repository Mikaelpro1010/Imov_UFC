from django.shortcuts import render
from .models import Apartment

def home(request):
    return render(request, 'home.html')

def view_register_apartment(request):
    return render(request, 'register_apartment.html')

def register_apartment(request):
    #Salvar os dados da tela no banco de dados
    new_apartment = Apartment()
    new_apartment.endereco = request.POST.get('endereco')
    new_apartment.preco = request.POST.get('preco')
    new_apartment.descricao = request.POST.get('descricao')
    new_apartment.save()

    #exibir todos os apartamentos cadastrados em uma nova página
    apartments = {
        'apartments' : Apartment.objects.all()
    }

    #Reetornar os dados para a página de listagem de apartamentos
    return render(request, 'apartments.html', apartments)