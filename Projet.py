# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 20:43:38 2017

@author: Xavier
"""

#import tkinter as Tk
#from tkinter import filedialog
import Tkinter as Tk
import tkFileDialog as filedialog

from Image import cImage

# Image:
image = cImage()

    
def ouvrirNewImage():
    # Demande le chemin d'accès du fichier:
    filename = filedialog.askopenfilename(filetypes=[('CompuServer GIF','*.gif')])
    
    # Charge l'image et l'affichage:
    ouvrir(filename)

def ouvrir(filename=''):  # Recharge l'image si filename=''
    # Charge l'image:
    image.ouvrir(filename)
    
    # Affiche l'image:
    updateImage()
    
    # Initialisation des outils:
    initTools()
    
    # Adapte les dimensions du canvas à l'image:
    canvas.config(width=image.width, height=image.height)

      
def saveImage():
    # Demande le nom du fichier:
    filename = filedialog.asksaveasfilename(filetypes=[('CompuServer GIF','*.gif')]) 
    
    # Enregistre l'image:
    image.save(filename) 

   
def updateImage():
    # Affiche l'image dans le canvas:
    canvas.config(width=image.width, height=image.height)
    canvas.itemconfig(canvasImage, image = image.imageTk)


# Applique les outils sur l'image :
def outils():
    # S'il n'y a pas d'image chargée:
    if image.open == False: return
    
    # Récupère les valeurs de chaque Checkbutton:
    check = []
    for i in ('symetrie','rotation','negatif','filtre', 'seuillage'): 
        check.append(checkButtons[i].get())
    
    # Charge l'image non modifiée;
    image.recharger()
    
    # Applique les outils sur l'image, si les Checkboxs sont cochées :
    if check[0]==1: image.symetrie(var_symetrie.get())  # Symétrie
    if check[1]==1: image.rotation(int(angle.get()))    # Rotation
    if check[2]==1: image.negatif()                     # Inversion des Niveaux de Gris
    if check[3]==1: image.filtre(var_filtre.get())      # Filtre
    if check[4]==1: # Seuillage
        seuil.set(image.seuillage(var_seuillage.get(), s = seuil.get()%255))
    seuilUpdate()  # Affichage de l'outil 'Seuillage'
    
    # Affichage de l'image dans le canvas:
    image.update()
    updateImage()

def initTools():  # Initialisation des outils
    for key in checkButtons.keys():  # Décochage des Checkbuttons
        checkButtons[key].set(0)
    angle.set(0)


def validate():
    # Enregistre les modifications:
    image.savePixels()
    
    # Initialisation des outils:
    initTools()
 

def rotate_plus(): # Ajoute +90 à l'angle de rotation
    a = int(angle.get()) + 90
    if a>=360: a-=360
    angle.set(str(a))
    outils()
    
def rotate_min(): # Ajoute -90 à l'angle de rotation
    a = int(angle.get()) - 90
    if a<0: a+=360
    angle.set(str(a))
    outils()

def seuilUpdate():  # Adapte l'affichage en fonction de l'option choisie
    fen.focus()  # Enlève le cursor de Spinbox 
    if var_seuillage.get() == 'Manuel':
        button_seuil.pack(padx=(5,0))
        box_seuil.config(state='normal')
    else:
        button_seuil.pack_forget()
        box_seuil.config(state='disabled')



fen = Tk.Tk()
fen.title('Projet informatique')


"""
Menu:
"""
menu = Tk.Menu(fen)

fichier = Tk.Menu(menu, tearoff=0)
fichier.add_command(label='Ouvrir une image', command=ouvrirNewImage)
fichier.add_separator()
fichier.add_command(label='Recharger l\'image', command=ouvrir)
fichier.add_command(label='Enregistrer la nouvelle image', command=saveImage)

menu.add_cascade(label='Fichier', menu=fichier)

fen.config(menu=menu)


"""
Outils
"""
frame_tools = Tk.Frame(fen)

space = 8   # Espace entre les widgets
checkButtons = {} # Dictionnaire pour récupérer les états des Checkbox 


'''
Symetrie:
'''
frame_symetrie = Tk.Frame(frame_tools)

# Checkbutton:
checkButtons['symetrie'] = Tk.IntVar()
check_symetrie = Tk.Checkbutton(frame_symetrie, text='Symetrie :', variable=checkButtons['symetrie'], command=outils)
check_symetrie.pack(anchor='w')

# Menu deroulant :
var_symetrie = Tk.StringVar()
var_symetrie.set('Verticale')
list_symetrie = Tk.OptionMenu(frame_symetrie, var_symetrie, 'Horizontale','Verticale', command=lambda x: outils())  # 'command = lambda...' car 'command=outils' donne un paramètre inutile
list_symetrie.pack(padx=(15,5))

frame_symetrie.grid(row=0, pady=space, sticky='w')


'''
Rotation:
'''
frame_rotation = Tk.Frame(frame_tools)

# Checkbutton:
checkButtons['rotation'] = Tk.IntVar()
check_rotation = Tk.Checkbutton(frame_rotation, text='Rotation :', variable=checkButtons['rotation'], command=outils)
check_rotation.pack(anchor='w')

# Boutons:
frame_angle = Tk.Frame(frame_rotation)

angle = Tk.IntVar()
box_angle = Tk.Spinbox(frame_angle,textvariable=angle, from_=0, to=359, width=3, wrap=True, command=outils,state="readonly")
box_angle.pack(side='left')

button_rotate_plus = Tk.Button(frame_angle, text='+90°', command=rotate_plus)
button_rotate_plus.pack(side='left', padx=5)

button_rotate_min = Tk.Button(frame_angle, text='-90°', command=rotate_min)
button_rotate_min.pack(side='left')

frame_angle.pack(padx=(10,5))


frame_rotation.grid(row=1, pady=space, sticky='w')


'''
Inversion de couleur:
'''
# Checkbutton:
checkButtons['negatif'] = Tk.IntVar()
check_negatif = Tk.Checkbutton(frame_tools, text='Inversion de couleur', variable=checkButtons['negatif'], command=outils)
check_negatif.grid(row=2, sticky='w', pady=space)


'''
Filtre:
'''
frame_filtre = Tk.Frame(frame_tools)

# Checkbutton:
checkButtons['filtre'] = Tk.IntVar()
check_filtre = Tk.Checkbutton(frame_filtre, text='Filtre :', variable=checkButtons['filtre'], command=outils)
check_filtre.pack(anchor='w')

# Menu deroulant :
var_filtre = Tk.StringVar()
var_filtre.set('Moyen')
list_filtre = Tk.OptionMenu(frame_filtre, var_filtre, 'Moyen','Gaussien','Prewitt |','Prewitt -','Laplacien', command=lambda x: outils())  # 'command = lambda...' car 'command=outils' donne un paramètre inutile
list_filtre.pack(padx=(15,5))


frame_filtre.grid(row=3, sticky='w', pady=space)


'''
Seuillage:
'''
frame_seuillage = Tk.Frame(frame_tools)

# Checkbutton:
checkButtons['seuillage'] = Tk.IntVar()
check_filtre = Tk.Checkbutton(frame_seuillage, text='Seuillage :', variable=checkButtons['seuillage'], command=outils)
check_filtre.pack(anchor='w')

# Menu deroulant :
var_seuillage = Tk.StringVar()
var_seuillage.set('Manuel')
list_seuillage = Tk.OptionMenu(frame_seuillage, var_seuillage, 'Manuel','Variance','Entropie', 'Nuees dynamiques', command=lambda x: outils())  # 'command = lambda...' car 'command=outils' donne un paramètre inutile
list_seuillage.pack(padx=(15,5))

frame_seuil = Tk.Frame(frame_seuillage)
# Spinbox:
seuil = Tk.IntVar()
box_seuil = Tk.Spinbox(frame_seuil,textvariable=seuil, from_=0, to=255, width=3, wrap=True)
box_seuil.pack(side='left')
# Bouton 'ok':
button_seuil = Tk.Button(frame_seuil, text='ok', command=outils)
button_seuil.pack(side='left', padx=(5,0))

frame_seuil.pack(padx=(10,0),pady=(2,0))

frame_seuillage.grid(row=4, sticky='w', pady=space)


'''
Validate:
'''
button_validate = Tk.Button(frame_tools, text='Valider', command=validate)
button_validate.grid(row=5, pady=(20,0))


frame_tools.pack(side='left', padx=10)


"""
Canvas:
"""
canvas = Tk.Canvas(fen, width=400, height=400, bg='white')
canvasImage = canvas.create_image(0,0, anchor='nw')
canvas.pack()


# Charge l'image de démarrage:
ouvrir('ImageNiveauGris.gif')


fen.mainloop()


