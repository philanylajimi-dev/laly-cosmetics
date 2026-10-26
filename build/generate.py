#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère index.html à partir de build/catalogue.py et de build/nuancier.py.

    python3 build/generate.py

Aucune dépendance : Python 3 seul suffit. Le script vérifie au passage que
chaque référence a bien une photographie, signale celles qui n'en ont pas et
celles dont le visuel reste à valider, puis rappelle les références laissées
non commandables.

Le modèle de données est la seule source de vérité : les prix affichés dans le
catalogue, ceux utilisés par le panier et ceux envoyés sur WhatsApp viennent
tous du même dictionnaire, exporté une fois en JSON dans la page.
"""

import html
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import catalogue as C
import nuancier as N

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(RACINE, "assets", "img", "p")
IMG_W = 640

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]

NBSP = " "


# --------------------------------------------------------------------------- #
# Petits outils de rendu
# --------------------------------------------------------------------------- #

def e(s):
    return html.escape(str(s), quote=False)


def euro(cts):
    """1290 → 12,<span>90</span> : les centimes en plus petit, comme sur une
    étiquette de prix. Le nombre reste lisible d'un coup d'œil."""
    return f'{cts // 100},<span class="prix__c">{cts % 100:02d}</span>'


def typo(doc):
    """Typographie française, appliquée aux seuls nœuds de texte.

    Insécable avant les ponctuations doubles et devant l'euro, apostrophe
    courbe, insécable dans les nombres à quatre chiffres. On ne touche jamais
    à ce qui se trouve entre chevrons : attributs, classes et URL doivent
    rester intacts.
    """
    morceaux = re.split(r"(<[^>]*>)", doc)
    for i, m in enumerate(morceaux):
        if m.startswith("<"):
            continue
        m = re.sub(r" +([:;!?»€])", NBSP + r"\1", m)
        m = re.sub(r"« +", "«" + NBSP, m)
        m = re.sub(r"(\d) (?=\d)", r"\1" + NBSP, m)
        m = m.replace("'", "’")
        morceaux[i] = m
    return "".join(morceaux)


def sans_accent(s):
    table = str.maketrans("àâäçéèêëîïôöùûüÿœæ", "aaaceeeeiioouuuyoa")
    return s.lower().translate(table)


def visuel(image, classe="visuel"):
    """Packshot, ou vignette d'attente quand la photographie n'existe pas.

    L'alt reste vide : le nom du produit est systématiquement juste à côté, le
    répéter n'apporterait rien au lecteur d'écran.
    """
    if not image:
        return (f'<div class="{classe} {classe}--attente">'
                f'<span>Visuel à venir</span></div>')
    return (f'<div class="{classe}">'
            f'<img src="assets/img/p/{image}.webp" alt="" '
            f'width="{IMG_W}" height="{IMG_W}" loading="lazy" decoding="async">'
            f'</div>')


# --------------------------------------------------------------------------- #
# Blocs
# --------------------------------------------------------------------------- #

def bloc_ouverture(maj):
    """Logo, promesse et offre dans un seul bloc sombre.

    Deux bandes noires successives se liraient comme une hésitation : la
    marque et l'offre tiennent dans le même champ, séparées par un filet.
    """
    o = C.OFFRE

    return f"""<section class="ouverture" id="offre" aria-labelledby="t-offre">
  <div class="wrap">

  <div class="ouverture__haut">
    <div class="ouverture__ident">
      <!-- Le titre du document est porté par le logo : on le redonne en toutes
           lettres aux lecteurs d'écran et aux moteurs. -->
      <h1 class="u-lecteur">Laly Cosmetics — catalogue professionnel pour les salons de coiffure</h1>
      <img class="ouverture__logo" src="assets/img/laly-logo-blanc.webp" alt="Laly Cosmetics" width="640" height="405" fetchpriority="high">
      <p class="ouverture__lede">Tarifs professionnels pour les salons de coiffure.
        Choisissez vos références, vos nuances et vos quantités, puis envoyez
        votre commande sur WhatsApp.</p>
    </div>
    <p class="ouverture__meta"><span>Prix en euros HT</span><span class="ouverture__sep" aria-hidden="true"></span><span>France</span></p>
  </div>

  <div class="offre">
    <p class="kicker kicker--orange">{o['surtitre']}</p>
    <h2 class="offre__titre" id="t-offre">
      <span class="offre__ligne">
        <span class="offre__nb">{o['seuil']}</span>
        <span class="offre__mot">colorations achetées</span>
      </span>
      <span class="offre__egal" aria-hidden="true">=</span>
      <span class="offre__ligne">
        <span class="offre__nb">{o['seuil']}</span>
        <span class="offre__mot">colorations offertes</span>
      </span>
    </h2>
    <p class="offre__gammes">{o['gammes']}</p>
    <a class="bouton bouton--orange" href="#colorations">Choisir mes nuances</a>
  </div>

  </div>
