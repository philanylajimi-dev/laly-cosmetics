# -*- coding: utf-8 -*-
"""
Laly Cosmetics — catalogue professionnel France.

Liste blanche : seules les références décrites ici sont publiées. Rien n'est
repris automatiquement de l'ancien catalogue suisse, qui ne sert qu'à fournir
les photographies et l'organisation des sections.

MODÈLE
------
`PRODUITS` est la source unique : une entrée par référence, nom, contenance,
prix et visuel compris. Les sections n'y renvoient que par identifiant.

Un même produit peut donc figurer dans plusieurs sections — un masque grand
format paraît à la fois dans « Masques grand format » et dans sa gamme — sans
jamais être décrit deux fois. Le panier étant indexé par identifiant, les deux
cartes alimentent la même ligne de commande.

    P("Nom", "Contenance", prix_en_centimes, image, **options)

    prix    en centimes d'euro HT, entier : tous les calculs se font en
            entiers, jamais en flottants.
    image   nom du fichier dans assets/img/p/, sans extension. None quand
            aucune photographie du produit n'existe : le catalogue affiche
            alors une vignette d'attente, jamais la photo d'un autre produit.

    attente="…"   la référence est affichée avec son prix mais n'est pas
                  commandable tant que l'information manque.
    photo_a_valider=True
                  la photographie est plausible mais n'a pas été confirmée
                  par Laly Cosmetics. Sans effet sur l'affichage : la mention
                  ne sort que dans le rapport de génération.

Un groupe de section se décrit soit par `"refs"` — la liste des identifiants à
afficher — soit par `"variantes"`, pour une fiche unique à sélecteur comme les
poudres décolorantes.

Modifier un prix : changer la valeur en centimes, puis relancer
`python3 build/generate.py`.
"""

# --------------------------------------------------------------------------- #
# Identité
# --------------------------------------------------------------------------- #

MARQUE = "Laly Cosmetics"
BASELINE = "Produits capillaires professionnels"
TELEPHONE_AFFICHE = "07 68 57 21 30"
TELEPHONE_WHATSAPP = "33768572130"

# --------------------------------------------------------------------------- #
# L'offre — la seule du catalogue
# --------------------------------------------------------------------------- #

OFFRE = {
    "seuil": 24,
    "surtitre": "Offre exclusive première commande",
    "gammes": "Profesia Hair — Nuances au choix",
    "regles": [
        "L'offre s'applique séparément aux deux gammes.",
        "Le seuil est de 24 tubes achetés dans une même gamme.",
        "En dessous de 24 tubes, aucune coloration offerte.",
        "À partir de 24 tubes achetés, chaque tube acheté donne droit à un tube offert.",
        "Les nuances offertes peuvent différer des nuances achetées, à condition "
        "d'appartenir à la même gamme.",
        "Les quantités Profesia Hair et Ekstra Color ne s'additionnent pas pour "
        "atteindre le seuil.",
    ],
    # Paliers et règles ne sont plus affichés dans l'ouverture, qui se limite
    # à l'annonce. Ils restent ici : le calcul du panier s'y réfère et ils
    # servent de mémoire des conditions validées.
    "paliers": [12, 23, 24, 30, 48],
}


def tubes_offerts(achetes):
    """La mécanique de l'offre, en un seul endroit.

    Le JavaScript du catalogue applique exactement la même règle.
    """
    return achetes if achetes >= OFFRE["seuil"] else 0


# --------------------------------------------------------------------------- #
# Produits — source unique
# --------------------------------------------------------------------------- #

def P(nom, contenance, prix, image, attente=None, photo_a_valider=False):
    return {
        "nom": nom,
        "contenance": contenance,
        "prix": prix,
        "image": image,
        "attente": attente,
        "photo_a_valider": photo_a_valider,
    }


