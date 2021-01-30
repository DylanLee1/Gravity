import random
import pygame
import time
import mysql.connector
from tkinter import *
from tkinter import simpledialog

done = 0
score = 0
name = ""


class Apple(object):
    def __init__(self, x, y):
        self.image = pygame.image.load('apple.png')
        self.x = x
        self.y = y

    def draw(self, display):
        display.blit(self.image, (self.x, self.y))


class Basket(object):
    def __init__(self, x, y):
        self.image = pygame.image.load('Basket.png')
        self.x = x
        self.y = y

    def draw(self, display):
        display.blit(self.image, (self.x, self.y))

    def move(self, move):
        self.x += move
        if self.x - 60 >= 600:
            self.x = 1
        elif self.x + 60 <= 0:
            self.x = 600


class Game:

    def __init__(self):
        self.running = True
        self.apples = []
        self.basket = Basket(350, 740)
        self.buf = 3
        self.score = 0
        self.time = time.time()

        pygame.init()

    def update(self):
        white = (255, 255, 255)
        black = (0, 0, 0)

        dis = pygame.display.set_mode((600, 800))
        pygame.display.set_caption('Gravity')

        move = 0

        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        move = -15
                    elif event.key == pygame.K_RIGHT:
                        move = 15
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        move = 0
                    elif event.key == pygame.K_RIGHT:
                        move = 0

            self.basket.move(move)
            dis.fill(white)
            self.basket.draw(dis)

            # pygame.draw.line(dis, black, (0, 760), (600, 760), 1)

            for obj in self.apples:
                if obj.y > 900:
                    self.apples.pop(self.apples.index(obj))

                elif (obj.y + 10) == 760 and ((obj.x > self.basket.x - 10) and obj.x < self.basket.x + 130):
                    self.apples.pop(self.apples.index(obj))
                    self.score += 1
                else:
                    obj.y += 5

            z = random.randint(1, 30)
            ran = random.randint(10, 790)

            for obj in self.apples:
                obj.draw(dis)

            if z <= 5 and self.buf == 1:
                self.apples.append(Apple(ran, 50))

            self.buf -= 1
            if self.buf == 0:
                self.buf = 3

            font = pygame.font.SysFont("arial", 20)
            text = font.render("Score: " + str(self.score), 1, (0, 0, 0))
            dis.blit(text, (5, 10))

            if round((time.time() - self.time), 2) >= 5:  # quits
                global done
                global score
                score = self.score
                done = 1
                self.running = False

            timetext = font.render("Time: " + str(round((time.time() - self.time), 2)), 1, (0, 0, 0))
            dis.blit(timetext, (510, 10))

            pygame.display.update()

            clock.tick(60)


g = Game()
while g.running:
    g.update()

pygame.quit()
# game over

if done == 1:
    win = Tk()
    e = Entry(win)
    e.pack()

    e.focus_set()


    def callback():
        global name
        name = e.get()
        win.destroy()


    b = Button(win, text="OK", height=2, width=10, command=callback)
    b.pack()

    mainloop()

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="{Password}",
        auth_plugin=' mysql_native_password',
        database="highscores"
    )
    mycursor = mydb.cursor()
    SQL = "INSERT INTO scores (name,score) VALUES (%s, %s)"
    val = (name, int(score))
    mycursor.execute(SQL, val)
    mydb.commit()

    stmt = "SELECT name,score FROM scores ORDER BY score DESC LIMIT 10"
    mycursor.execute(stmt)
    myresult = mycursor.fetchall()

    for row in myresult:
        print(row)
exit()
