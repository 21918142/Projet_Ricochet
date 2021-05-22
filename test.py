############################################
# Groupe MPCI 6
# Kevin SU
# Brice AUGUSTIN
# Lilya LAHJAILY
# Zinaida BENAOUDIA
# Celine DJADEL
# https://github.com/21918142/Projet_Ricochet
#############################################


# Import des librairies
import tkinter as tk
from tkinter.constants import BOTH
import tkinter.messagebox as tkm

# Constantes
height = 640
width  = 640
size = 16
side = height // size

# Variables globales 
table = None
target = None
pos_target = []
pos_robot = []
robots = []
dx = 0
dy = 0
cpt = 0
bot = 0

# Listes
coord_robot = []
bot_color = ['blue', 'red', 'green', 'yellow' ]

# Fonctions
#------------------------------------ Plateau ------------------------------------#

def grid():
    """Affiche un quadrillage sur le canvas"""
    for i in range(0, height, side):
        for j in range(0, width, side):
            color = "#B3B191"
            canvas.create_rectangle(i,j,i+side,j+side,fill=color,activefill="brown")
    for i in range(side*7, side*9, side):
        for j in range(side*7, side*9, side):
            color = "black"
            canvas.create_rectangle(i,j,i+side,j+side,fill=color,activefill="brown")
            
