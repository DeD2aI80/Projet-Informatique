# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 22:33:43 2017

@author: Xavier
"""

import numpy as np
import matplotlib.pyplot as plt
 

filtres = {
    'Moyen': np.full((3,3), 1./9),
    'Gaussien': np.array([[ 0, 1/8, 0],
                          [1/8,4/8,1/8],
                          [ 0, 1/8, 0]], dtype=np.float64),
    'Prewitt |': np.array([[-1,0,1],
                         [-1,0,1],
                         [-1,0,1]], dtype=np.float64),
    'Prewitt -': np.array([[ 1, 1, 1],
                          [ 0, 0, 0],
                          [-1,-1,-1]], dtype=np.float64),
    'Laplacien': np.array([[-1,-1,-1],
                           [-1, 8,-1],
                           [-1,-1,-1]], dtype=np.float64)
}   


def iFiltre(image, filtre):
    
    # Formes des images:
    image_shape = np.shape(image)
    newImage_shape = (image_shape[0]-2,image_shape[1]-2)

    # Nouvelle image vide (sans bord):
    newImage = np.zeros(newImage_shape)
    
    # Filtre:
    filtre = filtres[filtre]
    
    # Parcours les pixels de newImage
    for row in range(0,newImage_shape[0]):
        for col in range(0,newImage_shape[1]):
            
            #Matrice des voisins:
            pixels = image[row:row+3,col:col+3]
            
            # Calcul du nouveau pixel :
            m = np.multiply(pixels, filtre)  # multiplie les éléments 1 à 1 des 2 matrices
            pixel = abs(int(np.sum(m)))
            
            # Ajout du pixel dans la nouvelle image
            newImage[row,col] = np.clip(pixel, 0, 255)  # 0 <= int(pixel) <= 255 
    
    return newImage


"""
image = np.random.randint(256,size = (100, 100))

i = iFiltre(image, 'moyen')
#i = iFiltre(image, 'prewitt |')

plt.imshow(image, cmap=plt.cm.gray)
plt.show()

plt.imshow(i, cmap=plt.cm.gray)
plt.show()
"""


