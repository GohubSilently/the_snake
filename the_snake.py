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

KEYS = {
    pg.K_UP: UP,
    pg.K_DOWN: DOWN,
    pg.K_LEFT: LEFT,
    pg.K_RIGHT: RIGHT,
}

# Константы цвета:
BOARD_BACKGROUND_COLOR = (128, 128, 128)
BORDER_COLOR = (128, 128, 128)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка \\ ESC - выход')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Make the main class."""

    def __init__(
        self,
        body_color=None
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
    """Make new class Apple inhireted by GameObject."""

    def __init__(
        self,
        occupied_cells=None,
        body_color=APPLE_COLOR
    ):
        super().__init__(body_color)
        if occupied_cells is not None:
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
                return self.position

    def draw(
        self
    ):
        """Draw the object of the apple"""
        self.draw_one_cell(self.position)


class Snake(GameObject):
    """Make new class Snake inhireted by GameObject."""

    def __init__(
        self,
        body_color=SNAKE_COLOR
    ):
        super().__init__(body_color)
        self.reset()

    def get_head_position(
        self
    ):
        """Define the head of the snake."""
        return self.positions[0]

    def reset(
        self
    ):
        """Reset the snake."""
        self.length = 1
        self.direction = choice([UP, DOWN, RIGHT, LEFT])
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.last = None

    def update_direction(
        self,
        new_position
    ):
        """Update the directions."""
        if new_position:
            self.direction = new_position

    def move(
        self
    ):
        """The movement of the snake."""
        x, y = self.get_head_position()
        x_1, y_1 = self.direction

        head = ((x + x_1 * GRID_SIZE) % SCREEN_WIDTH,
                (y + y_1 * GRID_SIZE) % SCREEN_HEIGHT)

        self.positions.insert(0, head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(
        self
    ):
        """Draw the snake."""
        self.draw_one_cell(self.get_head_position())
        if self.last:
            self.draw_one_cell(self.last, BOARD_BACKGROUND_COLOR)


def handle_keys(snake):
    """Check the keybord."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            raise SystemExit

        if event.type == pg.KEYDOWN:
            new_direction = KEYS.get(event.key)
            if (
                new_direction
                and new_direction[0] != -snake.direction[0]
                and new_direction[1] != -snake.direction[1]
            ):
                snake.update_direction(new_direction)


def main():
    """Start the game."""
    # Инициализация pg:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pg.display.set_caption(
            f'ESC - выход | \t\t\t\t'
            f'Змейка \t\t\t\t'
            f'| Длина: {snake.length}'
        )

        pg.display.update()


if __name__ == '__main__':
    main()
