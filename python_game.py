#------------------------------------------------------------------importy-------------------------------------------------------
import pygame
from pygame.locals import *
import os.path
import sys
import random
import time
#------------------------------------------------------------- różne stałe ---------------------------------------------------------------

pygame.init()

screen_width = 1200
screen_height = 900
screen_size = (screen_width, screen_height)
screen = pygame.display.set_mode(screen_size)
menu_button_color = (200,200,200)
game_title = "Danger ahead"                                                          
pygame.display.set_caption(game_title)
road = pygame.image.load(os.path.join("assets", "road.png"))
line = pygame.image.load(os.path.join("assets", "line.png"))
line_width = 10
line_height = 90
car_width = 60
car_height = 108
other_car = pygame.transform.scale(pygame.image.load(os.path.join("assets", "other_car.png")), (car_width, car_height))
my_car = pygame.transform.scale(pygame.image.load(os.path.join("assets", "my_car.png")), (car_width,car_height))
heart = pygame.transform.scale(pygame.image.load(os.path.join("assets","heart.png")),(50, 50))
countdown = pygame.mixer.Sound(os.path.join("assets","countdown1.wav"))
soundtrack = pygame.mixer.Sound(os.path.join("assets","soundtrack.wav"))
crash = pygame.mixer.Sound(os.path.join("assets","crash.wav"))
death = pygame.mixer.Sound(os.path.join("assets","death.wav"))
fps = 60
start_pos = [ [-car_height,330], [-car_height,450], [-car_height,570], [-car_height,690], [-car_height,810] ]

#-----------------------------------------------------------  pomocnicze funkcje -----------------------------------------------------------------

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def message_display(text, width, height, size, anch):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    textSurf, text_rect = text_objects(text, largeText)
    if anch == "center":
        text_rect.center = (width, height)
    elif anch == "left":
        text_rect.midleft = (width, height)
    elif anch == "right":
        text_rect.midright = (width,height)
    screen.blit(textSurf, text_rect)

def window(mcr,heart_list,lines,current_car_list,score):
    screen.blit(road, (0,0))
    for i in range(len(lines)):
        screen.blit(line, (lines[i].x, lines[i].y))
    screen.blit(my_car, (mcr.x, mcr.y))
    for i in range(len(current_car_list)):
        screen.blit(other_car, (current_car_list[i].x, current_car_list[i].y))
    for i in range(len(heart_list)):
        screen.blit(heart, (heart_list[i].x, heart_list[i].y))
    message_display("Score: {}".format(score),20,50,48, "left")
    pygame.display.update()

def create_lines(lines):
    for i in range(1,5):
        for j in range (1,6):
            lines.append(pygame.Rect(300 + 120*i-line_width/2, -line_height + 200*j, line_width, line_height))

def move_lines(lines,score):
    for i in lines:
        i.y += 5 + 0.05*score
    if i.y > screen_height:
        lines.remove(i)

def move_cars(current_car_list,score):
    for i in current_car_list:
        i.y += 10 + 0.1*score
    if i.y > screen_height:
        current_car_list.remove(i)

def my_car_movement(keys_pressed, mcr,mcv):
    if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
        mcr.x -= mcv
        if mcr.x < 300:
            mcr.x = 300
    if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
        mcr.x += mcv
        if mcr.x > screen_width - car_width - 300:
            mcr.x = screen_width - car_width - 300
    if keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
        mcr.y += mcv
        if mcr.y > screen_height - car_height:
            mcr.y = screen_height - car_height
    if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
        mcr.y -= mcv
        if mcr.y < screen_height/2:
            mcr.y = screen_height/2

def remove_heart(heart_list,score):
    crash.play()
    if len(heart_list) > 1:
        heart_list.remove(heart_list[0])
    else:
        game_over(score)

def remove_car(current_car_list,mcr):
    for i in current_car_list:
        if pygame.Rect.colliderect(i, mcr) == True:
            current_car_list.remove(i)

def check_collision(mcr, current_car_list, heart_list,score):
    for i in current_car_list:
        if pygame.Rect.colliderect(i, mcr) == True:
            remove_heart(heart_list,score)
            remove_car(current_car_list,mcr)   

def update_highscore(score):
    with open("highscores.txt","r") as file:
        hl = file.readline().split(";")
        hl = [ int(x) for x in hl ]
        hl = sorted(hl, reverse=True)
        for i in range(len(hl)):
            if score >= hl[i]:
                hl = hl[0:i] + [score] + hl[i:-1]
                return hl
    return hl

