import os

def afficher_arborescence(dossier, indent=''):
    """
    Affiche l'arborescence du dossier spécifié.
    """
    # Afficher le nom du dossier actuel
    print(indent + os.path.basename(dossier) + '/')
    
    # Incrémenter l'indentation pour les sous-dossiers
    indent += '    '
    
    # Parcourir les fichiers et sous-dossiers du dossier
    contenu = os.listdir(dossier)
    for element in contenu:
        chemin = os.path.join(dossier, element)
        if os.path.isdir(chemin):
            # Si c'est un dossier, afficher son arborescence récursivement
            afficher_arborescence(chemin, indent)
        else:
            # Si c'est un fichier, simplement l'afficher
            print(indent + element)

# Chemin vers le dossier racine de votre projet
chemin_projet = 'C:\\Users\\gdaie\\Documents\\6Evaluation\\ProjetDataEng'

# Appel de la fonction pour afficher l'arborescence
afficher_arborescence(chemin_projet)