</section>"""


def carte(ref, p, groupe):
    """Carte produit : photo, nom, contenance, prix HT, quantité, ajout.

    Pas de description : le catalogue est une liste de prix, le conseil se
    donne dans la conversation.
    """
    recherche = sans_accent(f"{p['nom']} {p['contenance']} {groupe}")

    if p["attente"]:
        action = (f'<p class="carte__attente-note">{p["attente"]}</p>')
        etat = " carte--attente"
    else:
        action = f"""<div class="carte__action">
      <div class="pas" data-pas>
        <button type="button" class="pas__b" data-pas-moins aria-label="Retirer une unité de {e(p['nom'])} {e(p['contenance'])}">−</button>
        <input class="pas__n" type="number" inputmode="numeric" min="1" step="1" value="1"
               aria-label="Quantité de {e(p['nom'])} {e(p['contenance'])}" data-pas-valeur>
        <button type="button" class="pas__b" data-pas-plus aria-label="Ajouter une unité de {e(p['nom'])} {e(p['contenance'])}">+</button>
      </div>
      <button type="button" class="ajout" data-ajout="{ref}">Ajouter</button>
    </div>"""
        etat = ""

    return f"""<article class="carte{etat}" data-ref="{ref}" data-recherche="{e(recherche)}">
  {visuel(p['image'], 'carte__visuel')}
  <div class="carte__corps">
    <p class="carte__fmt">{e(p['contenance'])}</p>
    <h4 class="carte__nom">{e(p['nom'])}</h4>
    <p class="prix"><span class="prix__v">{euro(p['prix'])}</span><span class="prix__d">€</span><span class="prix__ht">HT</span></p>
    {action}
  </div>
</article>"""


def contenu(g):
    """Un groupe sans référence ni variante ne doit pas laisser d'en-tête."""
    return bool(g.get("refs") or g.get("variantes"))


def carte_variantes(v, groupe):
    """Fiche unique à sélecteur : une photographie, plusieurs puissances.

    Chaque variante garde son propre identifiant, donc sa propre ligne de
    panier et sa propre mention dans le message WhatsApp. Le sélecteur ne fait
    que choisir laquelle le bouton « Ajouter » vise.
    """
    premier = v["variantes"][0][1]
    options = "".join(
        f'<option value="{r}" data-prix="{C.PRODUITS[r]["prix"]}">{e(lib)}</option>'
        for lib, r in v["variantes"])
    mots = " ".join(lib for lib, _ in v["variantes"])
    recherche = sans_accent(f'{v["nom"]} {v["contenance"]} {groupe} {mots} décolorant')
    ident = "var-" + premier

    return f"""<article class="carte carte--variantes" data-variantes data-ref="{premier}" data-recherche="{e(recherche)}">
  {visuel(v['image'], 'carte__visuel')}
  <div class="carte__corps">
    <p class="carte__fmt">{e(v['contenance'])}</p>
    <h4 class="carte__nom">{e(v['nom'])}</h4>
    <p class="prix"><span class="prix__v" data-var-prix>{euro(C.PRODUITS[premier]['prix'])}</span><span class="prix__d">€</span><span class="prix__ht">HT</span></p>
    <div class="carte__variante">
      <label for="{ident}">{e(v['label'])}</label>
      <select id="{ident}" data-var-select>{options}</select>
    </div>
    <div class="carte__action">
      <div class="pas" data-pas>
        <button type="button" class="pas__b" data-pas-moins aria-label="Retirer une unité">−</button>
        <input class="pas__n" type="number" inputmode="numeric" min="1" step="1" value="1"
               aria-label="Quantité de {e(v['nom'])}" data-pas-valeur>
        <button type="button" class="pas__b" data-pas-plus aria-label="Ajouter une unité">+</button>
      </div>
      <button type="button" class="ajout" data-ajout="{premier}">Ajouter</button>
    </div>
  </div>
</article>"""