def overwrite_highscore(score):
    hlist = update_highscore(score)
    text = ""
    for i in range(len(hlist)-1):
        text += str(hlist[i]) + ";"
    text += str(hlist[-1])
    with open("highscores.txt","w") as file:
        file.write(text)

#-------------------------------------------------------- funkcje odpowiedzialne za nowe ekrany -----------------------------------
            
def game_over(score):
    soundtrack.stop()
    death.play()
    lines = []
    create_lines(lines)
    screen.blit(road, (0,0))
    for i in range(len(lines)):
        screen.blit(line, (lines[i].x, lines[i].y))
    message_display("Game over", screen_width/2, 450, 115, "center")
    overwrite_highscore(score)
    pygame.display.update()
    time.sleep(5)
    death.stop()
    soundtrack.play()
    soundtrack.set_volume(0.5)
    main_menu()

def main_menu():
    score = 0
    lines = []
    create_lines(lines)
    menu_clock = pygame.time.Clock()
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        menu_clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_game_button.collidepoint((mouse_x, mouse_y)):
                        game()
                    if options_button.collidepoint((mouse_x, mouse_y)):
                        options()
                    if highscore_button.collidepoint((mouse_x, mouse_y)):
                        highscore()
                    if about_author_button.collidepoint((mouse_x, mouse_y)):
                        about_author()
                    if exit_button.collidepoint((mouse_x, mouse_y)):
                        sys.exit()
        screen.blit(road, (0,0))
        for i in range(len(lines)):
            screen.blit(line, (lines[i].x, lines[i].y))
        start_game_button = pygame.Rect(400, 200, 400, 75)
        pygame.draw.rect(screen, (menu_button_color), start_game_button)
        options_button = pygame.Rect(400, 325, 400, 75)
        pygame.draw.rect(screen, (menu_button_color), options_button)
        highscore_button = pygame.Rect(400, 450, 400, 75)
        pygame.draw.rect(screen, (menu_button_color), highscore_button)
        about_author_button = pygame.Rect(400, 575, 400, 75)
        pygame.draw.rect(screen, (menu_button_color), about_author_button)
        exit_button = pygame.Rect(400, 700, 400, 75)
        pygame.draw.rect(screen, (menu_button_color), exit_button)
        message_display("Start game", screen_width/2, 240, 48, "center")
        message_display("Options", screen_width/2, 365, 48, "center")
        message_display("Highscore", screen_width/2, 490, 48, "center")
        message_display("About author", screen_width/2, 615, 48, "center")
        message_display("Exit", screen_width/2, 740, 48, "center")     
        message_display(game_title, screen_width/2, 100, 115, "center")
        pygame.display.update()
        if lines[-1].y > 200:
            for i in range(1,5):
                lines.append(pygame.Rect(300 + 120*i-line_width/2, -line_height, line_width, line_height))
        move_lines(lines,score)

def game():
    mcr = pygame.Rect((screen_width-car_width)/2, screen_height-car_height-10, car_width, car_height)
    soundtrack.set_volume(0.2)
    start_time = time.time()
    pygame.display.update()
    current_car_list = []
    current_car_list.append(pygame.Rect(start_pos[random.randint(0,4)][1], start_pos[random.randint(0,4)][0], car_width, car_height))
    lines = []
    score = 0
    create_lines(lines)
    heart_list = []
    for j in range(1,4):
        heart_list.append(pygame.Rect(10 + 50*j, 100, 50,50))
    window(mcr,heart_list,lines,current_car_list,score)
    pygame.display.update()
    countdown.play()
    message_display("3", screen_width/2,450,115, "center")
    pygame.display.update()
    time.sleep(1)
    window(mcr,heart_list,lines,current_car_list,score)
    message_display("2", screen_width/2,450,115, "center")
    pygame.display.update()
    time.sleep(1)
    window(mcr,heart_list,lines,current_car_list,score)
    message_display("1", screen_width/2,450,115, "center")
    pygame.display.update()
    time.sleep(1)
    soundtrack.set_volume(0.5)         
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  
        keys_pressed = pygame.key.get_pressed()
        if lines[-1].y > 200:
            for i in range(1,5):
                lines.append(pygame.Rect(300 + 120*i-line_width/2, -line_height, line_width, line_height))
        try:
            if current_car_list[-1].y > 120:
                rng = random.randint(1,max(1,20 - int(score/4)))
                if rng == 1:
                    current_car_list.append(pygame.Rect(start_pos[random.randint(0,4)][1], start_pos[random.randint(0,1)][0], car_width, car_height))
        except:
            current_car_list.append(pygame.Rect(start_pos[random.randint(0,4)][1], start_pos[random.randint(0,1)][0], car_width, car_height))
        score = int((time.time()-start_time-3)*1.5)
        mcv = 10 + 0.03*score
        try:
            move_cars(current_car_list,score)
        except:
            pygame.display.update()
        my_car_movement(keys_pressed, mcr, mcv)
        move_lines(lines,score)
        check_collision(mcr, current_car_list, heart_list,score)
        window(mcr,heart_list,lines,current_car_list,score)
    pygame.quit()

