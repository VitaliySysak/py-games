import pygame
import sys

MEDIUM_AQUAMARINE_COLOR = (111, 196, 169)

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"{current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)

    return current_time

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('My game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

sky_surf = pygame.image.load('./graphics/Sky.png').convert_alpha()
ground_surf = pygame.image.load('./graphics/ground.png').convert_alpha()

score_surf = test_font.render('My game', False, (60, 60, 60))
score_rect = score_surf.get_rect(center=(400, 50))

#Obstacles
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom=(800, 232))

obstacle_list = []

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(50, 232))

player_gravity = 0

#Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render("Pixel Runner", False, MEDIUM_AQUAMARINE_COLOR)
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press space to run', False, MEDIUM_AQUAMARINE_COLOR)
game_message_rect = game_message.get_rect(center=(400, 330))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if player_rect.collidepoint(mouse_pos) and player_rect.bottom >= 232:
                    player_gravity = -20 
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 232:
                        player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)
        if event.type == obstacle_timer and game_active:
            obstacle_list.append(snail_surf.get_rect(midbottom=(800, 232)))

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 232))
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        # screen.blit(score_surf, score_rect)
        score = display_score()

        snail_rect.x -= 4
        screen.blit(snail_surf, snail_rect)
        screen.blit(player_surf, player_rect)

        if snail_rect.right <= 0:
            snail_rect.left = 800
        
        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom >= 232:
            player_rect.bottom = 232

        if player_rect.colliderect(snail_rect):
            game_active = False

    else:
        screen.fill((94, 129, 162))
        screen.blit(game_name, game_name_rect)
        score_message = test_font.render(f'Your score: {score}', False, MEDIUM_AQUAMARINE_COLOR)
        score_message_rect = score_message.get_rect(center=(400, 330))
        if score:
            screen.blit(score_message, score_message_rect)
        else:
            screen.blit(game_message, game_message_rect)
        screen.blit(player_stand, player_stand_rect)

    pygame.display.update()
    clock.tick(60)
