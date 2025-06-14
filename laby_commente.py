
import random  # On importe la bibliothèque random pour choisir les salles et les pièges au hasard

# On demande le nom du joueur, on met la première lettre en majuscule et on enlève les espaces autour
nom = input("Bonjour mon apprenti mage quel est ton nom ?: ").capitalize().strip()

# On affiche un message d'accueil et les règles du jeu
print(f"""Bienvenue, mage {nom} !
Tu as 10 points d’énergie au départ.
Chaque déplacement te coûte 1 point. 
Tu peux en gagner ou perdre 
selon ce que tu rencontres dans chaque salle.
Si tu atteins 0, tu meurs. Si tu termines 10 salles, tu gagnes.""")

# Variables de départ
energie = 10             # L'énergie du joueur
tour = 0                 # Le numéro de la salle actuelle (on commence à 0)
chemin = []              # Liste pour garder en mémoire les directions prises (N, S, E, O)

# Boucle principale du jeu : elle continue tant que le joueur a de l'énergie et n'a pas traversé 10 salles
while energie > 0 and tour < 10:
    print(f"Energie actuelle = {energie} et tu entames le tour {tour + 1}")

    # On demande au joueur de choisir une direction
    direction = input("Choisis une direction entre (N/S/E/O) : ").upper().strip()

    # Si la direction n’est pas valide, on affiche un message et on recommence le tour
    if direction not in ["N", "S", "E", "O"]:
        print("Direction invalide. Choisis N, S, E ou O.")
        continue  # Repart au début de la boucle sans exécuter la suite

    chemin.append(direction)  # On ajoute la direction dans la liste des chemins
    energie -= 1              # Chaque déplacement coûte 1 énergie
    tour += 1                 # On passe au tour suivant

    # On choisit au hasard le type de salle
    type_salle = ["vide", "piege", "enigme"]
    salle = random.choice(type_salle)

    # Si la salle est vide
    if salle == "vide":
        print("Salle vide ! Tu ne perds rien, mais tu ne gagnes rien non plus.")

    # Si c’est une salle piégée
    elif salle == "piege":
        degat = random.choice([2, 3])  # Le piège enlève 2 ou 3 points d’énergie
        energie -= degat
        print(f"Salle piégée ! Tu perds {degat} points.")

    # Si c’est une salle énigme
    else:
        print("Salle énigme")

        try:
            # On demande au joueur de répondre à une question
            enigme = int(input("Combien font 5+2 : "))

            # Si la réponse est correcte, on lui ajoute 1 point d’énergie
            if enigme == 7:
                energie += 1
                print("Bonne réponse ! Tu gagnes une énergie en plus.")
            else:
                print("Mauvaise réponse ! Tu ne gagnes rien.")
        except ValueError:
            # Si le joueur tape une lettre ou un mot, on affiche un message gentil sans planter le programme
            print("Ce n’est pas un nombre valide. Tu ne gagnes rien.")

    # Affichage de l’énergie restante à la fin du tour
    print(f"Énergie restante : {energie}")

# Quand la boucle est terminée (soit parce que énergie = 0, soit 10 salles terminées)
print("Fin du jeu")

# Si le joueur a perdu
if energie <= 0:
    print(f"Dommage, mage {nom} ! Tu as perdu toute ton énergie...")

# Si le joueur a survécu
else:
    print(f"Bravo, mage {nom} ! Tu as survécu aux 10 salles du labyrinthe !")

# On affiche le chemin complet pris par le joueur (ex : N, E, S, O)
print(f"Chemin parcouru : {', '.join(chemin)}" )
