# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 16:01:35 2017

@author: x.jannin
"""

from PIL import ImageTk, Image
import numpy as np

from Filtre import iFiltre
from Seuillage import iSeuillage, iVariance, iEntropie

import tkMessageBox


class cImage:
    
    # Constructeur:
    def __init__(self, f=""):
        self.filename = f    # Nom du fichier
        
        self.pixels = None   # Matrice de pixels
        self.image = None    # Image PIL
        self.imageTk = None  # Image pour le canvas
        
        self.original_pixels = None # Matrice de pixels non modifié
        
        self.width = None   # Longueur de l'image
        self.height = None  # Largeur de l'image     
        
        self.open = False
        
    
    """
    Outils:
    """
    def ouvrir(self, name=""):
        if name!="":
            self.filename = name

        self.image = Image.open(self.filename)  # Charge l'image
        self.pixels = toPixels(self.image)      # image -> pixels
        self.original_pixels = np.copy(self.pixels)  # Copie
        self.imageTk = toImageTk(self.image)
        
        self.updateDim()  # Remplie self.width et self.height

        self.open = True
    
    def save(self, filename):
        self.image = toImage(self.pixels)
        if '.gif' not in filename: #.save(filename, 'gif') ne fonctionne pas
            filename += '.gif'  # Ajout de l'extension
        self.image.save(filename)
    
    def savePixels(self):
        self.original_pixels = self.pixels
    
    
    def update(self):
        self.image = toImage(self.pixels)     # pixels -> image
        self.imageTk = toImageTk(self.image)  # image  -> imageTk
        self.updateDim()
        
    def updateDim(self):  # Mise à jour des variables width et height
        s = np.shape(self.pixels)  # Récupère les dimensions de pixels
        self.width = s[1]
        self.height = s[0]
        
    def recharger(self):
        self.pixels = np.copy(self.original_pixels)
        
        
    """
    Transformations géometriques:
    """
    def rotation(self, a):
        # Conversion:
        image = toImage(self.pixels)  # pixels -> image
 
        # 'Rotation' des dimensions de l'image:
        r = int(a/45)
        if r in (1,2,5,6):
            image = image.transpose(Image.ROTATE_90)
            a+=90
        
        # Rotation :
        image = image.rotate(-a,expand=0)  # '-a' pour tourner dans le sens des aiguille d'une montre, 'expand=0': ne modifie pas les dimensions de l'image
        
        # Conversion:                    
        self.pixels = toPixels(image)  # image -> pixels
        
        self.updateDim()
        

    def symetrie(self, axe):
        if axe == 'Horizontale':
            self.pixels = np.flipud(self.pixels)
        elif axe == 'Verticale':
            self.pixels = np.fliplr(self.pixels)


    def negatif(self):
        # Parcours de chaque pixel de l'image:
        s = np.shape(self.pixels)
        for x in range(s[0]):
            for y in range(s[1]):
                self.pixels[x,y] = 255 - self.pixels[x,y]  # Inversion du niveau de gris
    
    
    """
    Filtres:
    """
    def filtre(self, filtre):
        self.pixels = iFiltre(self.pixels, filtre)

      
    """
    Seuillage:
    """
    def seuillage(self,t,s=128):
        if t=='Manuel':
            self.pixels = iSeuillage(self.pixels,s)
        elif t=='Variance':
            return self.variance()
        elif t=='Entropie':
            return self.entropie()
        elif t=='Nuees dynamiques':
            tkMessageBox.showerror('Error','Pas compris ! Veuillez Réexpliquer !')
        return s
    
    def variance(self):
        s = iVariance(self.pixels)
        self.pixels = iSeuillage(self.pixels,s)
        return s
    
    def entropie(self):
        s = iEntropie(self.pixels)
        self.pixels = iSeuillage(self.pixels,s)
        return s
       
        

"""
Convertisseurs:
"""
def toPixels(image):  # image -> pixels
    return np.array(image)

def toImage(pixels):  # pixels -> image
    return Image.fromarray(pixels)

def toImageTk(image): # image -> imageTk
    return ImageTk.PhotoImage(image)    