def groupe(g):
    if g.get("variantes"):
        cartes = carte_variantes(g["variantes"], g["nom"])
    else:
        cartes = "\n".join(carte(r, C.PRODUITS[r], g["nom"]) for r in g["refs"])
    note = f'<p class="groupe__note">{e(g["note"])}</p>' if g.get("note") else ""
    # Le nom reste celui du fournisseur ; la fonction, juste dessous, dit à
    # quoi la gamme sert — un salon français ne devine pas « No Yellow ».
    fonction = (f'<p class="groupe__fonction">{e(g["fonction"])}</p>'
                if g.get("fonction") else "")
    return f"""<div class="groupe" data-groupe>
  <header class="groupe__tete">
    <div class="groupe__ident">
      <h3 class="groupe__nom">{g['nom']}</h3>
      {fonction}
    </div>
    {note}
  </header>
  <div class="grille">
{cartes}
  </div>
</div>"""


def bloc_nuances(gamme, donnees):
    """Le nuancier d'une gamme : familles, codes, quantités."""
    familles = []
    for nom, codes in donnees["familles"]:
        cases = []
        for code, libelle in codes:
            lib = f'<span class="nuance__lib">{e(libelle)}</span>' if libelle else ""
            cases.append(f"""<li class="nuance" data-nuance="{e(code)}">
          <button type="button" class="nuance__b" data-nuance-moins aria-label="Retirer un tube {e(code)}">−</button>
          <span class="nuance__txt"><span class="nuance__code">{e(code)}</span>{lib}</span>
          <output class="nuance__qte" data-nuance-qte>0</output>
          <button type="button" class="nuance__b nuance__b--plus" data-nuance-plus aria-label="Ajouter un tube {e(code)}">+</button>
        </li>""")
        # <details> plutôt qu'un repli maison : le clavier, les lecteurs
        # d'écran et la recherche du navigateur le gèrent déjà, et la page
        # reste utilisable si le JavaScript ne se charge pas.
        familles.append(f"""<details class="famille" data-famille>
        <summary class="famille__tete">
          <h4 class="famille__nom">{e(nom)}</h4>
          <span class="famille__compte">{len(codes)} nuance{"s" if len(codes) > 1 else ""}</span>
          <span class="famille__choisies" data-famille-choisies hidden></span>
        </summary>
        <ul class="famille__liste">{''.join(cases)}</ul>
      </details>""")
    return "\n".join(familles)


