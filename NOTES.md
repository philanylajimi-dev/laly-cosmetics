# Points à confirmer avant diffusion

Rien n'a été inventé : ce qui suit est ce que le catalogue affiche en attendant
une confirmation de Laly Cosmetics.

**55 références** au catalogue, 7 sections, 56 cartes affichées (cinq produits paraissent à la fois dans leur section générale et dans leur gamme, les trois poudres tiennent sur une fiche unique).

## 1. Le numéro WhatsApp — à vérifier en premier

Le brief donnait deux écritures incompatibles du même numéro :

| Source | Valeur |
|---|---|
| Numéro affiché | 07 68 57 21 30 |
| Format international | +33 7 68 57 21 30 |
| « Format technique » du brief | `3368572130` — **10 chiffres** |

En retirant le 0 initial, 07 68 57 21 30 donne `768572130`, et avec l'indicatif
`33768572130`, soit **11 chiffres**. Le format technique du brief perdait le 7.
Le catalogue utilise `33768572130`, le numéro réellement composable.

**À faire** : composer une commande d'essai, l'envoyer, vérifier qu'elle arrive.
Si le bon numéro était un autre, corriger `TELEPHONE_WHATSAPP` dans
`build/catalogue.py` et régénérer.

## 2. Références retirées du catalogue (8)

Supprimées sur demande, le 24 octobre 2026 : fiches, recherche et système de
commande. Le groupe « Protection thermique » a disparu avec sa seule référence,
et le groupe « Extra Wave » ne contient plus que le neutralisant.

1. Masque No Yellow 500 ml
2. Shampoing No Yellow 500 ml
3. Lotion Curl 100 ml
4. Fluide riche Curl 250 ml
5. Shampoing Frequent Hair Care 300 ml
6. Lotion Frequent 100 ml
7. Permanente Extra Wave 500 ml
8. Spray Protection Thermal

## 3. Références affichées mais non commandables (1)

| Référence | En attente de |
|---|---|
| Shampoing No Yellow 1 000 ml | Disponibilité France — le stock signalé était celui d'AF Lix Lox Suisse |

Pour la rendre commandable : retirer son `attente="…"` dans
`build/catalogue.py`, régénérer.

Les trois poudres décolorantes, jusqu'ici bloquées faute de contenance, sont
désormais commandables : leur contenance de 500 g a été confirmée le
24 octobre 2026 et la mention « Contenance à confirmer » a disparu.

## 4. Recherche de photographies — ce qui a été fouillé

Quatre sources ont été passées en revue, le 24 octobre 2026 :

| Source | Résultat |
|---|---|
| `~/Documents/GitHub/aflixlox-catalogue-suisse` | 80 images, **identiques** aux 78 packshots déjà présents + 2 logos |
| `~/Documents/GitHub/aflixlox-shopify` (thème) | 24 images, uniquement des bannières de rubrique, aucun packshot |
| `~/Downloads/theme_export__…29SEP2026` | aucune image |
| Historique Git des deux dépôts | seules les 4 fiches activateurs 150 ml, écartées par le brief |
| Boutique Shopify AF Lix Lox (API Admin) | même fonds produit que l'export ; **aucun** des formats manquants n'y existe |
| **Bibliothèque de fichiers Shopify** | **144 visuels fournisseur** non rattachés à des produits — c'est là qu'a été retrouvée la crème à barbe |

**1 photographie récupérée** : Crème à barbe X Men 500 ml. L'étiquette porte
« X MEN — CREMA DA RASATURA / SHAVE CREAM » et « 16.9 fl.oz », soit 500 ml
exactement : le nom, la gamme et la contenance correspondent tous les trois.

## 5. Références sans photographie : aucune

Les six vignettes « Visuel à venir » ont toutes disparu, par arbitrage du
24 octobre 2026 :

| Référence | Décision |
|---|---|
| Lotion Loss | contenance corrigée en **150 ml** — visuel fournisseur retrouvé |
| Masque Dry Hair Care | format corrigé en **1 500 ml** — visuel retrouvé |
| Masque Curl Hair Care 1 000 ml | **supprimée** |
| Masque Greasy Hair Care 500 ml | **supprimée** |
| Masque Greasy Hair Care 1 000 ml | **supprimée** |
| Décoloration 10 tons | fondue dans la fiche unique des poudres |

