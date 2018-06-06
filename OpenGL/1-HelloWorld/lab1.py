import pygame

pygame.init()

WHITE = (255,255,255)

render = pygame.display.set_mode((800,600))
done = False
x = 500
y = 100
width = 100
height = 100
while not done:
    render.fill((0,0,0))
    pygame.Rect(2, 0, 1, 2)

    pygame.draw.rect(render, WHITE, (x,y,width,height))

    pygame.display.flip()

    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            done = True
        if pressed[pygame.K_RIGHT]:
            x+=20
        if pressed[pygame.K_DOWN]:
            y+=20
        if pressed[pygame.K_UP]:
            y-=20
        if pressed[pygame.K_LEFT]:
            x-=20
        if pressed[pygame.K_SPACE]:
            width+=20
            height+=20
    pass
