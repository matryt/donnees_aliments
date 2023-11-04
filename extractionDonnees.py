from requests import get as obtenir
import additifs
import colorama as clr

quantitesEnToFrench = {
    "low": "faible",
    "moderate": "moyen",
    "high": "élevé",
    None: "non indiqué"
}

nutriscoreToColor = {
    "A": clr.Fore.GREEN,
    "B": clr.Fore.GREEN,
    "C": clr.Fore.YELLOW,
    "D": clr.Fore.RED,
    "E": clr.Fore.RED,
    "Inconnu": clr.Fore.WHITE
}

quantitiesToColor = {
    "faible": clr.Fore.GREEN,
    "moyen": clr.Fore.YELLOW,
    "élevé": clr.Fore.RED,
    None: clr.Fore.WHITE
}


def getJson(code):
    url = f'https://world.openfoodfacts.org/api/v0/product/{code}.json'
    donnees = obtenir(url).json()
    if donnees.get('status') == 0:
        print('Ce produit est inconnu !')
        return None
    return donnees


def getNutrimentsPer100g(donnees, nutriment):
    return donnees.get("product").get("nutriments").get(f"{nutriment}_100g")


def getUnit(donnees, nutriment):
    return donnees.get("product").get("nutriments").get(f"{nutriment}_unit")


def percentApportTotal(nutriment, unit, quantite):
    if unit == "mg":
        quantite /= 1000
    elif unit == "µg":
        quantite /= 1000000
    if nutriment == "sugars":
        return quantite / 30 * 100
    elif nutriment == "saturated-fat":
        return quantite / 26 * 100
    elif nutriment == "salt":
        return quantite / 5 * 100


def getAllData(donnees):
    nutriments = ["sugars", "saturated-fat", "salt"]
    product = donnees.get("product")
    nom = product.get("product_name_fr") or "Inconnu"
    marque = product.get("brands_imported") or product.get("brands") or "Inconnu"
    preparation = product.get("preparation") or "Inconnu"
    quantite = product.get("quantity") or "Inconnu"
    vegan = "Oui" if product.get("ingredients")[0].get("vegan") else "Non"
    vegetarien = "Oui" if product.get("ingredients")[0].get("vegetarian") else "Non"
    ingredients = product.get("ingredients_text_fr") or "Inconnu"
    sucres = quantitesEnToFrench[product.get("nutrient_levels").get("sugars")]
    graissesSaturees = quantitesEnToFrench[product.get("nutrient_levels").get("saturated-fat")]
    sel = quantitesEnToFrench[product.get("nutrient_levels").get("salt")]
    nutriscore = product.get("nutrition_grade_fr").upper() if product.get("nutrition_grade_fr") else "Inconnu"
    l = [nom, marque, preparation, quantite, vegan, vegetarien, ingredients, sucres, graissesSaturees, sel, nutriscore]
    for i in range(7, len(l) - 1):
        percent = getNutrimentsPer100g(donnees, nutriments[i - 7])
        if percent is not None:
            unit = getUnit(donnees, nutriments[i - 7])
            pourcentageTotal = percentApportTotal(nutriments[i - 7], unit, percent)
            l[i] = (
                    f"{quantitiesToColor[l[i]]} {l[i]} ({str(round(percent, 2))}{unit}" + f"/100g = {round(pourcentageTotal)}% de l'apport recommandé)" + "\x1b[0m"
            )
        else:
            l[i] = quantitiesToColor[l[i]] + str(l[i]) + "\x1b[0m"
    return l


while True:
    donnees = getJson(input('Entrez le code-barre du produit : '))
    if donnees is None:
        continue
    nom, marque, preparation, quantite, vegan, vegetarien, ingredients, sucres, graissesSaturees, sel, nutriscore = getAllData(
        donnees)
    nutriRender = nutriscoreToColor[nutriscore] + nutriscore + "\x1b[0m"
    print(f'''
        Nom : {nom}
        Marque : {marque}
        Préparation : {preparation}
        Quantité : {quantite}
        Vegan : {vegan}
        Végétarien : {vegetarien}
        Ingrédients : {ingredients}
        Sucres : {sucres}
        Graisses saturées : {graissesSaturees}
        Sel : {sel}
        Nutriscore : {nutriRender}
        ''')

    listeAdditifs = donnees["product"]["additives_tags"]
    ingredients = donnees["product"].get("ingredients_text_fr")
    infos = True
    if listeAdditifs is None:
        if ingredients is None:
            infos = False
            print("Aucun information d'additif")
        else:
            listeAdditifs = additifs.trouver_additifs(ingredients)
    else:
        listeAdditifs = [l[3:] for l in listeAdditifs]
    if infos and len(listeAdditifs) > 0:
        additifs.infos(listeAdditifs)
    else:
        print("Aucun additif")
