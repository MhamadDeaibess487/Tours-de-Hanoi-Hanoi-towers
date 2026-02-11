# Binome : Mhamad Deaibess et Karim Hammoud
#Partie A
#1
def decroissant(n): #fonction pour utiliser dans init(n)
    liste = []
    for disques in range(n,0,-1):
        liste.append(disques)
    return liste





def init(n):
    source = decroissant(n)
    auxiliaire = []
    destination = []
    plateau = [source,auxiliaire,destination]
    return plateau

#2
def nbDisques(plateau, numtour):
    if numtour<0 or numtour>2:
        return "Error"
    else :
        return len(plateau[numtour])
    
#3
def disqueSup(plateau, numtour) :
    x = nbDisques(plateau,numtour)
    if x == 0 :
        return -1
    return min(plateau[numtour])

#4
def posDisque(plateau, numdisque):
    n = int(input("ENtrez le nombre total de disque"))
    if numdisque>=1 and numdisque<=n:
        if numdisque in plateau[0]:
            return 0
        if numdisque in plateau[1]:
            return 1
        return 2
    return -1

#5
def verifDepl(plateau, nt1, nt2):
    x = disqueSup(plateau,nt1)
    y = disqueSup(plateau,nt2)
    if x<y or (nbDisques(plateau,nt2)==0 and nbDisques(plateau,nt1)!=0):
        return True
    return False

#6
def verifVictoire(plateau, n) :
    x = decroissant(n)
    if plateau == [[],[],x]:
        return True
    return False


#Partie B
#1
from turtle import *
xplateau = -300
yplateau = -200
def dimension_du_plus_grand_disque(n): #fonction pour determiner une dimension du disque pour le dessiner
    dimension = 40
    for i in range(1,n+1):
        dimension +=30
    return dimension



def base(n):
    x = dimension_du_plus_grand_disque(n)
    for i in range(0,2):
        forward(30 + x + 20 + x + 20 + x +30)
        right(90)
        forward(n*2)
        right(90)
        
def tour(n):
    x = dimension_du_plus_grand_disque(n)
    hauteur = (n+1)*30
    epaisseur = n+(n*0.3)
    xtour1 = 30 + x/2
    xtour2 =  x + 20 + xtour1 
    xtour3 = xtour2 + x/2 + 20 + x/2
    liste_x = [xplateau + xtour1,xplateau + xtour2,xplateau + xtour3]
    for i in range (0,3):
        penup()
        goto(liste_x[i] + epaisseur,yplateau)
        pendown()
        left(90)
        forward(hauteur)
        left(90)
        forward(epaisseur)
        left(90)
        forward(hauteur)
        left(90)
        
def dessinePlateau(n):
    speed(11)
    penup()
    goto(xplateau,yplateau)
    pendown()
    base(n)
    tour(n)
    speed(3)
    
#2
def dimension_disque(n,nd):
    x = dimension_du_plus_grand_disque(n)
    for i in range (n,nd,-1) :
        x -=30
    return(x)


def dessineDisque(nd, plateau, n):
    dimension = dimension_disque(n,nd)
    x = dimension_du_plus_grand_disque(n)

    if nd in plateau[0]:
            a = plateau[0].index(nd)
            x1 = -300 +30+ x/2 - dimension/2 + (n+(n*0.3))/2
            y1 = -200 + 30*(a)
            penup()
            goto(x1,y1)
            pendown()
            for i in range(0,2):
                forward(dimension_disque(n,nd))
                left(90)
                forward(30)
                left(90)
            
    elif nd in plateau[1]:
            a = plateau[1].index(nd)  
            x2 = -300 + 30 + x + 20 +x/2 - dimension/2 + (n+(n*0.3))/2
            y2 = -200 + 30*(a)
            penup()
            goto(x2,y2)
            pendown()
            for i in range(0,2):
                forward(dimension_disque(n,nd))
                left(90)
                forward(30)
                left(90)
            
    elif nd in plateau[2]:
            a = plateau[2].index(nd)
            x3 = -300 + 30 + x + 20 + x +20+x/2 - dimension/2 + (n+(n*0.3))/2
            y3 = -200 + 30*(a)
            penup()
            goto(x3,y3)
            pendown()
            for i in range(0,2):
                forward(dimension_disque(n,nd))
                left(90)
                forward(30)
                left(90)
    
            
    

#3
def effaceDisque(nd, plateau, n) :
    pencolor("white")
    dessineDisque(nd, plateau, n)
    pencolor("black")
    dessinePlateau(n)
   
    
#4
def dessineConfig(plateau, n) :
    for tour in plateau:
        for disque in tour:
            dessineDisque(disque,plateau,n)
            
            
#5
def efface_tout(plateau, n) :
    pencolor("white")
    dessinePlateau(n)
    for tour in plateau:
        for disque in tour:
            dessineDisque(disque,plateau,n)
    pencolor("black")
    

