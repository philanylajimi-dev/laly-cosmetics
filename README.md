# Laly Cosmetics — Catalogue professionnel France

Catalogue de prix destiné aux salons de coiffure français, partagé par WhatsApp.
Page statique : pas de compte, pas de paiement en ligne. Le salon compose sa
commande, le catalogue calcule le montant HT, et le bouton WhatsApp ouvre une
conversation avec le message déjà rédigé.

Projet autonome. Il reprend l'organisation et les photographies de l'ancien
catalogue suisse AF Lix Lox — archivé dans `reference/` — mais ses produits,
ses prix, son offre et son identité lui sont propres.

## Structure

```
index.html              page générée — ne pas éditer à la main
assets/laly.css         direction artistique
assets/laly.js          commande, calculs, message WhatsApp
assets/img/laly-*.webp  logo détouré, version claire, icône
assets/img/p/           packshots produit
build/catalogue.py      produits, prix, sections, offre
build/nuancier.py       nuances de coloration
build/generate.py       générateur
reference/              catalogue suisse d'origine — jamais publié
source-marque/          logo original et photo du nuancier — jamais publiés
```

## Régénérer la page

```sh
python3 build/generate.py
```

Aucune dépendance : Python 3 seul suffit. Le script affiche les références sans
photographie, celles dont le visuel reste à valider et celles qui ne sont pas
commandables.

## Modifier le catalogue

Tout se passe dans `build/catalogue.py`, puis on régénère.

- **Un prix** — la valeur est en **centimes d'euro HT**, entière : `1290` vaut
  12,90 €. Tous les calculs se font en centimes, jamais en virgule flottante.
- **Une photographie** — remplacer `None` par le nom du fichier déposé dans
  `assets/img/p/`, sans l'extension `.webp`.
- **Rendre une référence commandable** — supprimer son `attente="…"`. Elle
  gagne aussitôt son sélecteur de quantité et son bouton d'ajout.
- **Ajouter ou retirer une référence** — ajouter ou retirer une ligne `P(...)`
  dans la bonne section. Le `ref` est l'identifiant du panier : une fois le
  catalogue diffusé, ne plus le changer, sinon les commandes en cours chez les
  salons perdent la ligne concernée.
- **L'offre** — `OFFRE` et `tubes_offerts()`. Le seuil, les paliers affichés et
  le calcul du panier découlent tous de ces deux endroits.
- **Le numéro WhatsApp** — `TELEPHONE_AFFICHE` et `TELEPHONE_WHATSAPP`.

Les nuances vivent dans `build/nuancier.py`. Pour retirer une nuance
indisponible, supprimer sa ligne ; pour en ajouter une, l'insérer dans sa
famille avec son code exact.

## Mettre en ligne — GitHub Pages

Le catalogue est entièrement statique : il n'a besoin d'aucun serveur et
fonctionne Mac éteint.

Le dépôt local est déjà initialisé, le premier commit est fait et le dépôt
distant est déclaré. Il reste à créer le dépôt `laly-cosmetics` sur GitHub,
puis :

```sh
git push -u origin main
```

Puis, sur GitHub : **Settings → Pages → Source : Deploy from a branch →
`main` / `/ (root)`**. L'adresse publique est
`https://philanylajimi-dev.github.io/laly-cosmetics/`.

Cette adresse ne change plus. Pour mettre à jour les produits ou les prix :
modifier `build/catalogue.py`, relancer `python3 build/generate.py`, puis
`git add . && git commit -m "…" && git push`. Le site se met à jour seul en une
minute environ.

`.gitignore` tient `reference/` et `source-marque/` hors du dépôt : ces deux
dossiers restent sur le Mac et ne sont jamais publiés. **Conservez-en une copie
de sauvegarde** : ils contiennent le logo original et la photographie du
nuancier.

`.nojekyll` évite que GitHub Pages n'essaie d'interpréter le dossier comme un
site Jekyll.

## Prévisualiser sur le Mac

Ouvrir `index.html` directement dans le navigateur suffit pour relire la page.
Pour être dans les mêmes conditions que GitHub Pages :

```sh
cd ~/Desktop/laly-cosmetics-catalogue
python3 -m http.server 8000
```

puis `http://localhost:8000` dans le navigateur. `Ctrl+C` arrête le serveur.

## Points ouverts

Voir `NOTES.md`.
