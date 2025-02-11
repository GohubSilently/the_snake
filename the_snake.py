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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
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
    """Make class GameObject"""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Define in under class"""
        pass


class Snake(GameObject):
    """Make new class (snake) inherite by GameObject."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Upgrade direction."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Function of the moving the snake"""
        x, y = self.get_head_position()

        if self.direction == RIGHT:
            self.positions.insert(0, (x + GRID_SIZE, y))
            if self.positions[0][0] > SCREEN_WIDTH:
                self.positions[0] = (0 + GRID_SIZE, y)

        elif self.direction == LEFT:
            self.positions.insert(0, (x - GRID_SIZE, y))
            if self.positions[0][0] < 0:
                self.positions[0] = (SCREEN_WIDTH - GRID_SIZE, y)

        elif self.direction == UP:
            self.positions.insert(0, (x, y - GRID_SIZE))
            if self.positions[0][1] < 0:
                self.positions[0] = (x, SCREEN_HEIGHT - GRID_SIZE)

        else:
            self.positions.insert(0, (x, y + GRID_SIZE))
            if self.positions[0][1] > SCREEN_HEIGHT:
                self.positions[0] = (x, 0 + GRID_SIZE)

        if self.length < len(self.positions):
            self.last = self.positions.pop()

    def draw(self):
        """Function of drawing the apple."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Return the head of the snake."""
        return self.positions[0]

    def reset(self):
        """Reset the snake."""
        self.length = 1
        self.direction = choice([UP, DOWN, RIGHT, LEFT])
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]


class Apple(GameObject):
    """Make new class (apple) inherite by GameObject."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Make the function, which define position."""
        return (randint(0, GRID_WIDTH) * GRID_SIZE,
                randint(0, GRID_HEIGHT) * GRID_SIZE)

    def draw(self):
        """Function of drawing the apple."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Handle key."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Main function."""
    # Инициализация pg:
    pg.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
