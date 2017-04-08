# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 21:12:34 2017

@author: Xavier
"""

import numpy as np
import matplotlib.pyplot as plt


#TODO: iVariance et iEntropie renvoie la  valeur de seuillage

def iSeuillage(image, s):
    image = image.copy()  # Pour ne pas modifier l'image d'origine
    shape = np.shape(image)
    for x in range(shape[0]):
        for y in range(shape[1]):
            if(image[x,y]<s): image[x,y]=0  # Classe 0
            else: image[x,y]=255            # Classe 1
    
    return image


def iVariance(image):
    
    h = histo(image)
    
    s, n = int(256/2), 0
    while n<8:  #Maximum 8 boucles
        Ms_0, Ms_1 = moyennes(s,h)[2:]
        
        m = int((Ms_0 + Ms_1)/2)    # Milieu de Ms_0 et Ms_1
        
        if s == m: break
        s = m
        
        n+=1
    
    return iSeuillage(image,s) #,s


def iEntropie(image):
    
    h = histo(image)

    Emax,s_max = 0,0
    for s in range(256):
        E = entropie(s,h)
        
        if E > Emax:
            Emax = E
            s_max = s
    
    return iSeuillage(image,s_max)    #,s_max
        
def entropie(s,h): # Calcul de l'entropie pour s
    
    Ns_0, Ns_1 = moyennes(s, h)[:2]
    
    E_0 = 0    
    for i in h[:s+1]:
        if i == 0: continue
        e = i / Ns_0
        E_0 += e * np.log10(e)
        
    E_1 = 0
    for i in h[s+1:]:
        if i == 0: continue     
        e = i / Ns_1
        E_1 += e * np.log10(e) 
    
    E = -E_0 - E_1

    return E    


def histo(image):
    
    histo = np.zeros(256)
    
    shape = np.shape(image)
    for x in range(shape[0]):
        for y in range(shape[1]):
            i = image[x,y]
            histo[i] += 1
    
    return histo

def moyennes(s, h):
    
    # Nombres de pixels de chaque classe:
    Ns_0 = np.sum(h[:s+1])
    Ns_1 = np.sum(h[s+1:])

    # Moyennes:
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