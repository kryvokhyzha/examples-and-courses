"""
Умова:
    На ігровому полі 3 × 3 розставлені фішки з цифрами від 1 до 8.
    Є одна вільна клітина, на яку можуть бути перенесені фішки з сусідніх позицій (нехай це нульова клітинка).
    При цьому не допускається переміщення фішок через одну, а також по діагоналі.
    Завдання полягає в тому, щоб перетворити початкову конфігурацію в цільову конфігураці.

Цільова конфігурація:
    [1, 2, 3]
    [4, 0, 5]
    [6, 7, 8]

Початкова конфігурація:
    [2, 8, 1]
    [3, 6, 4]
    [7, 0, 5]

Параметри:
    h_mode in {'manhattan', 'misplaced', 'None'}

Автор:
    Кривохижа Роман Андрійович
    КАУ, 122
"""

import numpy as np
import sys
from a_star import AstarAlgorithm
from utils import catchtime


if __name__ == '__main__':
    h_strategy = 'None'
    initial_state = np.asarray([[2, 8, 1], [3, 6, 4], [7, 0, 5]])
    goal_state = np.asarray([[1, 2, 3], [4, 0, 5], [6, 7, 8]])

    algorithm = AstarAlgorithm(
        initial_state, h_strategy=h_strategy, goal=goal_state,
    )

    if algorithm is None:
        print('Final state was not found!')
        sys.exit(-1)

    with catchtime() as elapsed:
        path, depth, f_value, acc_f = algorithm.fit()

    print('='*10 + ' A-star algorithm ' + '='*10)
    print('Heuristic strategy:', h_strategy)
    for state, action in path:
        print(action)
        print('\u2193')
        print(state)
        print('\u2193')
    print('Final state was found!\n')

    print('Number of steps:', depth)
    print('F-value:', f_value)
    print('Accumulate F-value:', acc_f)
    print('Close set size:', algorithm.close_set_size)
    print(f'Algorithm execution time: {elapsed():.3f} seconds')
