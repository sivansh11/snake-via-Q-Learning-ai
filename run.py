from dql import *


size = 40

q = QL(size)
q.load(open('q.p', 'rb'))
q.size = size
s = SnakeGame(size)
s.change_food_pos()


keytick = 0
update = 0
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill((0, 0, 0))

    s.show()

    moves = [UP, RIGHT, LEFT]
    q.snake = s
    s.move(moves[q.get_trained_move()])

    dead, f = s.update()
    if dead:
        s.reset()

    # print(s.get_state())

    pygame.display.flip()
pygame.quit()

