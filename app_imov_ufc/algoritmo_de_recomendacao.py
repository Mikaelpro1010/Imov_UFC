from abc import ABC, abstractmethod
import numpy as np
import scipy.stats as stats

# Interface Observer
class Observer(ABC):
    @abstractmethod
    def update(self, result_similarity, result_final_ratings):
        pass

# Concrete Observer
class RecommendationObserver(Observer):
    def update(self, result_similarity, result_final_ratings):
        print("Atualização de resultados:")
        print("Similaridade:", result_similarity)
        print("Avaliações Finais:", result_final_ratings)
        print()

# Subject
class RecommendationCalculatorSubject:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, result_similarity, result_final_ratings):
        for observer in self._observers:
            observer.update(result_similarity, result_final_ratings)

# RecommendationCalculatorSingleton mantém uma referência ao Subject
class RecommendationCalculatorSingleton(RecommendationCalculatorSubject):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RecommendationCalculatorSingleton, cls).__new__(cls)
            # Inicializar instância única aqui, se necessário
        return cls._instance

    def calculate_similarity(self, matrix, novoUsuario):
        similarities = []

        for i in range(len(matrix)):
            temp = matrix[i, :]
            tempUsuario = [t for n, t in zip(novoUsuario, temp) if n != 0]
            tempNovoUsuario = [n for n in novoUsuario if n != 0]
            similarity = stats.pearsonr(tempUsuario, tempNovoUsuario)[0]
            similarities.append(similarity)

        # Notificar Observers sobre a mudança
        self.notify_observers(similarities, None)

        return similarities

    def calculate_final_ratings(self, matrix, nao_curtidos, similarity):
        nota_peso = np.zeros((len(matrix), len(matrix[0])))
        for nUsuario in range(len(matrix)):
            for nApartamento in range(len(matrix[0])):
                nota_peso[nUsuario][nApartamento] = nao_curtidos[nApartamento] * matrix[nUsuario][nApartamento] * similarity[nUsuario]

        notas_acumuladas = np.sum(nota_peso.T, axis=1)

        temp_peso = nota_peso.copy()
        temp_peso[nota_peso > 0] = 1

        temp_similaridade = np.zeros((len(matrix), len(matrix[0])))
        for nUsuario in range(len(matrix)):
            for nApartamento in range(len(matrix[0])):
                temp_similaridade[nUsuario][nApartamento] = temp_peso[nUsuario][nApartamento] * similarity[nUsuario]

        similaridade_acumulada = np.sum(temp_similaridade.T, axis=1)

        nota_final = [0] * len(matrix[0])
        for nApartamento in range(len(matrix[0])):
            if similaridade_acumulada[nApartamento] > 0:
                nota_final[nApartamento] = notas_acumuladas[nApartamento] / similaridade_acumulada[nApartamento]
            else:
                nota_final[nApartamento] = 0

        # Notificar Observers sobre a mudança
        self.notify_observers(None, nota_final)

        return nota_peso, notas_acumuladas, temp_peso, temp_similaridade, similaridade_acumulada, nota_final

# RecommendationCalculatorDecorator agora é um Observer
class RecommendationCalculatorDecorator(Observer):
    def __init__(self, calculator):
        self._calculator = calculator
        calculator.add_observer(self)

    def calculate_similarity(self, matrix, novoUsuario):
        similarities = self._calculator.calculate_similarity(matrix, novoUsuario)
        return similarities

    def calculate_final_ratings(self, matrix, nao_curtidos, similarity):
        nota_peso, notas_acumuladas, temp_peso, temp_similaridade, similaridade_acumulada, nota_final = \
            self._calculator.calculate_final_ratings(matrix, nao_curtidos, similarity)
        return nota_peso, notas_acumuladas, temp_peso, temp_similaridade, similaridade_acumulada, nota_final

    # Método de atualização chamado pelo Subject
    def update(self, result_similarity, result_final_ratings):
        print("Decorator Notificado:")
        print("Similaridade Atualizada:", result_similarity)
        print("Avaliações Finais Atualizadas:", result_final_ratings)
        print()

# Uso do Singleton com Decorator e Observer
calculator_instance = RecommendationCalculatorDecorator(RecommendationCalculatorSingleton())

# Exemplo de cálculos
matrix = np.array([[8, 0, 3, 4, 6], [5, 6, 1, 8, 9], [8, 0, 0, 5, 10]])
novoUsuario = [8, 0, 2, 3, 0]

result_similarity = calculator_instance.calculate_similarity(matrix, novoUsuario)
result_final_ratings = calculator_instance.calculate_final_ratings(matrix, [0, 1, 0, 0, 1], result_similarity)
