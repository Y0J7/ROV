import pygame

pygame.init()
pygame.joystick.init()

print("Available Joysticks:")
for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    print(f"{i}: {joystick.get_name()}")
    print(f"  Axes: {joystick.get_numaxes()}")
    print(f"  Buttons: {joystick.get_numbuttons()}")
    print(f"  Hats: {joystick.get_numhats()}")
    print(f"  Balls: {joystick.get_numballs()}")
    print(f"  GUID: {joystick.get_guid()}")
    print(f"  ID: {joystick.get_id()}")
    print(f"  Instance ID: {joystick.get_instance_id()}")
