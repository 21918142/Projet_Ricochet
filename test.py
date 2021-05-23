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
from types import MethodWrapperType
from tkinter.filedialog import askopenfilename

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
high_score = 0
undocpt = 0

# Listes
coord_robotb = []
coord_robotr = []
coord_robotg = []
coord_roboty = []
coord_robot = [coord_robotb, coord_robotr, coord_robotg, coord_roboty]
coorddeplacement = []
coord_cible = []
bot_color = ['blue', 'red', 'green', 'yellow' ]

# Fonctions
#------------------------------------ Plateau ------------------------------------#
def grid():
    """Affiche un quadrillage sur le canvas"""
    for i in range(0, height, side):
        for j in range(0, width, side):
            color = "#D0CFD5"
            canvas.create_rectangle(i,j,i+side,j+side,fill=color,activefill="#928A99")
    for i in range(side*7, side*9, side):
        for j in range(side*7, side*9, side):
            color = "black"
            canvas.create_rectangle(i,j,i+side,j+side,fill=color,activefill="#928A99")
            
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
    x1, y1, x2, y2 = canvas.coords(blue)
    coord_robotb.append([x1, y1, x2, y2, 0])
    x = int(pos_robot[1][0])
    y = int(pos_robot[1][1])
    red = canvas.create_oval(x*side+5, y*side+5, x*side+35, y*side+35, fill = "red")
    u1, v1, u2, v2 = canvas.coords(red)
    coord_robotr.append([u1, v1, u2, v2, 1])
    x = int(pos_robot[2][0])
    y = int(pos_robot[2][1])
    green = canvas.create_oval(x*side+5, y*side+5, x*side+35, y*side+35, fill = "green")
    i1, j1, i2, j2 = canvas.coords(green)
    coord_robotg.append([i1, j1, i2, j2, 2])
    x = int(pos_robot[3][0])
    y = int(pos_robot[3][1])
    yellow = canvas.create_oval(x*side+5, y*side+5, x*side+35, y*side+35, fill = "yellow")
    n1, m1, n2, m2 = canvas.coords(yellow)
    coord_roboty.append([n1, m1, n2, m2, 3])
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
    x1, y1, x2 ,y2 = canvas.coords(target_b)
    coord_cible.append([x1, y1, x2, y2])
    u1, v1, u2 ,v2 = canvas.coords(target_r)
    coord_cible.append([u1, v1, u2, v2])
    i1, j1, i2 ,j2 = canvas.coords(target_g)
    coord_cible.append([i1, j1, i2, j2])
    n1, m1, n2 ,m2 = canvas.coords(target_y)
    coord_cible.append([n1, m1, n2, m2])
    pos_target.append(target_b)
    pos_target.append(target_r)
    pos_target.append(target_g)
    pos_target.append(target_y)

#------------------------------------ Déplacements ------------------------------------

def stop(robot,stop_x,stop_y):
    canvas.move(robot, stop_x, stop_y)
    return robot, stop_x, stop_y

def collision_blue():
    global undocpt
    global cpt
    coord = canvas.coords(robots[0])
    b = canvas.coords(pos_target[0])
    if coord[0]//40 == b[0]//40 and coord[1]//40 == b[1]//40:
        canvas.coords(pos_target[0], 16*side+10, 4*side+10, 16*side+30, 4*side+30)
        win()
        continues()
        cpt =0
        undocpt = 0
        cpt_move.config(text="Move = "+ str(cpt))
        
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
        stockage_coord()

def collision_red():
    global undocpt
    global cpt
    coord = canvas.coords(robots[1])
    r = canvas.coords(pos_target[1])
    if coord[0]//40 == r[0]//40 and coord[1]//40 == r[1]//40:
        canvas.coords(pos_target[1], 17*side+10, 4*side+10, 17*side+30, 4*side+30)
        win()
        continues()
        cpt = 0
        undoctp = 0
        cpt_move.config(text="Move = "+ str(cpt))
        
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
        stockage_coord()

def collision_green():
    global undocpt
    global cpt
    coord = canvas.coords(robots[2])
    g = canvas.coords(pos_target[2])
    if coord[0]//40 == g[0]//40 and coord[1]//40 == g[1]//40:
        canvas.coords(pos_target[2], 18*side+10, 4*side+10, 18*side+30, 4*side+30)
        win()
        continues()
        
        cpt = 0
        undocpt = 0
        cpt_move.config(text="Move = "+ str(cpt))
        
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
        stockage_coord()

def collision_yellow():
    global undocpt
    global cpt
    coord = canvas.coords(robots[3])
    y = canvas.coords(pos_target[3])
    if coord[0]//40 == y[0]//40 and coord[1]//40 == y[1]//40:
        canvas.coords(pos_target[3], 19*side+10, 4*side+10, 19*side+30, 4*side+30) 
        win()
        continues()
        
        cpt = 0
        undocpt = 0
        cpt_move.config(text="Move = "+ str(cpt))
        
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
        stockage_coord()

def click(event):
    global get_pos, bot
    """Permet d'effectuer le deplacement d'un robot quand on clique dessus et
       recommencer la partie quand on clique sur le carré au milieu"""
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
    
    elif 280 < event.x < 360 and 280 < event.y < 360:
        recommencer()

