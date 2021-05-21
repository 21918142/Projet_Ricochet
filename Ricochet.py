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
    for i in range(0, height, side):
        for j in range(0, width, side):
            color = "#B3B191"
            canvas.create_rectangle(i,j,i+side,j+side,fill=color,activefill="brown")
    for i in range(side*7, side*9, side):
        for j in range(side*7, side*9, side):
            color = "black"
            canvas.create_rectangle(i,j,i+side,j+side,fill=color,activefill="brown")
            

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
    x = int(pos_robot[0][0])+2
    y = int(pos_robot[0][1])+1
    target_r = canvas.create_rectangle(x*side+10, y*side+10, x*side+30, y*side+30, fill="red")
    x = int(pos_robot[0][0])
    y = int(pos_robot[0][1])-10
    target_y = canvas.create_rectangle(x*side+10, y*side+10, x*side+30, y*side+30, fill="yellow")
    x = int(pos_robot[0][0])+9
    y = int(pos_robot[0][1])-10
    target_g = canvas.create_rectangle(x*side+10, y*side+10, x*side+30, y*side+30, fill="green")


def stop(robot,stop_x,stop_y):
    canvas.move(robot, stop_x, stop_y)
    return robot, stop_x, stop_y

def collision_blue():
    coord = canvas.coords(robots[0])
    c = canvas.find_overlapping(*coord)   
    for id in c:
        color = canvas.itemcget(id, "fill")
        if color == "red" or color == "black" or color =="green" or color=="yellow":
            return True

def move_blue():
    global dx,dy,stop_move_b
    canvas.move(robots[0], dx, dy)
    stop_move_b = canvas.after(1, move_blue)
    if collision_blue():
        stop(robots[0], -dx, -dy)
        dx=0
        dy=0

def collision_red():
    coord = canvas.coords(robots[1])
    c = canvas.find_overlapping(*coord)   
    for id in c:
        color = canvas.itemcget(id, "fill")
        if color == "blue" or color == "black" or color =="green" or color=="yellow":
            return True

def move_red():
    global dx,dy,stop_move_r
    canvas.move(robots[1], dx, dy)
    stop_move_r = canvas.after(1, move_red)
    if collision_red():
        stop(robots[1], -dx, -dy)
        dx=0
        dy=0

def collision_green():
    coord = canvas.coords(robots[2])
    c = canvas.find_overlapping(*coord)   
    for id in c:
        color = canvas.itemcget(id, "fill")
        if color == "blue" or color == "black" or color =="red" or color=="yellow":
            return True

def move_green():
    global dx,dy, stop_move_g
    canvas.move(robots[2], dx, dy)
    stop_move_g = canvas.after(1, move_green)
    if collision_green():
        stop(robots[2], -dx, -dy)
        dx=0
        dy=0

def collision_yellow():
    coord = canvas.coords(robots[3])
    c = canvas.find_overlapping(*coord)   
    for id in c:
        color = canvas.itemcget(id, "fill")
        if color == "blue" or color == "black" or color =="green" or color=="red":
            return True

def move_yellow():
    global dx,dy, stop_move_y
    canvas.move(robots[3], dx, dy)
    stop_move_y = canvas.after(1, move_yellow)
    if collision_yellow():
        stop(robots[3], -dx, -dy)
        dx=0
        dy=0

def click(event):
    global get_pos
    """ Permet d'efectuer le deplacement d'1 robot quand on le clique dessus,
    Et restart quand on clique sur le carré milieu """
    get_pos = (event.x//40, event.y//40)
    x1,y1,x2,y2 = canvas.coords(robots[0])
    u1,v1,u2,v2 = canvas.coords(robots[1])
    i1,j1,i2,j2 = canvas.coords(robots[2])
    n1,m1,n2,m2 = canvas.coords(robots[3])

    if get_pos == (x1//40, y1//40):
        move_blue()
        canvas.after_cancel(stop_move_r)
        canvas.after_cancel(stop_move_g)
        canvas.after_cancel(stop_move_y)

    elif get_pos == (u1//40, v1//40):
        move_red()
        canvas.after_cancel(stop_move_b)
        canvas.after_cancel(stop_move_g)
        canvas.after_cancel(stop_move_y)

    elif get_pos == (i1//40, j1//40):
        move_green()
        canvas.after_cancel(stop_move_b)
        canvas.after_cancel(stop_move_r)
        canvas.after_cancel(stop_move_y)
        
    elif get_pos == (n1//40, m1//40):
        move_yellow()
        canvas.after_cancel(stop_move_b)
        canvas.after_cancel(stop_move_r)
        canvas.after_cancel(stop_move_g)
  

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


canvas.bind("<1>", click)
canvas.bind_all("<Key>", keyboard)

root.mainloop()