import pygame

# Initialize Pygame
pygame.init()
pygame.joystick.init()

# Set up display
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Joystick Detector")

# Initialize joysticks
joysticks = []
for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Detect joystick button events
        if event.type == pygame.JOYBUTTONDOWN:
            print(f"Joystick {event.joy} button {event.button} pressed")
        
        # Detect joystick axis motion
        if event.type == pygame.JOYAXISMOTION:
            print(f"Joystick {event.joy} axis {event.axis} value: {event.value:.2f}")
    
    # Fill screen with white
    screen.fill((255, 255, 255))
    pygame.display.flip()

# Quit Pygame
pygame.quit()