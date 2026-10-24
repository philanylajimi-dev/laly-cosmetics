"""
Nuances de coloration.

PROFESIA : relevé du nuancier officiel Profesia Hair fourni par Laly Cosmetics
(photographie `nuancier.HEIC`). Familles, ordre et codes repris tels quels.

EKSTRA : nuancier validé par Laly Cosmetics le 24 octobre 2026. Les codes
viennent du catalogue du fournisseur, rangés dans les mêmes familles de reflets
que le nuancier Profesia.

Les libellés français sont ceux du fournisseur. Une nuance sans libellé connu
s'affiche avec son seul code — rien n'est inventé.

Pour retirer une nuance indisponible : supprimer sa ligne, puis relancer
`python3 build/generate.py`.
"""

PROFESIA = {
    "gamme": "Profesia Hair",
    "confirme": True,
    "source": "Nuancier officiel Profesia Hair",
    "familles": [
        ("Naturels", [
            ('1/0', 'Noir'),
            ('3/0', 'Châtain foncé'),
            ('4/0', 'Châtain'),
            ('5/0', 'Châtain clair'),
            ('6/0', 'Blond foncé'),
            ('7/0', 'Blond'),
            ('8/0', 'Blond clair'),
            ('9/0', 'Blond très clair'),
            ('10/0', 'Blond platine'),
        ]),
        ("Naturels intenses", [
            ('5/00', 'Châtain clair profond'),
            ('6/00', 'Blond foncé profond'),
            ('7/00', 'Blond profond'),
            ('8/00', 'Blond clair profond'),
            ('9/00', 'Blond très clair profond'),
        ]),
        ("Cendrés", [
            ('5/1', 'Châtain clair cendré'),
            ('6/1', 'Blond foncé cendré'),
            ('7/1', 'Blond cendré'),
            ('8/1', 'Blond clair cendré'),
            ('9/1', 'Blond très clair cendré'),
            ('10/1', 'Blond platine cendré'),
            ('1/10', 'Noir bleu'),
        ]),
        ("Sable cendré", [
            ('5/71', 'Châtain clair sable cendré'),
            ('7/71', 'Blond sable cendré'),
            ('8/71', 'Blond clair sable cendré'),
        ]),
        ("Dorés cendrés", [
            ('5/31', 'Châtain clair doré cendré'),
            ('6/31', 'Blond foncé doré cendré'),
            ('7/31', 'Blond doré cendré'),
            ('8/31', 'Blond clair doré cendré'),
        ]),
        ("Dorés", [
            ('4/03', 'Châtain chaud doré'),
            ('5/3', 'Châtain clair doré'),
            ('6/3', 'Blond foncé doré'),
            ('7/3', 'Blond doré'),
            ('8/3', 'Blond clair doré'),
        ]),
        ("Dorés cuivrés", [
            ('6/34', 'Blond foncé doré cuivré'),
            ('7/34', 'Blond doré cuivré'),
            ('8/34', 'Blond clair doré cuivré'),
        ]),
        ("Cuivrés", [
            ('5/4', 'Châtain clair cuivré'),
            ('6/4', 'Blond foncé cuivré'),
            ('7/4', 'Blond cuivré'),
        ]),
        ("Cuivrés dorés", [
            ('5/43', 'Châtain clair cuivré doré'),
            ('6/43', 'Blond foncé cuivré doré'),
            ('7/43', 'Blond cuivré doré'),
            ('8/43', 'Blond clair cuivré doré'),
        ]),
        ("Cuivrés intenses", [
            ('6/44', ''),
            ('7/44', 'Blond cuivré intense'),
            ('8/44', 'Blond clair cuivré intense'),
        ]),
        ("Acajou", [
            ('4/5', 'Châtain acajou'),
            ('5/5', 'Châtain clair acajou'),
            ('6/5', 'Blond foncé acajou'),
        ]),
        ("Rouges", [
            ('5/6', 'Châtain clair rouge'),
            ('6/6', 'Blond foncé rouge'),
        ]),
        ("Rouges intenses", [
            ('6/656', 'Blond foncé rouge acajou intense'),
            ('6/666', 'Blond foncé rouge extra intense'),
        ]),
        ("Marrons", [
            ('4/7', 'Châtain marron'),
            ('5/7', 'Châtain clair marron'),
            ('6/7', 'Blond foncé marron'),
            ('7/7', 'Blond noyer'),
            ('8/7', 'Blond clair noisette'),
        ]),
        ("Violets", [
            ('4/2', 'Châtain violine'),
            ('5/2', 'Châtain clair violine'),
            ('5/226', 'Châtain clair irisé intense rouge'),
        ]),
        ("Blonds froids", [
            ('10/21 SS', 'Blond platine irisé cendré'),
            ('11/0 SS', 'Super éclaircissant'),
            ('11/1 SS', 'Super éclaircissant'),
            ('12/11 SS', 'Super éclaircissant'),
            ('12/21 SS', 'Super éclaircissant'),
            ('12/22 SS', 'Super éclaircissant'),
        ]),
        ("Tonalisants froids", [
            ('T.02', ''),
            ('T.12', ''),
            ('T.21', ''),
        ]),
    ],
}

