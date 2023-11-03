from requests import get as obtenir
import additifs

quantitesEnToFrench = {
    "low": "faible",
    "moderate": "moyen",
    "high": "élevé",
    None: "non indiqué"
}

def getJson(code):
    url = f'https://world.openfoodfacts.org/api/v0/product/{code}.json'
    try:
        statut = obtenir(url)
        donnees = statut.json()
        if len(donnees["code"]) == 0:
            print('Ce produit n\'est pas connu')
            return None
    except ValueError:
        return None
    return donnees

def getAllData(donnees):
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
    return nom, marque, preparation, quantite, vegan, vegetarien, ingredients, sucres, graissesSaturees, sel, nutriscore

while True:
    donnees = getJson(input('Entrez le code-barre du produit : '))
    if donnees is None:
        continue
    nom, marque, preparation, quantite, vegan, vegetarien, ingredients, sucres, graissesSaturees, sel, nutriscore = getAllData(donnees)
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
        Nutriscore : {nutriscore}
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
    if infos and len(listeAdditifs) > 0:
        additifs.infos(listeAdditifs)
    else:
        print("Aucun additif")
