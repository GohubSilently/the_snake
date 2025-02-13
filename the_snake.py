from random import choice

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTRAL_CELL = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

ALL_CELLS = {
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
}

# Константы движения и скорости:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

GAME_BUTTON = {
    pg.K_UP: UP,
    pg.K_DOWN: DOWN,
    pg.K_LEFT: LEFT,
    pg.K_RIGHT: RIGHT,
}

SPEED = 10

# Константы цвета:
BOARD_BACKGROUND_COLOR = (128, 128, 128)
BORDER_COLOR = (128, 128, 128)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Make the main class."""

    def __init__(
        self,
        body_color=None
    ):
        self.position = CENTRAL_CELL
        self.body_color = body_color

    def draw(
        self
    ):
        """Raise the problem in under class."""
        raise NotImplementedError(
            f'Метод draw() не выполняется в {type(self).__name__}'
        )

    def draw_one_cell(
        self,
        position,
        body_color=None
    ):
        """Draw one cell."""
        body_color = body_color or self.body_color

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)


class Apple(GameObject):
    """Make new class Apple inhireted by GameObject."""

    def __init__(
        self,
        occupied_cells=CENTRAL_CELL,
        body_color=APPLE_COLOR
    ):
        super().__init__(body_color)
        self.randomize_position(occupied_cells)

    def randomize_position(
        self,
        occupied_cells
    ):
        """Define the position of the apple"""
        random_cell = tuple(ALL_CELLS - set(occupied_cells))
        self.position = choice(random_cell)
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
        self.best_length = 1

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
        self.positions = [CENTRAL_CELL]
        self.last = None

    def update_direction(
        self,
        new_position
    ):
        """Update the directions."""
        if (
            new_position[0] != -self.direction[0]
            and new_position[1] != -self.direction[1]
        ):
            self.direction = new_position

    def move(
        self
    ):
        """The movement of the snake."""
        head_x, head_y = self.get_head_position()
        head_movement_x, head_movement_y = self.direction

        new_head = ((head_x + head_movement_x * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + head_movement_y * GRID_SIZE) % SCREEN_HEIGHT)

        self.positions.insert(0, new_head)
        self.last = (
            self.positions.pop()
            if len(self.positions) > self.length
            else None
        )

    def draw(
        self
    ):
        """Draw the snake."""
        self.draw_one_cell(self.get_head_position())
        if self.last:
            self.draw_one_cell(self.last, BOARD_BACKGROUND_COLOR)

    def grow(
        self
    ):
        """Grow the length of the snake and update record."""
        self.length += 1
        self.best_length = max(self.best_length, self.length)


def handle_keys(snake):
    """Check the keybord."""
    for event in pg.event.get():
        if (
            event.type == pg.QUIT
            or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)
        ):
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            new_position = GAME_BUTTON.get(event.key)
            if new_position:
                snake.update_direction(new_position)


def main():
    """Start the game."""
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        new_caption = (
            f'ESC | Змейка | Длина: {snake.length} '
            f'| Рекорд: {snake.best_length}'
        )
        if new_caption != pg.display.get_caption()[0]:
            pg.display.set_caption(new_caption)

        pg.display.update()


if __name__ == '__main__':
    main()
