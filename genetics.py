# Name: Jacob Williams
# Date: 1/20/16
# Purpose: use genetic algorithm
# Filename: genetics.py

import pygame
import time
import math
import sys
import random as r

# initialization
pygame.init()

screen_w = 500
screen_h = 500
size = [screen_w, screen_h]

screen = pygame.display.set_mode(size)

# colors
black = (0, 0, 0)
blue = (5,5,255)
red = (255,5,5)
green = (0,255,0)

# banners
generation = 1
gen_str = "Generation: " + str(generation)
gen_font = pygame.font.Font(None,75)
gen_size = gen_font.size(gen_str)
gen_banner = gen_font.render(gen_str, 1, red)

fps_str = "1"
fps_font = pygame.font.Font(None,25)
fps_banner = fps_font.render(fps_str,1,red)


# flyer class
class Flyer:
    dist = 0
    y = 0
    mass = 0
    w1 = 0
    w2 = 0
    w3 = 0
    l1 = 0
    l2 = 0
    l3 = 0
    r1 = 0
    r2 = 0
    r3 = 0
    origW1 = 0
    origW2 = 0
    origW3 = 0
    rigMass = 0
    pt1 = 0
    pt2 = 0
    pt3 = 0
    pt4 = 0
    a1 = 0
    a2 = 0
    a3 = 0
    fTotal = 0
    a = 0

    def __init__(self, trait):
        self.origW1 = trait[0]
        self.origW2 = trait[1]
        self.origW3 = trait[2]
        self.origMass = trait[9]
        self.w1 = trait[0] * (1 - (.01 * (trait[0] + trait[1] + trait[2])))
        self.w2 = trait[1] * (1 - (.01 * (trait[1] + trait[2])))
        self.w3 = trait[2] * (1 - (.01 * trait[2]))
        self.l1 = trait[3]
        self.l2 = trait[4]
        self.l3 = trait[5]
        self.r1 = trait[6]
        self.r2 = trait[7]
        self.r3 = trait[8]
        self.mass = trait[9] + 2 * (trait[3] + trait[4] + trait[5])
        self.pt1 = [240,400]
        self.pt2 = [240 - trait[3],250]
        self.pt3 = [240 - trait[3] - trait[4],250]
        self.pt4 = [240 - trait[3] - trait[4] - trait[5],250]

    def move(self,time):
        self.a1 += self.w1 * time
        if self.a1 > self.r1:
            self.a1 = (2 * self.r1) - self.a1
            self.w1 = self.w1 * -1
        elif self.a1 < 0:
            self.a1 = self.a1 * -1
            self.w1 = self.w1 * -1

        self.a2 += self.w2 * time
        if self.a2 > self.r2:
            self.a2 = (2 * self.r2) - self.a2
            self.w2 = self.w2 * -1
        elif self.a2 < 0:
            self.a2 = self.a2 * -1
            self.w2 = self.w2 * -1

        self.a3 += self.w3 * time
        if self.a3 > self.r3:
            self.a3 = (2 * self.r3) - self.a3
            self.w3 = self.w3 * -1
        elif self.a3 < 0:
            self.a3 = self.a3 * -1
            self.w3 = self.w3 * -1
    
        self.pt2[0] = self.pt1[0] - (math.cos(rad(self.a1)) * self.l1)
        self.pt2[1] = self.pt1[1] - (math.sin(rad(self.a1)) * self.l1)
        self.pt3[0] = self.pt2[0] - (math.cos(rad(self.a2)) * self.l2)
        self.pt3[1] = self.pt2[1] - (math.sin(rad(self.a2)) * self.l2)
        self.pt4[0] = self.pt3[0] - (math.cos(rad(self.a3)) * self.l3)
        self.pt4[1] = self.pt3[1] - (math.sin(rad(self.a3)) * self.l3)

        f1 = -1 * self.w1 * 3.1415926 * self.l1 / 360
        f2 = -1 * (self.w1 + self.w2) * 3.1415926 * (self.l1 + (self.l2 / 2)) / 180
        f3 = -1 * (self.w1 + self.w2 + self.w3) * 3.1415926 * (self.l1 + self.l2 + (self.l3 / 2)) / 180

        fT = 0 
        if f1 > 0:
            fT += f1
        if f2 > 0:
            fT += f2
        if f3 > 0:
            fT += f3

        self.fTotal = fT

        self.a = self.fTotal / self.mass

        self.y -= self.a * 20 * time
        self.dist += self.a * 20 * time
        self.pt1[1] = self.y + 400

    def mate(self, num, spouse, varSp):
        kids = []
        var = self.getVarListOrig()
        for num in range (num):
            varList = []
            for num in range (len(var)):
                if r.random() < .5:
                    varList.append(var[num])
                    if r.random() < .15:
                        varList[num] = varList[num] + (varList[num] * r.randrange(-10, 10, 1) / 1000)
                else:
                    varList.append(varSp[num])
                    if r.random() < .15:
                        varList[num] = varList[num] + (varList[num] * r.randrange(-10, 10, 1) / 1000)

                if varList[num] < 1:
                    varList[num] = 1

                if num in [0,1,2]:
                    if varList[num] > 100:
                        varList[num] = 100
                    
                if num in [6,7,8]:
                    if varList[num] > 90:
                        varList[num] = 90
                        
                if num == 9:
                    if varList[9] < 50:
                        varList[9] = 50

            newFlyer = Flyer(varList)
            kids.append(newFlyer)

        return kids

    def getVarList(self):
        return [self.w1,self.w2,self.w3,self.l1,self.l2,self.l3,self.r1,self.r2,self.r3,self.mass]

    def getVarListOrig(self):
        return [self.origW1,self.origW2,self.origW3,self.l1,self.l2,self.l3,self.r1,self.r2,self.r3,self.origMass]

