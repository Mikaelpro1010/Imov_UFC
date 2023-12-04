from django.test import TestCase
import numpy as np
from scipy import stats
from app_imov_ufc.utils import calculate_similarity, calculate_final_ratings

class MyTestCase(TestCase):

    def setUp(self):
        # Configurar dados para os testes
        self.matrix = np.array([[8, 0, 3, 4, 6], [5, 6, 1, 8, 9], [8, 0, 0, 5, 10]])
        self.novoUsuario = [8, 0, 2, 3, 0]
        self.nao_curtidos = [0, 1, 0, 0, 1]
        self.nomeApartamentos = ['São Jose Village', 'Home Desing Club', 'Seller Residence', 'Flat Derby', 'Cysne Hotel']

    def test_similarity_calculation(self):
        # Teste para a função de cálculo de similaridade
        similarity = calculate_similarity(self.matrix, self.novoUsuario)
        self.assertEqual(len(similarity), 3)

    def test_final_ratings_calculation(self):
        # Teste para a função de cálculo das classificações finais
        similarity = calculate_similarity(self.matrix, self.novoUsuario)
        nota_peso, notas_acumuladas, temp_peso, temp_similaridade, similaridade_acumulada, nota_final = calculate_final_ratings(
            self.matrix, self.nao_curtidos, similarity
        )
        self.assertEqual(np.shape(nota_peso), (3, 5))
        self.assertEqual(np.shape(notas_acumuladas), (5,))
        self.assertEqual(np.shape(temp_peso), (3, 5))
        self.assertEqual(np.shape(temp_similaridade), (3, 5))
        self.assertEqual(np.shape(similaridade_acumulada), (5,))
        self.assertEqual(np.shape(nota_final), (5,))

    def test_recommendations(self):
        # Teste para garantir que as recomendações são produzidas corretamente
        similarity = calculate_similarity(self.matrix, self.novoUsuario)
        nota_peso, notas_acumuladas, temp_peso, temp_similaridade, similaridade_acumulada, nota_final = calculate_final_ratings(
            self.matrix, self.nao_curtidos, similarity
        )
        nVistos = sum(self.nao_curtidos)
        notasOrdenadasIndex = sorted(range(len(nota_final)), key=nota_final.__getitem__)[::-1][0:nVistos]
        self.assertEqual(len(notasOrdenadasIndex), nVistos)


    def test_recommendation_names(self):
        # Teste para garantir que os nomes dos apartamentos recomendados são corretos
        similarity = calculate_similarity(self.matrix, self.novoUsuario)
        nota_peso, notas_acumuladas, temp_peso, temp_similaridade, similaridade_acumulada, nota_final = calculate_final_ratings(
            self.matrix, self.nao_curtidos, similarity
        )
        nVistos = sum(self.nao_curtidos)
        notasOrdenadasIndex = sorted(range(len(nota_final)), key=nota_final.__getitem__)[::-1][0:nVistos]
        recommended_names = [self.nomeApartamentos[i] for i in notasOrdenadasIndex]
        self.assertListEqual(recommended_names, ['Cysne Hotel', 'Home Desing Club'])