def generate():
    """Affiche walls + pos target + pos robots"""
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
    """Affiche les murs"""
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == "2": # -
                canvas.create_line(i//2*side, j*side, (i//2+1)*side, j*side, fill="black", width=5)

            if table[i][j] == "1": # |
                canvas.create_line(i//2*side, j*side, i//2*side, (j+1)*side, fill="black", width=5)

def show_robots():
    """Affiche les quatres robots"""
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
    """Affiche les quatres cibles"""
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

    pos_target.append(target_b)
    pos_target.append(target_r)
    pos_target.append(target_g)
    pos_target.append(target_y)

#------------------------------------ Déplacements ------------------------------------

def stop(robot,stop_x,stop_y):
    canvas.move(robot, stop_x, stop_y)
    return robot, stop_x, stop_y

def collision_blue():
    global cpt
    coord = canvas.coords(robots[0])
    b = canvas.coords(pos_target[0])
    if coord[0]//40 == b[0]//40 and coord[1]//40 == b[1]//40:
        canvas.delete(pos_target[0])
        win()
        continues()
        cpt =0
        pos_target[0]= canvas.create_rectangle(16*side+10, 4*side+10, 16*side+30, 4*side+30, fill="blue") 

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
    global cpt
    coord = canvas.coords(robots[1])
    r = canvas.coords(pos_target[1])
    if coord[0]//40 == r[0]//40 and coord[1]//40 == r[1]//40:
        canvas.delete(pos_target[1])
        win()
        continues()
        cpt = 0
        pos_target[1]= canvas.create_rectangle(17*side+10, 4*side+10, 17*side+30, 4*side+30, fill="red")

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
    global cpt
    coord = canvas.coords(robots[2])
    g = canvas.coords(pos_target[2])
    if coord[0]//40 == g[0]//40 and coord[1]//40 == g[1]//40:
        canvas.delete(pos_target[2])
        win()
        continues()
        cpt = 0
        pos_target[2]= canvas.create_rectangle(18*side+10, 4*side+10, 18*side+30, 4*side+30, fill="green")

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
    global cpt
    coord = canvas.coords(robots[3])
    y = canvas.coords(pos_target[3])
    if coord[0]//40 == y[0]//40 and coord[1]//40 == y[1]//40:
        canvas.delete(pos_target[3])
        win()
        continues()
        cpt = 0
        pos_target[3]= canvas.create_rectangle(19*side+10, 4*side+10, 19*side+30, 4*side+30, fill="yellow")

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
    global get_pos, bot
    """Permet d'effectuer le deplacement d'un robot quand on clique dessus et
       restart quand on clique sur le carré au milieu"""
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
        bot = 0

    elif get_pos == (u1//40, v1//40):
        move_red()
        canvas.after_cancel(stop_move_b)
        canvas.after_cancel(stop_move_g)
        canvas.after_cancel(stop_move_y)
        bot = 1

    elif get_pos == (i1//40, j1//40):
        move_green()
        canvas.after_cancel(stop_move_b)
        canvas.after_cancel(stop_move_r)
        canvas.after_cancel(stop_move_y)
        bot = 2
        
    elif get_pos == (n1//40, m1//40):
        move_yellow()
        canvas.after_cancel(stop_move_b)
        canvas.after_cancel(stop_move_r)
        canvas.after_cancel(stop_move_g)
        bot = 3
  
def keyboard(event):
    global dx, dy, cpt
    key = event.keysym
    if key == "Up":
        stockage_coord()
        dx = 0
        dy = -20
        cpt += 1
        cpt_move.config(text="Move = "+ str(cpt))
    elif key == "Down":
        stockage_coord()
        dx = 0
        dy = 20
        cpt += 1
        cpt_move.config(text="Move = "+ str(cpt))
    elif key == "Left":
        stockage_coord()
        dx = -20
        dy = 0
        cpt += 1
        cpt_move.config(text="Move = "+ str(cpt))
    elif key == "Right":
        stockage_coord()
        dx = 20
        dy = 0
        cpt += 1 
        cpt_move.config(text="Move = "+ str(cpt))
    
def stockage_coord():
    '''Stocke les coordonnées du robot'''
    global a, b, c, d
    a, b, c, d = canvas.coords(robots[bot])
    coord_robot.append([a, b, c, d])
    print(coord_robot)

#------------------------------------ Message ------------------------------------#

def win():
    """Affiche un message lorsque le joueur a gagné"""
    tkm.showinfo("Félicitation", "Vous avez gagné !\nMouvement: "+ str(cpt))

def continues():
    """Demande au joueur s'il veut continuer de jouer"""
    message = tkm.askquestion("Félicitation", "Continue de jouer ?")
    if message == "yes":
        pass # save score
    if message == "no":
        root.destroy()

#------------------------------------ Autre ------------------------------------#

def save():
    pass

def load():
    pass

def undo():
    """Annule les derniers déplacements du robot"""
    global robots
    if canvas.coords(robots[bot]) != coord_robot[0]:
        if bot == 0:                  
            canvas.delete(robots[bot])
            robots[bot] = canvas.create_oval(coord_robot[-1][0], coord_robot[-1][1],
                    coord_robot[-1][2], coord_robot[-1][3], fill = bot_color[0])
            coord_robot.remove(coord_robot[-1])
        elif bot == 1:
            canvas.delete(robots[bot])
            robots[bot] = canvas.create_oval(coord_robot[-1][0], coord_robot[-1][1],
                    coord_robot[-1][2], coord_robot[-1][3], fill = bot_color[1])
            coord_robot.remove(coord_robot[-1])
        elif bot == 2:
            canvas.delete(robots[bot])
            robots[bot] = canvas.create_oval(coord_robot[-1][0], coord_robot[-1][1],
                    coord_robot[-1][2], coord_robot[-1][3], fill = bot_color[2])
            coord_robot.remove(coord_robot[-1])
        elif bot == 3:
            canvas.delete(robots[bot])
            robots[bot] = canvas.create_oval(coord_robot[-1][0], coord_robot[-1][1],
                    coord_robot[-1][2], coord_robot[-1][3], fill = bot_color[3])
            coord_robot.remove(coord_robot[-1])
    else:
        pass

def save_score():
    pass

def show_best_score():
    pass

def restart():
    pass

#------------------------------------ Programme principal ------------------------------------#

root = tk.Tk()

# Creation des widgets
canvas = tk.Canvas(root,height=height, width=850)
bouton = tk.Button(root, text="Génération terrain")
cpt_move = tk.Label(root, text="Move = "+ str(cpt), font=("Marker Felt", 30))
b_undo = tk.Button(root, text='undo', command=undo, width=10, activebackground="grey")

# Placement des widgets
canvas.grid(columnspan=4, rowspan=6)
bouton.grid()
cpt_move.grid(column=3, row=0)
b_undo.grid(column=3, row=1)

grid()
generate()
show_robots()
show_target()
show_walls()

# Autre
canvas.bind("<1>", click)
canvas.bind_all("<Key>", keyboard)

root.mainloop()


def sauvegarde():
    fic = open("saverobot", "w")
    for i in range(4):
        print(type(pos_target[i]))
        print(type(robots[i]))
        fic.write(str(pos_target[i]) + "\n")
        fic.write(str(robots[i]) + "\n")

def load():
    fic = open("saverobot", "r")
    c = 0
    post = 0
    rob = 0
    for ligne in fic:
        if not c % 2:
            pos_target[post] = int(ligne)
            post += 1
        else :
            robots[rob] = int(ligne)
            rob += 1
        c += 1
