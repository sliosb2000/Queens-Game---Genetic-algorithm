# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 08:44:29 2021

@author: SLIOSBERG Benjamin

Genetic Algorithms Problem : Place n Queens on a n² chess board without any being a danger to others.
The values and function names are written in French, the commentaries have been translated to English for a better understanding.
"""

import random
import numpy as np
import random as rd
import matplotlib.pyplot as plt 
                                            
dim_echequier = abs(int(input("Please enter the number of Queens needed "))) #defining the number n of Queens needed : the board is size n².

class individu:                                                              #definition of our individual, each one is a n size array composed of the y position of each Queen. 
    def __init__(self,val=None):
        if(val == None):
            self.val = random.sample(range(0, dim_echequier), dim_echequier)
        elif(type(val) is individu):          
            self.val = val.val
        else:
            self.val = val 
        self.nbConflits = self.fitness()
        
    def __str__(self):
        return str(self.val)
    def __len__(self):
        return len(self.val)
    
        
    def fitness(self):                                                      #The fitness function of this solution is counting the number of conflicts with the placement of each Queen.
        tableau = self.val                                                  #a conflict being defined as more than one Queen on each Row, Column or small diagonal of the n² board.
        matrice01 = np.zeros((dim_echequier,dim_echequier))
        for i in range(len(tableau)):
            matrice01[tableau[i],i] = 1                                     #creating a binary matrix to identify the Queens
        return nbConflits(tableau, matrice01)
        


def nbConflits(tableau,matrice01):                                          #function counting the number of conflicts of an individual (on a board)
    cpt = 0
                                                                            #counting of the rows conflicts  
    for i in range(dim_echequier):
        for j in range(i+1,dim_echequier):
            if(tableau[i]==tableau[j]):
                cpt+=1
    
                                                                            #counting of the diagonals conflicts 
    diags = [matrice01[::-1,:].diagonal(i) for i in range(-matrice01.shape[0]+1,matrice01.shape[1])]
    diags.extend(matrice01.diagonal(i) for i in range(matrice01.shape[1]-1,-matrice01.shape[0],-1))
    

    sommeDiagos = list(map(lambda x : sum(x)  ,diags))                      #we sum in an array the values of each diagonals : We optain the number of Queens on each one of them. 
      
    
                                                                            #checking the diagonals with more than 1 individual 
    for val in sommeDiagos:
        if(val>1):
            cpt+= val-1     #si on a 3 dames sur une diago : on marque 2 conflit 
    
    return cpt                                                              #returning the total count of conflicts of the individual.
        
def verif_Unicite(individu):                                                #checking if all the values of an individual is unique else the individual isn't valid.
    for i in range (len(individu.val)):                                     #function used when crossing individuals for genetic mixing.
        if(individu.val[i] in individu.val[i+1:]):
            return False
    return True
   
""" Genetic Algorithm part """    
meilleur_individu = individu()
generation = 0
                                                                            #creation of the population, fixing it at 50 individuals. (no tests have been run to find an optimal population 50 seemed appropriate) 
population = []
for i in range(50):
    population.append(individu())
    

while(meilleur_individu.fitness()>0):                                       #a solution to the Game of Queens is only found when no conflicts arise : nbConflicts <= 0
    
                                                                            #1 Crossover by generation, 2 individuals that can have 2 valid children with half there genetic code are chosen 
    k=0     
    while(k!=2):                                                            #while the number of valid children of the chosen individuals isn't 2
        indiv1 = rd.choice(population)                                      #2 random individuals I1 = [a1,a2,a3,a4], I2 = [b1,b2,b3,b4]
        indiv2 = rd.choice(population)
                                                                            #the children are then C1 = [a1,a2,b3,b4] and C2 = [b1,b2,a3,a4]
        enfant1 = individu(indiv1.val[:len(indiv1.val)//2]+ indiv2.val[len(indiv2.val)//2:]) 
        enfant2 = individu(indiv2.val[:len(indiv2.val)//2]+ indiv1.val[len(indiv1.val)//2:])
        
        if(verif_Unicite(enfant1)):                                         #Checking if the children are valid individuals
            k+=1
        if(verif_Unicite(enfant2)):
            k+=1
        
    population.append(enfant1)                                              #appending of the children and deletion of random individuals
    population.append(enfant2)
    population.remove(rd.choice(population))
    population.remove(rd.choice(population))
                                                                            #mutation of an individual
    indiv = rd.choice(population)
    a_effacer = indiv
    a = rd.randint(0,dim_echequier-1)
    b = rd.randint(0,dim_echequier-1)
    inter = indiv.val[a]
    indiv.val[a] = indiv.val[b]
    indiv.val[b] = inter
    
    population.remove(a_effacer)
    population.append(indiv)
    for i in range(len(population)):                                        #checking if a new best individual emerged during this generation
        if(individu(population[i]).fitness()<meilleur_individu.fitness()):
            meilleur_individu=population[i]
    
    generation+=1
    print("fitness of the best individual :",meilleur_individu.fitness()," ",meilleur_individu," generation n",generation)

print(meilleur_individu," done in",generation,"generations")     
                                                                            #Visualisation of the board and the best individual
tableau = meilleur_individu.val
matrice01 = np.zeros((dim_echequier,dim_echequier))
for i in range(len(tableau)):
    matrice01[tableau[i],i] = 1 

plt.imshow(matrice01, cmap='Greys')
ax = plt.gca()
ax.set_xticks(np.arange(-.5, dim_echequier, 1))
ax.set_yticks(np.arange(-.5, dim_echequier, 1))
ax.set_xticklabels(np.arange(0,dim_echequier+1,1))
ax.set_yticklabels(np.arange(0, dim_echequier+1, 1))
ax.grid(color='black', linestyle='-', linewidth=2)
plt.show()
