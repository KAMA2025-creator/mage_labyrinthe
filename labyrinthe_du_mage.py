

import random
nom = input("Bonjour mon apprenti mage quel est ton nom ?: ").capitalize().strip()
print(f"""Bienvenue, mage {nom} !
Tu as 10 points d’énergie au départ.
Chaque déplacement te coûte 1 point. 
Tu peux en gagner ou perdre 
selon ce que tu rencontres dans chaque salle.
Si tu atteins 0, tu meurs. Si tu termines 10 salles, tu gagnes.""")
energie = 10
tour = 0
chemin = []
while energie >0 and tour < 10:
    print(f"Energie actuelle = {energie} et tu entame le tour {tour + 1}")
    direction = input("choisis une direction entre (N/S/E/O) : ").upper().strip()
    if direction not in ["N","S","E", "O"]:
        print("Direction invalide. Choisis N, S, E ou O.")
        continue
    chemin.append(direction)
    energie -= 1
    tour +=1
    type_salle = ["vide", "piege","enigme"]
    salle = random.choice(type_salle)
    if salle == "vide":
        print("salle vide ! tu ne perds rien mais, tu ne gagnes rien aussi")
    elif salle == "piege":
        degat = random.choice([2,3])
        energie -=degat
        print(f"Salle piégée ! Tu perds {degat} points.")
    else:
        print("salle enigme")
        try:
            enigme= int(input("combien font 5+2 : "))
            if enigme == 7:
                energie +=1
                print("bonne reponse ! tu gagnes un energie en plus")
            else:
                print("mauvaise reponse ! tu ne gagnes rien ")
        except ValueError:
            print("Ce n’est pas un nombre valide. Tu ne gagnes rien.")
    print(f"energie restante est {energie }")
print("fin du jeu")
if energie<=0:
    print(f"Dommage, mage {nom} ! Tu as perdu toute ton énergie...")
else:
    print(f"Bravo, mage {nom} ! Tu as survécu aux 10 salles du labyrinthe !")
print(f"Chemin parcouru : {', '.join(chemin)}" )
