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
import time
from tkinter.filedialog import askopenfilename
import pickle
from types import MethodWrapperType

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
dx, dy = 0, 0

cpt = 0
bot = 0
undocpt = 0

obstacle = []

high_score_b, high_score_r, high_score_g, high_score_y = 0, 0, 0, 0

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
            rectancle = canvas.create_rectangle(i,j,i+side,j+side,fill=color,activefill="#928A99")
            obstacle.append(rectancle)
            
def generate():
    """Affiche walls + pos target + pos robot"""
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
                line1 = canvas.create_line(i//2*side, j*side, (i//2+1)*side, j*side, fill="black", width=5)
                obstacle.append(line1)

            if table[i][j] == "1": # |
                line2 = canvas.create_line(i//2*side, j*side, i//2*side, (j+1)*side, fill="black", width=5)
                obstacle.append(line2)

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

def collision():
    global undocpt
    global cpt
    global bot

    coord = canvas.coords(robots[bot])
    b = canvas.coords(pos_target[bot])
    if coord[0]//40 == b[0]//40 and coord[1]//40 == b[1]//40:
        canvas.coords(pos_target[bot], (16 + bot)*side+10, 15*side+10, (16 + bot)*side+30, 15*side+30)
        win()
        continues()
        if robots[bot] == robots[0]:
            save_score_b()
            cpt = 0
            cpt_move.config(text="Move = "+ str(cpt))
        if robots[bot] == robots[1]:
            save_score_r()
            cpt = 0
            cpt_move.config(text="Move = "+ str(cpt))
        if robots[bot] == robots[2]:
            save_score_g()
            cpt = 0
            cpt_move.config(text="Move = "+ str(cpt))
        if robots[bot] == robots[3]:
            save_score_y()
            cpt = 0
            cpt_move.config(text="Move = "+ str(cpt))
        cpt = 0
        undocpt = 0
        cpt_move.config(text="Move = "+ str(cpt))
    for i in range(4):
        temp = []
        if i == bot:
            pass
        else:
            temp.append(robots[i])
            obstacle.append(robots[i])
    c = canvas.find_overlapping(*coord)  
    for id in c:
        color = canvas.itemcget(id, "fill")
        if id not in pos_target:
            if robots[bot] == robots[0]:
                if color == "red" or color == "black" or color =="green" or color=="yellow":
                    return True
            elif robots[bot] == robots[1]:
                if color == "blue" or color == "black" or color =="green" or color=="yellow":
                    return True
            elif robots[bot] == robots[2]:
                if color == "blue" or color == "black" or color =="red" or color=="yellow":
                    return True
            elif robots[bot] == robots[3]:
                if color == "blue" or color == "black" or color =="green" or color=="red":
                    return True
            
def move(): 
    global dx,dy, bot, cpt, undocpt

    canvas.move(robots[bot], dx, dy)
    canvas.after(5, move)
    
    if collision():
        stop(robots[bot], -dx, -dy)
        dx = 0
        dy = 0
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
        bot = 0

    elif get_pos == (u1//40, v1//40):
        bot = 1

    elif get_pos == (i1//40, j1//40):
        bot = 2
        
    elif get_pos == (n1//40, m1//40):
        bot = 3

    elif 280 < event.x < 360 and 280 < event.y < 360:
        recommencer()
  
def keyboard(event):
    """Permet d'effectuer les déplacemenets du robot en utilisant les flèches du clavier"""
    global bot, cpt, undocpt, dx, dy
    key = event.keysym
    if key == "Up":
        
        dx = 0
        dy = -20
        
        cpt += 1
        undocpt += 1
        cpt_move.config(text="Move = "+ str(cpt))
        move()

    elif key == "Down":
        
        dx = 0
        dy = 20
        cpt += 1
        undocpt += 1
        cpt_move.config(text="Move = "+ str(cpt))
        
        move()
        
    elif key == "Left":
        
        dx = -20
        dy = 0
        cpt += 1
        undocpt += 1
        cpt_move.config(text="Move = "+ str(cpt))
        
        move()
    elif key == "Right":
       
        dx = 20
        dy = 0
        cpt += 1
        undocpt += 1 
        cpt_move.config(text="Move = "+ str(cpt))
        
        move()

#------------------------------------ Message ------------------------------------#

def win():
    """Affiche un message lorsque le joueur a gagné"""
    tkm.showinfo("Congratulations", "Great job !\nMove: "+ str(cpt))

def continues():
    """Demande au joueur s'il veut continuer de jouer"""
    message = tkm.askquestion("Continue", "Continue to play ?")
    if message == "yes":
        pass # save score
    if message == "no":
        root.destroy()

#------------------------------------ Autre ------------------------------------#

def sauvegarde():
    with open("saverobot", "wb") as f:
        cb = canvas.coords(robots[0])
        cr = canvas.coords(robots[1])
        cg = canvas.coords(robots[2])
        cy = canvas.coords(robots[3])
        save = [cb,cr,cg,cy]
        pickle.dump(save, f)

def load():
    global robots
    with open("saverobot", "rb") as f:
        save = pickle.load(f)

        bleu = save[0]
        canvas.delete(robots[0])
        robots[0] = canvas.create_oval(bleu[0],bleu[1],bleu[2],bleu[3], fill = "blue")

        rouge = save[1]
        canvas.delete(robots[1])
        robots[1] = canvas.create_oval(rouge[0],rouge[1],rouge[2],rouge[3], fill="red")

        vert = save[2]
        canvas.delete(robots[2])
        robots[2] = canvas.create_oval(vert[0],vert[1],vert[2],vert[3], fill="green")

        jaune = save[3]
        canvas.delete(robots[3])
        robots[3] = canvas.create_oval(jaune[0],jaune[1],jaune[2],jaune[3],fill="yellow")

def save_score_b():
    """Sauvegarde du score du robot bleu"""
    with open("score_blue.txt", "a") as file_score:
        file_score.write(str(cpt) + " ")

def save_score_r():
    """Sauvegarde du score du robot rouge"""
    with open("score_red.txt", "a") as file_score:
        file_score.write(str(cpt) + " ")

def save_score_g():
    """Sauvegarde du score du robot vert"""
    with open("score_green.txt", "a") as file_score:
        file_score.write(str(cpt) + " ")

def save_score_y():
    """Sauvegarde du score du robot jaune"""
    with open("score_yellow.txt", "a") as file_score:
        file_score.write(str(cpt) + " ")

def show_high_score():
    """Permet d'afficher le meilleur score pour chaque robot"""
    global high_score_b, high_score_r, high_score_g, high_score_y
    with open("score_blue.txt", "r") as best_score:
        for scores in best_score:
            scores_rect = scores.split()
            high_score_b = min(scores_rect)
    with open("score_red.txt", "r") as best_score:
        for scores in best_score:
            scores_rect = scores.split()
            high_score_r = min(scores_rect)
    with open("score_green.txt", "r") as best_score:
        for scores in best_score:
            scores_rect = scores.split()
            high_score_g = min(scores_rect)
    with open("score_blue.txt", "r") as best_score:
        for scores in best_score:
            scores_rect = scores.split()
            high_score_y = min(scores_rect)

    root2 = tk.Tk()
    root2.title("High Score")
    score_bleu = tk.Label(root2, text = "Best score : " + str(high_score_b), fg = "blue",)
    score_red = tk.Label(root2, text = "Best score : " + str(high_score_r), fg = "red")
    score_green = tk.Label(root2, text = "Best score : " + str(high_score_g), fg = "green")
    score_yellow = tk.Label(root2, text = "Best score : " + str(high_score_y), fg = "#FFD700")
    score_bleu.pack()
    score_red.pack()
    score_green.pack()
    score_yellow.pack()
    root2.mainloop

def stockage_coord():
    '''Stocke les coordonnées du robot'''
    global bot, cpt, undocpt
    

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
        undocpt -= 1

def recommencer():
    """Permet de redémarrer la partie depuis le début"""
    cpt = 0
    
    cpt_move.config(text="Move = "+ str(cpt))
    for i in range(4):
        while len(coord_robot[i]) > 1:
            coord_robot[i].remove(coord_robot[i][-1])
        canvas.coords(robots[i], coord_robot[i][0][0], coord_robot[i][0][1], coord_robot[i][0][2], coord_robot[i][0][3])
    for i in range(4):
        canvas.coords(pos_target[i], coord_cible[i][0], coord_cible[i][1], coord_cible[i][2], coord_cible[i][3])

def rules():
    """Permet de charger les règles du jeu"""
    regles = askopenfilename(title="rules",filetypes=[('txt files','.txt'),('all files','.*')])
    fichier = open(regles, "r")
    content = fichier.read()
    fichier.close()
    tk.Label(root, text=content).grid(padx=5, pady=5)

#------------------------------------ Programme principal ------------------------------------#

root = tk.Tk()
root.title("Ricochet Robots")

# Creation des widgets
canvas = tk.Canvas(root,height=height, width=850)
cpt_move = tk.Label(root, text="Move = "+ str(cpt), font=("Marker Felt", 15))
bouton_undo = tk.Button(root, text='Undo', command=undo, width=15, height=3, activebackground="grey", relief='raised', borderwidth=6)
bouton_save = tk.Button(root, text='Save', command=sauvegarde, width=15, height=3, activebackground="grey", relief='raised', borderwidth=6)
bouton_load = tk.Button(root, text='Load', command=load, width=15, height=3, activebackground="grey", relief='raised', borderwidth=6)
bouton_b_score = tk.Button(root, text = 'High Score', command =show_high_score, width=15, height=3, activebackground="grey", relief='raised', borderwidth=6)
bouton_rules = tk.Button(root, text = 'Rules', command =rules, width=15, height=3, activebackground="grey", relief='raised', borderwidth=6)

# Placement des widgets
canvas.grid(columnspan=4, rowspan=6)
cpt_move.grid(column=3, row=0)
bouton_undo.grid(column=3, row=1)
bouton_save.grid(column=3, row=2)
bouton_load.grid(column=3, row=3)
bouton_b_score.grid(column=3, row=4)
bouton_rules.grid(column =1, row = 5)

grid()
generate()
show_robots()
show_target()
show_walls()

# Autre
canvas.bind("<1>", click)
canvas.bind_all("<Key>", keyboard)


root.mainloop()