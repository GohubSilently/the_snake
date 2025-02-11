from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Константы цвета:
BOARD_BACKGROUND_COLOR = (200, 200, 200)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Make the main class."""

    def __init__(
        self,
        body_color
    ):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(
        self
    ):
        """Raise the problem in under class."""
        raise NotImplementedError(
            f'Метод draw() не выполняется в {self.__init__.__name__}'
        )

    def draw_one_cell(
        self,
        position,
        body_color=None
    ):
        """Draw one cell."""
        if body_color is None:
            body_color = self.body_color

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Make new class Apple inhireteed by GameObject."""

    def __init__(
        self,
        occupied_cells: list[tuple],
        body_color=APPLE_COLOR
    ):
        super().__init__(body_color)
        self.randomize_position(occupied_cells)

    def randomize_position(
        self,
        occupied_cells
    ):
        """Define the position of the apple"""
        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position not in occupied_cells:
                self.position = new_position
                print(self.position)
                return self.position

    def draw(
        self
    ):
        """Draw the object of the apple"""
        self.draw_one_cell(self.position)



class Snake(GameObject):
    pass


def main():
    # Инициализация pg:
    pg.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple([(180, 200)])

    while True:
        clock.tick(SPEED)
        apple.draw()

        pg.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pg.draw.rect(screen, self.body_color, rect)
#     pg.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pg.draw.rect(screen, self.body_color, rect)
#         pg.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pg.draw.rect(screen, self.body_color, head_rect)
#     pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             pg.quit()
#             raise SystemExit
#         elif event.type == pg.KEYDOWN:
#             if event.key == pg.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pg.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
