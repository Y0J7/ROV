import pygame
import time

pygame.init()
pygame.joystick.init()

arry = [0, 0, 0, 0,0,0]
x = []
buttons = [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0]
prev_buttons = [0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0]
states = [0,0,0,0]
speed = 1
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    
    try:
        while True:
        
            pygame.event.pump()
            for i in range(joystick.get_numaxes()):
                axis = joystick.get_axis(i)
                buttons[i] = joystick.get_button(i)
                arry[i] = axis
            # print(buttons)
             
            motion = "N"

            x = arry[:4]
            if x[1] < -0.4:
                motion = "F"
            elif x[1] > 0.4:
                motion = "B"
            elif x[0] < -0.4:
                motion = "L"
            elif x[0] > 0.4:
                motion = "R"
            elif x[2] < -0.4:
                motion = "l"
            elif x[2] > 0.4:
                motion = "r"
            elif x[3] < -0.4:
                motion = "u"
            elif x[3] > 0.4:
                motion = "d"
            if buttons != prev_buttons:
                if buttons[0] == 1:
                    states[0] = int(not states[0])
                elif buttons[1] == 1:
                    states[1] = int(not states[1])
                elif buttons[2] == 1:
                    states[2] = int(not states[2])
                elif buttons[3] == 1:
                    states[3] = int(not states[3])
                prev_buttons = buttons.copy()
            
            if joystick.get_button(11)== 1:
                speed += 1
            elif joystick.get_button(12) == 1:
                speed -= 1
            print(f"{motion},{states[0]},{states[1]},{states[2]},{states[3]},{speed}")
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nExiting...")
else:
    print("No joystick found")

pygame.quit()