PRODUITS = {
    # ---- Activateurs ----------------------------------------------------- #
    "act-10": P("Activateur 10 volumes", "1 000 ml", 335,
                "activateur-10-volumes-1000-ml"),
    "act-20": P("Activateur 20 volumes", "1 000 ml", 335,
                "activateur-20-volumes-1000-ml"),
    "act-30": P("Activateur 30 volumes", "1 000 ml", 335,
                "activateur-30-volumes-1000-ml"),
    "act-40": P("Activateur 40 volumes", "1 000 ml", 335,
                "activateur-40-volumes-1000-ml"),

    # ---- Poudres décolorantes --------------------------------------------- #
    # Une seule fiche, trois puissances : contenance identique, seuls le
    # pouvoir éclaircissant et le prix changent.
    "dec-7": P("Poudre décolorante Profesia Hair", "500 g · 7 tons", 1490,
               "poudre-decolorante-profesia-500-g", photo_a_valider=True),
    "dec-9": P("Poudre décolorante Profesia Hair", "500 g · 9 tons", 1990,
               "poudre-decolorante-profesia-500-g", photo_a_valider=True),
    "dec-10": P("Poudre décolorante Profesia Hair", "500 g · 10 tons", 2290,
                "poudre-decolorante-profesia-500-g", photo_a_valider=True),

    # ---- Bidons 10 L ------------------------------------------------------- #
    "bid-dry": P("Dry Hair Care", "10 L", 6000,
                 "shampoing-pour-cheveux-secs-bidon-de-10-litres"),
    "bid-freq": P("Frequent Hair Care", "10 L", 3500,
                  "shampoing-aux-amandes-frequent-care-pour-lavages-frequents-bidon-de-10-litres",
                  photo_a_valider=True),

    # ---- Dry Hair Care ------------------------------------------------------ #
    "sh-dry-300": P("Shampoing Dry Hair Care", "300 ml", 590,
                    "shampoing-soin-cheveux-secs-300-ml"),
    "sh-dry-1000": P("Shampoing Dry Hair Care", "1 000 ml", 1290,
                     "shampoing-soin-cheveux-secs-pour-cheveux-secs-1000-ml"),
    "mas-dry-500": P("Masque Dry Hair Care", "500 ml", 1190,
                     "masque-soin-cheveux-secs-500-ml"),
    "mas-dry-1500": P("Masque Dry Hair Care", "1 500 ml", 1890,
                      "masque-soin-cheveux-secs-1500-ml"),
    "cr-dry-200": P("Crème volumisante Dry", "200 ml", 1090,
                    "creme-hydratante-pour-cheveux-secs-200-ml", photo_a_valider=True),

    # ---- Color Hair Care ----------------------------------------------------- #
    "sh-col-300": P("Shampoing Color Hair Care", "300 ml", 590,
                    "shampoing-color-care-pour-cheveux-colores-300-ml"),
    "sh-col-1000": P("Shampoing Color Hair Care", "1 000 ml", 1290,
                     "shampoing-color-care-pour-cheveux-colores-1000-ml"),
    "mas-col-500": P("Masque Color Hair Care", "500 ml", 1190,
                     "masque-soin-colorant-cheveux-colores-500-ml"),
    "mas-col-1000": P("Masque Color Hair Care", "1 000 ml", 1890,
                      "masque-soin-colorant-cheveux-colores-1000-ml"),
    "spr-col-200": P("Spray Color Protection", "200 ml", 1090,
                     "spray-protecteur-de-couleur-200-ml"),

    # ---- Frequent Hair Care --------------------------------------------------- #
    "sh-fre-1000": P("Shampoing Frequent Hair Care", "1 000 ml", 1290,
                     "shampoing-frequent-aux-agrumes-de-sicile-1000-ml"),
    "ap-fre-1000": P("Après-shampoing Frequent Hair Care", "1 000 ml", 1390,
                     "apres-shampoing-frequent-aux-agrumes-de-sicile-1000-ml"),
    "spr-fre-250": P("Spray démêlant Frequent", "250 ml", 990,
                     "spray-denouant-les-noeuds-frequents-250-ml"),

    # ---- Curl Hair Care ------------------------------------------------------- #
    "sh-cur-300": P("Shampoing Curl Hair Care", "300 ml", 590,
                    "shampoing-curls-pour-cheveux-boucles-300-ml"),
    "sh-cur-1000": P("Shampoing Curl Hair Care", "1 000 ml", 1290,
                     "shampoing-curls-pour-cheveux-boucles-1000-ml"),
    "mas-cur-500": P("Masque Curl Hair Care", "500 ml", 1190,
                     "masque-cheveux-boucles-curls-hair-care-500-ml"),
    "flu-cur-250": P("Fluide boucles Curl", "250 ml", 1190,
                     "fluide-boucles-soin-boucles-250-ml"),

    # ---- Greasy Hair Care ------------------------------------------------------ #
    "sh-gre-1000": P("Shampoing Greasy Hair Care", "1 000 ml", 1290,
                     "shampooing-anti-graisse-cheveux-gras-1000-ml"),

    # ---- Dandruff Hair Care ----------------------------------------------------- #
    "sh-dan-300": P("Shampoing Dandruff Hair Care", "300 ml", 590,
                    "shampooing-antipelliculaire-soin-capillaire-300-ml"),
    "sh-dan-1000": P("Shampoing Dandruff Hair Care", "1 000 ml", 1290,
                     "shampooing-antipelliculaire-1000-ml"),

    # ---- Loss Hair Care ---------------------------------------------------------- #
    "sh-los-300": P("Shampoing Loss Hair Care", "300 ml", 590,
                    "shampoing-anti-chute-aux-algues-marines-300-ml"),
    "sh-los-1000": P("Shampoing Loss Hair Care", "1 000 ml", 1290,
                     "shampoing-anti-chute-loss-hair-care-1000-ml"),
    "lot-los-150": P("Lotion Loss", "150 ml", 1290,
                     "lotion-energisante-anti-chute-150-ml"),
    "amp-los-12": P("Ampoules Loss", "12 × 10 ml", 2890,
                    "lotion-energisante-pour-le-soin-des-cheveux-contre-la-chute-12-flacons-de-10-ml"),

    # ---- No Yellow Hair Care ------------------------------------------------------- #
    "sh-noy-1000": P("Shampoing No Yellow", "1 000 ml", 1790,
                     "shampoing-anti-jaunissement-no-yellow-care-1000-ml",
                     attente="Disponibilité France à confirmer"),

    # ---- Botox Hair Therapy ---------------------------------------------------------- #
    "sh-bot-300": P("Shampoing Botox", "300 ml", 1120,
                    "shampoing-reconstruction-capillaire-botox-300-ml"),
    "sh-bot-1000": P("Shampoing Botox", "1 000 ml", 1720,
                     "botox-hair-therapy-reconstruction-shampoo-1000-ml"),
    "mas-bot-500": P("Masque Botox", "500 ml", 1490,
                     "masque-reconstruction-capillaire-botox-500-ml"),
    "mas-bot-1000": P("Masque Botox", "1 000 ml", 1990,
                      "masque-reconstruction-capillaire-botox-1000-ml"),
    "ser-bot-12": P("Sérum Botox", "12 × 10 ml", 2690,
                    "serum-reconstruction-capillaire-botox-12-ampoules-x-10-ml"),
    "bip-bot-200": P("Soin biphasé Botox", "200 ml", 1830,
                     "apres-shampoing-biphase-botox-200-ml"),
    "exp-bot-200": P("Soin express Botox", "200 ml", 1390,
                     "masque-spray-botox-hair-therapy-10-en-1-200-ml",
                     photo_a_valider=True),

    # ---- Nano Repair -------------------------------------------------------------------- #
    "sh-nan-300": P("Shampoing Nano Repair", "300 ml", 690,
                    "shampoing-preparateur-nano-repair-300-ml"),
    "mas-nan-500": P("Masque Nano Repair", "500 ml", 1390,
                     "masque-nano-repair-a-domicile-500-ml"),
    "flu-nan-250": P("Fluide Nano Repair", "250 ml", 1390,
                     "fluido-nano-repair-at-home-250-ml"),

    # ---- Extra Wave ----------------------------------------------------------------------- #
    "neu-wav-1000": P("Neutralisant Extra Wave", "1 000 ml", 1090,
                      "neutralisant-ekstra-wave-1000-ml"),

    # ---- Profesia X Men --------------------------------------------------------------------- #
    "xm-gel-500": P("Gel coiffant", "500 ml", 990,
                    "gel-capillaire-one-trillion-00186-fixation-forte-500-ml",
                    photo_a_valider=True),
    "xm-aqua-100": P("Cire Aqua", "100 ml", 790,
                     "acqua-wax-night-40121-profesia-x-men", photo_a_valider=True),
    "xm-cire-100": P("Cire coiffante", "100 ml", 790,
                     "cire-a-largile-effet-mat-09121-profesia-x-men", photo_a_valider=True),
    "xm-poudre-10": P("Poudre volume", "10 g", 990,
                      "poudre-volumisante-effet-mat-80121-profesia-x-men",
                      photo_a_valider=True),
    "xm-sel-250": P("Spray au sel", "250 ml", 1090,
                    "spray-salin-65121-profesia-x-men"),
    "xm-barbe-500": P("Crème à barbe", "500 ml", 1290,
                      "creme-a-barbe-x-men-500-ml"),
    "xm-apres-250": P("Après-rasage crème", "250 ml", 1090,
                      "creme-apres-rasage-belief-90121-profesia-x-men"),
    "xm-after-400": P("After Shave", "400 ml", 1390,
                      "apres-rasage-glace-effet-rafraichissant-23900-x-men-400ml",
                      photo_a_valider=True),
}