def options():
    score = 0
    lines = []
    for i in range(1,5):
        for j in range (1,6):
            lines.append(pygame.Rect(300 + 120*i-line_width/2, -line_height + 200*j, line_width, line_height))
    clock = pygame.time.Clock()
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and go_back_button.collidepoint((mouse_x,mouse_y)):
                    main_menu()
        screen.blit(road, (0,0))
        for i in range(len(lines)):
            screen.blit(line, (lines[i].x, lines[i].y))
        option1 = pygame.Rect(400, 200, 400, 75)
        pygame.draw.rect(screen, (menu_button_color), option1)
        go_back_button = pygame.Rect(350, 750, 500,75)
        pygame.draw.rect(screen, (menu_button_color), go_back_button)
        message_display("Go back to menu", screen_width/2, 790, 48, "center") 
        pygame.display.update()
        if lines[-1].y > 200:
            for i in range(1,5):
                lines.append(pygame.Rect(300 + 120*i-line_width/2, -line_height, line_width, line_height))
        move_lines(lines,score)

def highscore():
    score = 0
    lines = []
    for i in range(1,5):
        for j in range (1,6):
            lines.append(pygame.Rect(300 + 120*i-line_width/2, -line_height + 200*j, line_width, line_height))
    clock = pygame.time.Clock()
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                     if go_back_button.collidepoint((mouse_x, mouse_y)):
                        main_menu() 
        screen.blit(road, (0,0))
        for i in range(len(lines)):
            screen.blit(line, (lines[i].x, lines[i].y))
        highscore_rect = pygame.Rect(400, 100, 400, 630)
        pygame.draw.rect(screen, (menu_button_color), highscore_rect)
        with open("highscores.txt","r") as file:
            hl= file.readline().split(";")
        for i in range(len(hl)):
            message_display("{}. ".format(i+1),550,140 + 60*i,48, "right")
            message_display("{}".format(hl[i]), 650, 140 + 60*i, 48, "center")
        go_back_button = pygame.Rect(350, 750, 500,75)
        pygame.draw.rect(screen, (menu_button_color), go_back_button)
        message_display("Go back to menu", screen_width/2, 790, 48, "center")
        pygame.display.update()
        if lines[-1].y > 200:
            for i in range(1,5):
                lines.append(pygame.Rect(300 + 120*i-line_width/2, -line_height, line_width, line_height))
        move_lines(lines,score)

def about_author():
    abt = "I'm Piotr Piwowar and I'm"
    abt1_5 =  "a student of the Wrocław"
    abt2 =  "University of Science" 
    abt2_5 = "and Technology. This is"
    abt3 = "my project for a"
    abt4 = "programming course."
    score = 0
    lines = []
    for i in range(1,5):
        for j in range (1,6):
            lines.append(pygame.Rect(300 + 120*i-line_width/2, -line_height + 200*j, line_width, line_height))
    clock = pygame.time.Clock()
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if go_back_button.collidepoint((mouse_x, mouse_y)):
                        main_menu() 
        screen.blit(road, (0,0))
        for i in range(len(lines)):
            screen.blit(line, (lines[i].x, lines[i].y))
        abt_rect = pygame.Rect(400, 100, 400, 430)
        pygame.draw.rect(screen, (menu_button_color), abt_rect)
        message_display(abt, 420, 140, 30, "left")
        message_display(abt1_5, 420, 180, 30, "left")
        message_display(abt2, 420, 220, 30, "left")
        message_display(abt2_5, 420, 260, 30, "left")
        message_display(abt3, 420, 300, 30, "left")
        message_display(abt4, 420, 340, 30, "left")
        go_back_button = pygame.Rect(350, 750, 500,75)
        pygame.draw.rect(screen, (menu_button_color), go_back_button)
        message_display("Go back to menu", screen_width/2, 790, 48, "center")
        pygame.display.update()
        if lines[-1].y > 200:
            for i in range(1,5):
                lines.append(pygame.Rect(300 + 120*i-line_width/2, -line_height, line_width, line_height))
        move_lines(lines,score)

soundtrack.play()
soundtrack.set_volume(0.5)
main_menu()