def bloc_colorations():
    cartes = []
    for col in C.COLORATIONS:
        donnees = N.PROFESIA if col["gamme"] == "profesia" else N.EKSTRA
        total_nuances = sum(len(c) for _, c in donnees["familles"])
        avert = ""
        if not donnees["confirme"]:
            avert = (f'<p class="gamme__avert">Liste de nuances provisoire, issue du '
                     f'catalogue fournisseur. Le nuancier officiel {e(col["nom"])} '
                     f'reste à confirmer.</p>')

        cartes.append(f"""<article class="gamme" data-gamme="{col['gamme']}" data-ref="{col['ref']}">
  <div class="gamme__tete">
    {visuel(col['image'], 'gamme__visuel')}
    <div class="gamme__ident">
      <h3 class="gamme__nom">{e(col['nom'])}</h3>
      <p class="gamme__sous">{e(col['sous_titre'])}</p>
      <p class="gamme__meta">{e(col['contenance'])}<span class="gamme__sep" aria-hidden="true"></span>{total_nuances} nuances</p>
      <p class="prix prix--lg"><span class="prix__v">{euro(col['prix'])}</span><span class="prix__d">€</span><span class="prix__ht">HT le tube</span></p>
    </div>
  </div>

  {avert}

  <div class="gamme__corps">
    <div class="gamme__barre">
      <p class="compte" data-compte>
        <span class="compte__n" data-compte-achetes>0</span><span data-compte-mot> tube acheté</span>
        <span class="compte__plus" data-compte-bloc-offerts hidden>
          <span class="compte__sep" aria-hidden="true">+</span>
          <span class="compte__n compte__n--offert" data-compte-offerts>0</span> offert
        </span>
        <span class="compte__reste" data-compte-reste></span>
      </p>
      <div class="gamme__filtre">
        <label class="u-lecteur" for="f-{col['gamme']}">Filtrer les nuances de la gamme {e(col['nom'])}</label>
        <input id="f-{col['gamme']}" type="search" autocomplete="off"
               placeholder="Filtrer : 7/0, blond, cuivré…" data-filtre>
      </div>
    </div>

    <div class="gamme__nuancier">
      {bloc_nuances(col['gamme'], donnees)}
      <p class="gamme__vide" data-filtre-vide hidden>Aucune nuance ne correspond.</p>
    </div>

    <div class="offerts" data-offerts hidden>
      <div class="offerts__tete">
        <h4 class="offerts__titre">Choisissez vos nuances offertes</h4>
        <p class="offerts__solde" data-offerts-solde></p>
      </div>
      <p class="offerts__alerte" data-offerts-alerte hidden role="alert"></p>
      <div class="offerts__outils">
        <button type="button" class="bouton bouton--fin" data-offerts-miroir>Reprendre la même répartition</button>
        <div class="offerts__ajout">
          <label class="u-lecteur" for="sel-{col['gamme']}">Nuance offerte à ajouter</label>
          <select id="sel-{col['gamme']}" data-offerts-select></select>
          <button type="button" class="bouton bouton--fin" data-offerts-ajout>Ajouter</button>
        </div>
      </div>
      <ul class="offerts__liste" data-offerts-liste></ul>
    </div>
  </div>
</article>""")

    groupes = "\n".join(
        groupe(g)
        for g in next(s for s in C.SECTIONS if s["id"] == "colorations")["groupes"]
        if contenu(g))

    s = next(x for x in C.SECTIONS if x["id"] == "colorations")
    return f"""<section class="section" id="colorations" aria-labelledby="t-colorations">
  <div class="wrap">
    {tete_section(s)}
    <div class="gammes">
{chr(10).join(cartes)}
    </div>
    <p class="dilution">{C.DILUTION}</p>
{groupes}
  </div>
</section>"""


def tete_section(s):
    return f"""<header class="tete">
      <p class="tete__num">{s['numero']}</p>
      <h2 class="tete__titre" id="t-{s['id']}">{s['titre']}</h2>
      <p class="tete__intro">{s['intro']}</p>
    </header>"""


def section(s, alt):
    # Un groupe vidé de ses références ne laisse pas d'en-tête orpheline.
    groupes = "\n".join(groupe(g) for g in s["groupes"] if contenu(g))
    return f"""<section class="section{' section--alt' if alt else ''}" id="{s['id']}" aria-labelledby="t-{s['id']}">
  <div class="wrap">
    {tete_section(s)}
{groupes}
  </div>
</section>"""


def nav():
    liens = [("offre", "Offre")]
    liens += [(s["id"], s.get("nav", s["titre"])) for s in C.SECTIONS]
    return "".join(f'<a href="#{i}">{t}</a>' for i, t in liens)


# --------------------------------------------------------------------------- #
# Données exportées vers le JavaScript
# --------------------------------------------------------------------------- #

def donnees_json():
    # Une référence commandable, une entrée : c'est ce qui garantit qu'une
    # même carte affichée dans deux sections alimente une seule ligne de panier.
    produits = {
        ref: {"nom": p["nom"], "fmt": p["contenance"], "prix": p["prix"]}
        for ref, p in C.PRODUITS.items() if not p["attente"]
    }
    gammes = {}
    for col in C.COLORATIONS:
        donnees = N.PROFESIA if col["gamme"] == "profesia" else N.EKSTRA
        gammes[col["gamme"]] = {
            "nom": col["nom"],
            "prix": col["prix"],
            "nuances": [code for _, codes in donnees["familles"] for code, _ in codes],
        }
    return {
        "produits": produits,
        "gammes": gammes,
        "seuil": C.OFFRE["seuil"],
        "tel": C.TELEPHONE_WHATSAPP,
    }


# --------------------------------------------------------------------------- #
# Page
# --------------------------------------------------------------------------- #