def rad(num):
    return (num / 180) * 3.1415926

def avg(num):
    ans = 0
    for item in num:
        ans += item

    return ans / len(num)

flyers = []

for num in range(40):
    a = r.randrange(1, 100, 1)
    b = r.randrange(1, 100, 1)
    c = r.randrange(1, 100, 1)
    d = r.randrange(1, 50, 1)
    e = r.randrange(1, 50, 1)
    f = r.randrange(1, 50, 1)
    g = r.randrange(1, 90, 1)
    h = r.randrange(1, 90, 1)
    i = r.randrange(1, 90, 1)
    j = r.randrange(50, 100, 1)
    bird = Flyer([a,b,c,d,e,f,g,h,i,j])
    flyers.append(bird)

##### game loop ######################################
time1 = time.time()
deltaTime = .001
counter = 0
start = False
timeStart = time.time()
dists = []
fast = []

with open("Genetics_History", "a") as f:
    f.write("#############################\n")

#flyers = []
#bird = Flyer([67,78,89,45,34,23,67,45,34,75])
#flyers.append(bird)

while True:
    if start:
        start = False
        generation += 1
        for bird in flyers:
            dists.append(bird.dist)
        dists.sort()
        for bird in flyers:
            if bird.dist >= dists[20]:
                fast.append(bird)
                
            if bird.dist == dists[39]:  
                with open("Genetics_History", "a") as f:
                    f.write(str(generation - 1) + ") Avg: " + str(avg(dists)) + "      Max: " + str(dists[39]) + "        Bird stats: ")
                    for item in bird.getVarListOrig():
                        f.write(str(item) + "  ")
                    f.write("\n")
        
        flyers = []
        for num in range(0,20,2):
            children = fast[num].mate(2,fast[num + 1],fast[num + 1].getVarListOrig())
            flyers.append(children[0])
            flyers.append(children[1])
                
        timeStart = time.time()
        
    counter += 1
    if counter == 500:
        fps_str = "FPS: " + str(int(1 / deltaTime))
        fps_banner = fps_font.render(fps_str,1,red)
        counter = 0

    gen_str = "Generation: " + str(generation)
    gen_banner = gen_font.render(gen_str, 1, red)
    
    deltaTime = time.time() - time1
    time1 = time.time()

    if time1 > (timeStart + 10):
        start = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for bird in flyers:
        bird.move(deltaTime)

    # screen display
    screen.fill(black)

    for bird in flyers:
        # body
        pygame.draw.circle(screen, (0, 50 + (205 * (bird.origMass - 50) / 50),0), (int(size[1] / 2), int(bird.y + (4 * size[1] / 5))), 10, 0)
        # wings
        pygame.draw.line(screen, (50 + (205 * (bird.origW1 / 100)),0,0), (int(bird.pt1[0]),int(bird.pt1[1])), (int(bird.pt2[0]),int(bird.pt2[1])), 2)
        pygame.draw.line(screen, (50 + (205 * (bird.origW2 / 100)),0,0), (int(bird.pt2[0]),int(bird.pt2[1])), (int(bird.pt3[0]),int(bird.pt3[1])), 2)
        pygame.draw.line(screen, (50 + (205 * (bird.origW3 / 100)),0,0), (int(bird.pt3[0]),int(bird.pt3[1])), (int(bird.pt4[0]),int(bird.pt4[1])), 2)
        pygame.draw.line(screen, (50 + (205 * (bird.origW1 / 100)),0,0), (int(size[0] - bird.pt1[0]),int(bird.pt1[1])), (int(size[0] - bird.pt2[0]),int(bird.pt2[1])), 2)
        pygame.draw.line(screen, (50 + (205 * (bird.origW2 / 100)),0,0), (int(size[0] - bird.pt2[0]),int(bird.pt2[1])), (int(size[0] - bird.pt3[0]),int(bird.pt3[1])), 2)
        pygame.draw.line(screen, (50 + (205 * (bird.origW3 / 100)),0,0), (int(size[0] - bird.pt3[0]),int(bird.pt3[1])), (int(size[0] - bird.pt4[0]),int(bird.pt4[1])), 2)
        # joints
        pygame.draw.circle(screen, (0,0,50 + (205 * (bird.r1 / 90))), (int(bird.pt1[0]),int(bird.pt1[1])), 5, 0)
        pygame.draw.circle(screen, (0,0,50 + (205 * (bird.r2 / 90))), (int(bird.pt2[0]),int(bird.pt2[1])), 5, 0)
        pygame.draw.circle(screen, (0,0,50 + (205 * (bird.r3 / 90))), (int(bird.pt3[0]),int(bird.pt3[1])), 5, 0)
        pygame.draw.circle(screen, (0,0,50 + (205 * (bird.r1 / 90))), (int(size[0] - bird.pt1[0]),int(bird.pt1[1])), 5, 0)
        pygame.draw.circle(screen, (0,0,50 + (205 * (bird.r2 / 90))), (int(size[0] - bird.pt2[0]),int(bird.pt2[1])), 5, 0)
        pygame.draw.circle(screen, (0,0,50 + (205 * (bird.r3 / 90))), (int(size[0] - bird.pt3[0]),int(bird.pt3[1])), 5, 0)

    # banners
    screen.blit(gen_banner, ((size[0] - gen_size[0]) / 2, 0))
    screen.blit(fps_banner, (0,0))
    
    
    pygame.display.flip()











