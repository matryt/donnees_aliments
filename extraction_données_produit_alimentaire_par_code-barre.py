import numpy as np
from requests import get as obtenir
import additifs
import urllib.request
import cv2

def image_from_url(url):
    rep = urllib.request.urlopen(url).read()
    image = np.asarray(bytearray(rep), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


while True:
    code_barre=input('Quel est le code barre ? ')
    url='https://world.openfoodfacts.org/api/v0/product/'+code_barre+'.json'
    try:
        statut=obtenir(url)
        données=statut.json()
        if len(données["code"])==0:
            print('Ce produit n\'est pas connu')
            continue
    except ValueError:
        pass
    try:
        print('Le nom du produit est : ', données["product"]["product_name_fr"], "\n")
    except KeyError:
        print('Le nom de ce produit n\'est pas donné\n')

    try:
        print('La marque du produit est : ', données["product"]["brands_imported"], "\n")
    except KeyError:
        try:
            print('La marque du produit est : ', données["product"]["brands"], "\n")
        except:
            print('La marque du produit n\'est pas donnée \n')

    try:
        print('La préparation de ce produit est : ', données["product"]["preparation"], "\n")
    except KeyError:
        print('La préparation de ce produit n\'est pas donnée\n')

    try:
        print('La quantité de ce produit est : ', données["product"]["quantity"], "\n")
    except KeyError:
        print('La quantité de ce produit n\'est pas donnée\n')

    try:
        print('Ce produit est vegan  : ', 'oui' if données["product"]["ingredients"][0]["vegan"]=='yes' else 'non', "\n")
    except (KeyError, IndexError) as e:
        print('Le caractère vegan ou non de ce produit n\'est pas indiqué\n')

    try:
        print('Ce produit est végétarien  : ', 'oui' if données["product"]["ingredients"][0]["vegetarian"]=='yes' else 'non', "\n")
    except (KeyError, IndexError) as e:
        print('Le caractère végétarien ou non de ce produit n\'est pas indiqué\n')

    print('Les ingrédients précisés entre underscores (_) sont des allergènes potentiels')
    try:
        print('Ingrédients du produit  : ', données["product"]["ingredients_text_fr"], "\n")
    except KeyError:
        print('Les ingrédients de ce produit ne sont pas indiqués\n')

    try:
        if données["product"]["nutrient_levels"]["sugars"]=='low':
            print('Apport en sucres : faible\n')
        elif données["product"]["nutrient_levels"]["sugars"]=='moderate':
            print('Apport en sucres : moyen\n')
        else:
            print('Apport en sucres : élevé\n')
    except KeyError:
        print('L\'apport en sucres de ce produit n\'est pas indiqué\n')

    try:
        if données["product"]["nutrient_levels"]["saturated-fat"]=='low':
            print('Apport en graisses saturées : faible\n')
        elif données["product"]["nutrient_levels"]["saturated-fat"]=='moderate':
            print('Apport en graisses saturées : moyen\n')
        else:
            print('Apport en graisses saturées : élevé\n')
    except KeyError:
        print('L\'apport en graisses saturées de ce produit n\'est pas indiqué\n')

    try:
        if données["product"]["nutrient_levels"]["salt"]=='low':
            print('Apport en sel : faible\n')
        elif données["product"]["nutrient_levels"]["salt"]=='moderate':
            print('Apport en sel : moyen\n')
        else:
            print('Apport en sel : élevé\n')
    except KeyError:
        print('L\'apport en sel de ce produit n\'est pas indiqué\n')

    try:
        if données["product"]["nutrient_levels"]["fat"]=='low':
            print('Apport en graisses : faible\n')
        elif données["product"]["nutrient_levels"]["fat"]=='moderate':
            print('Apport en graisses : moyen\n')
        else:
            print('Apport en graisses : élevé\n')
    except KeyError:
        print('L\'apport en graisses de ce produit n\'est pas indiqué\n')

    try:
        print('Nutriscore du produit  : ', données["product"]["nutrition_grade_fr"].upper(), '\n')
    except KeyError:
        print('Le Nutriscore de ce produit n\'est pas indiqué\n')

    try:
        a=additifs.trouver_additifs(données["product"]["ingredients_text_fr"])
        b=additifs.trouver_information_additifs(a)
        if a==[]:
            repertoire=données["product"]["additives_tags"]
            for i in repertoire:
                add=i[4:]
                additif=additifs.trouver_additifs(i)
                b=additifs.trouver_information_additifs(additif)
    except KeyError:
        pass

    break
