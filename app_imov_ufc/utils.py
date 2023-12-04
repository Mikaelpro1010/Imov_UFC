# app_imov_ufc/utils.py

import numpy as np
import scipy  # Adicione esta linha
from scipy import stats

def calculate_similarity(matrix, novoUsuario):
    #Lista para armazenar semelhanças
    similarities = []

    #Loop pela matriz
    for i in range(len(matrix)):
        temp = matrix[i, :]

        #Obtenha elementos de linha temporários diferentes de zero e elementos novoUsuario correspondentes diferentes de zero
        tempUsuario = [t for n, t in zip(novoUsuario, temp) if n != 0]
        tempNovoUsuario = [n for n in novoUsuario if n != 0]
        
        #Calcular similaridade
        similarity = scipy.stats.pearsonr(tempUsuario, tempNovoUsuario)[0]
        
        #Anexar similaridade à lista
        similarities.append(similarity)

    #Retorna lista de similaridades
    return similarities

def calculate_final_ratings(matrix, nao_curtidos, similarity):
    # Calculate nota_peso
    nota_peso = np.zeros((len(matrix), len(matrix[0]))) 
    for nUsuario in range(len(matrix)):
        for nApartamento in range(len(matrix[0])):
            nota_peso[nUsuario][nApartamento] = nao_curtidos[nApartamento] * matrix[nUsuario][nApartamento] * similarity[nUsuario]

    # Calculate notas_acumuladas
    notas_acumuladas = np.sum(nota_peso.T, axis=1)

    # Calculate temp_peso
    temp_peso = nota_peso.copy()
    temp_peso[nota_peso > 0] = 1

    # Calculate temp_similaridade
    temp_similaridade = np.zeros((len(matrix), len(matrix[0])))
    for nUsuario in range(len(matrix)):
        for nApartamento in range(len(matrix[0])):
            temp_similaridade[nUsuario][nApartamento] = temp_peso[nUsuario][nApartamento] * similarity[nUsuario]

    # Calculate similaridade_acumulada
    similaridade_acumulada = np.sum(temp_similaridade.T, axis=1)

    # Calculate nota_final
    nota_final = [0] * len(matrix[0])
    for nApartamento in range(len(matrix[0])):
        if similaridade_acumulada[nApartamento] > 0:
            nota_final[nApartamento] = notas_acumuladas[nApartamento] / similaridade_acumulada[nApartamento]
        else:
            nota_final[nApartamento] = 0

    return nota_peso, notas_acumuladas, temp_peso, temp_similaridade, similaridade_acumulada, nota_final
