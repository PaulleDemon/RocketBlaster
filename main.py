import math
import random
import pygame

import AssetPaths
import Colors

pygame.init()

WIDTH, HEIGHT = size = (800, 600)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("RocketBlaster")

running = True
game_over = False

clock = pygame.time.Clock()

rocket_image = pygame.image.load(AssetPaths.ROCKET)
missile_image = pygame.image.load(AssetPaths.MISSILE)
monster_image = pygame.image.load(AssetPaths.SPACE_MONSTER)

rocket_pos = (screen.get_width() / 2, screen.get_height() - rocket_image.get_height() - 50)

rect = rocket_image.get_rect()
rocket_center = (rect.centery + rocket_pos[0]), (rect.centerx + rocket_pos[1])

rocket_angle = 0

bullet_speed = 5
max_bullets = 5
missile_angle = rocket_angle

counter = 60
monster_spawn_counter = counter  # spans after 30 seconds
max_monsters = max_bullets - 1
monster_speed = 1

bullet_lst = []
monster_lst = []

score = 0
score_font = pygame.font.SysFont('Consolas', 30)
game_over_font = pygame.font.SysFont('Times', 50, True)

pygame.mixer.init()
shoot_sound = pygame.mixer.Sound(AssetPaths.GUNSHOT)
shoot_sound.set_volume(0.5)

death_sound = pygame.mixer.Sound(AssetPaths.MONSTER_DEATH)
death_sound.set_volume(0.5)


class Missile:

    def __init__(self, angle=0, bx=0, by=0):
        self.bullet_x = bx
        self.bullet_y = by
        self.angle = angle
        self.bullet_pos = rocket_pos


class SpaceMonster:

    def __init__(self, init_pos=(0, 0)):
        self.pos = init_pos


def create_monsters():
    global monster_spawn_counter

    monster_spawn_counter -= 1

    if monster_spawn_counter < 0:
        monster_spawn_counter = 0

    if len(monster_lst) < max_monsters and monster_spawn_counter == 0:
        rand_x = random.randint(50, screen.get_width() - 100)
        rand_y = random.randint(50, 150)

        monster = SpaceMonster((rand_x, rand_y))
        monster_lst.append(monster)
        monster_spawn_counter = counter


def detect_collisions():
    global score

    for monster in monster_lst.copy():

        monster_rect = monster_image.get_rect()

        monster_rect[0] += monster.pos[0]
        monster_rect[1] += monster.pos[1]
        monster_rect[2] += monster.pos[0]
        monster_rect[3] += monster.pos[1]

        for bullet in bullet_lst.copy():

            if monster_rect[0] < bullet.bullet_pos[0] < monster_rect[2] and \
                    (monster_rect[1] < bullet.bullet_pos[1] < monster_rect[3]):

                try:
                    monster_lst.remove(monster)
                    bullet_lst.remove(bullet)
                    death_sound.play()

                except ValueError:
                    pass

                score += 1


def move_monsters():
    global game_over
    for monster in monster_lst:
        monster.pos = monster.pos[0], monster.pos[1] + monster_speed
        screen.blit(monster_image, monster.pos)

        if monster.pos[1] > screen.get_height() - 100:
            game_over = True


def move_bullet():
    for bullet in bullet_lst:
        rotated_bullet = pygame.transform.rotate(missile_image, -bullet.angle)
        screen.blit(rotated_bullet, bullet.bullet_pos)


def get_adj_opp(mousepos: tuple[float, float]):
    mouse_x, mouse_y = mousepos

    if mouse_x > screen.get_width() - 100:
        mouse_x = screen.get_width() - 100

    elif mouse_x < 100:
        mouse_x = 100

    if mouse_y > screen.get_height() - 100:
        mouse_y = screen.get_height() - 100

    adj_dist = mouse_x - rocket_center[0]
    opp_dist = mouse_y - rocket_center[1]

    hyp = math.sqrt(opp_dist ** 2 + adj_dist ** 2)

    return adj_dist, opp_dist, hyp


def rocket(mousepos: tuple[float, float]):
    global rocket_angle, rocket_pos

    adj_dist, opp_dist, hyp = get_adj_opp(mousepos)

    rocket_angle = math.degrees(math.atan2(opp_dist/hyp, -adj_dist/hyp)) + 90
    rotated = pygame.transform.rotate(rocket_image, rocket_angle)

    screen.blit(rotated, rocket_pos)


def change_game_speed():
    global monster_speed, counter, max_monsters, max_bullets

    if score > 0:
        if score % 50 == 0:
            monster_speed += 0.001

        if score % 100 == 0 and counter > 20:
            counter -= 1

        if counter == 20:
            counter = 50

        if score % 125 == 0:
            max_monsters += 1
            max_bullets += 1


while running:

    screen.fill(color=Colors.BLACK)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if len(bullet_lst) < max_bullets:
                adj_dist, opp_dist, hyp = get_adj_opp(pygame.mouse.get_pos())

                bullet_x = adj_dist / hyp * bullet_speed
                bullet_y = opp_dist / hyp * bullet_speed

                bullet = Missile(-rocket_angle, bullet_x, bullet_y)
                bullet_lst.append(bullet)

                shoot_sound.play()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                score = 0
                monster_lst = []
                bullet_lst = []

    rocket(pygame.mouse.get_pos())

    if not game_over:
        move_bullet()
        create_monsters()
        move_monsters()
        detect_collisions()

        change_game_speed()

    else:
        screen.blit(game_over_font.render("Game over.", True, (255, 255, 255)), (100, screen.get_height() / 3))
        screen.blit(game_over_font.render("Press Space to play again", True, (255, 255, 255)), (100, screen.get_height() / 2))

    screen.blit(score_font.render(f"Score: {score}", True, (255, 255, 255)), (screen.get_width()-200, 50))

    for bullet in bullet_lst.copy():
        if 0 < bullet.bullet_pos[0] > screen.get_width() or bullet.bullet_pos[1] < 0:
            bullet_lst.remove(bullet)

        else:
            bullet.bullet_pos = (bullet.bullet_x + bullet.bullet_pos[0], bullet.bullet_y + bullet.bullet_pos[1])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
