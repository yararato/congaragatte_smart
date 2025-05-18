#python -m pygbag congara_web2

import pygame
import sys
import math
import random
import asyncio

import webbrowser
import urllib.parse

fall_flag = False #落ちたことのフラグ
endless_flag = False

chk_0_A = True
chk_0_C = True
chk_0_T = True

chk_0 = True
 
chk_goal_A = False
chk_goal_C = False
chk_goal_T = False

chk_Lastgoal_C = False #False=ゴールしていない
chk_Lastgoal_T = False #False=ゴールしていない

chk_goal = False

index = 0
stage = 1
generated = []
life = 3

key_spc = 0

enshutsu = -200

en_ind = 1 #ページの進行
en_timer1 = 120

#音声関係
kansei = 0
messe = 0
bloomy = 0

tuto_ind = 1
con_ind = 3
SOUSA_MODE = 1


#=====SE======
se_jump = None
se_turn = None
se_fall = None


#=====col=====
RED = (255, 0, 0)
YELLOW = (255,255,128)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255, 255, 255)

PINK = (255,0,192)
NAVY = (0, 0, 64)
COLOR_A = (245, 66, 117)
COLOR_C = (160, 160, 160)
COLOR_T = (231, 91, 236)
#キャラの動き============================================
class Move_Amana: #済
    def __init__(self):
        self.ground = 125
        self.x_amana = 0 #甘奈の位置
        self.h = 50
        self.y = self.ground - self.h #(甘奈の縦幅)
        
        
        self.speed = 1
        self.land = True
        self.fall_flag = False

        self.jump_timer = 30
        self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.turn = False
        self.turn_int = 1

        self.t_draw = 0

        self.t_turn = 0 #方向切り替えタイマー
        self.canTurn = True

        self.height = 40 #ジャンプ高さ

        self.canJump = True
        self.t_canjump = 0

        self.t_move = 0
        self.t_jump = 0

        self.radPerFrame = 2 * math.pi  / 60

        self.run_amana = [
                pygame.image.load("character/amana0.png"),
                pygame.image.load("character/amana1.png"),
                pygame.image.load("character/amana2.png"),
                pygame.image.load("character/amana3.png"),
                ]
        self.jump_amana= [
                None,
                pygame.image.load("character/amana_up.png"),
                pygame.image.load("character/amana_down.png"),
                ]

        self.run_han_amana = [
                pygame.image.load("character/hantai_amana0.png"),
                pygame.image.load("character/hantai_amana1.png"),
                pygame.image.load("character/hantai_amana2.png"),
                pygame.image.load("character/hantai_amana3.png"),
                ]

        self.jump_han_amana =[
                None,
                pygame.image.load("character/hantai_amana_up.png"),
                pygame.image.load("character/hantai_amana_down.png"),            
                ]

        self.stand_amana =[
                pygame.image.load("character/amana_stand_left.png"),
                pygame.image.load("character/hantai_amana_up.png"),
                pygame.image.load("character/hantai_amana_down.png"), 

                pygame.image.load("character/amana_stand_right.png"),            
                ]        
        pygame.init()
        pygame.mixer.init()
        self.se_jump = pygame.mixer.Sound("sound/jump.ogg")
        self.se_turn = pygame.mixer.Sound("sound/turn.ogg")
        self.se_fall = pygame.mixer.Sound("sound/fall.ogg")

    def draw_chara(self, bg):
        global chk_goal_A, index
        if self.turn_int == -1:
            self.ANIMATION = [0]* 10 + [1] * 10 + [2] * 10 + [3] * 10

        if self.turn_int == 1:
            self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.ama_a = self.ANIMATION[self.x_amana % len(self.ANIMATION)]
    
        if index == 1 or index == 2 or index == 10:
            if chk_goal_A == False:
                if self.turn_int == -1 and self.land == True: #左への移動時
                    bg.blit(self.run_han_amana[self.ama_a], (self.x_amana, self.y))

                elif self.turn_int == 1 and self.land == True: #右への移動時
                    bg.blit(self.run_amana[self.ama_a], (self.x_amana, self.y))


                elif self.turn_int == -1 and self.land == False: #左へのジャンプ
                    bg.blit(self.jump_han_amana[self.i], (self.x_amana, self.y))

                elif self.turn_int == 1 and self.land == False: #右へのジャンプ
                    bg.blit(self.jump_amana[self.i], (self.x_amana, self.y))

            elif chk_goal_A == True:
                #i=1:上昇, i=2:下降
                bg.blit(self.stand_amana[self.i], (self.x_amana, self.y))

        elif index == 4:
            #if self.turn_int == 1 and self.land == True: #右への移動時
            bg.blit(self.run_amana[self.ama_a], (self.x_amana, self.y))

    def rect_x_update(self):
        global chk_0_A, chk_goal_A, index, life, chk_goal
        
        if chk_goal == False:
            self.speed = 1

        elif chk_goal == True:
            self.speed = 2

        if chk_goal_A == False:
            if chk_0_A == True: #床の上
                if self.turn_int == -1:
                    if self.canJump == False and self.land == False: #ジャンプ中
                        self.x_amana += -self.speed - 2

                    elif self.land == True: #左へ移動
                        self.x_amana -= self.speed * 2

                elif self.turn_int == 1:
                    
                    if self.canJump == False and self.land == False: #ジャンプ中
                        self.x_amana += self.speed + 2
            
                    elif self.land == True: #右へ移動
                        self.t_move = 0
                            
                        self.x_amana += self.speed


                if self.x_amana >= 480:
                    self.x_amana = 480
                if self.x_amana <= -100:
                    self.x_amana = -100

            if chk_0_A == False: #穴の上
                if self.turn_int == -1:
                    if self.land == False: #ジャンプ中
                        self.x_amana += -self.speed - 2

                    elif self.land == True: #左へ移動
                        self.x_amana -= 0

                elif self.turn_int == 1:
                    if self.land == False: #ジャンプ中
                        self.x_amana += self.speed + 2
                
                    elif self.land == True: #右へ移動
                        self.x_amana += 0

            if self.x_amana < -50: #画面外へ移動時ミス
                #Life = Life_Manage()
                life -= 1              
                index = 2

        #ゴール後の処理
        elif chk_goal_A == True: 

            #TODO 限度を設ける
            if self.x_amana <= 480 - 25 * 6: #「3」はゴールマスのマス数
                self.x_amana = 480 - 25 * 6

            self.x_amana -= 1

        if index == 4:
            self.x_amana += 3
            self.turn_int == 1

            if self.x_amana >= 480:
                self.x_amana = 480
   
    def rect_y_update(self):
        global chk_0_A, index, life, fall_flag

        #if (self.canJump== False or self.canJump == True) and self.land == True:
        if self.land == True:
            if chk_0_A == False:
                fall_flag = True
                self.y += 5
            if chk_0_A == True:
                self.y = self.ground - self.h 
        
        #elif (self.canJump== False or self.canJump == True) and self.land == False: #ジャンプ時に
        elif self.land == False: #ジャンプ時に
            if chk_0_A == True: #下が床なら
                self.t_jump += 1/60
                self.y = -self.height * (1.0 - (1.0 - math.sin(2*self.radPerFrame * self.t_jump))**10) + self.ground - self.h
            
                if self.y >= self.ground - self.h:
                    self.y = self.ground - self.h 
                    self.land = True #←←ここ着地

            if chk_0_A == False: #下が穴なら
                if self.y >= self.ground - self.h:
                    self.y = self.ground - self.h 
                    self.land = True #←←ここ着地
                       
        if self.y > 360:
            life -= 1
            index = 2

        if index == 4:
            self.y = self.ground - self.h 

    def move_amana(self):
        global endless_flag
        key = pygame.key.get_pressed()

        if chk_goal_A == False:
        #ここからジャンプ
            if self.canJump == True and self.land == True:
                if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                    if key[pygame.K_j] == True:
                        if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                            self.se_jump.play()  
                            self.jump()
                            self.jump_flag()

                if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                    if key[pygame.K_SEMICOLON] == True: #<===============================================
                        if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                            self.se_jump.play()  
                            self.jump()
                            self.jump_flag()

                #落下音
                if self.y == self.ground - self.height + 5:
                    self.se_fall.play()

        self.t_canjump -= 1

        if self.t_canjump == 0:
            self.jump_reset()


        #ここまでジャンプ
        
        #反対ごっこ
        if SOUSA_MODE == 1 or SOUSA_MODE == 3:
            if key[pygame.K_d] == True and self.canTurn == True:  #<===============================================   
                self.turn_chara() #反対ごっこ
                self.turn_flag() #次の反対ごっこまでの猶予
                self.se_turn.play()
            
        elif SOUSA_MODE == 2 or SOUSA_MODE == 4:
            if key[pygame.K_a] == True and self.canTurn == True:  #<===============================================   
                self.turn_chara() #反対ごっこ
                self.turn_flag() #次の反対ごっこまでの猶予
                self.se_turn.play()

        if endless_flag == False:
            if stage == 5:
                RN_A = random.randint(1, 1000)
                if RN_A == 1:
                    self.turn_chara() #反対ごっこ
                    self.turn_flag() #次の反対ごっこまでの猶予
                    self.se_turn.play()

        self.t_turn -= 1 #タイマーを起動

        if self.t_turn == 0: #タイマーが0で
            self.turn_reset() #ターン出来るようにする
    #ここまで反対ごっこ

        self.jump_down()

        #ゴール後ぴょんぴょん
        if chk_goal_A == True:
            self.i = 0
            if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                if key[pygame.K_j] == True: #<===============================================
                    if self.y == 150/2: #150 甘奈上角のy座標 
                        self.se_jump.play() 
                        self.jump()
                        self.jump_flag()

            if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                if key[pygame.K_SEMICOLON] == True: #<===============================================
                    if self.y == 150/2: #150 甘奈上角のy座標 
                        self.se_jump.play() 
                        self.jump()
                        self.jump_flag()

            if self.canJump == False and self.land == False:
                self.i = 1

            self.jump_down()
        #ゴール後ぴょんぴょん

    def move_amana_click(self):
        if self.canJump == True and self.land == True:
            self.se_jump.play()                                                   
            self.jump()
            self.jump_flag()

    def turn_amana_click(self):
        if self.canTurn == True:
            self.turn_chara() #反対ごっこ
            self.turn_flag() #次の反対ごっこまでの猶予
            self.se_turn.play()

    def jump(self): #ジャンプフラグ    
        if self.canJump:
            self.t_jump = 0
            self.canJump = False
            self.i = 1

    def jump_down(self): #下降時
        A = math.cos(self.radPerFrame * self.t_jump) - math.sin(2 * (self.radPerFrame * self.t_jump)) / 2

        if self.canJump == False and A < 0.3:
            self.i = 2

    def jump_flag(self):
        if self.land == True:
            self.t_canjump = 30            
            self.land = False

    def jump_reset(self):
        self.t_canjump = 0
        self.canJump = True

    def turn_chara(self):
        self.turn_int = -1 * self.turn_int

    def turn_flag(self):
        self.t_turn = 8
        self.canTurn = False
    
    def turn_reset(self):        
        self.t_turn = 0
        self.canTurn = True

#===============================================================================
class Move_Amana_tuto(Move_Amana): #済
    def __init__(self):
        super().__init__()
        self.ground = 125
        self.x_amana = 0 #甘奈の位置
        self.h = 50
        self.y = self.ground - self.h #(甘奈の縦幅)
        
        self.speed = 1
        self.land = True
        self.fall_flag = False

        self.jump_timer = 30
        self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.turn = False
        self.turn_int = 1

        self.t_draw = 0

        self.t_turn = 0 #方向切り替えタイマー
        self.canTurn = True

        self.height = 40 #ジャンプ高さ

        self.canJump = True
        self.t_canjump = 0

        self.t_move = 0
        self.t_jump = 0

        self.radPerFrame = 2 * math.pi  / 60

        self.ama_at = 0

    def draw_chara(self, bg):
        self.ama_a = self.ANIMATION[self.ama_at % len(self.ANIMATION)]

        if self.turn_int == -1 and self.land == True: #左への移動時
            bg.blit(self.run_han_amana[self.ama_a], (390, self.y))

        elif self.turn_int == 1 and self.land == True: #右への移動時
            bg.blit(self.run_amana[self.ama_a], (390, self.y))

        elif self.turn_int == -1 and self.land == False: #左へのジャンプ
            bg.blit(self.jump_han_amana[self.i], (390, self.y))

        elif self.turn_int == 1 and self.land == False: #右へのジャンプ
            bg.blit(self.jump_amana[self.i], (390, self.y))
            
    def draw_chara_title(self, bg):

        self.ama_a = self.ANIMATION[self.ama_at % len(self.ANIMATION)]

        if self.turn_int == -1 and self.land == True: #左への移動時
            bg.blit(pygame.transform.scale(self.run_han_amana[self.ama_a], [100,100]), (50, 240))

        elif self.turn_int == 1 and self.land == True: #右への移動時
            bg.blit(pygame.transform.scale(self.run_amana[self.ama_a], [100,100]), (50, 240))

    def rect_x_update(self):            
        self.x_amana += 0
        self.ama_at += self.speed
        
    def rect_y_update(self):
        if self.land == True:
            self.y = self.ground - self.h 

        elif self.land == False:
            
            self.t_jump += 1/60
            self.y = -self.height * (1.0 - (1.0 - math.sin(2*self.radPerFrame * self.t_jump))**10) + self.ground - self.h
            
            if self.y >= self.ground - self.h:
                self.y = self.ground - self.h 
                self.land = True #←←ここ着地
        
    def move_amana(self):
        key = pygame.key.get_pressed()

        self.t_move += 1
        self.t_jump += 1
        self.t_draw += 1
        #ここからジャンプ
        if self.canJump == True and self.land == True:
            if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                if key[pygame.K_j] == True: #<===============================================
                    if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                        self.se_jump.play()  
                        self.jump()
                        self.jump_flag()

        if SOUSA_MODE == 3 or SOUSA_MODE == 4:
            if key[pygame.K_SEMICOLON] == True: #<===============================================
                if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                    self.se_jump.play()  
                    self.jump()
                    self.jump_flag()

        self.t_canjump -= 1

        if self.t_canjump == 0:
            self.jump_reset()
            
        #ここまでジャンプ
        
        #反対ごっこ
        if SOUSA_MODE == 1 or SOUSA_MODE == 3:
            if key[pygame.K_d] == True and self.canTurn == True:  #<===============================================   
                self.turn_chara() #反対ごっこ
                self.turn_flag() #次の反対ごっこまでの猶予
                self.se_turn.play()
            
        if SOUSA_MODE == 2 or SOUSA_MODE == 4:
            if key[pygame.K_a] == True and self.canTurn == True:  #<===============================================   
                self.turn_chara() #反対ごっこ
                self.turn_flag() #次の反対ごっこまでの猶予
                self.se_turn.play()

        self.t_turn -= 1 #タイマーを起動

        if self.t_turn == 0: #タイマーが0で
            self.turn_reset() #ターン出来るようにする
        #ここまで反対ごっこ
        self.jump_down()

        self.rect_x_update()
        self.rect_y_update() 

    def move_amana_title(self):
        key = pygame.key.get_pressed()

        self.t_move += 1
        self.t_jump += 1
        self.t_draw += 1
        self.land == True

        #反対ごっこ
        if key[pygame.K_LEFT] == True and self.canTurn == True:  #<===============================================   
            self.turn_int = -1 #反対ごっこ
            self.t_turn = 10
            self.canTurn = False #次の反対ごっこまでの猶予 

        if key[pygame.K_RIGHT] == True and self.canTurn == True:  #<===============================================   
            self.turn_int = 1 #反対ごっこ
            self.t_turn = 10
            self.canTurn = False #次の反対ごっこまでの猶予

        self.t_turn -= 1 #タイマーを起動

        if self.t_turn == 0: #タイマーが0で
            self.turn_reset() #ターン出来るようにする
        #ここまで反対ごっこ
        self.jump_down()

        self.rect_x_update()
        self.rect_y_update()