#partie C
#1
def lireCoords(plateau) :
    possible=True 
    while True :
        tour_depart = int(input("numero du tour de depart?"))
        while tour_depart > 2 or tour_depart < 0 or len(plateau[tour_depart]) == 0  :
            tour_depart = int(input("invalide tour,entrez un nouveau tour depart :"))
        if len(plateau[tour_depart]) != 0 :
                save = min(plateau[tour_depart])
            
        tour_arrivee = int(input("numero du tour de destination?"))
        while tour_arrivee > 2 or tour_arrivee < 0 :
            tour_arrivee = int(input("invalide tour, entrez un nombre de tour de destination:"))
        if len(plateau[tour_arrivee]) != 0 :
                save1 = min(plateau[tour_arrivee]) 
                
        if len(plateau[tour_arrivee])== 0 or save<save1 :
            possible = False
            return tour_depart,tour_arrivee
            
        else :
            print("Invalide, tour vide")
            possible = True
        
        
        
        

       
#2
def jouerUnCoup(plateau,n) :
    tour_depart,tour_arrivee = lireCoords(plateau) 
    print(f"tu deplace de {tour_depart} au {tour_arrivee}")
    speed(11)
    dessinePlateau(n)
    speed(11)
    dessineConfig(plateau,n)
    speed(3)
    liste_depart = plateau[tour_depart]
    liste_arrivee = plateau[tour_arrivee]
    disque = min(liste_depart)
    effaceDisque(disque,plateau,n)
    liste_depart.remove(disque)
    liste_arrivee.append(disque)
    plateau[tour_depart] = liste_depart
    plateau[tour_arrivee] = liste_arrivee
    dessineDisque(disque,plateau,n)
    speed(11)
    dessineConfig(plateau,n)
    speed(3)
    return plateau



#3
def boucleJeu(plateau,n):
    coups ={}
    compteurs = 0
    nombre_total_de_coup = 2**(n) -1 +5
    while compteurs != nombre_total_de_coup and verifVictoire(plateau,n) == False  :
        if verifVictoire(plateau,n) == True :
            print (f"{True}  le nombre de fois est {compteurs}")
            return compteurs
        print(f"coups numero {compteurs}")
        plateau = jouerUnCoup(plateau,n)
        compteurs += 1
        coups[compteurs] = plateau
    print(f"{False} le nombre de coups est {compteurs}")
    return compteurs




#4
def main():
    print("Bienvenue dans les Tours de Hanoi :)")
    print("")
    n = int(input("entrez le nombre de disques :"))
    dessinePlateau(n)
    dessineConfig(init(n),n)
    liste  = boucleJeu(init(n),n)
    score = liste[0]
    nom = liste[1]
    sauvScore(nom,n,score)
    mainloop()


#Partie D
#1
def dernierCoup(coups):
    dernier_coup = coups[len(coups.keys())]
    avant_coup = coups[len(coups.keys())-1]
    for i in range(3):
        if len(avant_coup[i]) > len(dernier_coup[i]) :
            tour_depart = i
    for j in range(3):
        if len(avant_coup[j]) <len(dernier_coup[j]) :
            tour_arrivee = j
    return tour_depart,tour_arrivee


#2 
def annulerDernierCoup(coups):
    dernier_coup = list(dernierCoup(coups))
    inverse = []
    for i in range(len(dernier_coup)):
        i-=1
        inverse.append(dernier_coup[i])
    del coups[len(coups.keys())]
    return coups,inverse

#3
def annulation (plateau,tour_depart,tour_arrivee,n):
            speed(11)
            dessinePlateau(n)
            speed(11)
            dessineConfig(plateau,n)
            speed(3)
            liste_depart = plateau[tour_depart]
            liste_arrivee = plateau[tour_arrivee]
            disque = min(liste_depart)
            effaceDisque(disque,plateau,n)
            liste_depart.remove(disque)
            liste_arrivee.append(disque)
            plateau[tour_depart] = liste_depart
            plateau[tour_arrivee] = liste_arrivee
            
            dessineDisque(disque,plateau,n)
            speed(11)
            dessineConfig(plateau,n)
            speed(3)
            return plateau


import copy

#version modifiee      
def boucleJeu1(plateau, n):
    coups = {1: copy.deepcopy(plateau)}  
    compteurs = 2
    nombre_total_de_coup = 2**(n) - 1 + 5 #+5 pour donner une chance a l'utilisateur
    while compteurs != nombre_total_de_coup and not verifVictoire(plateau, n):
        plateau = jouerUnCoup(plateau, n)
        coups[compteurs] = copy.deepcopy(plateau) 
        annuler = input("annuler? (oui/non) :")
        if annuler == "oui":
            coups, liste = annulerDernierCoup(coups)
            tour_depart = liste[0]
            tour_arrivee = liste[1] 
            plateau = annulation(plateau,tour_depart,tour_arrivee,n)
            compteurs-=1
        else:
            if verifVictoire(plateau, n) == True :
                print(f"victoire  le nombre de fois est {compteurs-1}")
                return [compteurs-1,True,plateau]
        compteurs += 1
    return [compteurs-1,False,plateau]




