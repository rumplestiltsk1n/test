```python
import numpy as np


# Введення матриці втрат
def input_matrix():
    rows = []
    row = list(map(int, input('Введіть матрицю втрат\n').split()))

    while row:  # поки рядок не пустий
        rows.append(row)
        row = list(map(int, input().split()))

    return np.array(rows)


matrix = input_matrix()
# matrix = np.array([[20, 12, 15, 15],
#                    [14, 23, 12, 26],
#                    [25, 21, 24, 30]])

num_rows = matrix.shape[0]  # кількість рядків
num_cols = matrix.shape[1]  # кількість стовпців


# Критерій Вальда
def min_max_Wald(matrix):
    # Максимуми рядків
    row_max = matrix.max(axis=1)

    print('\nМатриця втрат')
    print(matrix)

    print('\nМаксимуми рядків')
    for i in range(num_rows):
        print(matrix[i], '\t', row_max[i])  # [рядок] максимум

    print('\nМінімум з максимумів', np.min(row_max))
    print('Стратегія', np.argmin(row_max) + 1)


# Матриця ризиків
def get_risk_matrix(matrix):
    print('Початкова матриця втрат')
    print(matrix)

    col_min = matrix.min(axis=0)  # мінімуми стовпців
    print(' ', ' '.join(map(str, col_min)), 'мінімуми стовпців ßj (віднімаються від елементів матриці втрат aij)')

    risk_matrix = np.copy(matrix)
    for i in range(num_rows):
        for j in range(num_cols):
            risk_matrix[i][j] -= col_min[j]  # відняти мінімуми стовпців від елементів

    print('\nМатриця ризиків')
    print(risk_matrix)

    return risk_matrix


# Критерій Севіджа
def min_max_Savage(matrix):
    print('Знаходимо матрицю ризиків')
    risk_matrix = get_risk_matrix(matrix)

    # Максимуми рядків
    row_max = risk_matrix.max(axis=1)

    print('\nМаксимуми рядків матриці ризиків')
    for i in range(num_rows):
        print(risk_matrix[i], '\t', row_max[i])  # [рядок] максимум

    print('\nМінімум з максимумів', np.min(row_max))
    print('Стратегія', np.argmin(row_max) + 1)


# # Критерій Гурвіца
def Hurwitz(matrix, p=0.6):  # коефіцієнт песимізму 0.6 за замовчуванням
    print('Ha = min{p*min aij + (1-p)*max aij}')

    row_min = matrix.min(axis=1)  # мінімуми рядків
    row_max = matrix.max(axis=1)  # максимуми рядків

    print('Мінімуми рядків матриці втрат')
    for i in range(num_rows):
        print(matrix[i], '\t', row_min[i])  # [рядок] максимум

    print('Максимуми рядків матриці втрат')
    for i in range(num_rows):
        print(matrix[i], '\t', row_max[i])  # [рядок] максимум

    row_results = np.zeros(num_rows)  # результати обчислень по рядкам
    print('Обчислення по рядкам')
    for i in range(num_rows):
        row_results[i] = p * row_min[i] + (1 - p) * row_max[i]
        print(p, '*', row_min[i], '+ ( 1 -', p, ') *', row_max[i], '=', row_results[i])

    print('\nМінімум з обчислених по рядкам значень', np.min(row_results))
    print('Стратегія', np.argmin(row_results) + 1)


print('Критерій Вальда')
min_max_Wald(matrix)

print('\n\nКритерій Севіджа')
min_max_Savage(matrix)

print('\n\nКритерій Гурвіца, коефіцієнт песимізму p = 0.6')
Hurwitz(matrix)
```