#===============================================================================
class Move_Chikiyu(Move_Amana): #済
    def __init__(self):
        super().__init__()
        self.x_amana = 0
        self.speed = 1
        self.ground = 225
        self.h = 55
        self.y = self.ground - self.h #(甘奈の縦幅)

        self.land = True
        self.fall_flag = False

        self.jump_timer = 30
        self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.turn = False
        self.turn_int = 1

        self.t_draw = 0

        self.t_turn = 0 #方向切り替えタイマー
        self.canTurn = True

        self.height = 40 #ジャンプ高さ

        self.canJump = True
        self.t_canjump = 0

        self.t_move = 0
        self.t_jump = 0

        self.radPerFrame = 2 * math.pi  / 60

        self.run_amana = [
                pygame.image.load("character/chikiyu0.png"),
                pygame.image.load("character/chikiyu1.png"),
                pygame.image.load("character/chikiyu2.png"),
                pygame.image.load("character/chikiyu3.png"),
                ]
        self.jump_amana= [
                None,
                pygame.image.load("character/chikiyu_up.png"),
                pygame.image.load("character/chikiyu_down.png"),
                ]

        self.run_han_amana = [
                pygame.image.load("character/hantai_chikiyu0.png"),
                pygame.image.load("character/hantai_chikiyu1.png"),
                pygame.image.load("character/hantai_chikiyu2.png"),
                pygame.image.load("character/hantai_chikiyu3.png"),
                ]

        self.jump_han_amana =[
                None,
                pygame.image.load("character/hantai_chikiyu_up.png"),
                pygame.image.load("character/hantai_chikiyu_down.png"),            
                ]
        
        self.stand_amana =[
                pygame.image.load("character/chikiyu_stand_left.png"),
                pygame.image.load("character/hantai_chikiyu_up.png"),
                pygame.image.load("character/hantai_chikiyu_down.png"), 

                pygame.image.load("character/chikiyu_stand_right.png"),#stage6       
                pygame.image.load("character/chikiyu_stand_right_ce.png"),#end    
                ]

    def draw_chara(self, bg):
        global chk_goal_C, chk_Lastgoal_C, index

        if self.turn_int == -1:
            self.ANIMATION = [0]* 10 + [1] * 10 + [2] * 10 + [3] * 10

        if self.turn_int == 1:
            self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.ama_a = self.ANIMATION[self.x_amana % len(self.ANIMATION)]
        if chk_Lastgoal_C == False:
            if chk_goal_C == False:
                if self.turn_int == -1 and self.land == True: #左への移動時
                    bg.blit(self.run_han_amana[self.ama_a], (self.x_amana, self.y))

                elif self.turn_int == 1 and self.land == True: #右への移動時
                    bg.blit(self.run_amana[self.ama_a], (self.x_amana, self.y))


                elif self.turn_int == -1 and self.land == False: #左へのジャンプ
                    bg.blit(self.jump_han_amana[self.i], (self.x_amana, self.y))

                elif self.turn_int == 1 and self.land == False: #右へのジャンプ
                    bg.blit(self.jump_amana[self.i], (self.x_amana, self.y))

            elif (index == 1 or index == 10) and chk_goal_C == True:
                #i=1:上昇, i=2:下降
                bg.blit(self.stand_amana[self.i], (self.x_amana, self.y))

            elif index == 4 and chk_goal_C == True:
                if self.turn_int == 1 and self.land == True: #右への移動時
                    bg.blit(self.run_amana[self.ama_a], (self.x_amana, self.y))

        elif chk_Lastgoal_C == True:
            bg.blit(self.stand_amana[3], (self.x_amana, self.y))

    def rect_x_update(self):
        global chk_0_C, chk_goal_C, chk_Lastgoal_C, index, life, chk_goal, endless_flag
        if chk_goal == False:
            self.speed = 1

        elif chk_goal == True:
            self.speed = 2

        if chk_Lastgoal_C == False:
            if chk_goal_C == False:
                if chk_0_C == True: #床の上
                    if self.turn_int == -1:
                        if self.canJump == False and self.land == False: #ジャンプ中
                            self.x_amana += -self.speed - 2

                        elif self.land == True: #左へ移動
                            self.x_amana -= self.speed * 2

                    elif self.turn_int == 1:
                    
                        if self.canJump == False and self.land == False: #ジャンプ中
                            self.x_amana += self.speed + 2
            
                        elif self.land == True: #右へ移動
                            self.t_move = 0
                            
                            self.x_amana += self.speed


                    if self.x_amana >= 480:
                        self.x_amana = 480
                    if self.x_amana <= -100:
                        self.x_amana = -100

                if chk_0_C == False: #穴の上
                    if self.turn_int == -1:
                        if self.land == False: #ジャンプ中
                            self.x_amana += -self.speed - 2

                    elif self.land == True: #左へ移動
                        self.x_amana -= 0
                        
                    elif self.turn_int == 1:
                        if self.land == False: #ジャンプ中
                            self.x_amana += self.speed + 2
                
                    elif self.land == True: #右へ移動
                        self.x_amana += 0

                if self.x_amana < -50: #画面外へ移動時ミス  
                    life -= 1   
                    index = 2
            #ゴール後の処理
            elif chk_goal_C == True: 

                #TODO 限度を設ける
                if self.x_amana <= 480 - 25 * 6: #「3」はゴールマスのマス数
                    self.x_amana = 480 - 25 * 6

                self.x_amana -= 1    

        elif chk_Lastgoal_C == True: #stage6の仕様
            if self.x_amana <= 480 - 25 * 10: #「3」はゴールマスのマス数
                self.x_amana = 480 - 25 * 10
            self.x_amana -= 1

        if index == 4:
            if stage == 6:
                if endless_flag == False:
                    self.x_amana += 0
            else:
                self.x_amana += 3
                self.turn_int == 1

            if self.x_amana >= 480:
                self.x_amana = 480

    def rect_y_update(self):
        global chk_0_C, index, life, fall_flag
        if self.land == True:
            if chk_0_C == False:
                fall_flag = True
                self.y += 5

            if chk_0_C == True:
                self.y = self.ground - self.h 

        elif self.land == False:
            if chk_0_C == True:
                self.t_jump += 1/60
                self.y = -self.height * (1.0 - (1.0 - math.sin(2*self.radPerFrame * self.t_jump))**10) + self.ground - self.h
            
                if self.y >= self.ground - self.h:
                    self.y = self.ground - self.h 
                    self.land = True #←←ここ着地
            if chk_0_C == False: #下が穴なら
                if self.y >= self.ground - self.h:
                    self.y = self.ground - self.h 
                    self.land = True #←←ここ着地 

        if self.y > 360:
            #Life = Life_Manage()
            life -= 1  
            index = 2

        if index == 4:
            self.y = self.ground - self.h

    def move_chikiyu(self):
        global endless_flag
        key = pygame.key.get_pressed()

        if chk_goal_C == False:
        #ここからジャンプ
            if self.canJump == True and self.land == True:
                if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                    if key[pygame.K_k] == True: #<===============================================
                        if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                            self.se_jump.play()  
                            self.jump()
                            self.jump_flag()

                if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                    if key[pygame.K_COLON] == True: #<===============================================
                        if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                            self.se_jump.play()  
                            self.jump()
                            self.jump_flag()

        self.t_canjump -= 1

        if self.t_canjump == 0:
            self.jump_reset()

        if self.y == self.ground - self.height + 5:
            self.se_fall.play()


        #ここまでジャンプ

        #反対ごっこ
        if key[pygame.K_s] == True and self.canTurn == True: #<===============================================    
            self.turn_chara() #反対ごzcっこ
            self.turn_flag() #次の反対ごっこまでの猶予
            self.se_turn.play()
        if endless_flag == False:
            if stage == 5:
                RN_A = random.randint(1, 1000)
                if RN_A == 1:
                    self.turn_chara() #反対ごっこ
                    self.turn_flag() #次の反対ごっこまでの猶予
                    self.se_turn.play()
            
        self.t_turn -= 1 #タイマーを起動

        if self.t_turn == 0: #タイマーが0で
            self.turn_reset() #ターン出来るようにする
        #ここまで反対ごっこ
        self.jump_down()
        #ゴール後ぴょんぴょん
        if chk_goal_C == True:
            self.i = 0
            if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                if key[pygame.K_k] == True: #<===============================================
                    if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                        self.se_jump.play()  
                        self.jump()
                        self.jump_flag()

            if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                if key[pygame.K_COLON] == True: #<===============================================
                    if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                        self.se_jump.play()  
                        self.jump()
                        self.jump_flag()

            if self.canJump == False and self.land == False:
                self.i = 1

                self.jump_down()
            #ゴール後ぴょんぴょん
#===============================================================================
class Move_Chikiyu_tuto(Move_Amana_tuto): #済
    def __init__(self):
        super().__init__()
        self.x_amana = 0
        self.speed = 1
        self.ground = 225
        self.h = 55
        self.y = self.ground - self.h #(甘奈の縦幅)

        self.land = True
        self.fall_flag = False

        self.jump_timer = 30
        self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.turn = False
        self.turn_int = 1

        self.t_draw = 0

        self.t_turn = 0 #方向切り替えタイマー
        self.canTurn = True

        self.height = 40 #ジャンプ高さ

        self.canJump = True
        self.t_canjump = 0

        self.t_move = 0
        self.t_jump = 0

        self.radPerFrame = 2 * math.pi  / 60

        self.run_amana = [
                pygame.image.load("character/chikiyu0.png"),
                pygame.image.load("character/chikiyu1.png"),
                pygame.image.load("character/chikiyu2.png"),
                pygame.image.load("character/chikiyu3.png"),
                ]
        self.jump_amana= [
                None,
                pygame.image.load("character/chikiyu_up.png"),
                pygame.image.load("character/chikiyu_down.png"),
                ]

        self.run_han_amana = [
                pygame.image.load("character/hantai_chikiyu0.png"),
                pygame.image.load("character/hantai_chikiyu1.png"),
                pygame.image.load("character/hantai_chikiyu2.png"),
                pygame.image.load("character/hantai_chikiyu3.png"),
                ]

        self.jump_han_amana =[
                None,
                pygame.image.load("character/hantai_chikiyu_up.png"),
                pygame.image.load("character/hantai_chikiyu_down.png"),            
                ]
        
        self.stand_amana =[
                pygame.image.load("character/chikiyu_stand_left.png"),
                pygame.image.load("character/hantai_chikiyu_up.png"),
                pygame.image.load("character/hantai_chikiyu_down.png"), 

                pygame.image.load("character/chikiyu_stand_right.png"),#stage6       
                pygame.image.load("character/chikiyu_stand_right_ce.png"),#end    
                ]
        self.ama_at = 0

    def draw_chara(self, bg):
        self.ama_a = self.ANIMATION[self.ama_at % len(self.ANIMATION)]

        if self.turn_int == -1 and self.land == True: #左への移動時
            bg.blit(self.run_han_amana[self.ama_a], (390, self.y))

        elif self.turn_int == 1 and self.land == True: #右への移動時
            bg.blit(self.run_amana[self.ama_a], (390, self.y))

        elif self.turn_int == -1 and self.land == False: #左へのジャンプ
            bg.blit(self.jump_han_amana[self.i], (390, self.y))

        elif self.turn_int == 1 and self.land == False: #右へのジャンプ
            bg.blit(self.jump_amana[self.i], (390, self.y))
            
    def draw_chara_title(self, bg):

        self.ama_a = self.ANIMATION[self.ama_at % len(self.ANIMATION)]

        if self.turn_int == -1 and self.land == True: #左への移動時
            bg.blit(pygame.transform.scale(self.run_han_amana[self.ama_a], [100,110]), (50, 230))

        elif self.turn_int == 1 and self.land == True: #右への移動時
            bg.blit(pygame.transform.scale(self.run_amana[self.ama_a], [100,110]), (50, 230))

    def rect_x_update(self):            
        self.x_amana += 0
        self.ama_at += self.speed

    def rect_y_update(self):
        if self.land == True:
            self.y = self.ground - self.h 

        elif self.land == False:
            
            self.t_jump += 1/60
            self.y = -self.height * (1.0 - (1.0 - math.sin(2*self.radPerFrame * self.t_jump))**10) + self.ground - self.h
            
            if self.y >= self.ground - self.h:
                self.y = self.ground - self.h 
                self.land = True #←←ここ着地

    def move_chikiyu(self):
        key = pygame.key.get_pressed()

        self.t_move += 1
        self.t_jump += 1
        self.t_draw += 1
        #ここからジャンプ
        if self.canJump == True and self.land == True:
            if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                if key[pygame.K_k] == True: #<===============================================
                    if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                        self.se_jump.play()  
                        self.jump()
                        self.jump_flag()

            if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                if key[pygame.K_COLON] == True: #<===============================================
                    if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                        self.se_jump.play()  
                        self.jump()
                        self.jump_flag()

        self.t_canjump -= 1

        if self.t_canjump == 0:
            self.jump_reset()
            
        #ここまでジャンプ
        
        #反対ごっこ
        if key[pygame.K_s] == True and self.canTurn == True: #<===============================================    
            self.turn_chara() #反対ごっこ
            self.turn_flag() #次の反対ごっこまでの猶予
            self.se_turn.play()
            
        self.t_turn -= 1 #タイマーを起動

        if self.t_turn == 0: #タイマーが0で
            self.turn_reset() #ターン出来るようにする
        #ここまで反対ごっこ
        self.jump_down()

        self.rect_x_update()
        self.rect_y_update() 

    def move_chikiyu_title(self):
        key = pygame.key.get_pressed()

        self.t_move += 1
        self.t_jump += 1
        self.t_draw += 1
        self.land == True

        #反対ごっこ
        if key[pygame.K_LEFT] == True and self.canTurn == True:  #<===============================================   
            self.turn_int = -1 #反対ごっこ
            self.t_turn = 10
            self.canTurn = False #次の反対ごっこまでの猶予 

        if key[pygame.K_RIGHT] == True and self.canTurn == True:  #<===============================================   
            self.turn_int = 1 #反対ごっこ
            self.t_turn = 10
            self.canTurn = False #次の反対ごっこまでの猶予

        self.t_turn -= 1 #タイマーを起動

        if self.t_turn == 0: #タイマーが0で
            self.turn_reset() #ターン出来るようにする
        #ここまで反対ごっこ
        self.jump_down()

        self.rect_x_update()
        self.rect_y_update()

#===============================================================================
class Move_Chikiyu_Ending(Move_Chikiyu): #済
    def __init__(self):
        super().__init__()
        self.ground = 200
        self.speed = 2
        self.h = 55

        self.h = 55
        self.y = self.ground - self.h #(甘奈の縦幅)
        self.x_amana = 0

        self.land = True
        self.fall_flag = False

        self.jump_timer = 30
        self.ANIMATION = [0]* 10 + [1] * 10 + [2] * 10 + [3] * 10

        self.turn = False
        self.turn_int = 1

        self.t_draw = 0

        self.t_turn = 0 #方向切り替えタイマー
        self.canTurn = True

        self.height = 40 #ジャンプ高さ

        self.canJump = True
        self.t_canjump = 0

        self.t_move = 0
        self.t_jump = 0

        self.radPerFrame = 2 * math.pi  / 60

    def draw_chara(self, bg):
        global en_ind7, stop_ce
        self.ama_a = self.ANIMATION[self.x_amana % len(self.ANIMATION)]

        if stop_ce == False:
            if en_ind7 == 1 or en_ind7 == 4:
                bg.blit(self.run_amana[self.ama_a], (self.x_amana, self.y))
        elif stop_ce == True:
            if en_ind7 == 2:
                bg.blit(self.stand_amana[0], (self.x_amana, self.y))

            elif en_ind7 == 3:
                bg.blit(self.stand_amana[4], (self.x_amana, self.y))

    def rect_x_update(self):
        global en_ind7, stop_ce

        self.t_move = 0
        if stop_ce == False:
            #if en_ind7 == 1 or en_ind7 == 4:                
                self.x_amana += self.speed
        
        elif stop_ce == True:
            #if en_ind7 == 2 or en_ind7 == 3:
                self.x_amana += 0

        if self.x_amana >= 480:
            self.x_amana = 480
        if self.x_amana <= -100:
            self.x_amana = -100

