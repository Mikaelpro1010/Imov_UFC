from django.shortcuts import redirect, render
from django.http.response import HttpResponse
from .models import Apartment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import  login as login_django
from django.contrib.auth.decorators import  login_required

#criando metodo para o usuário poder realizar login no sistema
def login(request):
    if request.method == "GET":
        return render(request, 'auth/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            #metodo login para realizar login do usuário
            login_django(request, user)

            return redirect('home')
        else:
            return HttpResponse('Usuário ou senha inválidos!')

#criando metodo para cadastrar o usuário no sistema
def registerUser(request):
    if request.method == "GET":
        return render(request, 'auth/register_user.html')
    
    else:
        #guarda os dados que estão vindo da requisição POST
        username = request.POST.get('username')
        email = request.POST.get('email')
        # number = request.POST.get('number')
        password = request.POST.get('password')
        # confirm_password = request.POST.get('confirm_password')

        #busca no banco de dados um nome de usuário semelhante ao que está sendo cadastrado
        user = User.objects.filter(username=username).first()

        #condição que verifica se o usuário já existe no banco de dados
        if user:
            return HttpResponse('Usuário já existente!')
        else:
            #caso não exista, o mesmo é cadastrado no banco de dados
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            
            return redirect('login')

#usando o metodo login_required() para verificar se o usuário tem permissão para acessar a página
@login_required(login_url='/auth/login/')
def home(request):
    return render(request, 'home.html')


#usando o metodo login_required() para verificar se o usuário tem permissão para acessar a página
@login_required(login_url='/login')
def registerApartment(request):
    if request.method == "GET":
        return render(request, 'register_apartment.html')
    
    else:
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

    #Retornar os dados para a página de listagem de apartamentos
    return render(request, 'apartments.html', apartments)