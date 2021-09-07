from tkinter import *
import random
import math


#TODO:
# - Reading Highscore
# - Styling (Amanda? as Game-tester?) (Retro!)
# - Finding and fixing Bugs
# - how to implement speed-up (Constant, fixed-percent, changing-percent, logarithmic)
# - Power-items (remove length, etc.)
# - "Roadblocks" on the Map


class snake_v2():
    def __init__(self, grid_size):
        self.x_max = grid_size[0]
        self.y_max = grid_size[1]
        logging_path = "SNAKE_v2_log.txt"

        # Framing and TK-Stuff
        self.root = Tk()
        self.root.title("SNAKE V2")
        self.play_frame = Frame(self.root)
        self.play_frame.pack()
        self.info_frame = Frame(self.root)
        self.info_frame.pack()
        self.text_frame = Frame(self.root)
        self.text_frame.pack(expand=True)

        # Filling the Info-Frame
        self.info_label = Label(self.info_frame, text="", justify="left")
        self.info_label.grid(row=0, column=0, padx=4)

        self.speed_label = Label(self.info_frame, text="", justify="left")
        self.speed_label.grid(row=0, column=1, padx=4)

        self.run_num_label = Label(self.info_frame, text="", justify="left")
        self.run_num_label.grid(row=0, column=2, padx=4)

        self.change_color_palette_button = Button(self.info_frame, text="Red Snake",
                                                  command=self.change_color_palette,
                                                  bg="red",
                                                  fg="white")
        self.change_color_palette_button.grid(row=1, column=0, columnspan=3)

        self.auto_mode_label = Label(self.info_frame, text="Auto OFF",
                                     fg="black", bg="red")
        self.auto_mode_label.grid(row=2, column=1)

        self.text_welcome_label = Label(self.text_frame,
                                        text=("Welcome to SNAKE v2 by Tobias Henkels "
                                              "\n Restart: R \n AUTO-movement: T"),
                                        justify="left")
        self.text_welcome_label.pack()

        self.text_you_lost_label = Label(self.text_frame, text="YOU LOST! \n Press \'R\'!", font=("Comic Sans", 22),
                                         fg="red")
        self.text_you_lost_label.pack()

        # Game Initials
        self.make_field()
        self.mapping = {
            "a": "Left",
            "Left": "Left",
            "d": "Right",
            "Right": "Right",
            "w": "Up",
            "Up": "Up",
            "s": "Down",
            "Down": "Down",
            "A": "Left",
            "D": "Right",
            "W": "Up",
            "S": "Down"

        }
        self.instruction_mapping = {
            "Left": lambda x, x_size: x - 1 if not x <= 0 else x - x + x_size - 1,
            "Right": lambda x, x_size: x + 1 if not x >= (x_size - 1) else x - x,
            "Up": lambda y, y_size: y - 1 if not y <= 0 else y - y + y_size - 1,
            "Down": lambda y, y_size: y + 1 if not y >= (y_size - 1) else y - y,
        }
        self.color_name_map = ["Red Snake", "Green Snake", "Blue Snake"]
        self.current_color_index = 0
        self.color_rgb_map = {
            "Red Snake": [[0, 13], [0, 0], [0, 0]],
            "Green Snake": [[0, 0], [0, 13], [0, 0]],
            "Blue Snake": [[0, 0], [0, 0], [0, 13]]
        }
        self.color_range = [
            [0, 13],
            [0, 0],
            [0, 0]
        ]
        self.run_num = 0

        # Setting re-used game-variables
        self.rerun()

        # Last Stuff
        self.direc = "Left"
        self.auto_movement_allowed = False
        self.root.bind_all("<Key>", self.input_analysis)
        self.root.mainloop()

    def make_field(self):
        self.field = []
        for y in range(0, self.y_max):
            row_ = []
            for x in range(0, self.x_max):
                lab = Label(master=self.play_frame, bg="light grey", width=2)
                lab.grid(row=y, column=x, padx=2, pady=2)
                row_.append(lab)
            self.field.append(row_)

    def spawn_fruit(self):
        self.score += 100
        self.info_label.config(text=f"SCORE: {self.score}")
        self.speed_rule_ceiled_constant_increase()
        self.speed_label.config(text=f"SPEED: {str(self.speed)[0:4]}")

        x = random.randint(1, self.x_max - 1)
        y = random.randint(1, self.y_max - 1)
        fruit_pos_theo = [y, x]
        while fruit_pos_theo in self.snake:
            x = random.randint(1, self.x_max - 1)
            y = random.randint(1, self.y_max - 1)
            fruit_pos_theo = [y, x]

        self.fruit = fruit_pos_theo
        self.field[y][x].config(bg="blue")

    def rerun(self):
        self.x_start = random.randint(0, self.x_max - 1)
        self.y_start = random.randint(0, self.y_max - 1)

        self.snake_head = self.field[self.y_start][self.x_start]
        self.snake = [[self.y_start, self.x_start]]
        self.snake_head.config(bg="yellow")
        self.snake_length = 1

        self.score = 0
        self.speed = 2.5
        self.spawn_fruit()
        self.lost = False
        self.manual_input = False
        self.snake_colors = []
        self.run_num += 1
        self.run_num_label.config(text=f"ROUND: {self.run_num}", justify="left")
        self.text_you_lost_label.config(text="")

    def move(self, direction):

        if not self.lost:

            # Change Heads Position
            if direction in ["Up", "Down"]:
                self.y_start = self.instruction_mapping[direction](self.y_start, self.y_max)
            else:
                self.x_start = self.instruction_mapping[direction](self.x_start, self.x_max)
            self.snake.append([self.y_start, self.x_start])
            self.direc = direction

            # Checks for cases
            if len(self.snake) > self.snake_length:
                self.field[self.snake[0][0]][self.snake[0][1]].config(bg="light grey")
                self.snake = self.snake[1::]

            # Got Fruit -> Increase Length
            if [self.y_start, self.x_start] == self.fruit:
                self.spawn_fruit()
                self.snake_length += 1
                self.snake_colors.append(color_coder(self.color_rgb_map[self.color_name_map[self.current_color_index]]))

            # Check if "Snake bites own tail"
            if self.snake.count([self.y_start, self.x_start]) >= 2:
                self.lost = True
                self.you_lost()
            else:
                # draw snake
                _index = 0
                for part in self.snake[:len(self.snake) - 1]:
                    self.field[part[0]][part[1]].config(bg=self.snake_colors[_index])
                    _index += 1
                self.field[self.y_start][self.x_start].config(bg="yellow")

    def input_analysis(self, event):
        if event.keysym in ["w", "a", "s", "d", "Left", "Right", "Up", "Down"]:
            direction = self.mapping[event.keysym]

            if self.auto_movement_allowed == False:
                self.move(direction)
            else:
                if self.direc in ["Up", "Down"] and direction in ["Left", "Right"]:
                    self.move(direction)
                elif self.direc in ["Left", "Right"] and direction in ["Up", "Down"]:
                    self.move(direction)
        elif event.keysym == "r":
            # Clean up and Restart
            for part in self.snake:
                self.field[part[0]][part[1]].config(bg="light grey")
            self.field[self.fruit[0]][self.fruit[1]].config(bg="light grey")
            self.rerun()
        elif event.keysym == "t":
            # toggle AUTO-movement
            if self.auto_movement_allowed:
                self.auto_movement_allowed = False
                self.auto_mode_label.config(text="Auto OFF", bg="red", fg="black")
            else:
                self.auto_movement_allowed = True
                self.auto_mode_label.config(text="Auto ON", bg="green", fg="white")
                self.auto_move()

    def auto_move(self):
        # continues down last direction
        if self.auto_movement_allowed:
            self.move(self.direc)
            self.root.after(math.floor(1000 / self.speed), self.auto_move)

    def you_lost(self):
        for part in self.snake:
            self.field[part[0]][part[1]].config(bg="red")
        self.text_you_lost_label.config(text="YOU LOST! \n Press \'R\'")

    def change_color_palette(self):
        self.current_color_index += 1
        if self.current_color_index >= len(self.color_name_map):
            self.current_color_index = 0

        self.change_color_palette_button.config(text=self.color_name_map[self.current_color_index],
                                                bg=self.color_name_map[self.current_color_index].split()[0],
                                                fg="white")

    def speed_rule_ceiled_constant_increase(self):
        if self.speed < 13:
            self.speed += 1


def color_coder(inp):
    aray = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    r = 3 * aray[random.randint(inp[0][0], inp[0][1])]
    g = 3 * aray[random.randint(inp[1][0], inp[1][1])]
    b = 3 * aray[random.randint(inp[2][0], inp[2][1])]

    color = "#" + r + g + b
    return color


app = snake_v2([13, 13])