#==============================================================================
class Move_Tenka(Move_Amana): #済
    def __init__(self):
        super().__init__()
        self.speed = 1
        self.h = 50
        self.ground = 325
        self.y = self.ground - self.h #(甘奈の縦幅)
        self.x_amana = 0

        self.land = True
        self.fall_flag = False

        self.jump_timer = 30
        self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.turn = False
        self.turn_int = 1

        self.t_draw = 0

        self.t_turn = 0 #方向切り替えタイマー
        self.canTurn = True

        self.height = 40 #ジャンプ高さ

        self.canJump = True
        self.t_canjump = 0

        self.t_move = 0
        self.t_jump = 0

        self.radPerFrame = 2 * math.pi  / 60
        self.run_amana = [
                pygame.image.load("character/tenka0.png"),
                pygame.image.load("character/tenka1.png"),
                pygame.image.load("character/tenka2.png"),
                pygame.image.load("character/tenka3.png"),
                ]
        self.jump_amana= [
                None,
                pygame.image.load("character/tenka_up.png"),
                pygame.image.load("character/tenka_down.png"),
                ]

        self.run_han_amana = [
                pygame.image.load("character/hantai_tenka0.png"),
                pygame.image.load("character/hantai_tenka1.png"),
                pygame.image.load("character/hantai_tenka2.png"),
                pygame.image.load("character/hantai_tenka3.png"),
                ]

        self.jump_han_amana =[
                None,
                pygame.image.load("character/hantai_tenka_up.png"),
                pygame.image.load("character/hantai_tenka_down.png"),            
                ]
        
        self.stand_amana =[
                pygame.image.load("character/tenka_stand_left.png"),
                pygame.image.load("character/hantai_tenka_up.png"),
                pygame.image.load("character/hantai_tenka_down.png"), 

                pygame.image.load("character/tenka_stand_right.png"),            
                ]
        
    def draw_chara(self, bg):
        global chk_goal_T, chk_Lastgoal_T, index
        if self.turn_int == -1:
            self.ANIMATION = [0]* 10 + [1] * 10 + [2] * 10 + [3] * 10

        if self.turn_int == 1:
            self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.ama_a = self.ANIMATION[self.x_amana % len(self.ANIMATION)]
        if chk_Lastgoal_T == False:
            if chk_goal_T == False:
                if self.turn_int == -1 and self.land == True: #左への移動時
                    bg.blit(self.run_han_amana[self.ama_a], (self.x_amana, self.y))

                elif self.turn_int == 1 and self.land == True: #右への移動時
                    bg.blit(self.run_amana[self.ama_a], (self.x_amana, self.y))


                elif self.turn_int == -1 and self.land == False: #左へのジャンプ
                    bg.blit(self.jump_han_amana[self.i], (self.x_amana, self.y))

                elif self.turn_int == 1 and self.land == False: #右へのジャンプ
                    bg.blit(self.jump_amana[self.i], (self.x_amana, self.y))

            elif (index == 1 or index == 10) and chk_goal_T == True:
                #i=1:上昇, i=2:下降
                bg.blit(self.stand_amana[self.i], (self.x_amana, self.y))

            elif index == 4 and chk_goal_T == True:
                if self.turn_int == 1 and self.land == True: #右への移動時
                    bg.blit(self.run_amana[self.ama_a], (self.x_amana, self.y))

        elif chk_Lastgoal_T == True:
            bg.blit(self.stand_amana[3], (self.x_amana, self.y))

    def rect_x_update(self):
        global chk_0_T, chk_goal_T, chk_Lastgoal_T, index, life, chk_goal, endless_flag
        if chk_goal == False:
            self.speed = 1

        elif chk_goal == True:
            self.speed = 2

        if chk_Lastgoal_T == False:
            if chk_goal_T == False:
                if chk_0_T == True: #床の上
                    if self.turn_int == -1:
                        if self.canJump == False and self.land == False: #ジャンプ中
                            self.x_amana += -self.speed - 2

                        elif self.land == True: #左へ移動
                            self.x_amana -= self.speed * 2

                    elif self.turn_int == 1:
                    
                        if self.canJump == False and self.land == False: #ジャンプ中
                            self.x_amana += self.speed + 2
            
                        elif self.land == True: #右へ移動
                            self.t_move = 0
                            
                            self.x_amana += self.speed


                    if self.x_amana >= 480:
                        self.x_amana = 480
                    if self.x_amana <= -100:
                        self.x_amana = -100

                if chk_0_T == False: #穴の上
                    if self.turn_int == -1:
                        if self.land == False: #ジャンプ中
                            self.x_amana += -self.speed - 2

                    elif self.land == True: #左へ移動
                        self.x_amana -= 0
                        
                    elif self.turn_int == 1:
                        if self.land == False: #ジャンプ中
                            self.x_amana += self.speed + 2
                
                    elif self.land == True: #右へ移動
                        self.x_amana += 0

                if self.x_amana < -50: #画面外へ移動時ミス  
                    life -= 1   
                    index = 2
            #ゴール後の処理
            elif chk_goal_T == True: 

                #TODO 限度を設ける
                if self.x_amana <= 480 - 25 * 6: #「3」はゴールマスのマス数
                    self.x_amana = 480 - 25 * 6

                self.x_amana -= 1    

        elif chk_Lastgoal_C == True: #stage6の仕様
            if self.x_amana <= 480 - 25 * 10: #「3」はゴールマスのマス数
                self.x_amana = 480 - 25 * 10
            self.x_amana -= 1

        if index == 4:
            if stage == 6:
                if endless_flag == False:
                    self.x_amana += 0
            else:
                self.x_amana += 3
                self.turn_int == 1

            if self.x_amana >= 480:
                self.x_amana = 480

    def rect_y_update(self):
        global chk_0_T, index, life, fall_flag
        if self.land == True:
            if chk_0_T == False:
                fall_flag = True
                self.y += 5
                
            if chk_0_T == True:
                self.y = self.ground - self.h 

        elif self.land == False:
            if chk_0_T == True:
                self.t_jump += 1/60
                self.y = -self.height * (1.0 - (1.0 - math.sin(2*self.radPerFrame * self.t_jump))**10) + self.ground - self.h
            
                if self.y >= self.ground - self.h:
                    self.y = self.ground - self.h 
                    self.land = True #←←ここ着地
            if chk_0_T == False: #下が穴なら
                if self.y >= self.ground - self.h:
                    self.y = self.ground - self.h 
                    self.land = True #←←ここ着地 

        if self.y > 360:
            #Life = Life_Manage()
            life -= 1  
            index = 2

        if index == 4:
            self.y = 225

    def move_tenka(self):
        global endless_flag
        key = pygame.key.get_pressed()

        if chk_goal_T == False:
        #ここからジャンプ
            if self.canJump == True and self.land == True:
                if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                    if key[pygame.K_l] == True: #<===============================================
                        if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                            self.se_jump.play()  
                            self.jump()
                            self.jump_flag()

                if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                    if key[pygame.K_RIGHTBRACKET] == True: #<===============================================
                        if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                            self.se_jump.play()  
                            self.jump()
                            self.jump_flag()
                    
                #落下音
                if self.y == self.ground - self.height + 5:
                    self.se_fall.play()

            if self.canJump == False and self.land == False:
                self.i = 1

                self.jump_down()

        self.t_canjump -= 1

        if self.t_canjump == 0:
            self.jump_reset()
        #ここまでジャンプ

        #反対ごっこ
        if SOUSA_MODE == 1 or SOUSA_MODE == 3:
            if key[pygame.K_a] == True and self.canTurn == True: #<===============================================
                self.turn_chara() #反対ごっこ
                self.turn_flag() #次の反対ごっこまでの猶予
                self.se_turn.play()
            
        if SOUSA_MODE == 2 or SOUSA_MODE == 4:
            if key[pygame.K_d] == True and self.canTurn == True: #<===============================================
                self.turn_chara() #反対ごっこ
                self.turn_flag() #次の反対ごっこまでの猶予
                self.se_turn.play()
        if endless_flag == False:
            if stage == 5:
                RN_A = random.randint(1, 1000)
                if RN_A == 1:
                    self.turn_chara() #反対ごっこ
                    self.turn_flag() #次の反対ごっこまでの猶予
                    self.se_turn.play()
        
        self.t_turn -= 1 #タイマーを起動

        if self.t_turn == 0: #タイマーが0で
            self.turn_reset() #ターン出来るようにする

            self.jump_down()
        #ここまで反対ごっこ

        #ゴール後ぴょんぴょん
        if chk_goal_T == True:
            self.i = 0
            if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                if key[pygame.K_l] == True: #<===============================================
                    if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                        self.se_jump.play()  
                        self.jump()
                        self.jump_flag()

            if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                if key[pygame.K_RIGHTBRACKET] == True: #<===============================================
                    if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                        self.se_jump.play()  
                        self.jump()
                        self.jump_flag()

            if self.canJump == False and self.land == False:
                self.i = 1

                self.jump_down()
            #ゴール後ぴょんぴょん

#==============================================================================
class Move_Tenka_tuto(Move_Amana_tuto): #済
    def __init__(self):
        super().__init__()
        self.ground = 325
        self.speed = 1
        self.h = 50
        self.y = self.ground - self.h #(甘奈の縦幅)
        self.x_amana = 0

        self.land = True
        self.fall_flag = False

        self.jump_timer = 30
        self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.turn = False
        self.turn_int = 1

        self.t_draw = 0

        self.t_turn = 0 #方向切り替えタイマー
        self.canTurn = True

        self.height = 40 #ジャンプ高さ

        self.canJump = True
        self.t_canjump = 0

        self.t_move = 0
        self.t_jump = 0

        self.radPerFrame = 2 * math.pi  / 60

        self.run_amana = [
                pygame.image.load("character/tenka0.png"),
                pygame.image.load("character/tenka1.png"),
                pygame.image.load("character/tenka2.png"),
                pygame.image.load("character/tenka3.png"),
                ]
        self.jump_amana= [
                None,
                pygame.image.load("character/tenka_up.png"),
                pygame.image.load("character/tenka_down.png"),
                ]

        self.run_han_amana = [
                pygame.image.load("character/hantai_tenka0.png"),
                pygame.image.load("character/hantai_tenka1.png"),
                pygame.image.load("character/hantai_tenka2.png"),
                pygame.image.load("character/hantai_tenka3.png"),
                ]

        self.jump_han_amana =[
                None,
                pygame.image.load("character/hantai_tenka_up.png"),
                pygame.image.load("character/hantai_tenka_down.png"),            
                ]
        
        self.stand_amana =[
                pygame.image.load("character/tenka_stand_left.png"),
                pygame.image.load("character/hantai_tenka_up.png"),
                pygame.image.load("character/hantai_tenka_down.png"), 

                pygame.image.load("character/tenka_stand_right.png"),            
                ]
        self.ama_at = 0

    def draw_chara(self, bg):
        self.ama_a = self.ANIMATION[self.ama_at % len(self.ANIMATION)]

        if self.turn_int == -1 and self.land == True: #左への移動時
            bg.blit(self.run_han_amana[self.ama_a], (390, self.y))

        elif self.turn_int == 1 and self.land == True: #右への移動時
            bg.blit(self.run_amana[self.ama_a], (390, self.y))

        elif self.turn_int == -1 and self.land == False: #左へのジャンプ
            bg.blit(self.jump_han_amana[self.i], (390, self.y))

        elif self.turn_int == 1 and self.land == False: #右へのジャンプ
            bg.blit(self.jump_amana[self.i], (390, self.y))
            
    def draw_chara_title(self, bg):

        self.ama_a = self.ANIMATION[self.ama_at % len(self.ANIMATION)]

        if self.turn_int == -1 and self.land == True: #左への移動時
            bg.blit(pygame.transform.scale(self.run_han_amana[self.ama_a], [100,100]), (50, 240))

        elif self.turn_int == 1 and self.land == True: #右への移動時
            bg.blit(pygame.transform.scale(self.run_amana[self.ama_a], [100,100]), (50, 240))

    def rect_x_update(self):            
        self.x_amana += 0
        self.ama_at += self.speed
        
    def rect_y_update(self):
        if self.land == True:
            self.y = self.ground - self.h 

        elif self.land == False:
            
            self.t_jump += 1/60
            self.y = -self.height * (1.0 - (1.0 - math.sin(2*self.radPerFrame * self.t_jump))**10) + self.ground - self.h
            
            if self.y >= self.ground - self.h:
                self.y = self.ground - self.h 
                self.land = True #←←ここ着地

    def move_tenka(self):
        key = pygame.key.get_pressed()

        self.t_move += 1
        self.t_jump += 1
        self.t_draw += 1
        #ここからジャンプ
        if self.canJump == True and self.land == True:
            if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                if key[pygame.K_l] == True: #<===============================================
                    if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                        self.se_jump.play()  
                        self.jump()
                        self.jump_flag()

            if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                if key[pygame.K_j] == True: #<===============================================
                    if self.y == self.ground - self.h: #150 甘奈上角のy座標 
                        self.se_jump.play()  
                        self.jump()
                        self.jump_flag()

        self.t_canjump -= 1

        if self.t_canjump == 0:
            self.jump_reset()
            
        #ここまでジャンプ
        
        #反対ごっこ
        if SOUSA_MODE == 1:
            if key[pygame.K_a] == True and self.canTurn == True: #<===============================================    
                self.turn_chara() #反対ごっこ
                self.turn_flag() #次の反対ごっこまでの猶予
                self.se_turn.play()

        if SOUSA_MODE == 2:
            if key[pygame.K_d] == True and self.canTurn == True: #<===============================================    
                self.turn_chara() #反対ごっこ
                self.turn_flag() #次の反対ごっこまでの猶予
                self.se_turn.play()
            
        self.t_turn -= 1 #タイマーを起動

        if self.t_turn == 0: #タイマーが0で
            self.turn_reset() #ターン出来るようにする
        #ここまで反対ごっこ
        self.jump_down()

        self.rect_x_update()
        self.rect_y_update() 

    def move_tenka_title(self):
        key = pygame.key.get_pressed()

        self.t_move += 1
        self.t_jump += 1
        self.t_draw += 1
        self.land == True

        #反対ごっこ
        if key[pygame.K_LEFT] == True and self.canTurn == True:  #<===============================================   
            self.turn_int = -1 #反対ごっこ
            self.t_turn = 10
            self.canTurn = False #次の反対ごっこまでの猶予 

        if key[pygame.K_RIGHT] == True and self.canTurn == True:  #<===============================================   
            self.turn_int = 1 #反対ごっこ
            self.t_turn = 10
            self.canTurn = False #次の反対ごっこまでの猶予

        self.t_turn -= 1 #タイマーを起動

        if self.t_turn == 0: #タイマーが0で
            self.turn_reset() #ターン出来るようにする
        #ここまで反対ごっこ
        self.jump_down()

        self.rect_x_update()
        self.rect_y_update()
#キャラの動き============================================

#ステージの動き============================================
class Stage_Create(): #済
    def __init__(self):
        super().__init__()
        self.chk_goal = False

        self.x_road = 0
        self.map_data = []

        self.BLUE = (128, 128, 255)
        self.BLACK = (0, 0, 64)
        self.PINK = (255,232,255)

        self.block = [
                pygame.image.load("block/block_kara.png"),
                pygame.image.load("block/block_pskyblue.png"),
                
                pygame.image.load("block/block_yellow.png"), #start
                pygame.image.load("block/block_yellow.png"), #goal

                pygame.image.load("block/block_chikiyu.png"),
                pygame.image.load("block/block_tenka.png"),
                pygame.image.load("block/block_tenka.png"), #stage6用
                pygame.image.load("block/block_yellow_2_2.png"), #ending用

                pygame.image.load("block/block_pskyblue.png"), #8
                pygame.image.load("block/block_chikiyu.png"), #9
                pygame.image.load("block/block_tenka.png"), #10
            ]

    def set_stage(self):
        global stage, generated, generated2
        if stage == 1:
            self.map_data = [
                [2,2,2,2,  1,1,1,1,1,1, 1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1, 3,3,3,3,3,3], #甘奈
                [2,2,2,2,  1,1,1,1,1,1, 1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1, 3,3,3,3,3,3], #ちきゆ
                [2,2,2,2,  1,1,1,1,1,1, 1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1, 3,3,3,3,3,3], #甜花
                ]
        
        if stage == 2:
            self.map_data = [
                [2,2,2,2,  1,1,1,1,  1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,  3,3,3,3,3,3], #甘奈
                [2,2,2,2,  1,1,1,1,  1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,  3,3,3,3,3,3], #ちきゆ
                [2,2,2,2,  1,1,1,1,  1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,  3,3,3,3,3,3], #甜花
                ]

        if stage == 3:
            self.map_data = [
                [2,2,2,2, 4,4,4,4,4,4,  4,4,4,4,0,0,4,4,4,4,0,0,4,4,4,4,4,4,4,4,4,4,0,0,4,4,4,4,4,4,4,4,4,4, 3,3,3,3,3,3], #甘奈
                [2,2,2,2, 4,4,4,4,4,4,  4,4,4,4,4,4,4,4,4,4,4,4,0,0,4,4,4,4,4,4,0,0,4,4,4,4,0,0,4,4,4,4,4,4, 3,3,3,3,3,3], #ちきゆ
                [2,2,2,2, 4,4,4,4,4,4,  4,4,4,4,4,4,0,0,4,4,4,4,0,0,4,4,4,4,4,4,4,4,0,0,4,4,4,4,4,4,4,4,4,4, 3,3,3,3,3,3], #甜花
                ]
            
        if stage == 4:
            #S_Random = Stage_Create_RN()
            self.map_data = generated

        if stage == 5:
            self.map_data = [
                [2,2,2,2,  5,5,5,5,5,5, 5,5,5,5,5,5,5,5,5,5,5,5,0,0,5,5,5,5,0,0,5,5,5,5,5,5,5,5,5,5,5,5,0,0,5,5, 3,3,3,3,3,3], #甘奈
                [2,2,2,2,  5,5,5,5,5,5, 5,5,5,5,5,5,5,5,5,5,5,5,0,0,5,5,5,5,0,0,5,5,5,5,5,5,5,5,0,0,5,5,5,5,5,5, 3,3,3,3,3,3], #ちきゆ
                [2,2,2,2,  5,5,5,5,5,5, 5,5,5,5,5,5,5,5,5,5,5,5,0,0,5,5,5,5,0,0,5,5,5,5,5,5,5,5,5,5,0,0,5,5,5,5, 3,3,3,3,3,3], #甜花
                ]

        if stage == 6:
            #S_Random = Stage_Create_RN()
            self.map_data = generated2

    def create_stage(self, bg):
        self.set_stage()
        stage_len = self.map_data[0]
    
        for i in range(len(stage_len)):

            #甘奈
            if self.map_data[0][i] == 0:
                bg.blit(self.block[0], (25 * i - self.x_road, 125))
                
            elif self.map_data[0][i] == 1:
                bg.blit(self.block[1], (25 * i - self.x_road, 125))

            elif self.map_data[0][i] == 2:
                bg.blit(self.block[2], (25 * i - self.x_road, 125))

            elif self.map_data[0][i] == 3:
                bg.blit(self.block[3], (25 * i - self.x_road, 125))     

            elif self.map_data[0][i] == 4:
                bg.blit(self.block[4], (25 * i - self.x_road, 125))

            elif self.map_data[0][i] == 5:
                bg.blit(self.block[5], (25 * i - self.x_road, 125))  

            #ちきゆ
            if self.map_data[1][i] == 0:
                bg.blit(self.block[0], (25 * i - self.x_road, 225))
                
            elif self.map_data[1][i] == 1:
                bg.blit(self.block[1], (25 * i - self.x_road, 225))

            elif self.map_data[1][i] == 2:
                bg.blit(self.block[2], (25 * i - self.x_road, 225))

            elif self.map_data[1][i] == 3:
                bg.blit(self.block[3], (25 * i - self.x_road, 225))

            elif self.map_data[1][i] == 4:
                bg.blit(self.block[4], (25 * i - self.x_road, 225))

            elif self.map_data[1][i] == 5:
                bg.blit(self.block[5], (25 * i - self.x_road, 225)) 

            elif self.map_data[1][i] == 6:
                bg.blit(self.block[5], (25 * i - self.x_road, 225))

            #甜花
            if self.map_data[2][i] == 0:
                bg.blit(self.block[0], (25 * i - self.x_road, 325))
                
            elif self.map_data[2][i] == 1:
                bg.blit(self.block[1], (25 * i - self.x_road, 325))

            elif self.map_data[2][i] == 2:
                bg.blit(self.block[2], (25 * i - self.x_road, 325))

            elif self.map_data[2][i] == 3:
                bg.blit(self.block[3], (25 * i - self.x_road, 325))

            elif self.map_data[2][i] == 4:
                bg.blit(self.block[4], (25 * i - self.x_road, 325))

            elif self.map_data[2][i] == 5:
                bg.blit(self.block[5], (25 * i - self.x_road, 325))  

            elif self.map_data[2][i] == 6:
                bg.blit(self.block[5], (25 * i - self.x_road, 325))

    def stage_scrool2(self):
        global fall_flag
        self.set_stage()
        if fall_flag == False:
            self.x_road += 1

        elif fall_flag == True:
            self.x_road += 0

        self.x_Limit()
        
    def x_Limit(self):
        global generated, generated2, chk_goal
        line = self.map_data[0]

        if self.x_road >= len(line)*25 - 480: #960:画面の横幅
            self.x_road = len(line)*25 - 480
            chk_goal = True
            
        if self.x_road <= -100:
            self.x_road = -100

