import tkinter as tk
import random 

# Constante
height = 640
width  = 640
size = 16
side = height // size

table = None
target = None
pos_robot = []
robots = []
dx = 0
dy = 0


def grid():
    for i in range(0,height,side):
        for j in range(0,width,side):
            canvas.create_rectangle(i,j,i+side,j+side,fill="white")


def generate():
    """ affiche walls + pos target + pos robots"""
    global table, target, pos_robot
    file = open("Board.txt", "r")
    nb_line = 0
    for line in file:
        if 4 <= nb_line < 36:
            table = [line.split() for line in file]
                        
        if nb_line == 0:
            target = line.split()
        
        if nb_line == 1:
            b = line.split()
            pos_robot.append(b)
        
        if nb_line == 2:
            r = line.split()
            pos_robot.append(r)
        
        if nb_line == 3:
            g = line.split()
            pos_robot.append(g)
        
        if nb_line == 4:
            y = line.split()
            pos_robot.append(y)

        nb_line +=1

def show_walls():
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == "2": # -
                canvas.create_line(i//2*side, j*side, (i//2+1)*side, j*side, fill="black", width=5)

            if table[i][j] == "1": # |
                canvas.create_line(i//2*side, j*side, i//2*side, (j+1)*side, fill="black", width=5)

def show_robots():
    global robot
    x = int(pos_robot[0][0])
    y = int(pos_robot[0][1])
    blue = canvas.create_oval(x*side+5, y*side+5, x*side+35, y*side+35, fill = "blue")

    x = int(pos_robot[1][0])
    y = int(pos_robot[1][1])
    red = canvas.create_oval(x*side+5, y*side+5, x*side+35, y*side+35, fill = "red")

    x = int(pos_robot[2][0])
    y = int(pos_robot[2][1])
    green = canvas.create_oval(x*side+5, y*side+5, x*side+35, y*side+35, fill = "green")

    x = int(pos_robot[3][0])
    y = int(pos_robot[3][1])
    yellow = canvas.create_oval(x*side+5, y*side+5, x*side+35, y*side+35, fill = "yellow")

    robots.append(blue)
    robots.append(red)
    robots.append(green)
    robots.append(yellow)


def show_target():
    x = int(target[0])
    y = int(target[1])
    target_b = canvas.create_rectangle(x*side+10, y*side+10, x*side+30, y*side+30, fill="blue")

 
def show_targets():
    pass 
    """Création des cibles + définir leur position """
    global targets, pos_target

    n = random.randrange(40, 600, 40)
    m = random.randrange(40, 600, 40)

    x = random.randrange(40, 600, 40)
    y = random.randrange(40, 600, 40)

    u = random.randrange(40, 600, 40)
    v = random.randrange(40, 600, 40)

    a = random.randrange(40, 600, 40)
    b = random.randrange(40, 600, 40)

    Blue = canvas.create_rectangle(n+5, m+5, n+35, m+35, fill="blue")
    Red = canvas.create_rectangle(x+5, y+5, x+35, y+35, fill="red")
    Yellow = canvas.create_rectangle(u+5, v+5, u+35, v+35, fill="yellow")
    Green = canvas.create_rectangle(a+5, b+5, a+35, b+35, fill="green")

    position_bleu = (n//side, m//side)
    position_red = (x//side, y//side)
    position_yellow = (u//side, v//side)
    position_green = (a/side, b//side)

    pos_target.append(position_bleu)
    pos_target.append(position_red)
    pos_target.append(position_yellow)
    pos_target.append(position_green)

    targets.append(Blue)
    targets.append(Red)
    targets.append(Yellow)
    targets.append(Green)

    

def stop(robot,stop_x,stop_y):
    canvas.move(robot, stop_x, stop_y)
    return robot, stop_x, stop_y

def collision():
    coord = canvas.coords(robots[0])
    c = canvas.find_overlapping(*coord)
    for id in c:
        color = canvas.itemcget(id, "fill")
        if color == "red" or color == "black" or color =="green" or color=="yellow":
            return True


   
def deplacement():
    global dx,dy
    canvas.move(robots[0], dx, dy)
    canvas.after(1, deplacement)
    if collision():
        stop(robots[0], -dx, -dy)
        dx=0
        dy=0     
  

def keyboard(event):
    global dx, dy
    key = event.keysym
    if key == "Up":
        dx = 0
        dy = -20
    elif key == "Down":
        dx = 0
        dy = 20
    elif key == "Left":
        dx = -20
        dy = 0
    elif key == "Right":
        dx = 20
        dy = 0



def click(event):
    global get_pos
    get_pos = (event.x//40, event.y//40)
    print(get_pos)

    

    

root = tk.Tk()


# Creation des widgets
canvas = tk.Canvas(root,height=height, width=width)
bouton = tk.Button(root, text="Génération terrain")


#Placement des widgets
canvas.grid()
bouton.grid()



grid()
generate()
show_robots()
show_target()
show_walls()
deplacement()

canvas.bind("<1>", click)
canvas.bind_all("<Key>", keyboard)

root.mainloop()