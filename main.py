start_board = [[' ', 'A', 'B', 'C'], ['1', '-', '-', '-'], ['2', '-', '-', '-'], ['3', '-', '-', '-']]  # Стартовое поле
cols = ['A', 'B', 'C']  # Заголовки столбцов
rows = ['1', '2', '3']  # Заголовки строк
possible_coords = []  # Список возможных координат клетки
for i in cols:
    for j in rows:
        possible_coords.append([i, j])


def print_board(board):
    """Функция производит распечатку игрового поля"""
    for row in range(4):
        for col in range(4):
            print(board[row][col], end=' ')
        print()


def coord_to_index(coord):
    """Функция преобразовывает координату в индекс элемента матрицы игрового поля"""
    for checked_index in range(3):
        if coord == cols[checked_index] or coord == rows[checked_index]:
            return checked_index + 1


def input_space(board, symbol):
    """Функция принимает игровое поле, запрашивает клетку, проверяет возможность хода в нее изменяет игровое поле"""
    coords = input('Введите координаты клетки, в которую хотите сходить, в формате Х 0: ').split()
    while True:
        if coords not in possible_coords:
            coords = input('Вы ввели недопустимые координаты. Введите координаты в формате Х 0: ').split()
        elif board[coord_to_index(coords[1])][coord_to_index(coords[0])] != '-':
            coords = input('Клетка уже занята. Введите координаты свободной клетки: ').split()
        else:  # Клетка свободна
            board[coord_to_index(coords[1])][coord_to_index(coords[0])] = symbol
            break


def full_check(board):
    """Функция проверяет, не кончились ли свободные клетки"""
    for row in range(1, 4):
        for col in range(1, 4):
            if board[row][col] == '-':
                return False
    return True  # Свободных клеток нет


def switch(a, b):
    """Генератор бесконечного чередования двух значений"""
    while True:
        yield a
        yield b


def display(printer, game, stat, turn, player, result):
    """Декоратор для вывода интерфейса, содержащего статистику, вместе с игровым полем"""
    def wrapper(board):
        for x in range(100):
            print('_', end='')  # Вывод разделителя
        print('\nСчёт:   ', end='')
        for k, v in stat.items():
            print(f'{k}: {v}   ', end='')  # Вывод счета
        print(f'\nПартия № {game}', end='')  # Вывод номера партии
        if not result:
            print(f'\nХод № {turn}')  # Вывод номера хода
            printer(board)  # Вывод игрового поля
            print(f'Ходит игрок {player}')  # Вывод текущего игрока
        else:  # Вывод результата
            print(' закончилась вничью' if result == 'Ничья' else f' закончилась победой игрока {result}')
            printer(board)  # Вывод игрового поля
    return wrapper


def win_check(board, symbol):
    """Проверка победы игрока, играющего за symbol"""
    for row in range(1, 4):  # Проверка заполненности одного из рядов
        win = True
        for col in range(1, 4):
            if board[row][col] != symbol:
                win = False
        if win:
            return win
    for col in range(1, 4):  # Проверка заполненности одного из столбцов
        win = True
        for row in range(1, 4):
            if board[row][col] != symbol:
                win = False
        if win:
            return win
    if board[2][2] == symbol:  # Проверка заполненности одной из диагоналей
        if board[1][1] == board[3][3] == symbol or board[1][3] == board[3][1] == symbol:
            return True
    return False  # Если ни одно из условий победы не выполняется


def play_more():
    """Запрос продолжения игры"""
    answer = input('Сыграть еще (Y/N)? ')
    while True:
        if answer in ('Y', 'y'):
            return True
        elif answer in ('N', 'n'):
            return False
        else:
            answer = input('Недопустимый ввод. Чтобы сыграть еще, введите Y. Чтобы отказаться, введите N. ')


print('Введите имена игроков, чтобы начать игру')  # Запрос и ввод имен игроков
player_1 = input('Игрок 1: ')
player_2 = input('Игрок 2: ')
while player_2 == player_1:  # Проверка имени второго игрока
    player_2 = input('Имя занято игроком 1. Введите другое имя: ')

game_num = 0  # Объявление счетчика партий
stats = {player_1: 0, player_2: 0, 'Ничья': 0}  # Объявление словаря, содержащего счет по партиям
first_player_switch = iter(switch(player_1, player_2))  # Переключатель игрока, ходящего первым в данной партии
play = True  # Начало игры
while play:
    game_num += 1
    current_board = [[start_board[r][c] for c in range(4)]for r in range(4)]  # Обнуление текущего игрового поля
    turn_num = 0  # Обнуление счетчика ходов
    first_player = next(first_player_switch)  # Игрок, которых ходит первым в текущей партии
    second_player = player_2 if first_player == player_1 else player_1  # Игрок, который ходит вторым в текущей партии
    current_player_switch = iter(switch(first_player, second_player))  # Переключатель текущего игрока

    winner = None  # Начало партии
    while not winner:
        turn_num += 1
        current_player = next(current_player_switch)
        current_symbol = 'x' if current_player == first_player else 'o'  # Текущий символ
        display_board = display(print_board, game_num, stats, turn_num, current_player, winner)  # Создание интерфейса
        display_board(current_board)  # Вывод интерфейса
        input_space(current_board, current_symbol)  # Ввод нового символа

        if win_check(current_board, current_symbol):  # Проверка победы одного из игроков
            winner = current_player
        elif full_check(current_board):  # Проверка ничьи
            winner = 'Ничья'

    else:  # Конец партии
        stats[winner] += 1
        display_board = display(print_board, game_num, stats, turn_num, None, winner)  # Формирование интерфейса
        display_board(current_board)  # Вывод интерфейса
        play = play_more()  # Запрос продолжения игры

else:  # Конец игры
    print('Игра окончена. Итоговый счёт:   ')  # Вывод итоговой статистики по окончании игры.
    for key, value in stats.items():
        print(f'{key}: {value}   ', end='')
    input()
