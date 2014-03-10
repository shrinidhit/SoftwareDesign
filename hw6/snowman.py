# -*- coding: utf-8 -*-
"""
SoftwareDesign HW6 - Video Game
Olin Snowman: A game for protecting Olin Snowman from Babsoners!

Created on Fri Mar  7 20:18:57 2014

@author:
    SeongHyeok Im
    Shrinidhi Thirumalai
    Inseong Joe

@note:
    Code-style:
        - Camelcase for function and class.
        - Underscore for variable.
        - Prefix 'g_' for global viarlable.
"""

############################################################################
# Imports
############################################################################

import pygame
from pygame.locals import *
import random
import math
import time
import sys, traceback

############################################################################
# Global variabless
############################################################################

# File paths
g_snowman_path = "./image/snowman.png"
g_babsoner_path = "./image/babsoner.png"
g_babsoner_flip_path = "./image/babsoner_flip.png"
g_babsoner_pink_path = "./image/babsoner_pink.png"
g_babsoner_pink_flip_path = "./image/babsoner_pink_flip.png"

g_wreck_video_path = "./video/wreck_edit_use.mpg"
g_music_jamesbond_path = "./music/jamesbond.mp3"
g_music_pinkpanther_path = "./music/pinkpanther.mp3"

# Screen
g_screen_width = 640
g_screen_height = 640

# Snowman
g_snowman_width = 50
g_snowman_height = 100
g_snowman_vx = 0
g_snowman_lives = 5

# Bansoner
g_babsoner_width = 60
g_babsoner_height = 45
g_babsoner_vy = 5

g_babsoner_vy_increase = 0.6
g_babsoner_vy_max = 17
g_babsoner_vy_pink_factor = 1.3
g_babsoner_magnify_max = 150    # percentile

g_max_babsoner = 10
g_num_rmvd_babsoners = 0

# Global variables
g_time = 0
g_level = 1
g_max_level = 20
# create is invoked every 50ms so if 10, 10*50ms = 500ms
g_create_checker_list = [
    20, 20, 19, 18, 17, 16, 15, 14, 13, 12,
    11, 10,  9,  8,  7,  7,  6,  6,  6,  5,
     4
]
g_create_checker_list_max = max(g_create_checker_list)

############################################################################
# Model Classes
############################################################################

class SnowManModel:
    """ Encodes overall game state of Snowman game """
    def __init__(self):
        # initialize
        self.babsoners = []
        self.snowman = SnowMan(g_snowman_width,
                               g_snowman_height,
                               (g_screen_width / 2 - g_snowman_width / 2),
                               (g_screen_height - g_snowman_height),
                               g_snowman_vx,
                               g_snowman_lives)
        self.score = 0
        self.snowman.printAll()

    def createBabsoner(self, vy):
        if len(self.babsoners) < g_max_babsoner:
            babson = Babsoner(g_babsoner_width,
                              g_babsoner_height,
                              random.randint(0, g_screen_width - g_babsoner_width),
                              0,
                              g_babsoner_vy,
                              True,
                              False)
            self.babsoners.append(babson)
            print "Babsoner Created! - %d" % (len(self.babsoners))
        else:
            for babsoner in self.babsoners:
                if babsoner.is_visible == False:
                    r_pink = random.randint(0, 7)

                    # Width and height are generated randomly if level >= 3
                    width = g_babsoner_width
                    height = g_babsoner_height
                    if g_level >= 3:
                        r = random.randint(90, 100 + g_level * 5)
                        if r > 100:
                            r = (g_babsoner_magnify_max) if (r > g_babsoner_magnify_max) else (r)
                            width = int(width * float(r / 100.0))
                            height = int(height * float(r / 100.0))

                    # X coordinate is generated randomly but centered to current location of snowman
                    if r_pink == 0:
                        # Pink one is coming much closer!
                        min_x = model.snowman.x - int(g_screen_width / 6.0)
                        max_x = model.snowman.x + int(g_screen_width / 6.0)
                    else:
                        min_x = model.snowman.x - int(g_screen_width / 3.0)
                        max_x = model.snowman.x + int(g_screen_width / 3.0)
                    if min_x < 0:
                        max_x += -(min_x)
                        min_x = 0
                    if max_x > g_screen_width - width:
                        min_x -= max_x - (g_screen_width - width)
                        max_x = g_screen_width - width

                    # Reset babsoner
                    if r_pink == 0:  # Pink!
                        babsoner.reset(width,
                                       height,
                                       random.randint(min_x, max_x),
                                       0,
                                       int(g_babsoner_vy * g_babsoner_vy_pink_factor),
                                       True)
                    else:
                        babsoner.reset(width,
                                       height,
                                       random.randint(min_x, max_x),
                                       0,
                                       g_babsoner_vy,
                                       False)
                    break

    def getScore(self, num_rmvd_babsoners):
        return self.score