def keyboard(event):
    global dx, dy, cpt, undocpt
    key = event.keysym
    if key == "Up":
        
        dx = 0
        dy = -20
        cpt += 1
        undocpt += 1
        cpt_move.config(text="Move = "+ str(cpt))

    elif key == "Down":
        
        dx = 0
        dy = 20
        cpt += 1
        undocpt += 1
        cpt_move.config(text="Move = "+ str(cpt))
    
    elif key == "Left":
        
        dx = -20
        dy = 0
        cpt += 1
        undocpt += 1
        cpt_move.config(text="Move = "+ str(cpt))
    
    elif key == "Right":
       
        dx = 20
        dy = 0
        cpt += 1
        undocpt += 1 
        cpt_move.config(text="Move = "+ str(cpt))

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
def rules ():
    regles = askopenfilename(title="rules",filetypes=[('txt files','.txt'),('all files','.*')])
    fichier = open(regles, "r")
    content = fichier.read()
    fichier.close()
    tk.Label(root, text=content).grid(padx=5, pady=5)

def sauvegarde():
    """Permet de sauvegarder une partie en cours"""
    fic = open("saverobot", "w")
    for i in range(4):
        print(type(pos_target[i]))
        print(type(robots[i]))
        fic.write(str(pos_target[i]) + "\n")
        fic.write(str(robots[i]) + "\n")

def load():
    """Permet de recharger une partie sauvegardée"""
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

def stockage_coord():
    '''Stocke les coordonnées du robot'''
    global bot
    a, b, c, d = canvas.coords(robots[bot])
    coord_robot[bot].append([a, b, c, d, bot])
    coorddeplacement.append([a, b, c, d, bot])

def undo():
    """Permet d'annuler les derniers déplacements du robot"""
    global undocpt
    global cpt
    if undocpt > 0:
        quelbot = coorddeplacement[-1][4]
        coorddeplacement.remove(coorddeplacement[-1])
        coord_robot[quelbot].remove(coord_robot[quelbot][-1])
        canvas.coords(robots[quelbot], coord_robot[quelbot][-1][0], coord_robot[quelbot][-1][1], coord_robot[quelbot][-1][2], coord_robot[quelbot][-1][3])

def save_score_b():
    with open("score_blue.txt", "a") as file_score:
        file_score.write(str(cpt))
        file_score.write(" ")
                
def save_score_r():
    with open("score_red.txt", "a") as file_score:
        file_score.write(str(cpt))
        file_score.write(" ")

def save_score_g():
    with open("score_green.txt", "a") as file_score:
        file_score.write(str(cpt))
        file_score.write(" ") 

def save_score_y():
    with open("score_yellow.txt", "a") as file_score:
        file_score.write(str(cpt))
        file_score.write(" ")

def show_high_score():
    """Permet d'afficher les meilleurs scores"""
    global high_score
    with open("score_blue.txt", "r") as best_score:
        for scores in best_score:
            scores_rect = scores.split()
            high_score = max(scores_rect)
            print(high_score)

def recommencer():
    """Permet de redémarrer la partie au début"""
    cpt = 0
    
    cpt_move.config(text="Move = "+ str(cpt))
    for i in range(4):
        while len(coord_robot[i]) > 1:
            coord_robot[i].remove(coord_robot[i][-1])
        canvas.coords(robots[i], coord_robot[i][0][0], coord_robot[i][0][1], coord_robot[i][0][2], coord_robot[i][0][3])
    for i in range(4):
        canvas.coords(pos_target[i], coord_cible[i][0], coord_cible[i][1], coord_cible[i][2], coord_cible[i][3])

#------------------------------------ Programme principal ------------------------------------#
root = tk.Tk()

canvas = tk.Canvas(root,height=height, width=640)
cpt_move = tk.Label(root, padx= 58, pady=5, bd = 8, fg = '#928A99', bg = "#D0CFD5", font = ('consolas', 30), text="Move = "+ str(cpt), )
b_undo = tk.Button(root, padx = 58, pady= 5, bd = 8, fg= '#928A99', font = ('consolas', 30), text='Undo', bg = "#D0CFD5", command=undo)
bttn_rules = tk.Button(root, padx = 58, pady = 5, bd = 8, fg = '#928A99', font = ('consolas', 30), text = 'Rules', bg = "#D0CFD5", command =rules)
bttn_load = tk.Button(root, padx = 58, pady = 5, bd = 8,fg = '#928A99', font = ('consolas', 30), text = 'Load', bg = "#D0CFD5", command = load)
#bttn_save = tk.Button(root, padx = 58, pady = 5, bd = 8, fg = '#D1D5E0', font = ('consolas', 30), text = 'Save', bg = "black", command = save_score)
bttn_best_score = tk.Button(root, padx = 58, pady = 5, bd = 8, fg = '#928A99', font = ('consolas', 30), text = 'High Score', bg = "#D0CFD5", command = show_high_score )


# Placement des widgets
canvas.grid(columnspan=4, rowspan=6)
cpt_move.grid(column=4, row=0)
b_undo.grid(column=4, row=1)
bttn_rules.grid(column =4, row = 2)
bttn_load.grid(column =4, row = 3)
#bttn_save.grid(column=4, row= 4)
bttn_best_score.grid(column=4, row=5)
#fonctions boutons 
grid()
generate()
show_robots()
show_target()
show_walls()

# Autre
canvas.bind("<1>", click)
canvas.bind_all("<Key>", keyboard)

root.mainloop()

# Fin du programme