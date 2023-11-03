import webbrowser
import time
import re

def trouver_additifs(texte):
    texte=str(texte)
    return re.findall("[eE][0-9]{3}", texte)

def infos(listeAdditifs):
    for i in listeAdditifs:
        print("Le produit contient l'additif E", i[1:])
        consent = input('Voulez-vous en savoir plus sur l\'additif E' + i[1:] + ' ? (o/n) ')
        if consent == 'o':
            url = f"https://fr.openfoodfacts.org/additif/E{i[1:]}"
            print('Une page d\'information sur l\'additif E', i[1:], ' a été ouverte dans le navigateur')
            webbrowser.open(url)
            time.sleep(1)