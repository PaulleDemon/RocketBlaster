import AssetPaths
import Colors
import pygame
import math

pygame.init()

WIDTH, HEIGHT = size = (800, 600)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Rocket")

running = True
clock = pygame.time.Clock()

rocket_image = pygame.image.load(AssetPaths.ROCKET)
missile_image = pygame.image.load(AssetPaths.MISSILE)
rocket_pos = (screen.get_width()/2, screen.get_height()-rocket_image.get_height()-50)
rect = rocket_image.get_rect()
rocket_center = (rect.centery + rocket_pos[0]), (rect.centerx + rocket_pos[1])

print(rocket_pos)
bullet_pos = rocket_pos
bullet_x, bullet_y = 0, 0

rocket_angle = 0

bullet_speed = 10
missile_angle = rocket_angle

fired = False


def fire_bullet():
    global fired

    if fired:
        bullet = pygame.transform.rotate(missile_image, -missile_angle)
        screen.blit(bullet, bullet_pos)


def rocket(mousepos: tuple[float, float]):
    global rocket_angle, rocket_dir, bullet_x, bullet_y, rocket_pos

    mouse_x, mouse_y = mousepos

    if mouse_x > screen.get_width() - 100:
        mouse_x = screen.get_width() - 100

    elif mouse_x < 100:
        mouse_x = 100

    if mouse_y > screen.get_height() - 250:
        mouse_y = screen.get_height() - 250

    adj_dist = mouse_x - rocket_center[0]
    opp_dist = mouse_y - rocket_center[1]

    rocket_angle = math.degrees(math.atan2(opp_dist, -adj_dist)) + 90
    # print(rocket_angle, mouse_x, mouse_y)

    if not fired:
        hyp = math.hypot(opp_dist, adj_dist)

        bullet_x = adj_dist/hyp * bullet_speed
        bullet_y = opp_dist/hyp * bullet_speed

    rotated = pygame.transform.rotate(rocket_image, rocket_angle)

    screen.blit(rotated, rocket_pos)


while running:

    screen.fill(color=Colors.BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif not fired and event.type == pygame.MOUSEBUTTONDOWN:

            # if -43 <= rocket_angle <= 43:
            fired = True
            missile_angle = -rocket_angle

    rocket(pygame.mouse.get_pos())
    fire_bullet()

    if fired:
        if 0 < bullet_pos[0] > screen.get_width() or bullet_pos[1] < 0:
            fired = False
            bullet_pos = rocket_pos

        else:

            bullet_pos = (bullet_x+bullet_pos[0], bullet_y+bullet_pos[1])
            # print(bullet_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
