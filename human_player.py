from Snake import SnakeGame
from Pygame import *


s = SnakeGame(10)
s.change_food_pos()


keytick = 0
update = 0
run = True
while run:
    clock.tick(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill((0, 0, 0))

    s.show()
    keytick += 1
    pressed = s.input(keytick)
    if pressed:
        keytick = 0

    update += 1
    if update > 20:
        update = 0
        dead, f = s.update()
        if dead:
            run = False

    # print(s.x_speed, s.y_speed)

    pygame.display.flip()
pygame.quit()
