import pygame
import sys
import random

class GameController:
    def __init__(self):
        pygame.init()
        self.score = 0
        pygame.joystick.init()

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Simple Cube Controller")

        self.font = pygame.font.Font(None, 36)

        self.cube_x = 400  
        self.cube_y = 300
        self.cube_speed = 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.cube_color = (255, 0, 0)
        self.acceleration = 0.2
        self.friction = 0.95
        self.game_over = False

        self.circle_x = random.randint(50, 750)
        self.circle_y = random.randint(50, 550)
        self.circle_radius = 20
        self.circle_color = (0, 255, 0)

        # Gripper properties
        self.gripper_offset = 0
        self.gripper_max_offset = 20
        self.gripper_speed = 2
        self.holding_ball = False

        if pygame.joystick.get_count() > 0:
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
            print(f"Controller connected: {self.controller.get_name()}")
        else:
            print("No controller found!")
            sys.exit(1)

    def show_game_over(self):
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render(f"Game Over! Final Score: {self.score}", True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(400, 300))
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 6:  # L2 button
                        self.score = 0
                        self.cube_x = 400
                        self.cube_y = 300
                        self.velocity_x = 0
                        self.velocity_y = 0
                        self.circle_x = random.randint(50, 750)
                        self.circle_y = random.randint(50, 550)
                        self.holding_ball = False
                        return True
        return False

    def check_border_collision(self):
        if self.cube_x <= 0 or self.cube_x >= 750 or self.cube_y <= 0 or self.cube_y >= 550:
            return True

        if not self.holding_ball:
            cube_center_x = self.cube_x + 25
            cube_center_y = self.cube_y + 25
            distance = ((cube_center_x - self.circle_x) ** 2 + (cube_center_y - self.circle_y) ** 2) ** 0.5

            if distance < (self.circle_radius + 25):
                self.circle_x = random.randint(50, 750)
                self.circle_y = random.randint(50, 550)
                self.score += 1
                print(f"Score: {self.score}")
        return False

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.JOYBUTTONDOWN:
                    self.cube_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            x_axis = self.controller.get_axis(0)
            y_axis = self.controller.get_axis(1)

            self.velocity_x += x_axis * self.acceleration
            self.velocity_y += y_axis * self.acceleration

            self.velocity_x *= self.friction
            self.velocity_y *= self.friction

            self.cube_x += self.velocity_x * self.cube_speed
            self.cube_y += self.velocity_y * self.cube_speed

            self.cube_x = max(0, min(750, self.cube_x))
            self.cube_y = max(0, min(550, self.cube_y))

            # Handle gripper controls with L2 and R2
            l2_trigger = self.controller.get_axis(2)  # L2 axis
            r2_trigger = self.controller.get_axis(5)  # R2 axis

            if r2_trigger > 0.5:  # R2 pressed to open
                self.gripper_offset = min(self.gripper_max_offset, self.gripper_offset + self.gripper_speed)
                self.holding_ball = False
            elif l2_trigger > 0.5:  # L2 pressed to close
                self.gripper_offset = max(0, self.gripper_offset - self.gripper_speed)
                # Check if grippers enclose the ball
                left_grip_x = self.cube_x - 10 - self.gripper_offset
                right_grip_x = self.cube_x + 50 + self.gripper_offset
                grip_y_top = self.cube_y + 10
                grip_y_bottom = self.cube_y + 40

                if (left_grip_x < self.circle_x < right_grip_x and
                    grip_y_top < self.circle_y < grip_y_bottom):
                    self.holding_ball = True

            if self.holding_ball:
                self.circle_x = self.cube_x + 25
                self.circle_y = self.cube_y + 25

            if self.check_border_collision():
                running = self.show_game_over()

            self.screen.fill((0, 0, 0))

            # Draw circle (ball)
            pygame.draw.circle(self.screen, self.circle_color, 
                             (int(self.circle_x), int(self.circle_y)), 
                             self.circle_radius)

            # Draw cube
            pygame.draw.rect(self.screen, self.cube_color, 
                           (self.cube_x, self.cube_y, 50, 50))

            # Draw grippers
            pygame.draw.rect(self.screen, (200, 200, 200),
                           (self.cube_x - 10 - self.gripper_offset, self.cube_y + 10, 10, 30))
            pygame.draw.rect(self.screen, (200, 200, 200),
                           (self.cube_x + 50 + self.gripper_offset, self.cube_y + 10, 10, 30))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    GameController().run()