Ces arbitrages confirment ce que la recherche avait établi : la gamme
fournisseur ne comporte ni masque Dry 1 000 ml, ni masque Curl 1 000 ml, ni
masque Greasy, ni lotion Loss 100 ml.

## 6. Photographies plausibles mais non validées (10)

Le visuel retenu correspond à la gamme et à la contenance, mais le nom du
produit français diffère de celui de la fiche d'origine, ou plusieurs visuels
étaient possibles.

| Référence | Visuel utilisé | Doute |
|---|---|---|
| Frequent Hair Care 10 L | Shampoing amande | Amande ou graines de lin ? |
| Crème volumisante Dry 200 ml | Crème hydratante Dry 200 ml | Même produit ? |
| Soin express Botox 200 ml | Masque spray Botox 10 en 1 | Même produit ? |
| Gel coiffant 500 ml | Gel One Trillion 500 ml | Trois gels possibles |
| Cire Aqua 100 ml | Acqua Wax Night | Ou Extreme Water Wax ? |
| Cire coiffante 100 ml | Cire à l'argile effet mat | Ou pâte mate ? |
| Poudre volume 10 g | Poudre volumisante effet mat | Contenance jamais documentée |
| After Shave 400 ml | Après-rasage glacé | Ou après-rasage Belief ? |
| Poudre décolorante Profesia Hair | Sachet neutre, 500 g | Un seul visuel pour les trois puissances |

**Le visuel unique des poudres mérite un mot.** Vous avez demandé une seule
photographie pour les trois puissances. Le fonds n'en contient que deux formes :
un sachet bleu, le seul où la marque « profésia » est lisible, mais étiqueté
« DECOLORANTE BLU COMPATTO » — donc faux dès qu'on sélectionne 9 ou 10 tons —
et un sachet gris sans étiquette lisible. **C'est le gris qui a été retenu**,
neutre vis-à-vis des trois puissances. Si vous préférez le sachet de marque,
copier `poudre-decolorante-bleue-7-tons-500-g.webp` sur
`poudre-decolorante-profesia-500-g.webp` suffit.

Il existe par ailleurs un packshot de pot noir, net, étiqueté « POLVERE
DECOLORANTE GRIGIA NOVE TONI — 500 g », bien meilleur que les sachets. Il montre
un pot, pas un sachet : il contredirait la mention « sachet » du catalogue.
À votre main.

## 7. Nuanciers — validés

Le nuancier officiel fourni (`source-marque/nuancier.HEIC`) couvre la gamme
**Profesia Hair** : 70 nuances, 17 familles, reprises exactement.

**Ekstra Color** : ses 41 nuances ont été **validées par Laly Cosmetics le
24 octobre 2026**. Le bandeau d'avertissement a été retiré. Deux particularités
d'affichage subsistent, sans incidence sur les codes :

- deux nuances, 5/46 et 6/46, n'ont pas d'équivalent de famille dans le
  nuancier Profesia : elles sont regroupées sous « Reflets 46 », sans nom
  inventé ;
- quatre boosters (argent, bleu, rouge, violet) s'affichent sans libellé,
  faute de désignation fournisseur.

Les 111 codes sont figés dans `build/nuancier.py`. Aucun n'a été modifié.

## 8. Accueil allégé — deux sections retirées

Les sections « Bidons 10 litres » et « Masques grand format », qui suivaient
les colorations, ont été retirées le 24 octobre 2026. Leurs **cinq produits
n'ont pas été supprimés** : ils restent visibles dans leur gamme, section
« Soins par gamme ».

| Référence | Désormais visible dans |
|---|---|
| Dry Hair Care 10 L | Dry Hair Care |
| Frequent Hair Care 10 L | Frequent Hair Care |
| Masque Dry Hair Care 1 500 ml | Dry Hair Care |
| Masque Color Hair Care 1 000 ml | Color Hair Care |
| Masque Botox 1 000 ml | Botox Hair Therapy |