EKSTRA = {
    "gamme": "Ekstra Color sans ammoniaque",
    "confirme": True,
    "source": "Nuancier validé par Laly Cosmetics",
    "familles": [
        ("Naturels", [
            ('1/0', 'Noir'),
            ('3/0', 'Châtain foncé'),
            ('4/0', 'Châtain'),
            ('5/0', 'Châtain clair'),
            ('6/0', 'Blond foncé'),
            ('7/0', 'Blond'),
            ('8/0', 'Blond clair'),
            ('10/0', 'Blond platine'),
        ]),
        ("Cendrés", [
            ('5/1', 'Châtain clair cendré'),
            ('6/1', 'Blond foncé cendré'),
            ('7/1', 'Blond cendré'),
            ('8/1', 'Blond clair cendré'),
        ]),
        ("Dorés cendrés", [
            ('5/31', 'Châtain clair doré cendré'),
            ('6/31', 'Blond foncé doré cendré'),
            ('7/31', 'Blond doré cendré'),
            ('8/31', 'Blond clair doré cendré'),
        ]),
        ("Dorés", [
            ('4/03', 'Châtain chaud doré'),
            ('5/3', 'Châtain clair doré'),
            ('6/3', 'Blond foncé doré'),
            ('7/3', 'Blond doré'),
            ('8/3', 'Blond clair doré'),
        ]),
        ("Dorés cuivrés", [
            ('6/34', 'Blond foncé doré cuivré'),
            ('8/34', 'Blond clair doré cuivré'),
        ]),
        ("Cuivrés", [
            ('5/4', 'Châtain clair cuivré'),
        ]),
        ("Cuivrés dorés", [
            ('5/43', 'Châtain clair cuivré doré'),
            ('7/43', 'Blond cuivré doré'),
        ]),
        ("Cuivrés intenses", [
            ('6/44', 'Blond foncé cuivré intense'),
            ('8/44', 'Blond clair cuivré intense'),
        ]),
        ("Marrons", [
            ('6/7', 'Blond foncé marron'),
            ('7/7', 'Blond noyer'),
        ]),
        ("Violets", [
            ('4/2', 'Châtain violine'),
            ('5/2', 'Châtain clair violine'),
            ('5/226', 'Châtain clair irisé intense rouge'),
        ]),
        ("Reflets 46", [
            ('5/46', 'Châtain clair cuivré rouge'),
            ('6/46', 'Blond foncé cuivré rouge'),
        ]),
        ("Blonds froids", [
            ('11/3 SS', 'Super éclaircissant'),
            ('11/0 SS', 'Super éclaircissant'),
        ]),
        ("Boosters", [
            ('Booster argent', ''),
            ('Booster bleu', ''),
            ('Booster rouge', ''),
            ('Booster violet', ''),
        ]),
    ],
}
