import turtle
import math
import random
import keyboard
import pyautogui
import winsound

screen_width, screen_height = pyautogui.size()

class Menu(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.hideturtle()
        self.goto(x, y)
        self.write("ЛАБИРИНТ", align="center", font=("Courier", 105, "normal"))
        self.color("Gray")
        self.goto(x, y - 250)
        self.color("white")
        self.write("Нажмите 'P', чтобы начать игру", align="center", font=("Courier", 24, "normal"))
        self.color("white")
        self.goto(0, 250)
        self.write("                              Правила игры:"
                    '\n' "      1. Используйте стрелки для перемещения игрока по лабиринту."
                    '\n' "      2. Соберите все сокровища, избегая столкновения с врагами."
                    '\n' "3. Как только все сокровища в лабиринте будут собраны, врата к выходу будут открыты.", align="center",
                   font=("Courier", 12, "normal"))

    def wait_for_input(self):
        while True:
            if keyboard.is_pressed("p"):
                self.clear()
                break

def exit_game():
    wn.bye()

def wn_create():
    global wn
    wn = turtle.Screen()
    screen_width, screen_height = pyautogui.size()
    wn.setup(screen_width, screen_height, startx=0, starty=0)

music_playing = False

def pause_music():
    global music_playing
    if music_playing:
        winsound.PlaySound(None, winsound.SND_PURGE)
        music_playing = False

def play_music():
    global music_playing
    if not music_playing:
        winsound.PlaySound("music.wav", winsound.SND_ASYNC)
        music_playing = True

def block_key():
    keyboard.block_key('caps lock')
    keyboard.block_key('shift')

def menu_start():
    global menu, images, image
    wn_create()
    wn.bgpic("wp.gif")
    wn.bgcolor("DimGray")
    wn.title("Labirint")
    wn.tracer(0, 0)
    wn.update()
    menu = Menu(0, 0)
    menu.wait_for_input()
    turtle.listen()
    turtle.onkey(pause_music, "o")
    play_music()
    block_key()

    images = ["pers.gif", "pers2.gif", "gates.gif",
            "sun.gif", "pen.gif", "vrag.gif", "vrag.gif", "exit.gif"]
    for image in images:
        turtle.register_shape(image)

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)

