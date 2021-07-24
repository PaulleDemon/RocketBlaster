import AssetPaths
import Colors
import pygame
import math

pygame.init()

WIDTH, HEIGHT = size = (800, 600)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("RocketBlaster")

running = True
clock = pygame.time.Clock()

rocket_image = pygame.image.load(AssetPaths.ROCKET)
missile_image = pygame.image.load(AssetPaths.MISSILE)

missiles = []

rocket_pos = (screen.get_width() / 2, screen.get_height() - rocket_image.get_height() - 50)

rect = rocket_image.get_rect()
rocket_center = (rect.centery + rocket_pos[0]), (rect.centerx + rocket_pos[1])

rocket_angle = 0

bullet_speed = 5
max_bullets = 2
missile_angle = rocket_angle


class Missile:

    def __init__(self, angle=0, bx=0, by=0):
        self.bullet_x = bx
        self.bullet_y = by
        self.angle = angle
        self.bullet_pos = rocket_pos


def fire_bullet():

    for x in missiles:
        missile = pygame.transform.rotate(missile_image, -x.angle)
        screen.blit(missile, x.bullet_pos)


def get_bullet_pos(mousepos: tuple[float, float]):
    mouse_x, mouse_y = mousepos

    if mouse_x > screen.get_width() - 100:
        mouse_x = screen.get_width() - 100

    elif mouse_x < 100:
        mouse_x = 100

    if mouse_y > screen.get_height() - 250:
        mouse_y = screen.get_height() - 250

    adj_dist = mouse_x - rocket_center[0]
    opp_dist = mouse_y - rocket_center[1]

    hyp = math.sqrt(opp_dist**2 + adj_dist**2)

    return adj_dist, opp_dist, hyp


def rocket(mousepos: tuple[float, float]):
    global rocket_angle, rocket_pos

    adj_dist, opp_dist, hyp = get_bullet_pos(mousepos)

    rocket_angle = math.degrees(math.atan2(opp_dist, -adj_dist)) + 90
    rotated = pygame.transform.rotate(rocket_image, rocket_angle)

    screen.blit(rotated, rocket_pos)


while running:

    screen.fill(color=Colors.BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if len(missiles) < max_bullets:
                adj_dist, opp_dist, hyp = get_bullet_pos(pygame.mouse.get_pos())

                bullet_x = adj_dist / hyp * bullet_speed
                bullet_y = opp_dist / hyp * bullet_speed

                missel = Missile(-rocket_angle, bullet_x, bullet_y)
                missiles.append(missel)

                print(len(missiles))

    rocket(pygame.mouse.get_pos())
    fire_bullet()

    for bullet in missiles.copy():
        if 0 < bullet.bullet_pos[0] > screen.get_width() or bullet.bullet_pos[1] < 0:
            missiles.remove(bullet)

        else:
            bullet.bullet_pos = (bullet.bullet_x + bullet.bullet_pos[0], bullet.bullet_y + bullet.bullet_pos[1])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