# La fiche à sélecteur des poudres : une photographie, trois puissances.
POUDRES = {
    "nom": "Poudre décolorante Profesia Hair",
    "contenance": "500 g",
    "image": "poudre-decolorante-profesia-500-g",
    "label": "Pouvoir éclaircissant",
    "variantes": [
        ("7 tons", "dec-7"),
        ("9 tons", "dec-9"),
        ("10 tons", "dec-10"),
    ],
}


# --------------------------------------------------------------------------- #
# Colorations — vendues à la nuance, pilotées par le nuancier
# --------------------------------------------------------------------------- #

COLORATIONS = [
    {
        "ref": "col-profesia",
        "gamme": "profesia",
        "nom": "Profesia Hair",
        "sous_titre": "Coloration permanente kératine et huile d'argan",
        "contenance": "Tube 100 ml",
        "prix": 800,
        "image": "coloration-color-7-0-100-ml",
    },
    {
        "ref": "col-ekstra",
        "gamme": "ekstra",
        "nom": "Ekstra Color",
        "sous_titre": "Coloration sans ammoniaque",
        "contenance": "Tube 100 ml",
        "prix": 840,
        "image": "coloration-sans-ammoniaque-ekstra-color-7-0-100-ml",
    },
]

DILUTION = "Dilution indiquée au nuancier : 1:1,5 — 1:2 pour les super éclaircissants SS."


