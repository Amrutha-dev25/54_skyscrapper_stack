import random
import pygame
from game.block import Block, OffcutDebris


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.block_height = 28
        self.base_width = 180

        self.font_title = pygame.font.SysFont(None, 38)
        self.font_hud = pygame.font.SysFont(None, 28)
        self.font_big = pygame.font.SysFont(None, 46)

        self.reset()

    def get_color(self, index):
        palette = [
            (230, 75, 75),   # Crimson
            (240, 140, 45),  # Orange
            (245, 210, 50),  # Gold
            (60, 195, 110),  # Green
            (50, 150, 240),  # Blue
            (165, 80, 225),  # Purple
        ]
        return palette[index % len(palette)]

    def reset(self):
        self.score = 0
        self.game_over = False

        # Task 2: Perfect placement state
        self.perfect_streak = 0
        self.perfect_popup_timer = 0
        self.debris = []

        base_x = (self.width - self.base_width) // 2
        base_y = self.height - 60

        base_block = Block(
            base_x,
            base_y,
            self.base_width,
            self.block_height,
            self.get_color(0),
            speed=0
        )

        self.stack = [base_block]

        self.spawn_active_block()

    def spawn_active_block(self):
        top_block = self.stack[-1]

        next_y = top_block.y - self.block_height - 4

        speed = min(
            10.0,
            4.5 + (len(self.stack) * 0.35)
        )

        color = self.get_color(len(self.stack))

        start_x = (
            25
            if random.choice([True, False])
            else self.width - 25 - top_block.width
        )

        self.active_block = Block(
            start_x,
            next_y,
            top_block.width,
            self.block_height,
            color,
            speed=speed
        )

    def drop_block(self):
        if self.game_over:
            return

        top_block = self.stack[-1]
        act = self.active_block

        # Calculate horizontal overlap
        left = max(act.x, top_block.x)
        right = min(
            act.x + act.width,
            top_block.x + top_block.width
        )

        overlap = right - left

        # Task 1:
        # Positive overlap means the block successfully lands.
        # Zero or negative overlap means it completely misses.
        is_successful_drop = overlap > 0

        # Task 2:
        # A placement is perfect when the left edges are
        # within 3 pixels of each other.
        is_perfect = (
            is_successful_drop
            and abs(act.x - top_block.x) <= 3
        )

        if is_successful_drop:

            if is_perfect:
                # Increase perfect streak
                self.perfect_streak += 1

                # Snap block exactly to the previous block
                new_block_x = top_block.x

                # Preserve the full width
                new_block_width = act.width

                # Show PERFECT! popup
                self.perfect_popup_timer = 45

                # After 3 consecutive perfect placements,
                # slightly expand the block width.
                if self.perfect_streak == 3:
                    new_block_x -= 5
                    new_block_width += 10

            else:
                # Normal successful placement
                # breaks the perfect streak.
                self.perfect_streak = 0

                if act.x < left:
                    self.debris.append(
                        OffcutDebris(
                            act.x,
                            act.y,
                            left - act.x,
                            act.height,
                            act.color,
                            horizontal_velocity=-2.0
                        )
                    )

                if right < act.x + act.width:
                    self.debris.append(
                        OffcutDebris(
                            right,
                            act.y,
                            act.x + act.width - right,
                            act.height,
                            act.color,
                            horizontal_velocity=2.0
                        )
                    )

                new_block_x = left
                new_block_width = max(10.0, overlap)

            # Create the newly placed block
            new_block = Block(
                new_block_x,
                act.y,
                new_block_width,
                self.block_height,
                act.color,
                speed=0
            )

            self.stack.append(new_block)

            # Normal placement = +1
            # Perfect placement = +3
            self.score += 1 + (2 if is_perfect else 0)

            # Camera scrolling
            if new_block.y < 180:
                shift_amount = self.block_height + 4

                for b in self.stack:
                    b.y += shift_amount

                for debris in self.debris:
                    debris.y += shift_amount

            # Spawn next active block
            self.spawn_active_block()

        else:
            # No overlap -> tower collapses
            self.game_over = True

    def handle_event(self, event):
        if self.game_over:
            # Restart using R, Space, or left mouse click
            if (
                event.type == pygame.KEYDOWN
                and event.key in (pygame.K_r, pygame.K_SPACE)
            ) or (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                self.reset()

            return

        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
        ):
            self.drop_block()

        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            self.drop_block()

    def update(self):
        # Task 2:
        # Countdown PERFECT! popup timer.
        if self.perfect_popup_timer > 0:
            self.perfect_popup_timer -= 1

        for debris in self.debris:
            debris.update()

        self.debris = [
            debris
            for debris in self.debris
            if not debris.is_finished(self.height)
        ]

        if not self.game_over:
            self.active_block.update(self.width)

    def render(self, screen):
        # Existing background
        screen.fill((24, 27, 36))

        # Title
        title_surf = self.font_title.render(
            "Skyscraper Stack",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                16
            )
        )

        # Score
        score_surf = self.font_hud.render(
            f"Height: {self.score}",
            True,
            (255, 220, 80)
        )

        screen.blit(
            score_surf,
            (
                self.width // 2 - score_surf.get_width() // 2,
                54
            )
        )

        # Render placed blocks
        for b in self.stack:
            b.render(screen)

        for debris in self.debris:
            debris.render(screen)

        # Task 2:
        # Display PERFECT! popup while timer is active.
        if self.perfect_popup_timer > 0:
            perfect_surf = self.font_hud.render(
                "PERFECT!",
                True,
                (255, 220, 80)
            )

            screen.blit(
                perfect_surf,
                (
                    self.width // 2 - perfect_surf.get_width() // 2,
                    92
                )
            )

        # Render active block
        if not self.game_over:
            self.active_block.render(screen)

        # Game Over screen
        if self.game_over:
            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill((0, 0, 0, 195))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render(
                "TOWER COLLAPSED!",
                True,
                (240, 75, 75)
            )

            screen.blit(
                over_surf,
                (
                    self.width // 2 - over_surf.get_width() // 2,
                    self.height // 2 - 40
                )
            )

            final_surf = self.font_hud.render(
                f"Final Height: {self.score}",
                True,
                (255, 255, 255)
            )

            screen.blit(
                final_surf,
                (
                    self.width // 2 - final_surf.get_width() // 2,
                    self.height // 2 + 10
                )
            )

            restart_surf = self.font_hud.render(
                "Press [Space] or [R] to Play Again",
                True,
                (200, 200, 200)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    self.height // 2 + 50
                )
            )