Chaque référence ne paraît donc plus qu'une seule fois. La mention « Aucune
promotion sur les bidons » a suivi les bidons dans leurs gammes.

Le modèle reste capable d'afficher un produit à plusieurs endroits : il suffit
d'ajouter son identifiant à la liste `refs` d'un autre groupe, dans `SECTIONS`
(`build/catalogue.py`). `PRODUITS` restant la source unique, nom, prix,
contenance et visuel seraient identiques partout, et le panier — indexé par
identifiant — n'en ferait qu'une seule ligne.

## 9. Écarts avec l'ancien catalogue suisse

- Le nuancier officiel ajoute **5 nuances** absentes du fonds suisse : 12/11 SS,
  12/22 SS, T.02, T.12, T.21. Elles sont au catalogue.
- Il ne contient **pas** la nuance 10/00, qui existait côté suisse : elle a été
  écartée, le nuancier officiel faisant foi.
- La section « Autour du poste » de l'ancien catalogue (nuancier physique,
  rouleau de lit, gommage corporel) **disparaît** : aucune de ses références
  ne figure dans la grille française.
- 25 packshots de l'ancien catalogue restent dans `assets/img/p/` sans être
  utilisés. Ils ne pèsent sur rien et serviront si une référence est ajoutée.

## 10. L'offre n'affiche plus ses conditions détaillées

L'ouverture se limite désormais à l'annonce « 24 colorations achetées = 24
colorations offertes ». Le tableau des paliers et la liste des six règles ont
été retirés de la page sur demande.

**Le calcul, lui, n'a pas bougé** : seuil de 24 tubes, par gamme, sans
addition entre Profesia Hair et Ekstra Color. Les paliers et les règles restent
consignés dans `OFFRE` (`build/catalogue.py`) et pilotent toujours le panier.

