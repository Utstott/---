from tkinter import *
# Импортируем рандом
import random
# Глобальные переменные
# Настройки окна
WIDTH = 900
HEIGHT = 900

# Очки для каждого игрока
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

# Счет скорости
INITIAL_SPPED = 20
# Настройки ракеток
# Ширина ракеток
PAD_W = 10
# Высота ракетки
PAD_H = 100
# Настройка мяча
# Радиус мяча
BALL_RADIUS = 40
# Скорость мяча
# горизонтально
BALL_X_CHANGE = 20
# Вертикально
BALL_Y_CHANGE = 0
# Окно
root = Tk()
root.title('Пинг понг:)')
# canvas
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#44944A")
c.pack()
# Элемент игрового поля
# Левая линия
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill='white')
# Правая линия
c.create_line(WIDTH-PAD_W, 0, WIDTH-PAD_W, HEIGHT, fill='white')
# Разделитель игрового поля
c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill='white')
# Мяч
BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2,
                     HEIGHT/2-BALL_RADIUS/2,
                     WIDTH/2+BALL_RADIUS/2,
                     HEIGHT/2+BALL_RADIUS/2,
                     fill='#D5D5D5')
# Ракетки
# Левая ракетка
LEFT_PAD = c.create_line(PAD_W/2, 0, PAD_W/2, PAD_H,
                         width=PAD_W, fill='#DA70D6')
# Правая ракетка
RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2, PAD_H,
                          width=PAD_W, fill='#DA70D6')
# Текст очков
p_1_text = c.create_text(WIDTH - WIDTH/6, PAD_H/4,
                         text=PLAYER_1_SCORE,
                         font='Arial 20',
                         fill='aqua')
p_2_text = c.create_text(WIDTH/6, PAD_H/4,
                         text=PLAYER_2_SCORE,
                         font='Arial 20',
                         fill='aqua')
# Скорости ракеток
PAD_SPPED = 20
# Скорости левой ракетки
LEFT_PAD_SPPED = 0
# Скорости правой ракетки
RIGHT_PAD_SPEED = 0

# Скорость мяча с каждым ударом
BALL_SPEED_UP = 1.00
# Макс.скорость мяча
BALL_MAX_SPPED = 30
# Начальная скорость мяча по горизонтали
BALL_X_SPEED = 20
# Начальная скорость мяча по вертикали
BALL_Y_SPEED = 20
# Расстояние до правого края
right_line_distance = WIDTH - PAD_W

# Счет


def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == 'right':
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)

# Респаун


def spawn_ball():
    global BALL_X_SPEED
    c.coords(BALL, WIDTH/2-BALL_RADIUS/2,
             HEIGHT/2-BALL_RADIUS/2,
             WIDTH/2+BALL_RADIUS/2,
             HEIGHT/2+BALL_RADIUS/2)
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPPED)/abs(BALL_X_SPEED)


# Отскок мяча от ракеток


def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == 'strike':
        BALL_Y_SPEED = random.randrange(-10, 10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPPED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED


# Функция движения мяча


def move_ball():
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2
    # Вертикальный отскок
    if ball_right + BALL_X_SPEED < right_line_distance and ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    elif ball_right == right_line_distance or ball_left == PAD_W:
        if ball_right > WIDTH / 2:
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                bounce('strike')
            else:
                update_score('left')
                spawn_ball()
        else:
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                bounce('strike')
            else:
                update_score('right')
                spawn_ball()
    else:
        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance-ball_right, BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left+PAD_W, BALL_Y_SPEED)
    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce('ricochet')
    # Функция движения ракеток


def move_pads():
    PADS = {LEFT_PAD: LEFT_PAD_SPPED,
            RIGHT_PAD: RIGHT_PAD_SPEED}
    for pad in PADS:
        c.move(pad, 0, PADS[pad])
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])


def main():
    move_ball()
    move_pads()
    # Вызываем саму себя
    root.after(30, main)


# Фокус на канвас(реакция на клавиши)
c.focus_set()

# Обработка нажатий


def moveent_handler(event):
    global LEFT_PAD_SPPED, RIGHT_PAD_SPEED
    if event.keysym == 'w':
        LEFT_PAD_SPPED = -PAD_SPPED
    elif event.keysym == 's':
        LEFT_PAD_SPPED = PAD_SPPED
    elif event.keysym == 'Up':
        RIGHT_PAD_SPEED = -PAD_SPPED
    elif event.keysym == 'Down':
        RIGHT_PAD_SPEED = PAD_SPPED


# Привязка к канвас
c.bind('<KeyPress>', moveent_handler)

# Клавиши не нажаты


def stop_pad(event):
    global LEFT_PAD_SPPED, RIGHT_PAD_SPEED
    if event.keysym in 'ws':
        LEFT_PAD_SPPED = 0
    elif event.keysym in ('Up', 'Down'):
        RIGHT_PAD_SPEED = 0


c.bind('<KeyRelease>', stop_pad)

# Запуск
main()


# Запуск окна
root.mainloop()