def rendre():
    j = date.today()
    maj = f"{j.day} {MOIS[j.month - 1]} {j.year}"

    autres = [s for s in C.SECTIONS if s["id"] != "colorations"]
    corps = [bloc_ouverture(maj), bloc_colorations()]
    corps += [section(s, alt=(i % 2 == 0)) for i, s in enumerate(autres)]

    data = json.dumps(donnees_json(), ensure_ascii=False, separators=(",", ":"))

    return typo(f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Laly Cosmetics — Catalogue professionnel</title>
<meta name="description" content="Catalogue professionnel Laly Cosmetics : colorations, soins, technique et gamme homme aux tarifs professionnels HT. Commande directe par WhatsApp.">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#171514">
<meta property="og:title" content="Laly Cosmetics — Catalogue professionnel">
<meta property="og:description" content="Tarifs professionnels HT pour les salons de coiffure. Colorations, soins, technique et gamme homme.">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/img/laly-icone.png">
<link rel="icon" href="assets/img/laly-icone.png" sizes="any">
<link rel="apple-touch-icon" href="assets/img/laly-icone.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&amp;family=Jost:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap">
<link rel="stylesheet" href="assets/laly.css">
</head>
<body>
<a class="saut" href="#offre">Aller au catalogue</a>

<header class="entete">
  <div class="wrap entete__haut">
    <a class="entete__logo" href="#haut" aria-label="Laly Cosmetics — haut de page">
      <img src="assets/img/laly-logo.webp" alt="Laly Cosmetics" width="640" height="405">
    </a>
    <div class="entete__outils">
      <div class="rech">
        <label class="u-lecteur" for="rech">Rechercher une référence</label>
        <input id="rech" type="search" placeholder="Rechercher une référence" autocomplete="off" data-rech>
      </div>
      <button type="button" class="panier-b" data-ouvre>
        <span>Ma commande</span>
        <span class="panier-b__n" data-compteur hidden>0</span>
      </button>
    </div>
  </div>
  <nav class="entete__nav" aria-label="Sections du catalogue">
    <div class="wrap piste">{nav()}</div>
  </nav>
</header>

<main id="haut">

{chr(10).join(corps)}

</main>

<footer class="pied">
  <div class="wrap pied__grille">
    <div class="pied__marque">
      <img src="assets/img/laly-logo-blanc.webp" alt="Laly Cosmetics" width="640" height="405">
      <p>{C.BASELINE}</p>
    </div>
    <div class="pied__col">
      <h2>Commander</h2>
      <p>Composez votre commande dans le catalogue, puis envoyez-la sur WhatsApp
        au {C.TELEPHONE_AFFICHE}. La disponibilité et la date de livraison vous
        sont confirmées en retour.</p>
    </div>
    <div class="pied__col">
      <h2>Tarifs</h2>
      <p>Prix professionnels en euros hors taxes, par unité. L'offre 24 achetées
        = 24 offertes s'applique séparément à chaque gamme de coloration et ne se
        cumule avec aucune autre remise.</p>
      <p class="pied__maj">Catalogue à jour au {maj}</p>
    </div>
  </div>
</footer>

<button type="button" class="haut-page" data-haut aria-label="Revenir en haut de page" hidden>↑</button>

<div class="voile" data-voile hidden></div>

<!-- Les confirmations d'ajout s'empilent ici. aria-live="polite" les annonce
     aux lecteurs d'écran sans jamais interrompre la navigation. -->
<div class="avis" data-avis role="status" aria-live="polite"></div>

<aside class="panier" data-panier aria-label="Ma commande" aria-hidden="true" hidden>
  <header class="panier__tete">
    <h2 class="panier__titre">Ma commande</h2>
    <button type="button" class="panier__fermer" data-ferme aria-label="Fermer le récapitulatif">×</button>
  </header>

  <div class="panier__corps" data-panier-corps>
    <p class="panier__vide" data-vide>Votre commande est vide. Ajoutez des références
      depuis le catalogue.</p>
    <div class="panier__blocs" data-blocs></div>
  </div>

  <div class="panier__pied">
    <p class="panier__alerte" data-panier-alerte hidden role="alert"></p>
    <p class="total"><span>Total HT</span><span class="total__v" data-total>0,00 €</span></p>

    <div class="champ">
      <label for="salon">Nom du salon</label>
      <input id="salon" type="text" autocomplete="organization" data-salon placeholder="Salon Laly, Paris">
    </div>
    <div class="champ">
      <label for="livraison">Date de livraison souhaitée</label>
      <input id="livraison" type="date" data-livraison>
      <p class="champ__note">Date de livraison souhaitée, sous réserve de confirmation.</p>
    </div>

    <a class="bouton bouton--wa" data-whatsapp href="#" target="_blank" rel="noopener">
      Envoyer ma commande sur WhatsApp</a>
    <button type="button" class="lien-vider" data-vider>Vider la commande</button>
  </div>
</aside>

<script id="donnees" type="application/json">{data}</script>
<script src="assets/laly.js" defer></script>
</body>
</html>
""")


# --------------------------------------------------------------------------- #
# Vérifications
# --------------------------------------------------------------------------- #

def verifier():
    """Contrôle la cohérence du modèle avant d'écrire la page."""
    sans_photo, a_valider, non_commandables, orphelines = [], [], [], []

    for ref, p in sorted(C.PRODUITS.items()):
        if not isinstance(p["prix"], int) or p["prix"] <= 0:
            print(f"  !! prix invalide : {ref}", file=sys.stderr)
        if p["image"] is None:
            sans_photo.append(f"{p['nom']} {p['contenance']}")
        else:
            if not os.path.exists(os.path.join(IMG, p["image"] + ".webp")):
                print(f"  !! image absente du disque : {p['image']}.webp "
                      f"({p['nom']})", file=sys.stderr)
            if p["photo_a_valider"]:
                a_valider.append(f"{p['nom']} {p['contenance']} → {p['image']}")
        if p["attente"]:
            non_commandables.append(f"{p['nom']} {p['contenance']} — {p['attente']}")

    # Toute référence citée par une section doit exister, et toute référence
    # du catalogue doit être affichée quelque part.
    citees = set()
    for s in C.SECTIONS:
        for g in s["groupes"]:
            for ref in g.get("refs", []):
                if ref not in C.PRODUITS:
                    print(f"  !! référence inconnue : {ref} ({s['titre']} / "
                          f"{g['nom']})", file=sys.stderr)
                citees.add(ref)
            for _, ref in (g.get("variantes") or {}).get("variantes", []):
                if ref not in C.PRODUITS:
                    print(f"  !! variante inconnue : {ref}", file=sys.stderr)
                citees.add(ref)
    orphelines = sorted(set(C.PRODUITS) - citees)
    for ref in orphelines:
        print(f"  !! référence jamais affichée : {ref}", file=sys.stderr)

    for col in C.COLORATIONS:
        if not os.path.exists(os.path.join(IMG, col["image"] + ".webp")):
            print(f"  !! image absente : {col['image']}.webp", file=sys.stderr)

    return len(C.PRODUITS), sans_photo, a_valider, non_commandables


def main():
    total, sans_photo, a_valider, non_commandables = verifier()

    sortie = os.path.join(RACINE, "index.html")
    with open(sortie, "w", encoding="utf-8") as f:
        f.write(rendre())

    n_prof = sum(len(c) for _, c in N.PROFESIA["familles"])
    n_ekst = sum(len(c) for _, c in N.EKSTRA["familles"])

    print(f"index.html généré · {total + len(C.COLORATIONS)} références "
          f"({total} au prix unitaire, {len(C.COLORATIONS)} gammes de coloration)")
    print(f"  nuancier : {n_prof} nuances Profesia Hair, {n_ekst} Ekstra Color")

    if sans_photo:
        print(f"\n  Sans photographie ({len(sans_photo)}) — vignette d'attente :",
              file=sys.stderr)
        for x in sans_photo:
            print(f"    · {x}", file=sys.stderr)
    if a_valider:
        print(f"\n  Photographie à valider ({len(a_valider)}) :", file=sys.stderr)
        for x in a_valider:
            print(f"    · {x}", file=sys.stderr)
    if non_commandables:
        print(f"\n  Non commandables ({len(non_commandables)}) :", file=sys.stderr)
        for x in non_commandables:
            print(f"    · {x}", file=sys.stderr)


if __name__ == "__main__":
    main()