Conséquence à connaître : un salon qui commande 20 tubes ne lit plus nulle part
pourquoi rien ne lui est offert. Le compteur de la section Colorations l'indique
en direct (« 4 tubes avant l'offre »), mais plus aucun texte ne l'explique en
amont. Si cela pose problème à l'usage, une ligne sous l'annonce suffirait.

## 11. Fonctions de gamme — quatre libellés à valider

Chaque gamme porte désormais sa fonction en français sous son nom anglais.
Sept libellés viennent de vous ; les quatre autres ont été rédigés ici, d'après
l'usage réel des produits de la gamme :

| Gamme | Fonction affichée | Source |
|---|---|---|
| Dandruff Hair Care | Anti-pelliculaire | vous |
| Greasy Hair Care | Cheveux gras | vous |
| Dry Hair Care | Cheveux secs | vous |
| Color Hair Care | Cheveux colorés | vous |
| No Yellow Hair Care | Anti-reflets jaunes | vous |
| Botox Hair Therapy | Réparation et revitalisation des cheveux | vous |
| Extra Wave | Permanente et ondulation des cheveux | vous |
| **Frequent Hair Care** | **Lavages fréquents** | rédigé ici |
| **Curl Hair Care** | **Cheveux bouclés** | rédigé ici |
| **Loss Hair Care** | **Anti-chute et cheveux fins** | rédigé ici |
| **Nano Repair** | **Lissage réparateur** | rédigé ici |

Les groupes déjà nommés en français — Activateurs, Poudres décolorantes,
Shampoings de bac, Coiffage, Rasage — n'ont pas reçu de fonction : leur nom la
dit déjà. Les deux gammes de coloration gardent leur sous-titre existant.

Pour corriger un libellé : la clé `fonction` du groupe, dans `SECTIONS`
(`build/catalogue.py`).

## 12. Affichage sur téléphone

En dessous de 576 px, les cartes passent à **deux par ligne** : le visuel
descend de 354 px à 137–192 px selon l'appareil, et la page de produits est
deux fois moins haute. Les photographies ne sont ni rognées ni déformées —
elles gardent leur cadre carré et `object-fit: contain`.

Le sélecteur de quantité et le bouton « Ajouter », qui ne tiennent plus côte à
côte sur une demi-largeur, s'empilent sur toute la largeur de la carte.

Le bouton flottant « retour en haut » **disparaît sur téléphone** : il venait
nécessairement recouvrir une commande de quantité. La barre d'onglets reste
visible en permanence et son premier onglet ramène à l'ouverture.

L'affichage sur ordinateur et sur tablette est inchangé : mêmes colonnes,
mêmes tailles de visuel qu'avant.

## 13. Offre : une seule grille, répartition déduite

Depuis le 26 octobre 2026, le salon ne choisit plus ses cadeaux séparément.
Il prend toutes ses nuances dans la grille habituelle ; le catalogue déduit
seul ce qui est payant et ce qui est offert, et l'affiche sous la grille :
tubes sélectionnés, payants, offerts, montant à payer.

La règle, tenue en un seul endroit — `repartition()` dans `build/catalogue.py`,
avec sa jumelle dans `assets/laly.js` :

| Sélection | Payants | Offerts |
|---|---|---|
| ≤ 24 | tout | 0 |
| 25 à 47 | 24 | le reste |
| 48 et au delà | la moitié, arrondie au supérieur | l'autre moitié |

Soit : les payants ne descendent jamais sous le seuil, ni sous la moitié de la
sélection, puisqu'un tube offert doit être couvert par un tube payant.
30 → 24 + 6 · 48 → 24 + 24 · 50 → 25 + 25 · 60 → 30 + 30.

Conséquence : le dépassement est devenu **impossible par construction**.
L'alerte et le verrou sur l'envoi WhatsApp, qui protégeaient l'ancienne saisie
manuelle, ont été retirés faute d'objet.

L'offre reste propre à chaque gamme : Profesia Hair et Ekstra Color ne
s'additionnent pas.

## 14. Message WhatsApp : les tubes offerts en déduction

Le modèle de message demandé le 26 octobre 2026 prévoit, pour chaque
coloration, une ligne « nom – Nuance X » suivie de
« quantité × prix unitaire = sous-total ». Il ne prévoyait pas les tubes
offerts, qui ne sont rattachés à aucune nuance en particulier puisque le salon
choisit librement dans une seule grille.

Depuis le 26 octobre 2026, le bloc tient en un en-tête de gamme, une ligne par
nuance et **une seule ligne de récapitulation** :

    Profesia Hair – Colorations 100 ml

    Nuance 7/0 : 20 tubes

    Nuance 6/1 : 18 tubes

    Nuance 12/22 SS : 12 tubes

    50 tubes (dont 25 offerts)

Sans promotion, la dernière ligne se limite au total — jamais de « dont
0 offert ». Les quantités annoncées par nuance sont les quantités totales,
tubes offerts compris.

**À savoir** : le montant des colorations ne figure plus dans le message. Les
lignes « Tubes payants » et « Tubes OFFERTS », qui le portaient, ont été
retirées sur demande. Sur une commande mixte, le destinataire lit le détail
chiffré des produits, puis les colorations sans montant, et le total général
en fin de message. Pour le rétablir, ajouter `+ ' = ' + euros(g.prix *
r.payants)` à la ligne de récapitulation, dans `message()` (`assets/laly.js`).

## 15. Autres points

- **TVA** : le catalogue affiche des prix HT, mentionnés comme tels partout.
  Aucun taux n'est appliqué ni affiché, faute d'instruction.
- **Frais de port** : aucun, conformément au brief.
- **Échelle des photos** : les packshots du fournisseur sont tous cadrés plein
  format. Un flacon de 300 ml et un de 1 000 ml apparaissent donc de taille
  comparable. La contenance est affichée au-dessus de chaque nom pour éviter
  toute confusion.
- **Nuancier en couleur** : la photographie fournie permettrait d'extraire des
  pastilles de couleur par nuance, mais elle est prise de biais et sous une
  lumière inégale — les teintes seraient fausses. Un scan à plat permettrait
  d'ajouter un aperçu couleur à côté de chaque code.