#partie E
#1
def sauvScore(nom,n,nb_coups,d):
    d[nom] = {}
    d[nom]["nombre de disques"] = n
    d[nom]["nombre de coups"] = nb_coups
    return d

#2 optionnelle

#3
def main1():
    print("Bienvenue dans les Tours de Hanoi :)")
    print("")
    drapeau = True
    d = {}
    while drapeau == True:
        n = int(input("entrez le nombre de disques :"))
        dessinePlateau(n)
        dessineConfig(init(n),n)
        liste_boucle = boucleJeu1(init(n),n)
        score = liste_boucle[0]
        bol = liste_boucle[1]
        plateau = liste_boucle[2]
        if bol == True:
            nom = input("Nom?")
            print(sauvScore(nom,n,score,d))
        continu = input("rejouer? (oui/non) :")
        if continu == "non":
            drapeau = False
        elif continu == "oui":
            efface_tout(plateau,n)
    print("Fin du jeu")
    mainloop()
   
#4
def auxiliere1(d): # une fonction pour l'utiliser dans affiche score
    d_n = {}
    liste_n = []
    for joueur in d.keys():
        liste_n.append(d[joueur]["nombre de disques"])
    sorted_n = sorted(liste_n)
    for n in range (0,len(sorted_n)):
        d_n[sorted_n[n]] = {}
    for n in range (0,len(sorted_n)):
        for joueur in d.keys():
            if d[joueur]["nombre de disques"] == sorted_n[n]:
                 
                d_n[sorted_n[n]][joueur]= d[joueur]
    return d_n


def afficheScore(d):
    d_n = auxiliere1(d)
    for i in d_n.keys():
        liste_score = []
        for joueur in d_n[i]:
            liste_score.append(d_n[i][joueur]["nombre de coups"])
        sorted_score = sorted(liste_score)
        for n in range (0,len(sorted_score)):
            for joueur in d_n[i].keys():
                if d_n[i][joueur]["nombre de coups"] == sorted_score[n]:  
                    print(f"{joueur}:{d_n[i][joueur]}")
            break

#les partie 5-6-7 sont en relation avec la partie 2 qui est optionnelle
#8
def menu(d):
    scores = input("voir les scores? (oui/non) :")
    if scores == "oui":
        afficheScore(d)
        

#partie F
#1
def hanoi(n, source, target, auxiliary):
    if n == 1:
        return [(source, target)]
    else:
        moves = hanoi(n - 1, source, auxiliary, target)
        moves.append((source, target))
        moves.extend(hanoi(n - 1, auxiliary, target, source))
        return moves



#2
def jouerUnCoup1(plateau,n,tour_depart,tour_arrivee) : # fontion auxiliere pour dessiner
    print(f"tu deplace de {tour_depart} au {tour_arrivee}")
    speed(11)
    dessinePlateau(n)
    speed(11)
    dessineConfig(plateau,n)
    speed(3)
    liste_depart = plateau[tour_depart]
    liste_arrivee = plateau[tour_arrivee]
    disque = min(liste_depart)
    effaceDisque(disque,plateau,n)
    liste_depart.remove(disque)
    liste_arrivee.append(disque)
    plateau[tour_depart] = liste_depart
    plateau[tour_arrivee] = liste_arrivee
    dessineDisque(disque,plateau,n)
    speed(11)
    dessineConfig(plateau,n)
    speed(3)
    return plateau

def solutionTurtle(plateau,n, source, target, auxiliary):
    liste = hanoi(n, source, target, auxiliary)
    for i in liste:
        tour_depart,tour_arrivee = i
        jouerUnCoup1(plateau,n,tour_depart,tour_arrivee)
        

    
#3
def main2():
    print("Bienvenue dans les Tours de Hanoi :)")
    print("")
    drapeau = True
    d = {}
    while drapeau == True:
        n = int(input("entrez le nombre de disques :"))
        dessinePlateau(n)
        dessineConfig(init(n),n)
        liste_boucle = boucleJeu1(init(n),n)
        score = liste_boucle[0]
        bol = liste_boucle[1]
        plateau = liste_boucle[2]
        if bol == True:
            nom = input("Nom?")
            d = sauvScore(nom,n,score,d)
        continu = input("rejouer? (oui/non) :")
        if continu == "non":
            drapeau = False
        elif continu == "oui":
            efface_tout(plateau,n)
        else:
            while continu != "non" or continu != "oui":
                continu = input("rejouer? (repondre par oui/non) :")
    solution = input("voir la solution? (oui/non) :")
    if solution == "oui":
        efface_tout(plateau,n)
        solutionTurtle(init(n),n,0,2,1)
    menu(d)
    print("")
    print("Fin du jeu")
    mainloop()   
    
main2()
    
            
#4 optionnel
        

        
        