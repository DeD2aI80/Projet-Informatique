# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 21:12:34 2017

@author: Xavier
"""

import numpy as np
import matplotlib.pyplot as plt


def iSeuillage(image, s):
    image = image.copy()  # Pour ne pas modifier l'image d'origine
    
    # Parcours chaque pixel de l'image:                
    shape = np.shape(image)
    for x in range(shape[0]):
        for y in range(shape[1]):         
            # Change la valeur du pixel:
            if(image[x,y]<s): image[x,y]=0  # Classe 0
            else: image[x,y]=255            # Classe 1
    
    return image


def iVariance(image):
    
    # Histogramme de l'image:
    h = histo(image)
    
    # Initialisation:    
    s, n = int(256/2), 0  # Valeur de s de départ, compteur
              
    while n<8:  # Maximum 8 boucles
        # Moyennes pondérées:
        Ms_0, Ms_1 = moyennes(s,h)[2:]
        
        # Milieu de Ms_0 et Ms_1:
        m = int((Ms_0 + Ms_1)/2)  
        
        if s == m: break  # Si variance trouvée
        s = m             # Sinon
        
        n+=1  # Incrémente le compteur
    
    return s


def iEntropie(image):
    
    # Histogramme de l'image:
    h = histo(image)  
    
    # Initialisation:
    Emax,s_max = 0,0  # Couple du maximum de l'entropie
    
    # Pour chaque nuance de gris:
    for s in range(256):
        # Calcul de l'entropie pour s:
        E = entropie(s,h)
        
        # Compare à l'entropie maximum:
        if E > Emax:
            Emax = E
            s_max = s
    
    return s_max
        
def entropie(s,h):  # Calcul de l'entropie pour s
    
    # Nombre de pixels de chaque classe:
    Ns_0, Ns_1 = moyennes(s, h)[:2]
    
    # Entropie de la classe 0:
    E_0 = 0    
    for i in h[:s+1]:
        if i == 0: continue
        e = i / Ns_0
        E_0 += e * np.log10(e)
    
    # Entropie de la classe 1:
    E_1 = 0
    for i in h[s+1:]:
        if i == 0: continue     
        e = i / Ns_1
        E_1 += e * np.log10(e) 
    
    # 'Somme' des entropies:
    E = -E_0 - E_1

    return E    


def histo(image):
    
    # Initialisation:
    histo = np.zeros(256)  # Liste de compteurs pour chaque nuance de gris
    
    # Parcours chaque pixel de l'image:
    shape = np.shape(image)
    for x in range(shape[0]):
        for y in range(shape[1]):
            i = int(image[x,y])  # Récupère la valeur du pixel
            histo[i] += 1        # Incrémente le compteur de valeur i 
    
    return histo

def moyennes(s, h):
    
    # Nombres de pixels de chaque classe:
    Ns_0 = np.sum(h[:s+1])
    Ns_1 = np.sum(h[s+1:])

    # Moyennes pondérées:
    Ms_0 = 0
    if Ns_0 != 0:
        Ms_0 = sum([i*h[i] for i in range(s+1)]) / Ns_0 

    Ms_1 = 255    
    if Ns_1 != 0: 
        Ms_1 = sum([i*h[i] for i in range(s+1,256)]) / Ns_1 

    return int(Ns_0), int(Ns_1), int(Ms_0), int(Ms_1)



"""
im = np.array([[12,145,140,8],
              [65,135,139,124],
              [5,69,12,31],
              [2,1,241,226]])

print(im)

e = iEntropie(im)

print(e)

"""

"""
i = np.random.randint(256, size=(50, 50))

e = iEntropie(i)
v = iVariance(i)

ie = iSeuillage(i,e)
iv = iSeuillage(i,v)

print(e,v)

plt.imshow(i, cmap=plt.cm.gray)
plt.show()

plt.imshow(ie, cmap=plt.cm.gray)
plt.show()
plt.imshow(iv, cmap=plt.cm.gray)
plt.show()

"""