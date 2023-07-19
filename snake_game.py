from tkinter import *
import random


GAME_WIDTH = 600
GAME_HEIGHT = 600
SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
DIRECTION = "down"

score = 0
direction = DIRECTION
game_window = None
label = None



class Snake:

    def __init__(self, canvas):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, self.body_size):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)



class Food:

    def __init__(self, canvas):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE)-1) * SPACE_SIZE

        self.coordinates = [x, y]
        
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")



def next_turn(snake, food, canvas):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score, label

        score += 1

        label.config(text="Score: {}".format(score))
        
        canvas.delete("food")

        food = Food(canvas)
    else:
        del snake.coordinates[-1]
        
        canvas.delete(snake.squares[-1])
        
        del snake.squares[-1]

    if check_collesion(snake):
        game_over(canvas)
        return

    game_window.after(SPEED, next_turn, snake, food, canvas)

def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collesion(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for xb, yb in snake.coordinates[1:]: 
        if x == xb and y == yb:
            return True
    
    return False
    

def game_over(canvas):
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70),
                       text="GAME OVER!",
                       fill="red",
                       tag="game_over")


def new_game():
    global game_window, score, direction, label
    
    game_window = Tk()
    game_window.title("Snake Game")
    game_window.resizable(False, False)

    score = 0
    direction = DIRECTION

    label = Label(game_window, text="Score: {}".format(score), font=('consolas', 40))
    label.pack()

    canvas = Canvas(game_window, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
    canvas.pack()

    game_window.update()


    window_width = game_window.winfo_width()
    window_height = game_window.winfo_height()
    screen_width = game_window.winfo_screenwidth()
    screen_height = game_window.winfo_screenheight()

    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2))

    game_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    game_window.bind('<Left>', lambda event: change_direction('left'))
    game_window.bind('<Right>', lambda event: change_direction('right'))
    game_window.bind('<Up>', lambda event: change_direction('up'))
    game_window.bind('<Down>', lambda event: change_direction('down'))

    snake = Snake(canvas)
    food = Food(canvas)

    next_turn(snake, food, canvas)

    game_window.mainloop()


new_game()