class Gates(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("gates.gif")
        self.color("white")
        self.penup()
        self.speed(0)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()
        self.clear()
        gates.remove(self)

class Player(turtle.Turtle):
    global gates
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("pers.gif")
        self.color("red")
        self.penup()
        self.speed(0)
        self.gold = 0

    def go_up(self):
        move_to_x = player.xcor()
        move_to_y = player.ycor() + 24

        if (move_to_x, move_to_y) not in walls and not self.check_collision_with_gates(move_to_x, move_to_y):
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        move_to_x = player.xcor()
        move_to_y = player.ycor() - 24

        if (move_to_x, move_to_y) not in walls and not self.check_collision_with_gates(move_to_x, move_to_y):
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        move_to_x = player.xcor() - 24
        move_to_y = player.ycor()

        self.shape("pers.gif")

        if (move_to_x, move_to_y) not in walls and not self.check_collision_with_gates(move_to_x, move_to_y):
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        move_to_x = player.xcor() + 24
        move_to_y = player.ycor()

        self.shape("pers2.gif")

        if (move_to_x, move_to_y) not in walls and not self.check_collision_with_gates(move_to_x, move_to_y):
            self.goto(move_to_x, move_to_y)

    def check_collision_with_gates(self, x, y):
        for gate in gates:
            if gate.distance(x, y) < 5:
                return True
        return False

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 5:
            return True
        else:
            return False

    def show_collision_message(self):
        turtle.goto(0, 0)
        turtle.color("red")
        turtle.write("       Вы были пойманы врагом!"
                     '\n' "Нажмите 'ENTER' чтобы открыть главное меню", align="center",
                     font=("Courier", 25, "normal"))
        keyboard.wait('enter')
        restart_game()
        turtle.done()

    def check_treasures(self):
        if len(treasures) == 0:
            for gate in gates:
                gate.destroy()
            gates.clear()
        return len(treasures) == 0

    def show_message(self):
        turtle.goto(0, 0)
        turtle.color("white")
        turtle.write("Поздравляем! Вы собрали все сокровища!"
                     '\n' "Нажмите Enter, чтобы продолжить.", align="center",
                     font=("Courier", 25, "normal"))
        keyboard.wait('enter')
        turtle.clear()

class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("sun.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 10
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

class Exit(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("exit.gif")
        self.color("green")
        self.penup()
        self.speed(0)
        self.goto(x, y)

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 5:
            return True
        else:
            return False

class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("vrag.gif")
        self.color("red")
        self.penup()
        self.speed(0)
        self.gold = 25
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])
        self.active = True

    def move(self):
        if not self.active:
            return
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
            self.shape("vrag.gif")
        elif self.direction == "right":
            dx = 24
            dy = 0
            self.shape("vrag.gif")
        else:
            dx = 0
            dy = 0

        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            elif player.ycor() > self.ycor():
                self.direction = "up"

        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["up", "down", "left", "right"])

        turtle.ontimer(self.move, t=random.randint(100,300))

    def is_close(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 75:
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

def objects_init():
    global levels, treasures, enemies, exits, gates
    levels = [""]

    level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXX                  XX                E               XXXX  XX",
    "XX         X           XXX    XX    XXXXX    XXXXXXXX     XXXXXX      XX",
    "XX    P           XXXXXXXX         XXXXXX  T XXXXX                  XXXX",
    "XX         X            XXXXXXXXXXX    XXXXXXXXXXXXXXXXXXXXXXXXX      XX",
    "XXXXXXXXXXXX                                   XXX              E    XXX",
    "XX  T   XXXXX   XXXXXXXXXXXXXXXXXX    XXXXXXX  XXX   XXXXXXXXXX      XXX",
    "XXXXX   XXXX              XXXXXXXX    XXXXXXX  XXX          XXXXX    XXX",
    "XX         XXXXXXXXXXXX   XX          XXXXXX    XXXXXXXX    XXXXXX T  XX",
    "XXX    XXXXXXXXXX                    E                XX    XXXXXXXXXXXX",
    "XXX           XXXXXXXX    XXXX  XXXXXXXXXXXXX   XXXX           E      XX",
    "XXX    XXXXXXXXXX         XXXX   T XXXXXXXXX       X  XX  XXXXXXXXX   XX",
    "XXX    XXXXXXXXXXXXXXX    XXXX  XXXXXXX         X  X  XX  X  XXXXXX   XX",
    "XXX    XXXXXXX   T   X    XXXX  XXX            XX  X  XXXXX           XX",
    "XXX                      XXXXX  XXXXXX        XXX  X  XXXXX  XXX  XXXXXX",
    "XXXXXXXXXXXXXX       XX  XXXXX  XXXXXXXXX    XXX   X  XXXXX           XX",
    "XXXXXX      XXXXXX   XX              E             X  XXX T  XXXXXX   XX",
    "XX   XXXXX    XXX   XXX  XXX  XXX   XXXXXXXXXXXX   X  XXXXXXXXX       XX",
    "XX   XXXXX  XXXXXX   XX  XXX  XXX     XXX          X  XXX   XXX   XXXXXX",
    "XX      E            XX  XXX          XXXXXXXXX    X  XXX         XXXXXX",
    "XX            XXXX       XXXXXXXX    XXXXXXXX         XXX   XX        XX",
    "XXXXX   XXXX  XXXXXXXXXXXXXXXXXXXXX    XXXXXXX  XXXXXXXXX   XXXXXXXXXXXX",
    "XXXXX   XXXX              XXX  XXXXX    XXXXX   XXXX              XXXXXX",
    "XXXXX   XXXX  XXXX   XXX  XXX  XX        E         XXXXXX   XXX   XX  XX",
    "X       T      XXX   XXX  XXX  XXXXXXXXXXXXXX        XXXX   XXX   XX  XX",
    "X   XXXXXXXXX  XXXX             E  T             XX  XXXX   XXX     T XX",
    "X       XXXXX  XXXXXXXXX  XXX   XXXXXXXX   XXX  XXX  XXXX   XXXXXXXXXXXX",
    "X   XXXXXXXXX  XXXXXXXXX   XXXXXXXXXXX     XXX  XXX                  XXX",
    "X         E                 XXX                 XXXXXXXXXXXXXXX  E   XXX",
    "XXXXXX   XXXXX   XXX   XXXXXXXXXXXXX   XX     XXXX    T     XXX  T   XXX",
    "XX       XXXX   XXXXXXXXXXXX   XXXXXXXXXX           XXXX    XXXXXXXXXXXX",
    "XXXXX                                 XXX    XXXXXXXXXXX    X         XX",
    "XX  XX   XXXXXXXXXX  XXXXXXXXXXXXXXXXXXX                    G    R    XX",
    "XX  XX   XXXXXXX                 XXXXXX                     X         XX",
    "XX  T                 XXXXXXX T     E        XXXX           XXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    ]
    treasures = []
    enemies = []
    exits = []
    gates = []

    levels.append(level_1)

def restart_game():
    for enemy in enemies:
        enemy.active = False
    wn.clear()
    wn.clearscreen()
    wn.update()
    menu_start()
    objects_init()
    game_process()
    process()

def game_completed_message():
    turtle.goto(0, 0)
    turtle.color("white")
    turtle.write("Поздравляем, вы нашли выход из лабиринта  и остались живы!"
                 '\n' "         Нажмите 'ENTER' чтобы открыть главное меню", align="center",
                 font=("Courier", 25, "normal"))
    keyboard.wait('enter')
    restart_game()
    turtle.done()

def setup_maze(level):
    global gates
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -850 + (x * 24)
            screen_y = 440 - (y * 24)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.shape("pen.gif")
                pen.stamp()
                walls.append((screen_x, screen_y))

            if character == "G":
                pen.goto(screen_x, screen_y)
                pen.shape("gates.gif")
                new_gate = Gates()
                new_gate.goto(screen_x, screen_y)
                gates.append(new_gate)



            if character == "P":
                player.goto(screen_x, screen_y)

            if character == "T":
                treasures.append(Treasure(screen_x, screen_y))

            if character == "E":
                enemies.append(Enemy(screen_x, screen_y))

            if character == "R":
                exits.append(Exit(screen_x, screen_y))

def game_process():
    global pen, player, walls, gold_text
    pen = Pen()
    player = Player()
    walls = []

    setup_maze(levels[1])

    turtle.listen()
    turtle.onkey(player.go_left,"Left")
    turtle.onkey(player.go_right,"Right")
    turtle.onkey(player.go_up,"Up")
    turtle.onkey(player.go_down,"Down")

    wn.tracer(0)

    for enemy in enemies:
        turtle.ontimer(enemy.move, t=250)

    # вывод информации о золоте
    gold_text = turtle.Turtle()
    gold_text.hideturtle()
    gold_text.penup()
    gold_text.color("gold")
    gold_text.goto(-865, 455)
    gold_text.write("Сокровище: 0", font=("Comic Sans", 20, "normal"))

    exit_text = turtle.Turtle()
    exit_text.hideturtle()
    exit_text.penup()
    exit_text.color("white")
    exit_text.goto(465, -444)
    exit_text.write("Нажмите 'Q' чтобы завершить игру", font=("Comic Sans", 15, "normal"))

    music_text = turtle.Turtle()
    music_text.hideturtle()
    music_text.penup()
    music_text.color("white")
    music_text.goto(-865, -444)
    music_text.write("Нажмите 'O' чтобы выключить звук", font=("Comic Sans", 15, "normal"))

def process():
    game_over = False
    while game_over == False:
        for treasure in treasures:
            if player.is_collision(treasure):
                player.gold += treasure.gold
                gold_text.clear()
                gold_text.write("Сокровище: {}".format(player.gold), font=("Comic Sans", 20, "normal"))
                treasure.destroy()
                treasures.remove(treasure)

                if player.check_treasures():
                    player.show_message()
                    for exit_obj in exits:
                        exit_obj.color("green")
                        turtle.onkey(exit_game, "q")

        for enemy in enemies:
            if player.is_collision(enemy):
                player.show_collision_message()
                game_over = True

        for exit in exits:
            if player.is_collision(exit):
                game_over = True

        gold_text.clear()
        gold_text.write("Сокровище: {}".format(player.gold), font=("Comic Sans", 20, "normal"))

        if game_over == True:
            break

        turtle.onkeypress(exit_game, "q")

        wn.update()
    game_completed_message()

wn_create()
menu_start()
objects_init()
game_process()
process()