class Stage_Create_RN(Stage_Create):
    def __init__(self):
        super().__init__()
        self.x_road = 0
        self.map_data = []

    def set_stage(self, tip_num,repeat):
        #TODO ランダム生成
        self.map_data = [[2] * 4, [2] * 4, [2] * 4]

        if tip_num == 4:
            map_tip = [[tip_num,tip_num,tip_num,tip_num,tip_num,tip_num,0,0,],
                       [tip_num,tip_num,tip_num,tip_num,0,0,tip_num,tip_num,],
                       [tip_num,tip_num,0,0,tip_num,tip_num,tip_num,tip_num,],
                       [tip_num,tip_num,tip_num,tip_num,tip_num,tip_num,tip_num,tip_num]]
        
        if tip_num == 5:
            map_tip = [[tip_num,tip_num,tip_num,tip_num,tip_num,tip_num,0,0,],
                       [tip_num,tip_num,tip_num,tip_num,0,0,tip_num,tip_num,],
                       [tip_num,tip_num,0,0,tip_num,tip_num,tip_num,tip_num,],
                       [tip_num,tip_num,tip_num,tip_num,0,0,tip_num,tip_num,]]
        
        map_line1 = []
        map_line2 = []
        map_line3 = []

        i = 1
        j = 1
        k = 1

        while i <= repeat:
            n = random.randint(0, 3)
            if n == 0:
                map_line1 += map_tip[0]
            elif n == 1:
                map_line1 += map_tip[1]
            elif n == 2:
                map_line1 += map_tip[2]
            elif n == 3:
                map_line1 += map_tip[3]
            i += 1
        map_line1 += [tip_num, tip_num]

        if tip_num == 5:
            map_line1 += [tip_num] * 4

        map_line1 += [3] * 6
        #print(len(map_line1))
        self.map_data[0] += map_line1

        while j <= repeat:
            n = random.randint(0, 3)
            if n == 0:
                map_line2 += map_tip[0]
            elif n == 1:
                map_line2 += map_tip[1]
            elif n == 2:
                map_line2 += map_tip[2]
            elif n == 3:
                map_line2 += map_tip[3]
            j += 1
        map_line2 += [tip_num, tip_num]

        if tip_num == 5:
            map_line2 += [6] * 4

        map_line2 += [3] * 6
        #print(len(map_line2))
        self.map_data[1] += map_line2

        while k <= repeat:
            n = random.randint(0, 3)
            if n == 0:
                map_line3 += map_tip[0]
            elif n == 1:
                map_line3 += map_tip[1]
            elif n == 2:
                map_line3 += map_tip[2]
            elif n == 3:
                map_line3 += map_tip[3]
            k += 1

        map_line3 += [tip_num, tip_num]

        if tip_num == 5:
            map_line3 += [6] * 4

        map_line3 += [3] * 6
        #print(len(map_line3))
        self.map_data[2] += map_line3

    def set_stage_endless(self, tip_num,repeat):
        #TODO ランダム生成
        self.map_data = [[2] * 4, [2] * 4, [2] * 4]


        map_tip =  [[tip_num,tip_num,tip_num,tip_num,tip_num,tip_num,0,0,],
                    [tip_num,tip_num,tip_num,tip_num,0,0,tip_num,tip_num,],
                    [tip_num,tip_num,0,0,tip_num,tip_num,tip_num,tip_num,],
                    [tip_num,tip_num,tip_num,tip_num,0,0,tip_num,tip_num,]]
        
        map_line1 = []
        map_line2 = []
        map_line3 = []

        i = 1
        j = 1
        k = 1

        while i <= repeat:
            n = random.randint(0, 3)
            if n == 0:
                map_line1 += map_tip[0]
            elif n == 1:
                map_line1 += map_tip[1]
            elif n == 2:
                map_line1 += map_tip[2]
            elif n == 3:
                map_line1 += map_tip[3]
            i += 1

        map_line1 += [tip_num]*4
        map_line1 += [3] * 6
        self.map_data[0] += map_line1

        while j <= repeat:
            n = random.randint(0, 3)
            if n == 0:
                map_line2 += map_tip[0]
            elif n == 1:
                map_line2 += map_tip[1]
            elif n == 2:
                map_line2 += map_tip[2]
            elif n == 3:
                map_line2 += map_tip[3]
            j += 1
        map_line2 += [tip_num]*4
        map_line2 += [3] * 6
        self.map_data[1] += map_line2

        while k <= repeat:
            n = random.randint(0, 3)
            if n == 0:
                map_line3 += map_tip[0]
            elif n == 1:
                map_line3 += map_tip[1]
            elif n == 2:
                map_line3 += map_tip[2]
            elif n == 3:
                map_line3 += map_tip[3]
            k += 1

        map_line3 += [tip_num]*4
        map_line3 += [3] * 6
        self.map_data[2] += map_line3

    def create_stage(self, bg):
        #self.set_stage_endless(tip_num,repeat)
        stage_len = self.map_data[0]
    
        for i in range(len(stage_len)):

            #甘奈
            if self.map_data[0][i] == 0:
                bg.blit(self.block[0], (25 * i - self.x_road, 125))
                
            elif self.map_data[0][i] == 1:
                bg.blit(self.block[1], (25 * i - self.x_road, 125))

            elif self.map_data[0][i] == 2:
                bg.blit(self.block[2], (25 * i - self.x_road, 125))

            elif self.map_data[0][i] == 3:
                bg.blit(self.block[3], (25 * i - self.x_road, 125))     

            elif self.map_data[0][i] == 4:
                bg.blit(self.block[4], (25 * i - self.x_road, 125))

            elif self.map_data[0][i] == 5:
                bg.blit(self.block[5], (25 * i - self.x_road, 125))  

            #ちきゆ
            if self.map_data[1][i] == 0:
                bg.blit(self.block[0], (25 * i - self.x_road, 225))
                
            elif self.map_data[1][i] == 1:
                bg.blit(self.block[1], (25 * i - self.x_road, 225))

            elif self.map_data[1][i] == 2:
                bg.blit(self.block[2], (25 * i - self.x_road, 225))

            elif self.map_data[1][i] == 3:
                bg.blit(self.block[3], (25 * i - self.x_road, 225))

            elif self.map_data[1][i] == 4:
                bg.blit(self.block[4], (25 * i - self.x_road, 225))

            elif self.map_data[1][i] == 5:
                bg.blit(self.block[5], (25 * i - self.x_road, 225)) 

            elif self.map_data[1][i] == 6:
                bg.blit(self.block[5], (25 * i - self.x_road, 225))

            #甜花
            if self.map_data[2][i] == 0:
                bg.blit(self.block[0], (25 * i - self.x_road, 325))
                
            elif self.map_data[2][i] == 1:
                bg.blit(self.block[1], (25 * i - self.x_road, 325))

            elif self.map_data[2][i] == 2:
                bg.blit(self.block[2], (25 * i - self.x_road, 325))

            elif self.map_data[2][i] == 3:
                bg.blit(self.block[3], (25 * i - self.x_road, 325))

            elif self.map_data[2][i] == 4:
                bg.blit(self.block[4], (25 * i - self.x_road, 325))

            elif self.map_data[2][i] == 5:
                bg.blit(self.block[5], (25 * i - self.x_road, 325))  

            elif self.map_data[2][i] == 6:
                bg.blit(self.block[5], (25 * i - self.x_road, 325))

    def stage_scrool2(self):
        global fall_flag
        if fall_flag == False:
            self.x_road += 1

        elif fall_flag == True:
            self.x_road += 0

        self.x_Limit()

    def x_Limit(self):
        global chk_goal

        line = self.map_data[0]

        if self.x_road >= len(line)*25 - 480: #960:画面の横幅
            self.x_road = len(line)*25 - 480
            chk_goal = True
            
        if self.x_road <= -100:
            self.x_road = -100

#ステージの動き============================================

#ライフ管理================================================
class Life_Manage(): #済
    def __init__(self):
        self.mark =pygame.image.load("enshutsu/mark2.png")

    def life_draw(self, bg):
        global index, life
        
        if life <= 3:
            for i in range(life):
                bg.blit(self.mark, (120 + 30 * i , 15))

        Txt = Text_Manage()

        if life >= 4:
            for i in range(3):
                bg.blit(self.mark, (120 + 30 * i , 15))

            Txt.text_draw("+" + str(life-3), WHITE, 25, 225, 30, bg)


#テキスト管理================================================
class Text_Manage():
    def __init__(self):
        self.message = "text"

    def text_draw(self, msg, col, size, x, y, bg):
        font = pygame.font.Font(("JF-Dot-Shinonome16.ttf"), size)

        sur3 = font.render(msg, True, (0,0,0))
        sur3_rect = sur3.get_rect(center=(x+1, y+1))
        bg.blit(sur3, sur3_rect)

        sur1 = font.render(msg, True, col)
        sur1_rect = sur1.get_rect(center=(x, y))
        bg.blit(sur1, sur1_rect)

        sur2 = font.render(msg, True, col)
        sur2_rect = sur2.get_rect(center=(x-1, y-1))
        bg.blit(sur2, sur2_rect)

