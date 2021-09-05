from tkinter import *
import random
import datetime
#sound_path = "C:/Users/TobiasH/OneDrive/Tobias/PycharmProjects/CHARM/Tetris.mp3"
logging_path = "C:/Users/TobiasH/OneDrive/Tobias/PycharmProjects/CHARM/SNAKE_v1_log.txt"

# BUGS:

# TODO:
# - implement logging of scores into in-dir txt-file
# - read out logging-file for past highscores
# - make .exe compatible
# - Work with graphics for snake-body and head




def make_field(x_size, y_size):
    field = []
    for y in range(0, y_size):
        row_ = []
        for x in range(0, x_size):
            lab = Label(master=play_frame, bg="light grey", width=2)
            lab.grid(row=y, column=x, padx=2, pady=2)
            row_.append(lab)
        field.append(row_)
    return field


def spawn_fruit(x_size, y_size):
    global fruit_pos, snake, game_field
    x = random.randint(1, x_size-1)
    y = random.randint(1, y_size-1)
    fruit_pos_theo = [y, x]
    while fruit_pos_theo in snake:
        x = random.randint(1, x_size-1)
        y = random.randint(1, y_size-1)
        fruit_pos_theo = [y, x]
    fruit_pos = fruit_pos_theo
    fruit_p = game_field[fruit_pos[0]][fruit_pos[1]]
    fruit_p.config(bg="blue")


def rerun():
    global x_start, y_start, x_size, y_size, game_field, snake, current_snake_length, lost, fruit_pos
    global score, log, snake_colors, mapping_dic, game_field, First_move, highscore_score, highscore_label, logging_path
    global score_label

    x_start = random.randint(0, x_size - 1)
    y_start = random.randint(0, y_size - 1)
    First_move = True


    game_field = make_field(x_size, y_size)
    p = game_field[y_start][x_start]
    p.config(bg="yellow")
    snake = [[y_start, x_start]]
    lost = False
    current_snake_length = 1
    spawn_fruit(x_size, y_size)
    snake_colors = []
    score = 100  # 100 per length, starting with 1-length

    # Get highscore in file
    log = open(logging_path, "r").readlines()
    highscore_score = score
    for i in log:
        if int(i.split()[0]) >= highscore_score:
            highscore_score = int(i.split()[0])
    highscore_label.config(text="TOP: " + str(highscore_score))

    # Update Score-label
    score_label.config(text="SCORE: "+str(score))

    mapping_dic = {
    "a":    "Left",
    "Left": "Left",
    "d":    "Right",
    "Right": "Right",
    "w":    "Up",
    "Up":   "Up",
    "s":    "Down",
    "Down": "Down",
    "A": "Left",
    "D": "Right",
    "W": "Up",
    "S": "Down"

}


def key(event):
    # upon pressing of button, all things get re-rendered (and all changes from previous round get done)
    global x_start, y_start, x_size, y_size, game_field, snake, current_snake_length, lost, fruit_pos
    global score, snake_colors, mapping_dic, First_move, color_range, logging_path, highscore_label, highscore_score

#   log.write(str(datetime.datetime) + "//" + str(score) + "\n")

    if lost == True:
        #exit()
        print("YOU LOST!")
        print("SCORE: ", score)
        print("LOGGED TO: ", logging_path)
        print("RESTART : r")
        print("----------------")

        # Want to restart?
        if event.keysym == "r":
            log = open(logging_path, "a")
            log_txt = (str(datetime.datetime.now()) + " " + str(score) + "\n")
            log_txt = str(score) + "\n"
            log.write(log_txt)
            log.close()
            rerun()
            lost = False
    else:
        # run event-kesysm through mapper-dic
        try:
            if First_move == True:
                game_field[y_start][x_start].config(bg="light grey")
                First_move = False

            instruction = mapping_dic[event.keysym]
            instruction_mapping = {
                "Left": lambda x, x_size: x - 1 if not x <= 0 else x - x + x_size - 1,
                "Right": lambda x, x_size: x + 1 if not x >= (x_size - 1) else x - x,
                "Up": lambda y, y_size: y - 1 if not y <= 0 else y - y + y_size - 1,
                "Down": lambda y, y_size: y + 1 if not y >= (y_size - 1) else y - y,
            }

            if instruction in ["Up", "Down"]:
                y_start = instruction_mapping[instruction](y_start, y_size)
            else:
                x_start = instruction_mapping[instruction](x_start, x_size)


            snake.append([y_start, x_start])
            if len(snake) > current_snake_length:
                game_field[snake[0][0]][snake[0][1]].config(bg="light grey")
                snake = snake[1::]

            if snake.count([y_start, x_start]) >= 2:
                lost = True

            if [y_start, x_start] == fruit_pos:
                # got the fruit
                spawn_fruit(x_size, y_size)
                current_snake_length += 1
                snake_colors.append(colorcoder(color_range))
                score += 100
                score_label.config(text=score)

            p = game_field[y_start][x_start]
            p.config(bg="yellow")

            if lost == True:
                for i in snake:
                    yi = i[0]
                    xi = i[1]
                    game_field[yi][xi].config(bg="red")
            else:
                index_ = 0
                for i in snake[:len(snake)-1]:
                    game_field[i[0]][i[1]].config(bg=snake_colors[index_])
                    index_ += 1
        except:
            print("Wrong key")


def colorcoder(inp):
    # input: [[1, 16], [0, 0], [0, 0]]


    aray = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]

    r = 3 * aray[random.randint(inp[0][0], inp[0][1])]
    g = 3 * aray[random.randint(inp[1][0], inp[1][1])]
    b = 3 * aray[random.randint(inp[2][0], inp[2][1])]

    color = "#" + r + g + b

    return color







root = Tk()
root.title("SNAKE V1")

# Title:
title_frame = Frame(root)
title_frame.pack()

title_label = Label(title_frame, text="SNAKE V1", font=('Verdana', 30))
title_label.pack()

# Playing Field:

play_frame = Frame(root)
play_frame.pack()

# Framing
info_frame = Frame(root)
info_frame.pack()

score_label = Label(info_frame, text=0)
score_label.pack()

highscore_label = Label(info_frame, text="0")
highscore_label.pack()


# Game-sepcifics
x_size = 15
y_size = 15
score = 100
color_range = [
    [0, 15],
    [0, 0],
    [0, 0]
]
# Data for the Game:
rerun()





# Playing Field - take action
root.bind_all('<Key>', key)
root.mainloop()


