import numpy as np


# Чи унікальні всі значення масиву
def is_unique(array):
    return len(array) == len(set(array))


# Підрахунок кількості оцінок по рядкам
def count_occurrences(row):
    unique, counts = np.unique(row, return_counts=True)

    dictionary = dict(zip(unique, counts))  # словник {ранг: кількість повторень}
    array = np.array(list(dictionary.values()))  # значення tij по рядкам

    print(dictionary)
    # print(array)

    return np.sum(array ** 3 - array)


# Стандартизація масиву
def standardize(array):
    # Шкала строга (всі оцінки унікальні)
    if is_unique(array):
        return array
    else:
        ranks_copy = np.copy(array)  # копія вхідного масиву
        result = np.zeros(len(array))  # ініціалізація результуючого масиву 0-ми

        # Стандартизовані індекси
        M = np.array([], dtype=int)

        # Кількість не стандартизованих рангів
        delta = len(array)

        while len(M) < len(array):
            # Індекси максимальних рангів (не стандартизованих)
            L = np.ndarray.flatten(np.argwhere(ranks_copy == ranks_copy.max()))

            for i in L:
                result[i] = delta - (len(L) - 1) / 2  # стандартизоване значення
                M = np.append(M, i)
                ranks_copy[i] = -1

            delta -= len(L)

        return result


# Обчислення коефіцієнту конкордації
def concordance_coefficient(matrix, is_standardized):
    S = np.sum((np.sum(matrix, axis=0) - m * (n + 1) / 2) ** 2)

    # Якщо є не стандартизовані рядки
    if is_standardized:
        return 12 * S / (m ** 2 * (n ** 3 - n))

    else:
        print('\nОцінки, що повторюються {ранг: кількість повторень}')
        Tj = np.apply_along_axis(count_occurrences, axis=1, arr=matrix)  # сума tij по рядкам
        W = 12 * S / (m ** 2 * (n ** 3 - n) - m * np.sum(Tj))
        return W


# Виведення рядка та його суми
def row_sum(row):
    print(f'{row} {row.sum()}')


# Виведення результатів обчислення χ²
def x_squared(W):
    X2 = m * (n - 1) * W
    print('Значущість коефіцієнта конкордації оцінюється χ² розподілом')
    print(f'χ² = {X2:.3f}')
    print('χ²кр = 23.2 при рівні значущості α=0.01 та числі ступенів свободи φ=n-1=10')
    if X2 > 23.2:
        print('χ² > χ²кр гіпотеза про узгодженість думок всієї групи експертів приймається')
    else:
        print('χ² < χ²кр гіпотеза про узгодженість думок всієї групи експертів не приймається')


matrix = np.array([
    [3, 2, 2, 2, 3, 3, 4, 6, 1, 4, 5],
    [1, 2, 3, 6, 9, 10, 7, 9, 4, 5, 8],
    [1, 4, 4, 7, 6, 8, 11, 5, 3, 2, 9],
    [3, 3, 4, 1, 8, 8, 5, 8, 6, 2, 7],
    [2, 7, 1, 6, 5, 6, 2, 8, 3, 5, 4],
    [1, 1, 3, 2, 3, 3, 4, 6, 2, 5, 4],
    [1, 1, 2, 2, 4, 3, 4, 5, 2, 2, 4],
    [1, 2, 3, 3, 3, 3, 4, 2, 3, 4, 4],
    [1, 3, 4, 3, 3, 4, 4, 2, 4, 5, 2],
    [1, 4, 4, 2, 4, 4, 4, 3, 3, 5, 6],
    [2, 4, 5, 6, 1, 7, 7, 3, 4, 5, 8],
    [2, 1, 4, 3, 2, 6, 1, 7, 3, 5, 3],
    [3, 2, 1, 5, 6, 2, 3, 3, 4, 5, 6],
    [3, 2, 1, 2, 6, 7, 5, 6, 4, 6, 8],
    [2, 1, 3, 5, 7, 8, 8, 3, 4, 6, 2],
    [1, 5, 3, 5, 6, 6, 6, 2, 4, 6, 5],
    [1, 4, 2, 5, 7, 8, 6, 2, 3, 3, 9],
    [1, 4, 2, 3, 5, 5, 5, 7, 3, 5, 6]
])

print('Початкова матриця з сумами рядків')
np.apply_along_axis(row_sum, axis=1, arr=matrix)

# Матриця m x n
m = matrix.shape[0]  # кількість рядків (експертів)
n = matrix.shape[1]  # кількість стовпців (оцінок)

# Коефіцієнт конкордації без стандартизації
W = concordance_coefficient(matrix, is_standardized=False)
print(f'\nКоефіцієнт конкордації без стандартизації W = {W:.3f}')

# χ^2 розподіл
x_squared(W)


# Стандартизація рядків матриці
standardized_matrix = np.apply_along_axis(standardize, axis=1, arr=matrix)

print('\nСтандартизована матриця з сумами рядків')
np.apply_along_axis(row_sum, axis=1, arr=standardized_matrix)
# print(np.sum(standardized_matrix, axis=1))  # check sum

# Коефіцієнт конкордації
W = concordance_coefficient(standardized_matrix, is_standardized=True)
print(f'Коефіцієнт конкордації стандартизованих рядків W = {W:.3f}')

# χ² розподіл
x_squared(W)