# --------------------------------------------------------------------------- #
# Sections — elles ne font que renvoyer aux identifiants
# --------------------------------------------------------------------------- #

SECTIONS = [
    {
        "id": "colorations",
        "numero": "02",
        "titre": "Colorations",
        "nav": "Colorations",
        "intro": "Deux gammes, avec ou sans ammoniaque. Choisissez vos nuances "
                 "et vos quantités directement dans le nuancier.",
        "coloration": True,
        "groupes": [
            {
                "nom": "Activateurs",
                "note": "Émulsion oxydante crème, flacon de 1 000 ml",
                "refs": ["act-10", "act-20", "act-30", "act-40"],
            },
        ],
    },
    {
        "id": "soins",
        "numero": "03",
        "titre": "Soins par gamme",
        "nav": "Soins",
        "intro": "Chaque gamme au complet : shampoings, masques, soins sans "
                 "rinçage et formats de bac.",
        "groupes": [
            {"nom": "Dry Hair Care", "fonction": "Cheveux secs",
             "note": "Aucune promotion sur les bidons 10 L",
             "refs": ["sh-dry-300", "sh-dry-1000", "mas-dry-500", "mas-dry-1500",
                      "cr-dry-200", "bid-dry"]},
            {"nom": "Color Hair Care", "fonction": "Cheveux colorés", "note": "",
             "refs": ["sh-col-300", "sh-col-1000", "mas-col-500", "mas-col-1000",
                      "spr-col-200"]},
            {"nom": "Frequent Hair Care", "fonction": "Lavages fréquents",
             "note": "Aucune promotion sur les bidons 10 L",
             "refs": ["sh-fre-1000", "ap-fre-1000", "spr-fre-250", "bid-freq"]},
            {"nom": "Curl Hair Care", "fonction": "Cheveux bouclés", "note": "",
             "refs": ["sh-cur-300", "sh-cur-1000", "mas-cur-500", "flu-cur-250"]},
            {"nom": "Greasy Hair Care", "fonction": "Cheveux gras", "note": "",
             "refs": ["sh-gre-1000"]},
            {"nom": "Dandruff Hair Care", "fonction": "Anti-pelliculaire", "note": "",
             "refs": ["sh-dan-300", "sh-dan-1000"]},
            {"nom": "Loss Hair Care", "fonction": "Anti-chute et cheveux fins", "note": "",
             "refs": ["sh-los-300", "sh-los-1000", "lot-los-150", "amp-los-12"]},
            {"nom": "Botox Hair Therapy", "fonction": "Réparation et revitalisation des cheveux", "note": "",
             "refs": ["sh-bot-300", "sh-bot-1000", "mas-bot-500", "mas-bot-1000",
                      "ser-bot-12", "bip-bot-200", "exp-bot-200"]},
            {"nom": "No Yellow Hair Care", "fonction": "Anti-reflets jaunes", "note": "",
             "refs": ["sh-noy-1000"]},
        ],
    },
    {
        "id": "technique",
        "numero": "04",
        "titre": "Technique salon",
        "nav": "Technique",
        "intro": "Lissage réparateur, décoloration et neutralisation.",
        "groupes": [
            {"nom": "Nano Repair", "fonction": "Lissage réparateur", "note": "",
             "refs": ["sh-nan-300", "mas-nan-500", "flu-nan-250"]},
            {"nom": "Poudres décolorantes",
             "note": "Sachet de 500 g, trois puissances",
             "variantes": POUDRES},
            {"nom": "Extra Wave", "fonction": "Permanente et ondulation des cheveux", "note": "", "refs": ["neu-wav-1000"]},
        ],
    },
    {
        "id": "homme",
        "numero": "05",
        "titre": "Profesia X Men",
        "nav": "Homme",
        "intro": "Coiffage et rasage pour l'espace barbier.",
        "groupes": [
            {"nom": "Coiffage", "note": "",
             "refs": ["xm-gel-500", "xm-aqua-100", "xm-cire-100", "xm-poudre-10",
                      "xm-sel-250"]},
            {"nom": "Rasage", "note": "",
             "refs": ["xm-barbe-500", "xm-apres-250", "xm-after-400"]},
        ],
    },
]