class SnowMan:
    """ Encodes state of snowman """
    def __init__(self, width, height, x, y, vx, lives):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vx = vx
        self.lives = lives
        self.image = pygame.transform.scale(pygame.image.load(g_snowman_path), (self.width, self.height))

    def printAll(self):
        print "== Snowman =="
        print "width:", self.width
        print "height:", self.height
        print "x:", self.x
        print "y:", self.y
        print "vx:", self.vx
        print "lives:", self.lives
        print "============="

class Babsoner:
    """ Encodes state of babsoner """
    def __init__(self, width, height, x, y, vy, is_visible, is_pink):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vy = vy
        self.is_visible = is_visible
        self.is_pink = is_pink

        r = random.randint(0, 2)
        image = None
        if is_pink:
            if r == 0:
                image = pygame.image.load(g_babsoner_pink_flip_path)
            else:
                image = pygame.image.load(g_babsoner_pink_path)
        else:
            if r == 0:
                image = pygame.image.load(g_babsoner_flip_path)
            else:
                image = pygame.image.load(g_babsoner_path)

        self.image = pygame.transform.scale(image, (self.width, self.height))
        # Make image transparent
        alpha = 255
        self.image.fill((211, 242, 241, alpha), None, pygame.BLEND_RGBA_MULT)

    def reset(self, width, height, x, y, vy, is_pink):
        self.__init__(width, height, x, y, vy, True, is_pink)

############################################################################
# View Classes
############################################################################

