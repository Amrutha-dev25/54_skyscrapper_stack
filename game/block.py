import pygame


class Block:
    def __init__(self, x, y, width, height, color, speed=0):
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.color = color
        self.speed = speed
        self.direction = 1

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.width), int(self.height))

    def update(self, screen_width):
        if self.speed == 0:
            return

        self.x += self.speed * self.direction
        if self.x <= 20:
            self.x = 20
            self.direction = 1
        elif self.x + self.width >= screen_width - 20:
            self.x = screen_width - 20 - self.width
            self.direction = -1

    def render(self, surface):
        draw_rect = self.rect
        pygame.draw.rect(surface, self.color, draw_rect, border_radius=4)
        pygame.draw.rect(surface, (245, 245, 250), draw_rect, width=2, border_radius=4)


class OffcutDebris:
    def __init__(self, x, y, width, height, color, horizontal_velocity):
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.color = color
        self.velocity_x = horizontal_velocity
        self.velocity_y = -1.0
        self.gravity = 0.35
        self.angle = 0.0
        self.angular_velocity = 7.0 if horizontal_velocity < 0 else -7.0
        self.lifetime = 240

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += self.gravity
        self.angle = (self.angle + self.angular_velocity) % 360
        self.lifetime -= 1

    def is_finished(self, screen_height):
        return self.y > screen_height + self.height or self.lifetime <= 0

    def render(self, surface):
        debris_surface = pygame.Surface(
            (max(1, round(self.width)), max(1, round(self.height))),
            pygame.SRCALPHA
        )
        debris_surface.fill(self.color)
        pygame.draw.rect(
            debris_surface,
            (245, 245, 250),
            debris_surface.get_rect(),
            width=2,
            border_radius=4
        )

        rotated_surface = pygame.transform.rotate(debris_surface, self.angle)
        position = rotated_surface.get_rect(
            center=(round(self.x + self.width / 2), round(self.y + self.height / 2))
        )
        surface.blit(rotated_surface, position)