#インターバル================================================
class Enshutsu():
    def __init__(self):
        self.i = -200
        self.amana1 = pygame.image.load("enshutsu/amn1.png")
        self.amana2 = pygame.image.load("enshutsu/amn2.png")

        self.tenka1 = pygame.image.load("enshutsu/tnk1.png")
        self.tenka2 = pygame.image.load("enshutsu/tnk2.png")

        self.chikiyu1 = pygame.image.load("enshutsu/cky1.png")
        self.chikiyu2 = pygame.image.load("enshutsu/cky2.png")            

        self.sP = pygame.image.load("enshutsu/P.png")

        self.last1 = pygame.image.load("enshutsu/last1.png")    
        self.last2 = pygame.image.load("enshutsu/last2.png")
        self.last3 = pygame.image.load("enshutsu/last3.png")

    def text_draw_left(self, msg, col, size, x, y, bg):
        font = pygame.font.Font(("JF-Dot-Shinonome16.ttf"), size)

        sur3 = font.render(msg, True, col)
        bg.blit(sur3, (x-1, y-1))

        sur1 = font.render(msg, True, col)
        bg.blit(sur1, (x, y))

    def text_draw_center(self, msg, col, size, x, y, bg):
        font = pygame.font.Font(("JF-Dot-Shinonome16.ttf"), size)
        
        sur_s = font.render(msg, True, (0,0,0))
        sur_rect_s = sur_s.get_rect(center=(x+2, y+2))
        bg.blit(sur_s, sur_rect_s)

        sur3 = font.render(msg, True, col)
        sur3_rect = sur3.get_rect(center=(x-1, y-1))
        bg.blit(sur3, sur3_rect)

        sur1 = font.render(msg, True, col)
        sur1_rect = sur1.get_rect(center=(x, y))
        bg.blit(sur1, sur1_rect)

        sur2 = font.render(msg, True, col)
        sur2_rect = sur2.get_rect(center=(x+1, y+1))
        bg.blit(sur2, sur2_rect)

    def text_draw_center56(self, msg, col, size, x, y, bg):
        font = pygame.font.Font(("JF-Dot-Shinonome16.ttf"), size)

        sur3 = font.render(msg, True, col)
        sur3_rect = sur3.get_rect(center=(x-1, y-1))
        bg.blit(sur3, sur3_rect)

        sur1 = font.render(msg, True, col)
        sur1_rect = sur1.get_rect(center=(x, y))
        bg.blit(sur1, sur1_rect)

        sur2 = font.render(msg, True, col)
        sur2_rect = sur2.get_rect(center=(x+1, y+1))
        bg.blit(sur2, sur2_rect)

    def tuto_rial(self, bg): #済
        global tuto_ind
        #sousa = pygame.image.load("enshutsu/sousa.png")        
        #self.text_draw_left(("[←]      ") + str(tuto_ind) + ("/3      [→]"), (255,255,255), 25, 35,300, bg)
        #bg.blit(sousa, (0,0))

        if tuto_ind == 1:
            sousa1 = pygame.image.load("enshutsu/sousa1.png")
            bg.blit(sousa1, (-1,0))

        if tuto_ind == 2:
            sousa2 = pygame.image.load("enshutsu/sousa2.png")
            bg.blit(sousa2, (0,0))

        if tuto_ind == 3:
            sousa3 = pygame.image.load("enshutsu/sousa3.png")
            bg.blit(sousa3, (0,0))

    def config(self, bg): #済
        global SOUSA_MODE, con_ind
        #con = pygame.image.load("enshutsu/config.png")
        #bg.blit(con, (0,0))

        if SOUSA_MODE == 1:
            con1 = pygame.image.load("enshutsu/config1.png")
            bg.blit(con1, (0,2))

        if SOUSA_MODE == 2:
            con2 = pygame.image.load("enshutsu/config2.png")
            bg.blit(con2, (0,0))

    def stage0(self, bg):
        global enshutsu
    
        WHITE = (255,255,255)

        img_s_a = pygame.transform.scale(self.amana1,[60, 60])
        img_s_c = pygame.transform.scale(self.chikiyu1,[60, 60])

        # -200 から100 -100から200 
        self.text_draw_center("STAGE 1",WHITE, 25, 240, 50 + enshutsu, bg)
        self.text_draw_center("「アプリコット」", WHITE, 25, 240, 100 + enshutsu, bg)

        self.text_draw_center("アルストロメリアは雑誌「アプリコット」の", WHITE, 15, 240, 140+ enshutsu, bg)
        self.text_draw_center("オーディションに向けて練習中で...", WHITE, 15, 240, 160+ enshutsu, bg)

        self.text_draw_left("「もっと厳しくお願いしたいのー！」", WHITE, 17, 125, 200, bg)
        self.text_draw_left("「反対ごっこなら──空っぽ", WHITE, 17, 50, 275, bg)
        self.text_draw_left("　ですね...何も感じません...！」", WHITE, 17, 50, 300, bg)

        bg.blit(img_s_a, (50, 175))
        #bg.blit(self.tenka1, (100, 250))
        bg.blit(img_s_c, (360, 275))

    def stage1(self, bg):
        global enshutsu
        WHITE = (255,255,255)

        img_s_a = pygame.transform.scale(self.amana1,[60, 60])
        img_s_c = pygame.transform.scale(self.chikiyu1,[60, 60])

        self.text_draw_center("STAGE 2",WHITE, 25, 240, 50 + enshutsu, bg)
        self.text_draw_center("「反対ごっこ」", WHITE, 25, 240, 100 + enshutsu, bg)
        self.text_draw_center("千雪さんは「アプリコット」に何か思い出があるようで...", WHITE, 15, 240, 140+ enshutsu, bg)

        self.text_draw_left("「これ『アプリコット』...！？", WHITE, 17, 125, 195, bg)
        self.text_draw_left("　千雪さん…持ってたの…！」", WHITE, 17, 125, 220, bg)
    
        self.text_draw_left("「...あっ…ううん...！", WHITE, 17, 50, 275, bg)
        self.text_draw_left("　たまたまなの...」", WHITE, 17, 50, 300, bg)

        bg.blit(img_s_a, (50, 175))
        bg.blit(img_s_c, (360, 275))

    def stage2(self, bg):
        global enshutsu
        WHITE = (255,255,255)

        img_s_a = pygame.transform.scale(self.amana1,[60, 60])
        img_s_t = pygame.transform.scale(self.tenka1,[60, 60])
        img_s_c = pygame.transform.scale(self.chikiyu1,[60, 60])
        img_s_p = pygame.transform.scale(self.sP,[60, 60])

        self.text_draw_center("STAGE 3",WHITE, 25, 240, 50 + enshutsu, bg)
        self.text_draw_center("「そして彼女はインターホンを鳴らす」", WHITE, 25, 240, 100 + enshutsu, bg)
        self.text_draw_center("甜花ちゃんが偶然聞いた話の内容とは...？", WHITE, 15, 240, 140+ enshutsu, bg)
        #self.text_draw_center("何か思い出があるようで…", WHITE, 30, 480, 320, bg)

        self.text_draw_left("「いや、だって…！グランプリがうちの", WHITE, 17, 125, 195, bg)
        self.text_draw_left("　大崎甘奈に内定してるっていうのは─」", WHITE, 17, 125, 220, bg)
    
        self.text_draw_left("「...えっ」", WHITE, 17, 180, 285, bg)

        bg.blit(img_s_p, (50, 175))
        bg.blit(img_s_t, (360, 275))

    def stage3(self, bg):
        global enshutsu
        WHITE = (255,255,255)

        img_s_a = pygame.transform.scale(self.amana1,[60, 60])
        img_s_t = pygame.transform.scale(self.tenka1,[60, 60])
        img_s_c = pygame.transform.scale(self.chikiyu1,[60, 60])
        img_s_p = pygame.transform.scale(self.sP,[60, 60])

        self.text_draw_center("STAGE 4",WHITE, 25, 240, 50 + enshutsu, bg)
        self.text_draw_center("「ふたつの夜」", WHITE, 25, 240, 100 + enshutsu, bg)
        self.text_draw_center("千雪さんは甘奈ちゃんと甜花ちゃんに大事な話があるようで…", WHITE, 15, 240, 140+ enshutsu, bg)

        self.text_draw_left("「...千雪さん...」", WHITE, 17, 125, 200, bg)
    
        self.text_draw_left("「───アプリコットのオーディション", WHITE, 17, 50, 275, bg)
        self.text_draw_left("　私も...受けたい」", WHITE, 17, 50, 300, bg)

        bg.blit(img_s_a, (50, 175))
        bg.blit(img_s_c, (360, 275))

    def stage4(self, bg):
        global enshutsu
        BLACK = (128,128,192)

        img_s_a = pygame.transform.scale(self.amana1,[60, 60])
        img_s_t = pygame.transform.scale(self.tenka1,[60, 60])
        img_s_c = pygame.transform.scale(self.chikiyu1,[60, 60])
        img_s_p = pygame.transform.scale(self.sP,[60, 60])

        self.text_draw_center56("STAGE 5",BLACK, 25, 240, 50 + enshutsu, bg)
        self.text_draw_center56("「こわい」", BLACK, 25, 240, 100 + enshutsu, bg)
        self.text_draw_center56("出来レースの話を聞いた甘奈ちゃんは", BLACK, 15, 240, 130+ enshutsu, bg)
        self.text_draw_center56("ユニットを思いオーディションの辞退を考えますが...", BLACK, 15, 240, 150+ enshutsu, bg)


        self.text_draw_left("「反対ごっこ...しよっか」", BLACK, 17, 125, 200, bg)
    
        self.text_draw_left("「アルストロメリア、なんか...", BLACK, 17, 50, 275, bg)
        self.text_draw_left("　一番...大事じゃない...！」", BLACK, 17, 50, 300, bg)

        bg.blit(img_s_c, (50, 175))
        bg.blit(img_s_t, (360, 275))

    def stage5(self, bg):
        global enshutsu
        BLACK = (128,128,192)

        img_s_a = pygame.transform.scale(self.amana2,[60, 60])
        img_s_t = pygame.transform.scale(self.tenka1,[60, 60])
        img_s_c = pygame.transform.scale(self.chikiyu1,[60, 60])
        img_s_p = pygame.transform.scale(self.sP,[60, 60])

        self.text_draw_center56("STAGE 6",BLACK, 25, 240, 50 + enshutsu, bg)
        self.text_draw_center56("「薄桃色にこんがらがって」", BLACK, 25, 240, 100 + enshutsu, bg)
        self.text_draw_center56("「声」を出したアルストロメリアは...", BLACK, 15, 240, 140+ enshutsu, bg)

        self.text_draw_left("「───甘奈と戦ってください、", BLACK, 17, 125, 195, bg)
        self.text_draw_left("　千雪さん」", BLACK, 17, 125, 220, bg)
    
        self.text_draw_left("「───はい」", BLACK, 17, 150, 285, bg)

        bg.blit(img_s_a, (50, 175))
        bg.blit(img_s_c, (360, 275))

    def ending(self, bg):
        global en_ind, en_timer1, kansei, messe, bloomy
        WHITE = (255,255,255)

        img_s_t = pygame.transform.scale(self.tenka1,[60, 60])
        img_s_t2 = pygame.transform.scale(self.tenka2,[60, 60])
        img_s_c = pygame.transform.scale(self.chikiyu1,[60, 60])
        img_s_c2 = pygame.transform.scale(self.chikiyu2,[60, 60])

        #se_kansei = pygame.mixer.Sound("fan_no_minasan.ogg")
        se_messe = pygame.mixer.Sound("sound/messe.ogg")

        if en_ind == 1:
            bg.blit(self.last1, (0,0))
            self.text_draw_center("あーまーな☆ あーまーな☆",WHITE, 25, 240, 240, bg)

        if en_ind == 2:
            bg.blit(self.last1, (0,0))
            bg.blit(img_s_c2, (50,235))
            self.text_draw_left("「あーまーな☆」",WHITE, 25, 120, 240, bg)

        if en_ind == 3:
            bg.blit(self.last1, (0,0))
            bg.blit(img_s_t2, (50,235))
            self.text_draw_left("「あーまーな......☆」",WHITE, 25, 120, 240, bg)

        if en_ind == 4:
            bg.blit(self.last1, (0,0))
            bg.blit(img_s_t, (50,235))
            self.text_draw_left("「千雪さん...ありがと...」",WHITE, 25, 120, 240, bg)    

        if en_ind == 5:
            bg.blit(self.last1, (0,0))
            bg.blit(img_s_t, (50,235))
            self.text_draw_left("「千雪さん...大事なもの...",WHITE, 25, 120, 240, bg)
            self.text_draw_left("　諦めなかった...」",WHITE, 25, 120, 270, bg)

        if en_ind == 6:
            bg.blit(self.last1, (0,0))
            bg.blit(img_s_t, (50,235))
            self.text_draw_left("「だから甜花も、わかった...",WHITE, 25, 120, 240, bg)
            self.text_draw_left("　大事なもの...」",WHITE, 25, 120, 270, bg)

        if en_ind == 7:
            bg.blit(self.last1, (0,0))
            bg.blit(img_s_c, (50,235))
            self.text_draw_left("「─────",WHITE, 25, 120, 240, bg)
            self.text_draw_left("　甜花ちゃん......」",WHITE, 25, 120, 270, bg) 

        if en_ind == 8:
            bg.blit(self.last1, (0,0))
            bg.blit(img_s_c, (50,235))
            self.text_draw_left("「─────",WHITE, 25, 120, 240, bg) 
            self.text_draw_left("　悔しい......」",WHITE, 25, 120, 270, bg)

        if en_ind == 9:
            bg.blit(self.last2, (0,0))
            self.text_draw_center("「悔しいなぁ............っ」",WHITE, 25, 240, 240, bg)
            
            bloomy += 1
            if bloomy == 1:
                pygame.mixer.music.load("sound/bloomy+.ogg")
                pygame.mixer.music.play(0)

        if en_ind == 10:
            bg.blit(self.last2, (0,0))
            self.text_draw_left("「ちょっとだけ...",WHITE, 25, 120, 240, bg)  
            self.text_draw_left("　肩、貸してね......」",WHITE, 25, 120, 270, bg) 

        if en_ind == 11:
            bg.blit(self.last2, (0,0))
            self.text_draw_center("「う、うん.........!」",WHITE, 25, 240, 240, bg)

        if en_ind == 12:
            bg.blit(self.last2, (0,0))
            self.text_draw_center("「甜花......",WHITE, 25, 240, 240, bg) 
            self.text_draw_center("　でも.........」",WHITE, 25, 240, 270, bg) 

        if en_ind == 13:
            bg.blit(self.last2, (0,0))
            self.text_draw_center("「だから...大事な",WHITE, 25, 240, 240, bg) 
            self.text_draw_center("　オーディションになった...」",WHITE, 25, 240, 270, bg) 

        if en_ind == 14:
            bg.blit(self.last2, (0,0))
            self.text_draw_center("「私も思ったの、声にしなきゃ",WHITE, 25, 240, 240, bg)  
            self.text_draw_center("　いけないことで──」",WHITE, 25, 240, 270, bg)

        if en_ind == 15:
            bg.blit(self.last2, (0,0))
            self.text_draw_center("「───してないこと、",WHITE, 25, 240, 240, bg) 
            self.text_draw_center("　あったなって」",WHITE, 25, 240, 270, bg)

        if en_ind == 16:
            bg.blit(self.last3, (0,0))
            bg.blit(img_s_c, (50,235))
            self.text_draw_left("『くやしい！、",WHITE, 25, 120, 240, bg)  
            self.text_draw_left("　負けたのくやしいよー！』",WHITE, 25, 120, 270, bg)
            messe += 1
            if messe == 1:
                se_messe.play()

        if en_ind == 17:
            bg.blit(self.last3, (0,0))
            bg.blit(img_s_t, (50,235))
            self.text_draw_left("「──わ......!",WHITE, 25, 120, 240, bg)  
            self.text_draw_left("　グループに......──」",WHITE, 25, 120, 270, bg)

        if en_ind == 18:
            bg.blit(self.last3, (0,0))
            bg.blit(img_s_c, (50,235))
            self.text_draw_left("「ふふっ",WHITE, 25, 120, 240, bg)  
            self.text_draw_left("　3人でアルストロメリア...」",WHITE, 25, 120, 270, bg)

        if en_ind == 19:
            bg.blit(self.last3, (0,0))
            bg.blit(img_s_c2, (50,235))
            self.text_draw_left("「遠慮はしないんだ、もう」",WHITE, 25, 120, 240, bg)   

    def tuto_sentaku(self):
        global index, t_key, mt_key, tuto_ind
        key = pygame.key.get_pressed()
        mt_key -= 1

        if mt_key <= 0:
            mt_key = 0
                
        if key[pygame.K_LEFT] == True and mt_key <= 0:
            tuto_ind -= 1
            mt_key = 10
        if key[pygame.K_RIGHT] == True and mt_key <= 0:
            tuto_ind += 1
            mt_key = 10

        if key[pygame.K_SPACE] == True and mt_key <= 0:
            index = 0
            t_key = 10


        if tuto_ind <= 1:
            tuto_ind = 1
        if tuto_ind >= 3:
            tuto_ind = 3

    def config_sentaku(self):
        global t_key,SOUSA_MODE,index

        key = pygame.key.get_pressed()
        if t_key <= 0:
            t_key = 0
            if key[pygame.K_LEFT] == True:
                SOUSA_MODE -= 1
                t_key = 10
            if key[pygame.K_RIGHT] == True:
                SOUSA_MODE += 1
                t_key = 10

            if key[pygame.K_SPACE] == True:
                index = 0
                t_key = 10

        if SOUSA_MODE < 1:
            SOUSA_MODE = 2
        if SOUSA_MODE > 2:
            SOUSA_MODE = 1

#UI=========================================================
class UI():
    def __init__(self):
        self.width = 480
        self.height = 360
        self.radius = 40

        self.alphaC = pygame.image.load("enshutsu/alpha_circle.png")
        self.alphaR = pygame.image.load("enshutsu/alpha_rect.png")
    
    def draw_under_screen(self, scrn):
        pygame.draw.rect(scrn, NAVY, [0, self.height, self.width, self.height*2])

    def draw_button_bg(self, scrn, col1, col6, col2, col5, col3, col4, ENTER):
        #slct:           WHITE, WHITE, NAVY, NAVY,NAVY, NAVY, WHITE
        #SOUSA_MODE == 1:COLOR_A, COLOR_A, COLOR_C, COLOR_C, COLOR_T, COLOR_T, NAVY
        #SOUSA_MODE == 2:COLOR_A, COLOR_T, COLOR_C, COLOR_C, COLOR_T, COLOR_A, NAVY
        
        radius = 40
        pygame.draw.circle(scrn, col1, [70, self.height + 140], self.radius)
        pygame.draw.circle(scrn, col6, [self.width - 70, self.height + 140], self.radius)

        pygame.draw.circle(scrn, col2, [120, self.height + 220], self.radius)
        pygame.draw.circle(scrn, col5, [self.width - 120, self.height + 220], self.radius)

        pygame.draw.circle(scrn, col3, [195, self.height + 280], self.radius)
        pygame.draw.circle(scrn, col4, [self.width - 195, self.height + 280], self.radius)

        pygame.draw.rect(scrn, ENTER, [70 + radius + 30, self.height + 100, 200, 70])

    def draw_button(self, scrn):
        radius = 40
        pygame.draw.circle(scrn, WHITE, [70, self.height + 140], self.radius, width=5)
        pygame.draw.circle(scrn, WHITE, [self.width - 70, self.height + 140], self.radius, width=5)

        pygame.draw.circle(scrn, WHITE, [120, self.height + 220], self.radius, width=5)
        pygame.draw.circle(scrn, WHITE, [self.width - 120, self.height + 220], self.radius, width=5)

        pygame.draw.circle(scrn, WHITE, [195, self.height + 280], self.radius, width=5)
        pygame.draw.circle(scrn, WHITE, [self.width - 195, self.height + 280], self.radius, width=5)

        pygame.draw.rect(scrn, WHITE, [70 + radius + 30, self.height + 100, 200, 70], width=5)

    def draw_button_tri(self, scrn):
        radius = 40
        pygame.draw.rect(scrn, WHITE, [70 + radius + 30, self.height + 100, 70-1, 70])
        pygame.draw.rect(scrn, WHITE, [70 + radius + 30 + 70 + 1, self.height + 100, 60 - 1, 70])
        pygame.draw.rect(scrn, WHITE, [70 + radius + 30 + 70 + 60 + 1, self.height + 100, 70 - 1, 70])

    def draw_b_chara(self, scrn, b1, b6, b2, b5, b3, b4, ENTER):
        #ctrl: "A", "L", "S", "K", "D", "J"
        #slct: "←", "→", "", "", "", ""

        Txt = Text_Manage()
        Txt.text_draw(b1, NAVY, 50, 70, self.height + 140, scrn)
        Txt.text_draw(b6, NAVY, 50, self.width - 70, self.height + 140, scrn)

        Txt.text_draw(b2, NAVY, 50, 120, self.height + 220, scrn)
        Txt.text_draw(b5, NAVY, 50, self.width - 120, self.height + 220, scrn)

        Txt.text_draw(b3, NAVY, 50, 195, self.height + 280, scrn)
        Txt.text_draw(b4, NAVY, 50, self.width - 195, self.height + 280, scrn)

        Txt.text_draw(ENTER, NAVY, 50, 240, self.height + 138, scrn)

    def calc_range_button1(self, X1, Y1):
        global x1, y1
        #(x1 >= 70 - ui.radius and x1 <= 70 + ui.radius) and (y1 >= ui.height + 140 - ui.radius and y1 <= ui.height + 140 + ui.radius)
        
        #(x1 >= ui.width - 70 - ui.radius and x1 <= ui.width - 70 + ui.radius) and (y1 >= ui.height + 140 - ui.radius and y1 <= ui.height + 140 + ui.radius)
        return [(x1 >= X1- self.radius and x1 <= X1 + self.radius) and (y1 >= self.height + Y1- self.radius and y1 <= self.height + Y1+ self.radius),
                (x1 >= self.width - X1 - self.radius and x1 <= self.width - X1 + self.radius) and (y1 >= self.height + Y1 - self.radius and y1 <= self.height + Y1 + self.radius)]

    def calc_range_Enter(self):
        global x1, y1
        #(x1 >= 100 + ui.radius and x1 <= 100 + ui.radius + 200) and (y1 >= ui.height + 100 and y1 <= ui.height + 100 + 70)
        X_min = (x1 >= 100 + self.radius)
        X_max = (x1 <= 100 + self.radius + 200)

        Y_min = (y1 >= self.height + 100)
        Y_max = (y1 <= self.height + 100 + 70)

        return (X_min and X_max) and (Y_min and Y_max)
    
    def calc_range_Enter_L(self):
        global x1, y1
        #(x1 >= 100 + ui.radius and x1 <= 100 + ui.radius + 200) and (y1 >= ui.height + 100 and y1 <= ui.height + 100 + 70)
        X_min = (x1 >= 100 + self.radius)
        X_max = (x1 <= 100 + self.radius + 50)

        Y_min = (y1 >= self.height + 100)
        Y_max = (y1 <= self.height + 100 + 70)

        return (X_min and X_max) and (Y_min and Y_max)

    def calc_range_Enter_C(self):
        global x1, y1
        #(x1 >= 100 + ui.radius and x1 <= 100 + ui.radius + 200) and (y1 >= ui.height + 100 and y1 <= ui.height + 100 + 70)
        X_min = (x1 >= 100 + self.radius + 50)
        X_max = (x1 <= 100 + self.radius + 50 + 100)

        Y_min = (y1 >= self.height + 100)
        Y_max = (y1 <= self.height + 100 + 70)

        return (X_min and X_max) and (Y_min and Y_max)

    def calc_range_Enter_R(self):
        global x1, y1
        #(x1 >= 100 + ui.radius and x1 <= 100 + ui.radius + 200) and (y1 >= ui.height + 100 and y1 <= ui.height + 100 + 70)
        X_min = (x1 >= 100 + self.radius + 50 + 100)
        X_max = (x1 <= 100 + self.radius + 50 + 100 + 50)

        Y_min = (y1 >= self.height + 100)
        Y_max = (y1 <= self.height + 100 + 70)

        return (X_min and X_max) and (Y_min and Y_max)

    def button_turn_white(self, scrn):
                if self.calc_range_button1(70, 140)[0]:
                    scrn.blit(self.alphaC, (70 - self.radius, self.height + 140 - self.radius))
                if self.calc_range_button1(70, 140)[1]:
                    scrn.blit(self.alphaC, (self.width - 70 - self.radius, self.height + 140 - self.radius))

                if self.calc_range_button1(120, 220)[0]:
                    scrn.blit(self.alphaC, (120 - self.radius, self.height + 220 - self.radius))
                if self.calc_range_button1(120, 220)[1]:
                    scrn.blit(self.alphaC, (self.width - 120 - self.radius, self.height + 220 - self.radius))

                if self.calc_range_button1(195, 280)[0]:
                    scrn.blit(self.alphaC, (195 - self.radius, self.height + 280 - self.radius))
                if self.calc_range_button1(195, 280)[1]:
                    scrn.blit(self.alphaC, (self.width - 195 - self.radius, self.height + 280 - self.radius))

                if self.calc_range_Enter():
                    scrn.blit(self.alphaR, (100 + self.radius, self.height + 105))