class SnowManView:
    """ A view of brick breaker rendered in a Pygame window """
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def draw(self):
        # Filling Background Color
        self.screen.fill(pygame.Color(211, 242, 241))

        # Display current information: lives, level and score
        font = pygame.font.Font(None, 36)
        text = font.render("Lives: %d / Level: %d / Score: %d" % (model.snowman.lives, g_level, self.model.score), \
                           1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = g_screen_width / 2
        screen.blit(text, textpos)

        # Displaying Snowman
        screen.blit(self.model.snowman.image, (model.snowman.x, model.snowman.y))

        # Displaying Babsoners
        for babsoner in self.model.babsoners:
            if babsoner.is_visible == True:
                #print "Babsoner Displayed!"
                try:
                    screen.blit(babsoner.image, (babsoner.x, babsoner.y))
                except:
                    print "x: %d / y: %d", (babsoner.x, babsoner.y)
                    traceback.print_exc(file=sys.stdout)
                    sys.exit(1)
        pygame.display.flip()

    def drawScore(self):
        # Filling Background Color
        size = (g_screen_width, g_screen_height)
        screen = pygame.display.set_mode(size)
        screen.fill(pygame.Color(211, 242, 241))

        # Display current information: lives, level and score
        font = pygame.font.Font(None, 40)
        text = font.render("Level Reached: %d / Your Score: %d" % (g_level, self.model.score), \
                           1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = g_screen_width / 2
        textpos.centery = g_screen_height/2
        screen.blit(text, textpos)
        #updating
        pygame.display.flip()

    def playMovie(self):
        """ """
        FPS = 60
        clock = pygame.time.Clock()
        movie = pygame.movie.Movie(g_wreck_video_path)
        movie.skip(41.5)
        size = (g_screen_width, g_screen_height)
        screen = pygame.display.set_mode(size)
        #screen = pygame.display.set_mode(movie.get_size())
        #movie_screen = pygame.Surface(movie.get_size()).convert()
        movie_screen = pygame.Surface(size).convert()
        movie.set_display(movie_screen)
        movie.play()
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    movie.stop()
                    playing = False
            #print 'current:' + str(movie.get_time())
            #print 'total:' + str(movie.get_length())
            if movie.get_time() >= movie.get_length() - 42:
                movie.stop()
                playing = False
            screen.blit(movie_screen,(0,0))
            pygame.display.update()
            clock.tick(FPS)

    def showScore(self):
        """ """
        chart_showing = True
        while chart_showing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    chart_showing = False
            view.drawScore()

class SnowManPreview:
    """ Pre-game sequence """
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def draw(self):
        # Filling Background Color
        self.screen.fill(pygame.Color(211, 242, 241))

        # Display title
        font = pygame.font.Font(None, 40)
        title = font.render("Mission: Defend the Olin Snowman", 1, (10, 10, 10))
        textpos = title.get_rect()
        textpos.centerx = g_screen_width / 2
        textpos.centery = g_screen_height / 3
        screen.blit(title, textpos)

        # Display subtitle
        font = pygame.font.Font(None, 20)
        subtitle = font.render("Instructions: Use your mouse to dodge the babson beavers. Keep the Olin Snowman Alive", 1, (10, 10, 10))
        subtextpos = subtitle.get_rect()
        subtextpos.centerx = g_screen_width/2
        subtextpos.centery = g_screen_height/2
        screen.blit(subtitle, subtextpos)

        pygame.display.flip()

############################################################################
# Controller Classes
############################################################################

class SnowManMouseController:
    """ """
    def __init__(self, model):
        self.model = model

    def handleMouseEvent(self, event):
        if event.type == MOUSEMOTION:
            self.model.snowman.x = event.pos[0] - (self.model.snowman.width / 2.0)
            self.model.snowman.y = event.pos[1] - (self.model.snowman.height / 2.0)

class SnowManBabsonerController:
    """ """
    def __init__(self, model):
        self.model = model

    def update(self):
        """ """
        for babsoner in self.model.babsoners:
            babsoner.y += babsoner.vy
            if babsoner.y > g_screen_height and babsoner.is_visible == True:
                global g_num_rmvd_babsoners
                g_num_rmvd_babsoners += 1
                babsoner.is_visible = False
                self.model.score += g_level

    def create(self):
        """ """
        self.model.createBabsoner(g_babsoner_vy)

class SnowManCollisionController:
    """ """
    def __init__(self, model):
        self.model = model

    def check(self):
        """ Check collision between snowman and babsoner """
        # Rect(left, top, width, height) -> Rect
        # Rect((left, top), (width, height)) -> Rect
        rect_snowman = pygame.Rect(model.snowman.x, model.snowman.y, model.snowman.width, model.snowman.height)
        for babsoner in self.model.babsoners:
            if babsoner.is_visible == True:
                rect = pygame.Rect(babsoner.x, babsoner.y, babsoner.width, babsoner.height)
                if rect.colliderect(rect_snowman):
                    if babsoner.is_pink:
                        model.snowman.lives -= 2
                    else:
                        model.snowman.lives -= 1

                    babsoner.is_visible = False
                    print "Collision! - remaining lives: %d" % (model.snowman.lives)

class SnowManMusicController:
    def __init__(self):
        self.jamesbond = None
        self.pinkpanther = None
        pygame.mixer.music.load(g_music_jamesbond_path)
        pygame.mixer.music.set_volume(1.0) #value between 0.0 and 1.0

    def playMusic(self, loop,start):
        pygame.mixer.music.play(loop, start)

    def stopMusic(self):
        pygame.mixer.music.stop()

    def pauseMusic(self):
        pygame.mixer.music.pause()

    def changeMusisc(self):
        if g_level % 10 == 1:
            self.stopMusic()
            pygame.mixer.music.load(g_music_jamesbond_path)
            self.playMusic(-1, 0.0)
            self.jamestime = pygame.mixer.music.get_pos()
        if g_level % 10 == 6:
            self.stopMusic()
            pygame.mixer.music.load(g_music_pinkpanther_path)
            self.playMusic(-1, 0.0)
            self.panthertime = pygame.mixer.music.get_pos()
        if g_level % 10 == range(2, 6):
            pygame.mixer.music.load(g_music_jamesbond_path)
            pygame.mixer.music.set_pos(self.jamestime)
            self.playMusic(-1, self.jamestime)
            newtime = pygame.mixer.music.get_pos()
            self.jamestime += newtime
        if g_level % 10 == range(6, 11):
            pygame.mixer.music.load(g_music_pinkpanther_path)
            pygame.mixer.music.set_pos(self.panthertime)
            self.playMusic(-1, self.panthertime)
            newwtime = pygame.mixer.music.get_pos()
            self.panthertime += newwtime

############################################################################
# Main
############################################################################

if __name__ == "__main__":
    pygame.init()

    # Initialize screen
    size = (g_screen_width, g_screen_height)
    screen = pygame.display.set_mode(size)

    # MVC objects
    model = SnowManModel()
    view = SnowManView(model, screen)
    preview = SnowManPreview(model, screen)
    controller_mouse = SnowManMouseController(model)
    controller_babsoner = SnowManBabsonerController(model)
    controller_collision = SnowManCollisionController(model)
    controller_music = SnowManMusicController()

    # Play music
    controller_music.playMusic(-1, 0.0)

    # Create timer event for preview
    pygame.time.set_timer(USEREVENT + 1, 1000)

    # Preview
    while g_time < 5:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == USEREVENT + 1:
                g_time += 1
        preview.draw()

    # Create timer event for user events
    pygame.time.set_timer(USEREVENT + 1, 40)
    pygame.time.set_timer(USEREVENT + 2, 50)
    pygame.time.set_timer(USEREVENT + 3, 7000)    # every 8 seconds
    create_checker = 1

    # Running loop
    running = True
    quit_from_game = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_from_game = False
                running = False
                break

            if event.type == MOUSEMOTION:
                controller_mouse.handleMouseEvent(event)

            if event.type == USEREVENT + 1:
                controller_babsoner.update()
                controller_collision.check()

            if event.type == USEREVENT + 2:
                if create_checker % g_create_checker_list[g_level] == 0:
                    controller_babsoner.create()
                    create_checker = 1
                else:
                    create_checker += 1
                    if create_checker > g_create_checker_list_max:
                        create_checker = 1
                #print create_checker

            if event.type == USEREVENT + 3:
                if g_babsoner_vy < g_babsoner_vy_max:
                    g_babsoner_vy += g_babsoner_vy_increase
                if g_level < g_max_level:
                    g_level += 1
                    print "Level UP!"
                controller_music.changeMusisc()
        view.draw()
        time.sleep(.001)

        if model.snowman.lives <= 0:
            running = False

    pygame.mixer.quit()

    if quit_from_game:
        # Play wrecking ball movie
        view.playMovie()

    view.showScore()

    pygame.quit()
