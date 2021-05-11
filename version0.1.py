import tkinter as tk
import random 

# Constante
HEIGHT = 640
WIDTH  = 640
SIZE = 16
COTE = HEIGHT // SIZE

tableau = None
target = None
pos_robot = []
robots = []
dx = 0
dy = 0


def grid():
    for i in range(0,HEIGHT,COTE):
        for j in range(0,WIDTH,COTE):
            canvas.create_rectangle(i,j,i+COTE,j+COTE,fill="white")


def generate():
    """ affiche walls + pos target + pos robots"""
    global tableau, target, pos_robot
    fichier = open("Board.txt", "r")
    nb_line = 0
    for line in fichier:
        if 4 <= nb_line < 36:
            tableau = [line.split() for line in fichier]
                        
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
    for i in range(len(tableau)):
        for j in range(len(tableau[i])):
            if tableau[i][j] == "2": # -
                canvas.create_line(i//2*COTE, j*COTE, (i//2+1)*COTE, j*COTE, fill="black", width=5)

            if tableau[i][j] == "1": # |
                canvas.create_line(i//2*COTE, j*COTE, i//2*COTE, (j+1)*COTE, fill="black", width=5)

def show_robots():
    global robot
    x = int(pos_robot[0][0])
    y = int(pos_robot[0][1])
    bleu = canvas.create_oval(x*COTE+5, y*COTE+5, x*COTE+35, y*COTE+35, fill = "blue")

    x = int(pos_robot[1][0])
    y = int(pos_robot[1][1])
    red = canvas.create_oval(x*COTE+5, y*COTE+5, x*COTE+35, y*COTE+35, fill = "red")

    x = int(pos_robot[2][0])
    y = int(pos_robot[2][1])
    green = canvas.create_oval(x*COTE+5, y*COTE+5, x*COTE+35, y*COTE+35, fill = "green")

    x = int(pos_robot[3][0])
    y = int(pos_robot[3][1])
    yellow = canvas.create_oval(x*COTE+5, y*COTE+5, x*COTE+35, y*COTE+35, fill = "yellow")

    robots.append(bleu)
    robots.append(red)
    robots.append(green)
    robots.append(yellow)

def show_target():
    x = int(target[0])
    y = int(target[1])
    target_b = canvas.create_rectangle(x*COTE+10, y*COTE+10, x*COTE+30, y*COTE+30, fill="blue")
    

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
canvas = tk.Canvas(root,height=HEIGHT, width=WIDTH)
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