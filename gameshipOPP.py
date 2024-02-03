class Board:
    def __init__(self):
        self.board = [[' ' for _ in range(6)] for _ in range(6)]

    def print_board(self):
        print('   1 2 3 4 5 6')
        print('  ------------')
        for i, row in enumerate(self.board):
            print(chr(i + 65) + ' | ' + ' '.join(row) + ' |')
        print('  ------------')

    def place_ships(self, ships):
        for size, count in ships.items():
            for _ in range(count):
                self.place_ship(size)

    def place_ship(self, size):
        while True:
            coordinates = input(f'Введите координаты корабля длиной {size} (например, "A1 A2 A3"): ')
            coordinates = coordinates.split()

            if len(coordinates) != size:
                print(f'Некорректный ввод! Введите {size} координаты')
                continue

            try:
                for coordinate in coordinates:
                    x, y = coordinate[:1], int(coordinate[1:]) - 1
                    x = ord(x.upper()) - 65
                    if not (0 <= x < 6 and 0 <= y < 6):
                        raise ValueError
                    if self.board[x][y] != ' ':
                        raise ValueError
                    self.board[x][y] = 'O'
                break
            except (ValueError, IndexError):
                print('Некорректные координаты! Повторите ввод.')


class Game:
    def __init__(self):
        self.player_board = Board()
        self.bot_board = Board()
        self.player_turn = True

    def play(self):
        self.player_board.place_ships({3: 1, 2: 2, 1: 4})
        self.bot_board.place_ships({3: 1, 2: 2, 1: 4})

        while True:
            self.player_board.print_board()

            if self.player_turn:
                self.player_attack()
                if self.check_game_over(self.bot_board):
                    print('Вы победили! Игра завершена.')
                    break
            else:
                self.bot_attack()
                if self.check_game_over(self.player_board):
                    print('К сожалению, вы проиграли. Игра завершена.')
                    break

            self.player_turn = not self.player_turn

    def player_attack(self):
        while True:
            target = input('Введите координаты для атаки (например, "A1"): ')
            x, y = target[:1], int(target[1:]) - 1
            x = ord(x.upper()) - 65

            if not (0 <= x < 6 and 0 <= y < 6):
                print('Некорректные координаты! Повторите ввод.')
                continue

            if self.bot_board.board[x][y] == 'O':
                self.bot_board.board[x][y] = 'X'
                print('Вы попали!')
            elif self.bot_board.board[x][y] == ' ':
                self.bot_board.board[x][y] = 'T'
                print('Вы промахнулись!')
            else:
                print('Вы уже стреляли в эту клетку! Повторите ввод.')
                continue

            break

    def bot_attack(self):
        from random import randint

        while True:
            x = randint(0, 5)
            y = randint(0, 5)

            if self.player_board.board[x][y] == 'O':
                self.player_board.board[x][y] = 'X'
                print(f'ИИ попал в клетку {chr(x + 65)}{y + 1}!')
            elif self.player_board.board[x][y] == ' ':
                self.player_board.board[x][y] = 'T'
                print(f'ИИ промахнулся в клетку {chr(x + 65)}{y + 1}!')
            else:
                continue

            break

    @staticmethod
    def check_game_over(board):
        for row in board.board:
            if 'O' in row:
                return False
        return True


if __name__ == '__main__':
    game = Game()
    game.play()