#=================================================================================
async def main():
    global fall_flag, chk_0_A, chk_0_C, chk_0_T, index, stage, generated, generated2, life,enshutsu
    global chk_goal_A, chk_goal_C, chk_goal_T, chk_goal
    global chk_Lastgoal_C, chk_Lastgoal_T
    global rect1, rect2
    global en_ind, en_timer1, stop_ce, en_ind7, tuto_ind, t_key, mode_flag
    global SOUSA_MODE, con_ind
    global key_spc, mt_key, endless_flag
    global x1, y1

    pygame.init()
    pygame.display.set_caption("")

    screen = pygame.display.set_mode((480, 720))
    clock = pygame.time.Clock()

    #甘奈
    Moving_A = Move_Amana()
    Moving_AT = Move_Amana_tuto()
    #ちきゆ
    Moving_C = Move_Chikiyu()
    Moving_CT = Move_Chikiyu_tuto()
    Moving_CE = Move_Chikiyu_Ending()
    #甜花
    Moving_T = Move_Tenka()
    Moving_TT = Move_Tenka_tuto()

    #演出
    En = Enshutsu()

    #ステージ
    StCre = Stage_Create()
    S_Random = Stage_Create_RN()

    #ライフ
    Life = Life_Manage()
    #テキスト
    Txt = Text_Manage()
    #UI
    ui = UI()
    
    #甘奈
    chk_0_A = True
    chk_goal_A = False #False=ゴールしていない
    #ちきゆ
    chk_0_C = True
    chk_goal_C = False #False=ゴールしていない
    chk_Lastgoal_C = False #False=ゴールしていない
    #甜花
    chk_0_T = True
    chk_goal_T = False #False=ゴールしていない
    chk_Lastgoal_T = False #False=ゴールしていない


    chk_goal = False

    t_GO = 0

    index = 0 #11に戻す
    tmr_music = 0
    tmr_se = 0
    life = 3
    stage = 1
    mode_flag = 1
    endless_flag = False

    #アイキャッチ用
    from5to1 = 60
    from5toaccA = 480
    from5toaccB = 480
    can_SPACE = False

    #説明用
    tuto_ind = 1
    t_key = 90
    mt_key = 0
    tmr = 0

    #エンディング用
    stop_ce = False
    en_ind7 = 1
    
    #ページの進行
    en_ind = 1
    en_timer1 = 120
    en_timer2 = 180
    en_timer3 = 600

    #キーコン
    con_ind = 1
    SOUSA_MODE = 1

    S_Random = Stage_Create_RN()
    S_Random.set_stage(5, 2)
    generated2 = S_Random.map_data

    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.load("sound/arusutoromeria.ogg")

    se_jump = pygame.mixer.Sound("sound/jump.ogg")
    se_turn = pygame.mixer.Sound("sound/turn.ogg")
    se_fall = pygame.mixer.Sound("sound/fall.ogg")
    se_gameover = pygame.mixer.Sound("sound/gameover.ogg")
    se_sairen = pygame.mixer.Sound("sound/sairen.ogg")

    button = [pygame.image.load("under/ub_index0.png"),
              
              pygame.image.load("under/ub_index1_S1.png"),
              pygame.image.load("under/ub_index1_S2.png"),
              
              pygame.image.load("under/ub_index1_S1_st6.png"),
              pygame.image.load("under/ub_index1_S2_st6.png"),

              pygame.image.load("under/ub_index2_GAMEOVER.png"),
              pygame.image.load("under/ub_index2_RETRY.png"),
              pygame.image.load("under/ub_index2_ENDLESS.png"),

              pygame.image.load("under/ub_index4.png"),
              pygame.image.load("under/ub_index7_E.png"),
              pygame.image.load("under/ub_index8~9_S1.png"),
              pygame.image.load("under/ub_index9_S2.png"),

              pygame.image.load("under/ub_basic.png"),
            ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #pygame.mouse.get_pressed()
            
        if index == 0: #済
            pygame.mixer.music.stop()
            screen.fill((0, 0, 64))
            #pygame.draw.rect(screen, NAVY, [0, 360, 480, 720])
            screen.blit(button[0], (0,360))

            TITLE = pygame.image.load("title.png")
            title_s = pygame.transform.scale(TITLE, [528, 396])
            screen.blit(title_s, (-30, -30)) 

            chk_goal = False

            Moving_A.__init__()
            chk_goal_A = False

            Moving_C.__init__()
            chk_goal_C = False

            Moving_T.__init__()
            chk_goal_T = False

            StCre.__init__()
            Moving_CE.__init__()
            
            index = 0
            tmr_music = 0
            tmr_se = 0
            
            life = 3
            t_GO = 0

            rect1 = 0
            rect2 = 0

            en_ind = 1
            en_timer1 = 120

            
            tmr += 1
            #t_key -= 1
            if tmr % 40 < 20: 
                pygame.draw.polygon(screen, (255,255,255), [[180,258],[180,278],[160,268]])
                pygame.draw.polygon(screen, (255,255,255), [[450,258],[450,278],[470,268]])

            if mode_flag == 1:
                Txt.text_draw("STORY MODE", WHITE, 40, 320, 270, screen)
                #pygame.draw.polygon(screen, (255,255,255), [[90,200],[90,220],[125,210]])
            elif mode_flag == 2:
                Txt.text_draw("ENDLESS MODE", WHITE, 40, 320, 270, screen)
                #pygame.draw.polygon(screen, (255,255,255), [[90,240],[90,260],[125,250]])
            elif mode_flag == 3:
                Txt.text_draw("MANUAL", WHITE, 40, 320, 270, screen)
                #pygame.draw.polygon(screen, (255,255,255), [[90,275],[90,295],[125,285]])
            elif mode_flag == 4:
                Txt.text_draw("CONFIG", WHITE, 40, 320, 270, screen)
                #pygame.draw.polygon(screen, (255,255,255), [[90,315],[90,335],[125,325]])

            Txt.text_draw("START TO PRESS [SPACE]", WHITE, 20, 320, 320, screen)

            if tmr == 1:
                title_chara = random.randint(0,2)

            if title_chara == 0:
                Moving_AT.move_amana_title()
                Moving_AT.draw_chara_title(screen)
            elif title_chara == 1:
                Moving_CT.move_chikiyu_title()
                Moving_CT.draw_chara_title(screen)
            elif title_chara == 2:
                Moving_TT.move_tenka_title()
                Moving_TT.draw_chara_title(screen)

            key = pygame.key.get_pressed()

            #キー入力==================================================
            if t_key < 0:
                t_key = 0
                #左右=================================================
                if key[pygame.K_LEFT] == True:
                    se_turn.play()
                    mode_flag -= 1
                    t_key = 10

                if key[pygame.K_RIGHT] == True:
                    se_turn.play()
                    mode_flag += 1
                    t_key = 10

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #マウス左ボタンダウンイベント
                        x1,y1 = event.pos

                        if ui.calc_range_button1(70, 140)[0]:
                            se_turn.play()
                            mode_flag -= 1
                            t_key = 10

                        if ui.calc_range_button1(70, 140)[1]:
                            se_turn.play()
                            mode_flag += 1
                            t_key = 10

                if mode_flag < 1:
                    mode_flag = 4
                if mode_flag > 4:
                    mode_flag = 1
                
                #決定=================================================
                if key[pygame.K_SPACE] == True:
                    #se_jump.play()
                    if mode_flag == 1:
                        stage = 1
                        fall_flag = False
                        t_key = 50
                        endless_flag = False
                        life = 3
                        index = 5

                    elif mode_flag == 2:
                        pygame.mixer.music.load("arusutoromeria.ogg")
                        S_Random.set_stage_endless(1, 5)
                        generated = S_Random.map_data
                        stage = 1
                        fall_flag = False
                        t_key = 50
                        endless_flag = True
                        life = 3                        
                        index = 10

                    elif mode_flag == 3:
                        mt_key = 50
                        tuto_ind = 1
                        index = 8

                    elif mode_flag == 4:
                        t_key = 50
                        tuto_ind = 1
                        index = 9

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #マウス左ボタンダウンイベント
                        x1,y1 = event.pos
                        if ui.calc_range_Enter():
                            if mode_flag == 1:
                                stage = 1
                                fall_flag = False
                                t_key = 50
                                endless_flag = False
                                life = 3
                                index = 5

                            elif mode_flag == 2:
                                pygame.mixer.music.load("sound/arusutoromeria.ogg")
                                S_Random.set_stage_endless(1, 5)
                                generated = S_Random.map_data
                                stage = 1
                                fall_flag = False
                                t_key = 50
                                endless_flag = True
                                life = 3                        
                                index = 10

                            elif mode_flag == 3:
                                t_key = 50
                                tuto_ind = 1
                                index = 8

                            elif mode_flag == 4:
                                t_key = 50
                                tuto_ind = 1
                                index = 9
            #キー入力==================================================

        if index == 1: #済
            if tmr_music == 1:
                pygame.mixer.music.play(-1)

            if stage == 1 or stage == 2:
                screen.fill(StCre.BLUE)

            if stage == 3 or stage == 4:
                screen.fill(StCre.BLACK)

            if stage == 5 or stage == 6:
                screen.fill(StCre.PINK)
        #甘奈        
            Moving_A.t_move += 1
            Moving_A.t_jump += 1
            Moving_A.t_draw += 1
        #ちきゆ        
            Moving_C.t_move += 1
            Moving_C.t_jump += 1
            Moving_C.t_draw += 1
        #甜花        
            Moving_T.t_move += 1
            Moving_T.t_jump += 1
            Moving_T.t_draw += 1

            StCre.stage_scrool2()
            StCre.create_stage(screen)

#====================甘奈=======================================================
        # キャラの描画
            Moving_A.draw_chara(screen)        
        #床の判定(なんか関数に出来ない)
            StA = StCre.map_data[0]
            #print(StA)　#チェック用

            if Moving_A.turn_int == -1: #左向き
                if chk_goal_A == False:                
                    B = int((Moving_A.x_amana + StCre.x_road)/25) #左向きの右寄り
                    #C = int((Moving_A.x_amana + StCre.x_road)/100 + 1) #左向きの左寄り

                if chk_goal_A == False:                
                    B = int((Moving_A.x_amana + StCre.x_road)/25)
                    #print(B)　チェック用
                    if StA[B] == 0 and StA[B+1] == 0:
                        chk_0_A = False

                    elif StA[B] == 6:
                        Moving_A.canJump = False

                    elif StA[B] == 3:
                        chk_goal_A = True

                    else:
                        chk_0_A = True

            if Moving_A.turn_int == 1: #右向き
                if chk_goal_A == False: 
                    A = int((Moving_A.x_amana + StCre.x_road )/25)
                #print(A)　チェック用
                    if StA[A] == 0:
                        chk_0_A = False
                    if StA[A] == 1 or StA[A] == 2 or StA[A] == 4 or StA[A] == 5:
                        chk_0_A = True
                
                    if StA[A] == 3:
                        chk_goal_A = True
                #print(chk_0_A)　チェック用
        #ここまで床
            key = pygame.key.get_pressed()
            Moving_A.move_amana()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #マウス左ボタンダウンイベント
                    x1,y1 = event.pos
                    if ui.calc_range_button1(195, 280)[1]:
                        Moving_A.move_amana_click()

                    if SOUSA_MODE == 1:
                        if ui.calc_range_button1(195, 280)[0]:
                            Moving_A.turn_amana_click()
                    if SOUSA_MODE == 2:
                        if ui.calc_range_button1(70, 140)[0]:
                            Moving_A.turn_amana_click()

            Moving_A.t_canjump -= 1

            if Moving_A.t_canjump == 0:
                Moving_A.jump_reset()

            if Moving_A.t_turn == 0: #タイマーが0で
                Moving_A.turn_reset() #ターン出来るようにする

#====================ちきゆ=======================================================
        # キャラの描画
            Moving_C.draw_chara(screen)
        #床の判定(なんか関数に出来ない)
            StC = StCre.map_data[1]
            #print(StC) #チェック用

            if Moving_C.turn_int == -1:
                if chk_goal_C == False:                
                    B = int((Moving_C.x_amana + StCre.x_road)/25)
                    #print(B)　チェック用
                    if StC[B] == 0 and StC[B+1] == 0:
                        chk_0_C = False

                    elif StC[B] == 6:
                        Moving_C.canJump = False
                        chk_Lastgoal_C = True  

                    elif StC[B] == 3:
                        chk_goal_C = True
                    else:
                        chk_0_C = True

            if Moving_C.turn_int == 1:
                A = int((Moving_C.x_amana + StCre.x_road )/25)
            #print(A)　チェック用
                if StC[A] == 0:
                    chk_0_C = False
                if StC[A] == 1 or StC[A] == 2 or StC[A] == 4 or StC[A] == 5:
                    chk_0_C = True
                
                if StC[A] == 3:
                    chk_goal_C = True

                if StC[A] == 6:
                    Moving_C.canJump = False
                    chk_Lastgoal_C = True
            #print(chk_0_A)　チェック用
        #ここまで床
            key = pygame.key.get_pressed()

            Moving_C.move_chikiyu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #マウス左ボタンダウンイベント
                    x1,y1 = event.pos
                    if ui.calc_range_button1(120, 220)[1]:                   
                        Moving_C.move_amana_click()
                    
                    if ui.calc_range_button1(120, 220)[0] and Moving_C.canTurn == True:
                        Moving_C.turn_amana_click()

            Moving_C.t_canjump -= 1

            if Moving_C.t_canjump == 0:
                Moving_C.jump_reset()

            if Moving_C.t_turn == 0: #タイマーが0で
                Moving_C.turn_reset() #ターン出来るようにする
#====================甜花=======================================================
        # キャラの描画
            Moving_T.draw_chara(screen)
            #print(Moving_T.y)
        
        #床の判定(なんか関数に出来ない)
            StT = StCre.map_data[2]
            #print(StT)　#チェック用
            
            if Moving_T.turn_int == -1:
                if chk_goal_T == False:                
                    B = int((Moving_T.x_amana + StCre.x_road)/25)
                    #print(B)　チェック用
                    if StT[B] == 0 and StT[B+1] == 0:
                        chk_0_T = False

                    elif StT[B] == 6:
                        Moving_T.canJump = False
                        chk_Lastgoal_T = True  

                    elif StT[B] == 3:
                        chk_goal_T = True

                    else:
                        chk_0_T = True

            if Moving_T.turn_int == 1:
                A = int((Moving_T.x_amana + StCre.x_road )/25)
            #print(A)　チェック用
                if StT[A] == 0:
                    chk_0_T = False
                if StT[A] == 1 or StT[A] == 2 or StT[A] == 4 or StT[A] == 5:
                    chk_0_T = True

                if StT[A] == 6:
                    Moving_T.canJump = False
                    chk_Lastgoal_T = True                

                if StT[A] == 3:
                    chk_goal_T = True
            #print(chk_0_A)　チェック用
        #ここまで床
            key = pygame.key.get_pressed()
            Moving_T.move_tenka()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #マウス左ボタンダウンイベント
                    x1,y1 = event.pos
                    if ui.calc_range_button1(70, 140)[1]:
                        Moving_T.move_amana_click()

                    if SOUSA_MODE == 1:
                        if ui.calc_range_button1(70, 140)[0]:
                            Moving_T.turn_amana_click()
                    if SOUSA_MODE == 2:
                        if ui.calc_range_button1(195, 280)[0]:
                            Moving_T.turn_amana_click()
            Moving_T.t_canjump -= 1

            if Moving_T.t_canjump == 0:
                Moving_T.jump_reset()

            if Moving_T.t_turn == 0: #タイマーが0で
                Moving_T.turn_reset() #ターン出来るようにする

#===========================================================================

            #固定=============================================================
            Life.life_draw(screen)
            Txt.text_draw("STAGE  " + str(stage), WHITE, 25, 390, 30, screen)
            Txt.text_draw("MENTAL: ", WHITE, 25, 75, 30, screen)

            Moving_A.rect_x_update()
            Moving_A.rect_y_update()

            Moving_C.rect_x_update()
            Moving_C.rect_y_update()

            Moving_T.rect_x_update()
            Moving_T.rect_y_update()

            #下画面=========================================================
            ui.draw_under_screen(screen)
            if stage == 6 and \
                chk_goal == True and \
                chk_goal_A == True and\
                chk_Lastgoal_C == True and\
                chk_Lastgoal_T == True:

                if SOUSA_MODE == 1:
                    screen.blit(button[2], (0,360))
                elif SOUSA_MODE == 2:
                    screen.blit(button[4], (0,360))
            
            else:        
                if SOUSA_MODE == 1:
                    screen.blit(button[1], (0,360))
                elif SOUSA_MODE == 2:
                    screen.blit(button[3], (0,360))
            #下画面=========================================================

            #ストーリー仕様=============================================================================
            if stage == 6:
                if chk_goal == True and \
                    chk_goal_A == True and\
                    chk_Lastgoal_C == True and\
                    chk_Lastgoal_T == True:

                    if SOUSA_MODE == 1 or SOUSA_MODE == 3:
                        if key[pygame.K_d] == True:  #<===============================================
                            index = 4
                            tmr_music = 0
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1: #マウス左ボタンダウンイベント
                                x1,y1 = event.pos
                                if ui.calc_range_button1(195, 280)[0]:
                                    index = 4
                                    tmr_music = 0

                    if SOUSA_MODE == 2 or SOUSA_MODE == 4:
                        if key[pygame.K_a] == True:  #<===============================================
                            index = 4
                            tmr_music = 0
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1: #マウス左ボタンダウンイベント
                                x1,y1 = event.pos
                                if ui.calc_range_button1(70, 140)[0]:
                                    index = 4
                                    tmr_music = 0
            #ストーリー仕様=============================================================================

            #ステージクリアへ=============================================================================
            if chk_goal == True and \
                chk_goal_A == True and\
                chk_goal_C == True and\
                chk_goal_T == True:

                index = 4
                tmr_music = 0

            #固定

        if index == 2: #ミス、ゲームオーバー
            pygame.mixer.music.stop()
            
            #通常モード
            if endless_flag == False:
                if stage == 1 or stage == 2:
                    screen.fill(StCre.BLUE)

                elif stage == 3 or stage == 4:
                    screen.fill(StCre.BLACK) 

                elif stage == 5 or stage == 6:
                    screen.fill(StCre.PINK)
                
                StCre.create_stage(screen)
            
            #エンドレスモード
            if endless_flag == True:
                if stage%6 == 1 or stage%6 == 2:
                    screen.fill(StCre.BLUE)
                    S_Random.stage_scrool2()
                    S_Random.create_stage(screen)
                
                if stage%6 == 3 or stage%6 == 4:
                    screen.fill(StCre.BLACK)
                    S_Random.stage_scrool2()
                    S_Random.create_stage(screen)
                
                if stage%6 == 5 or stage%6 == 0:
                    screen.fill(StCre.PINK)
                    S_Random.stage_scrool2()
                    S_Random.create_stage(screen)

            Moving_A.draw_chara(screen)
            Moving_C.draw_chara(screen)
            Moving_T.draw_chara(screen)

            Life.life_draw(screen)
            Txt.text_draw("STAGE  " + str(stage), WHITE, 25, 390, 30, screen)
            Txt.text_draw("MENTAL: ", WHITE, 25, 75, 30, screen)

            StCre.x_road += 0
            if life > 0:
                Txt.text_draw("Miss", YELLOW, 54, 240, 180, screen)
                #Life.life_draw(screen)
                
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE] == True:    
                    Moving_A.__init__()
                    chk_goal_A = False

                    Moving_C.__init__()
                    chk_goal_C = False
                    chk_Lastgoal_C = False

                    Moving_T.__init__()
                    chk_goal_T = False
                    chk_Lastgoal_T = False

                    chk_goal = False
                    fall_flag = False

                    if endless_flag == False:
                        index = 1
                        StCre.__init__()
                    elif endless_flag == True:
                        S_Random.x_road = 0
                        #S_Random = Stage_Create_RN()
                        #print(S_Random.map_data)
                        
                        index = 10

                    tmr_music = 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #マウス左ボタンダウンイベント
                        x1,y1 = event.pos
                        if ui.calc_range_Enter():
                            Moving_A.__init__()
                            chk_goal_A = False

                            Moving_C.__init__()
                            chk_goal_C = False
                            chk_Lastgoal_C = False

                            Moving_T.__init__()
                            chk_goal_T = False
                            chk_Lastgoal_T = False

                            chk_goal = False
                            fall_flag = False

                            if endless_flag == False:
                                index = 1
                                StCre.__init__()
                            elif endless_flag == True:
                                S_Random.x_road = 0                        
                                index = 10

                            tmr_music = 0   
            #ゲームオーバー=================================================
            if life <= 0:
                StCre.x_road += 0
                Txt.text_draw("GAME OVER", BLUE, 54, 240, 180, screen)    
                pygame.mixer.music.stop()
                
                t_GO += 1
                if t_GO == 1:
                    se_gameover.play()

                key = pygame.key.get_pressed()
                #決定キー===================================================                
                if key[pygame.K_SPACE] == True:
                    S_Random.x_road = 0
                    t_key = 80
                    if endless_flag == False:
                        index = 0

                    elif endless_flag == True:
                        index = 7
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #マウス左ボタンダウンイベント
                        x1,y1 = event.pos
                        if ui.calc_range_Enter():
                            S_Random.x_road = 0
                            t_key = 80
                            if endless_flag == False:
                                index = 0

                            elif endless_flag == True:
                                index = 7
                            
            #下画面=========================================================
            if life <= 0:
                if endless_flag == False:
                    screen.blit(button[5], (0,360))
                else:
                    screen.blit(button[7], (0,360))
            else:            
                screen.blit(button[6], (0,360))
            #================================================================

        if index == 4: #ステージクリア #済
            #通常モード
            if endless_flag == False:
                if stage == 1 or stage == 2:
                    screen.fill(StCre.BLUE)

                elif stage == 3 or stage == 4:
                    screen.fill(StCre.BLACK) 

                elif stage == 5 or stage == 6:
                    screen.fill(StCre.PINK) 
                
                StCre.create_stage(screen)
            
            #エンドレスモード
            if endless_flag == True:
                if stage%6 == 1 or stage%6 == 2:
                    screen.fill(StCre.BLUE)
                    S_Random.create_stage(screen)

                if stage%6 == 3 or stage%6 == 4:
                    screen.fill(StCre.BLACK)
                    S_Random.create_stage(screen)

                if stage%6 == 5 or stage%6 == 0:
                    screen.fill(StCre.PINK)
                    S_Random.create_stage(screen)

            Moving_A.t_jump += 1
            Moving_C.t_jump += 1
            Moving_T.t_jump += 1

            if tmr_music == 1:
                pygame.mixer.music.load("sound/clear3.ogg")
                pygame.mixer.music.play(0)

            Moving_A.y = Moving_A.ground - Moving_A.h
            Moving_C.y = Moving_C.ground - Moving_C.h
            Moving_T.y = Moving_T.ground - Moving_T.h

            Moving_A.draw_chara(screen)
            Moving_C.draw_chara(screen)
            Moving_T.draw_chara(screen)
            Life.life_draw(screen)

            Moving_A.rect_x_update()
            Moving_C.rect_x_update()
            Moving_T.rect_x_update()

            Moving_A.rect_y_update()
            Moving_C.rect_y_update()
            Moving_T.rect_y_update()

            #下画面===============================================================
            ui.draw_under_screen(screen)
            if SOUSA_MODE == 1:
                ui.draw_button_bg(screen, NAVY, NAVY, NAVY, NAVY, NAVY, NAVY, RED)
            elif SOUSA_MODE == 2:
                ui.draw_button_bg(screen, NAVY, NAVY, NAVY, NAVY, NAVY, NAVY, RED)
            ui.draw_button(screen)
            ui.draw_b_chara(screen, "A", "L", "S", "K", "D", "J", "NEXT")
            screen.blit(button[8], (0,360))
            #入力=====================================================================
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] == True:    
                Moving_A.__init__()
                chk_goal_A = False

                Moving_C.__init__()
                chk_goal_C = False

                Moving_T.__init__()
                chk_goal_T = False

                chk_goal = False

                StCre.__init__()
                if endless_flag == False:
                    if stage == 3:
                        #S_Random = Stage_Create_RN()
                        S_Random.set_stage(4, 4)
                        generated = S_Random.map_data

                    elif stage == 5:
                        #S_Random = Stage_Create_RN()
                        S_Random.set_stage(5, 5)
                        generated2 = S_Random.map_data

                    elif stage == 6:
                        index = 6
                        chk_Lastgoal_C = False
                        chk_Lastgoal_T = False
                    
                    if stage <= 5:
                        index = 5
                        life += 1 
                        stage += 1
                
                elif endless_flag == True:
                    if stage%6 == 1 or stage%6 == 2:
                        pygame.mixer.music.load("sound/arusutoromeria.ogg")
                        S_Random.set_stage_endless(1, 5)
                        generated = S_Random.map_data

                    elif stage%6 == 3 or stage%6 == 4:
                        pygame.mixer.music.load("sound/arusutoromeria.ogg")
                        S_Random.set_stage_endless(4, 5)
                        generated = S_Random.map_data

                    elif stage%6 == 5 or stage%6 == 0:
                        pygame.mixer.music.load("sound/bloomy.ogg")
                        S_Random.set_stage_endless(5, 5)
                        generated = S_Random.map_data

                    S_Random.x_road = 0
                    tmr_music = 0
                    
                    if stage == 99:
                        index = 7
                    stage += 1  
                    index = 10              
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #マウス左ボタンダウンイベント
                    x1,y1 = event.pos
                    if ui.calc_range_Enter():
                        Moving_A.__init__()
                        chk_goal_A = False

                        Moving_C.__init__()
                        chk_goal_C = False

                        Moving_T.__init__()
                        chk_goal_T = False

                        chk_goal = False

                        StCre.__init__()
                        if endless_flag == False:
                            if stage == 3:
                                #S_Random = Stage_Create_RN()
                                S_Random.set_stage(4, 4)
                                generated = S_Random.map_data

                            elif stage == 5:
                                #S_Random = Stage_Create_RN()
                                S_Random.set_stage(5, 5)
                                generated2 = S_Random.map_data

                            elif stage == 6:
                                index = 6
                                chk_Lastgoal_C = False
                                chk_Lastgoal_T = False
                    
                            if stage <= 5:
                                index = 5
                                life += 1 
                                stage += 1
                
                        elif endless_flag == True:
                            if stage%6 == 1 or stage%6 == 2:
                                pygame.mixer.music.load("sound/arusutoromeria.ogg")
                                S_Random.set_stage_endless(1, 5)
                                generated = S_Random.map_data

                            elif stage%6 == 3 or stage%6 == 4:
                                pygame.mixer.music.load("sound/arusutoromeria.ogg")
                                S_Random.set_stage_endless(4, 5)
                                generated = S_Random.map_data

                            elif stage%6 == 5 or stage%6 == 0:
                                pygame.mixer.music.load("sound/bloomy.ogg")
                                S_Random.set_stage_endless(5, 5)
                                generated = S_Random.map_data

                            S_Random.x_road = 0
                            tmr_music = 0
                    
                            if stage == 99:
                                index = 7
                            stage += 1  
                            index = 10


            Txt.text_draw("STAGE  " + str(stage), WHITE, 25, 390, 30, screen)
            Txt.text_draw("MENTAL: ", WHITE, 25, 75, 30, screen)
            
            if endless_flag == False:
                if stage == 6:
                    pass
                elif stage <= 5:
                    Txt.text_draw("UMASTROMERIA!", PINK, 48, 240, 180, screen)

            elif endless_flag == True:
                Txt.text_draw("UMASTROMERIA!", PINK, 48, 240, 180, screen)

        if index == 5:#アイキャッチ
            scrool = False
            sc_rect1 = False
            sc_rect2 = False
            sc_acc = False

            if stage == 1 or stage == 2:
                screen.fill(StCre.BLUE)

            if stage == 3 or stage == 4:
                screen.fill(StCre.BLACK) 

            if stage == 5 or stage == 6:
                screen.fill(StCre.PINK) 

            if stage == 1:
                En.stage0(screen)
                pygame.draw.rect(screen, StCre.BLUE,(rect1,175,480,75))
                pygame.draw.rect(screen, StCre.BLUE,(rect2,270,480,75))

            elif stage == 2:
                En.stage1(screen)
                pygame.draw.rect(screen, StCre.BLUE,(rect1,175,480,75))
                pygame.draw.rect(screen, StCre.BLUE,(rect2,270,480,75))

            elif stage == 3:
                En.stage2(screen)
                pygame.draw.rect(screen, StCre.BLACK,(rect1,175,480,75))
                pygame.draw.rect(screen, StCre.BLACK,(rect2,270,480,75))

            elif stage == 4:
                En.stage3(screen)
                pygame.draw.rect(screen, StCre.BLACK,(rect1,175,480,75))
                pygame.draw.rect(screen, StCre.BLACK,(rect2,270,480,75))
            elif stage == 5:
                En.stage4(screen)
                pygame.draw.rect(screen, StCre.PINK,(rect1,175,480,75))
                pygame.draw.rect(screen, StCre.PINK,(rect2,270,480,75))

            elif stage == 6:
                En.stage5(screen)
                pygame.draw.rect(screen, StCre.PINK,(rect1,175,480,75))
                pygame.draw.rect(screen, StCre.PINK,(rect2,270,480,75))

            enshutsu += 6
            if enshutsu >= 0:
                enshutsu = 0
                scrool = True

            if scrool == True:
                rect1 += 10
                if rect1 >= 480:
                    rect1 = 480
                    sc_rect1 = True

            if sc_rect1 == True:
                rect2 += 10
                if rect2 >= 480:
                    rect2 == 480
                    sc_rect2 = True
                    

            if sc_rect2 == True:
                if stage == 1 or stage == 2 or stage == 3:
                    from5to1 -= 4
                elif stage == 4 or stage ==  5 or stage == 6:
                    se_sairen.play()
                    acc = pygame.image.load("enshutsu/acc.png")
                    
                    screen.blit(acc, (from5toaccA,0)) # 960 > 0 > -960
                    from5toaccA -= 40

                    if from5toaccA <= 0:
                        from5toaccA = 0
                        from5toaccB -= 15
                        if from5toaccB <= -720:
                            from5toaccB = -720
                            sc_acc = True

                        if stage == 4:
                            En.text_draw_left("Accident!:ステージランダム生成!", (255,255,255), 40, from5toaccB, 160, screen)
                        if stage == 5:
                            En.text_draw_left("Accident!:確率で自分から反対ごっこ!", (255,255,255), 40, from5toaccB, 160, screen)
                        if stage == 6:
                            En.text_draw_left("Accident!:ステージランダム生成!", (255,255,255), 40, from5toaccB, 160, screen)
                    if sc_acc == True:
                        from5to1 -= 4


            if from5to1 == 0:
                enshutsu = -200
                rect1 = 0
                rect2 = 0

                scrool = False
                sc_rect1 = False
                sc_rect2 = False
                sc_acc = False
                chk_goal = False

                from5to1 = 60
                from5toaccA = 480
                from5toaccB = 480

                tmr_music = 0
                if stage == 5 or stage == 6:
                    pygame.mixer.music.load("sound/bloomy.ogg")
                else:
                    pygame.mixer.music.load("sound/arusutoromeria.ogg")
                index = 1

        if index == 6: #ゲームクリア
            screen.fill((0,0,0))
            en_timer1 -= 1

            En.ending(screen)

            if en_timer1 == 0:
                en_timer1 = 64 #VSC上なら128
                en_ind += 1
            if en_ind == 20:
                index = 7
                #en_ind = 19
            #下画面===============================================================
            screen.blit(button[12], (0,360))

        if index == 7: #済
            #pygame.mixer.music.stop()
            key = pygame.key.get_pressed()

            screen.fill((0,0,0))
            en_timer2 -= 1
            en_timer3 -= 1

            screen.blit(StCre.block[7], (210, 200))
            En.text_draw_center("THANK YOU FOR PLAYING!", (255,255,255), 32, 240, 100, screen)
            #En.text_draw_center("POST YOUR RESULT ON X TO PRESS [X]!", (255,255,255), 20, 240, 240, screen)
    
            if endless_flag == True:
                Txt.text_draw("POST YOUR RESULT ON X TO PRESS [X]!", WHITE, 24, 240, 280, screen)

            Moving_CE.draw_chara(screen)

            if Moving_CE.x_amana == 210:
                en_ind7 = 2
                en_timer2 = 60
                Moving_CE.x_amana = 211
                stop_ce = True

            if en_timer2 == 0:
                en_ind7 += 1
                en_timer2 = 90

                if en_ind7 >= 4:
                    stop_ce = False
                    en_ind7 = 4
            if endless_flag == False:
                if en_timer3 == 0:
                    index = 0

            elif endless_flag == True:
                if t_key < 0:
                    t_key = 0
                    if key[pygame.K_SPACE] == True:
                        t_key = 80
                        index = 0

                if key[pygame.K_x] == True:
                    text =  'エンドレスモードでアルストロメリアはステージ'+ str(stage) + 'まで到達！\n' \
                            '#反対ごっこでこんがらがって\n' \
                            '#非公式ゲーム\n' \
                            'https://yararato.github.io/congaragatte/'
                    url_text = urllib.parse.quote(text)
                    url = f'https://x.com/intent/post?text={url_text}'
                    webbrowser.open(url)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #マウス左ボタンダウンイベント
                        x1,y1 = event.pos
                        if t_key <= 0:
                            if ui.calc_range_Enter:
                                t_key = 80
                                index = 0
                            if ui.calc_range_button1(195, 280)[0]:
                                text =  'エンドレスモードでアルストロメリアはステージ'+ str(stage) + 'まで到達！\n' \
                                        '#反対ごっこでこんがらがって\n' \
                                        '#非公式ゲーム\n' \
                                        'https://yararato.github.io/congaragatte/'
                                url_text = urllib.parse.quote(text)
                                url = f'https://x.com/intent/post?text={url_text}'
                                webbrowser.open(url)

            Moving_CE.rect_x_update()

            #下画面===============================================================
            screen.blit(button[9], (0,360))
        
        if index == 8: #マニュアル

            screen.fill(StCre.BLUE)
            for j in range(3):
                for i in range(6):
                    screen.blit(StCre.block[1], (330 + 25 * i, 125 + 100*j))
            
            #=======甘奈=====================================================================
            Moving_AT.draw_chara(screen)

            if True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #マウス左ボタンダウンイベント
                        x1,y1 = event.pos
                        if ui.calc_range_button1(195, 280)[1]:
                            Moving_AT.move_amana_click()

                        if SOUSA_MODE == 1:
                            if ui.calc_range_button1(195, 280)[0]:
                                Moving_AT.turn_amana_click()
                        if SOUSA_MODE == 2:
                            if ui.calc_range_button1(70, 140)[0]:
                                Moving_AT.turn_amana_click()

                Moving_AT.t_canjump -= 1

                if Moving_AT.t_canjump == 0:
                   Moving_AT.jump_reset()

                if Moving_AT.t_turn == 0: #タイマーが0で
                    Moving_AT.turn_reset() #ターン出来るようにする

            Moving_AT.move_amana()
            #=======ちきゆ=====================================================================
            Moving_CT.draw_chara(screen)

            if True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #マウス左ボタンダウンイベント
                        x1,y1 = event.pos
                        if ui.calc_range_button1(120, 220)[1]:
                            Moving_CT.move_amana_click()

                        if SOUSA_MODE == 1:
                            if ui.calc_range_button1(120, 220)[0]:
                                Moving_CT.turn_amana_click()
                        if SOUSA_MODE == 2:
                            if ui.calc_range_button1(120, 220)[0]:
                                Moving_CT.turn_amana_click()

                Moving_CT.t_canjump -= 1

                if Moving_CT.t_canjump == 0:
                   Moving_CT.jump_reset()

                if Moving_CT.t_turn == 0: #タイマーが0で
                    Moving_CT.turn_reset() #ターン出来るようにする

            Moving_CT.move_chikiyu()
            #=======甜花=====================================================================
            Moving_TT.draw_chara(screen)

            if tuto_ind == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #マウス左ボタンダウンイベント
                        x1,y1 = event.pos
                        if ui.calc_range_button1(70, 140)[1]:
                            Moving_TT.move_amana_click()

                        if SOUSA_MODE == 1:
                            if ui.calc_range_button1(70, 140)[0]:
                                Moving_TT.turn_amana_click()
                        if SOUSA_MODE == 2:
                            if ui.calc_range_button1(195, 280)[0]:
                                Moving_TT.turn_amana_click()

                Moving_TT.t_canjump -= 1

                if Moving_TT.t_canjump == 0:
                   Moving_TT.jump_reset()

            Moving_TT.move_tenka()
            #============================================================================
            En.tuto_rial(screen)
            En.tuto_sentaku()
            
            
            if event.type == pygame.MOUSEBUTTONUP:
                if True:
                    if event.button == 1: #マウス左ボタンダウンイベント
                        x1,y1 = event.pos
                        
                        #if ui.calc_range_button1(70, 140)[1]:
                        if ui.calc_range_Enter_R():
                            if t_key <= 0:
                                t_key = 30
                                tuto_ind += 1
                                if tuto_ind > 3:
                                    tuto_ind = 1
                        
                        #if ui.calc_range_button1(70, 140)[0]:
                        if ui.calc_range_Enter_L():
                            if t_key <= 0:
                                t_key = 30
                                tuto_ind -= 1
                        
                            if tuto_ind < 1:
                                tuto_ind = 3
                
                if event.button == 1:
                    if ui.calc_range_Enter_C():
                        if t_key <= 0:
                            t_key = 30
                            index = 0
                            tuto_ind = 1

            #下画面=========================================================
            screen.blit(button[10], (0,360))

        if index == 9: #コンフィグ #済

            screen.fill(StCre.BLUE)

            screen.fill(StCre.BLUE)
            for j in range(3):
                for i in range(6):
                    screen.blit(StCre.block[1], (330 + 25 * i, 125 + 100*j))
            
            #=======甘奈=====================================================================
            Moving_AT.draw_chara(screen)

            if True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #マウス左ボタンダウンイベント
                        x1,y1 = event.pos
                        if ui.calc_range_button1(195, 280)[1]:
                            Moving_AT.move_amana_click()

                        if SOUSA_MODE == 1:
                            if ui.calc_range_button1(195, 280)[0]:
                                Moving_AT.turn_amana_click()
                        if SOUSA_MODE == 2:
                            if ui.calc_range_button1(70, 140)[0]:
                                Moving_AT.turn_amana_click()

                Moving_AT.t_canjump -= 1

                if Moving_AT.t_canjump == 0:
                   Moving_AT.jump_reset()

                if Moving_AT.t_turn == 0: #タイマーが0で
                    Moving_AT.turn_reset() #ターン出来るようにする

            Moving_AT.move_amana()
            #=======ちきゆ=====================================================================
            Moving_CT.draw_chara(screen)

            if True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #マウス左ボタンダウンイベント
                        x1,y1 = event.pos
                        if ui.calc_range_button1(120, 220)[1]:
                            Moving_CT.move_amana_click()

                        if SOUSA_MODE == 1:
                            if ui.calc_range_button1(120, 220)[0]:
                                Moving_CT.turn_amana_click()
                        if SOUSA_MODE == 2:
                            if ui.calc_range_button1(120, 220)[0]:
                                Moving_CT.turn_amana_click()

                Moving_CT.t_canjump -= 1

                if Moving_CT.t_canjump == 0:
                   Moving_CT.jump_reset()

                if Moving_CT.t_turn == 0: #タイマーが0で
                    Moving_CT.turn_reset() #ターン出来るようにする

            Moving_CT.move_chikiyu()
            #=======甜花=====================================================================
            Moving_TT.draw_chara(screen)

            if tuto_ind == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #マウス左ボタンダウンイベント
                        x1,y1 = event.pos
                        if ui.calc_range_button1(70, 140)[1]:
                            Moving_TT.move_amana_click()

                        if SOUSA_MODE == 1:
                            if ui.calc_range_button1(70, 140)[0]:
                                Moving_TT.turn_amana_click()
                        if SOUSA_MODE == 2:
                            if ui.calc_range_button1(195, 280)[0]:
                                Moving_TT.turn_amana_click()

                Moving_TT.t_canjump -= 1

                if Moving_TT.t_canjump == 0:
                   Moving_TT.jump_reset()

            Moving_TT.move_tenka()
            #============================================================================
            En.config(screen)
            En.config_sentaku()
            
            
            if event.type == pygame.MOUSEBUTTONUP:
                if True:
                    if event.button == 1: #マウス左ボタンダウンイベント
                        x1,y1 = event.pos
                        
                        #if ui.calc_range_button1(70, 140)[1]:
                        if ui.calc_range_Enter_R():
                            if t_key <= 0:
                                t_key = 30
                                SOUSA_MODE += 1
                                if SOUSA_MODE > 2:
                                    SOUSA_MODE = 1
                        
                        #if ui.calc_range_button1(70, 140)[0]:
                        if ui.calc_range_Enter_L():
                            if t_key <= 0:
                                t_key = 30
                                SOUSA_MODE -= 1
                        
                            if SOUSA_MODE < 1:
                                SOUSA_MODE = 2
                
                if event.button == 1:
                    if ui.calc_range_Enter_C():
                        if t_key <= 0:
                            t_key = 30
                            index = 0

            #下画面=========================================================
            if True:                
                if SOUSA_MODE == 1:
                    screen.blit(button[10], (0,360))
                elif SOUSA_MODE == 2:
                    screen.blit(button[11], (0,360))

        if index == 10: #エンドレスモード
            #音楽
            if tmr_music == 1:
                pygame.mixer.music.play(-1)

            #背景
            if stage%6 == 1 or stage%6 == 2:
                screen.fill(StCre.BLUE)

            elif stage%6 == 3 or stage%6 == 4:
                screen.fill(StCre.BLACK)

            elif stage%6 == 5 or stage%6 == 0:
                screen.fill(StCre.PINK)
        #甘奈        
            Moving_A.t_move += 1
            Moving_A.t_jump += 1
            Moving_A.t_draw += 1
        #ちきゆ        
            Moving_C.t_move += 1
            Moving_C.t_jump += 1
            Moving_C.t_draw += 1
        #甜花        
            Moving_T.t_move += 1
            Moving_T.t_jump += 1
            Moving_T.t_draw += 1

            if stage%6 == 1 or stage%6 == 2:
                S_Random.stage_scrool2()
                S_Random.create_stage(screen)
            elif stage%6 == 3 or stage%6 == 4:
                S_Random.stage_scrool2()
                S_Random.create_stage(screen)
            elif stage%6 == 5 or stage%6 == 0:
                S_Random.stage_scrool2()
                S_Random.create_stage(screen)
        #====================甘奈=======================================================
        # キャラの描画
            Moving_A.draw_chara(screen)        
        #床の判定(なんか関数に出来ない)
            StA = S_Random.map_data[0]
            #print(StA)　#チェック用

            if Moving_A.turn_int == -1: #左向き
                if chk_goal_A == False:                
                    B = int((Moving_A.x_amana + S_Random.x_road)/25) #左向きの右寄り
                    #C = int((Moving_A.x_amana + StCre.x_road)/100 + 1) #左向きの左寄り

                if chk_goal_A == False:                
                    B = int((Moving_A.x_amana + S_Random.x_road)/25)
                    #print(B)　チェック用
                    if StA[B] == 0 and StA[B+1] == 0:
                        chk_0_A = False

                    elif StA[B] == 6:
                        Moving_A.canJump = False

                    elif StA[B] == 3:
                        chk_goal_A = True

                    else:
                        chk_0_A = True

            if Moving_A.turn_int == 1: #右向き
                if chk_goal_A == False: 
                    A = int((Moving_A.x_amana + S_Random.x_road )/25)
                #print(A)　チェック用
                    if StA[A] == 0:
                        chk_0_A = False
                    if StA[A] == 1 or StA[A] == 2 or StA[A] == 4 or StA[A] == 5:
                        chk_0_A = True
                
                    if StA[A] == 3:
                        chk_goal_A = True
                #print(chk_0_A)　チェック用
        #ここまで床
            key = pygame.key.get_pressed()
            Moving_A.move_amana()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #マウス左ボタンダウンイベント
                    x1,y1 = event.pos
                    if ui.calc_range_button1(195, 280)[1]:
                        Moving_A.move_amana_click()

                    if SOUSA_MODE == 1:
                        if ui.calc_range_button1(195, 280)[0]:
                            Moving_A.turn_amana_click()
                    if SOUSA_MODE == 2:
                        if ui.calc_range_button1(70, 140)[0]:
                            Moving_A.turn_amana_click()

            Moving_A.t_canjump -= 1

            if Moving_A.t_canjump == 0:
                Moving_A.jump_reset()

            if Moving_A.t_turn == 0: #タイマーが0で
                Moving_A.turn_reset() #ターン出来るようにする

        #====================ちきゆ=======================================================
        # キャラの描画
            Moving_C.draw_chara(screen)
        #床の判定(なんか関数に出来ない)
            StC = S_Random.map_data[1]
            #print(StC) #チェック用

            if Moving_C.turn_int == -1:
                if chk_goal_C == False:                
                    B = int((Moving_C.x_amana + S_Random.x_road)/25)
                    #print(B)　チェック用
                    if StC[B] == 0 and StC[B+1] == 0:
                        chk_0_C = False

                    elif StC[B] == 6:
                        Moving_C.canJump = False
                        chk_Lastgoal_C = True  

                    elif StC[B] == 3:
                        chk_goal_C = True
                    else:
                        chk_0_C = True

            if Moving_C.turn_int == 1:
                A = int((Moving_C.x_amana + S_Random.x_road )/25)
            #print(A)　チェック用
                if StC[A] == 0:
                    chk_0_C = False
                if StC[A] == 1 or StC[A] == 2 or StC[A] == 4 or StC[A] == 5:
                    chk_0_C = True
                
                if StC[A] == 3:
                    chk_goal_C = True

                if StC[A] == 6:
                    Moving_C.canJump = False
                    chk_Lastgoal_C = True
            #print(chk_0_A)　チェック用
        #ここまで床
            key = pygame.key.get_pressed()

            Moving_C.move_chikiyu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #マウス左ボタンダウンイベント
                    x1,y1 = event.pos
                    if ui.calc_range_button1(120, 220)[1]:                   
                        Moving_C.move_amana_click()
                    
                    if ui.calc_range_button1(120, 220)[0] and Moving_C.canTurn == True:
                        Moving_C.turn_amana_click()

            Moving_C.t_canjump -= 1

            if Moving_C.t_canjump == 0:
                Moving_C.jump_reset()

            if Moving_C.t_turn == 0: #タイマーが0で
                Moving_C.turn_reset() #ターン出来るようにする

        #====================甜花=======================================================
        # キャラの描画
            Moving_T.draw_chara(screen)
            #print(Moving_T.y)
        
        #床の判定(なんか関数に出来ない)
            StT = S_Random.map_data[2]
            #print(StT)　#チェック用
            
            if Moving_T.turn_int == -1:
                if chk_goal_T == False:                
                    B = int((Moving_T.x_amana + S_Random.x_road)/25)
                    #print(B)　チェック用
                    if  StT[B] == 0 and StT[B+1] == 0:
                        chk_0_T = False

                    elif StT[B] == 6:
                        Moving_T.canJump = False
                        chk_Lastgoal_T = True  

                    elif StT[B] == 3:
                        chk_goal_T = True

                    else:
                        chk_0_T = True

            if Moving_T.turn_int == 1:
                A = int((Moving_T.x_amana + S_Random.x_road )/25)
            #print(A)　チェック用
                if StT[A] == 0:
                    chk_0_T = False
                if StT[A] == 1 or StT[A] == 2 or StT[A] == 4 or StT[A] == 5:
                    chk_0_T = True

                if StT[A] == 6:
                    Moving_T.canJump = False
                    chk_Lastgoal_T = True                

                if StT[A] == 3:
                    chk_goal_T = True
            #print(chk_0_A)　チェック用
        #ここまで床
            key = pygame.key.get_pressed()
            Moving_T.move_tenka()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #マウス左ボタンダウンイベント
                    x1,y1 = event.pos
                    if ui.calc_range_button1(70, 140)[1]:
                        Moving_T.move_amana_click()

                    if SOUSA_MODE == 1:
                        if ui.calc_range_button1(70, 140)[0]:
                            Moving_T.turn_amana_click()
                    if SOUSA_MODE == 2:
                        if ui.calc_range_button1(195, 280)[0]:
                            Moving_T.turn_amana_click()
            Moving_T.t_canjump -= 1

            if Moving_T.t_canjump == 0:
                Moving_T.jump_reset()

            if Moving_T.t_turn == 0: #タイマーが0で
                Moving_T.turn_reset() #ターン出来るようにする
        #===========================================================================
            #固定
            Life.life_draw(screen)
            Txt.text_draw("STAGE  " + str(stage), WHITE, 25, 390, 30, screen)
            Txt.text_draw("MENTAL: ", WHITE, 25, 75, 30, screen)

            Moving_A.rect_x_update()
            Moving_A.rect_y_update()

            Moving_C.rect_x_update()
            Moving_C.rect_y_update()

            Moving_T.rect_x_update()
            Moving_T.rect_y_update()

            #下画面=========================================================
            if SOUSA_MODE == 1:
                screen.blit(button[1], (0,360))
            elif SOUSA_MODE == 2:
                screen.blit(button[3], (0,360))

            if chk_goal == True and \
                chk_goal_A == True and\
                chk_goal_C == True and\
                chk_goal_T == True:
                if stage == 99:
                    index = 7
                index = 4
                tmr_music = 0

        if index == 11:
            screen.fill((255,255,255))
            
            adjust = 150

            En.text_draw_left('・このゲームは', ((0,0,0)), 20, 50, 60 + adjust, screen)
            En.text_draw_left('　アイドルマスターシャイニーカラーズの', ((0,0,0)), 20, 50, 90 + adjust, screen)
            En.text_draw_left('　非公式ゲームです', ((0,0,0)), 20, 50, 120 + adjust, screen)
            En.text_draw_left('', ((0,0,0)), 20, 50, 150, screen)
            En.text_draw_left('・ゲーム中に原作内のイベント', ((0,0,0)), 20, 50, 210 + adjust, screen)
            En.text_draw_left('  「薄桃色にこんがらがって」の', ((0,0,0)), 20, 50, 240 + adjust, screen)
            En.text_draw_left('　ネタバレがあります', ((0,0,0)), 20, 50, 270 + adjust, screen)

            if t_key == 0:
                t_key = 20
                index = 0 

        #UI==================================================================================
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #マウス左ボタンダウンイベント
                x1,y1 = event.pos
                ui.button_turn_white(screen)

#======================================================
        tmr_music += 1
        tmr_se += 1
        t_key -= 1
        #print(mt_key)

        pygame.display.update()        
        clock.tick(30)
        await asyncio.sleep(0)

asyncio.run(main())

