/**
 * Laly Cosmetics — catalogue professionnel.
 *
 * Trois responsabilités, pas une de plus :
 *   1. tenir la commande en cours (produits, nuances achetées, nuances offertes) ;
 *   2. en déduire les montants, en centimes entiers ;
 *   3. rédiger le message WhatsApp, strictement identique au récapitulatif.
 *
 * Le catalogue reste lisible et imprimable sans JavaScript : seule la prise de
 * commande disparaît.
 */

(function () {
  'use strict';

  var DONNEES = JSON.parse(document.getElementById('donnees').textContent);
  var CLE = 'laly-commande';

  /* ---- État --------------------------------------------------------- */

  var etat = {
    produits: {},   // ref -> quantité
    achats: {},     // gamme -> { nuance: quantité }
    offerts: {},    // gamme -> { nuance: quantité }
    salon: '',
    livraison: ''
  };

  Object.keys(DONNEES.gammes).forEach(function (g) {
    etat.achats[g] = {};
    etat.offerts[g] = {};
  });

  function charger() {
    try {
      var brut = sessionStorage.getItem(CLE);
      if (!brut) return;
      var lu = JSON.parse(brut);
      if (!lu || typeof lu !== 'object') return;
      // On ne reprend que ce qui existe encore au catalogue : un prix ou une
      // nuance retirés ne doivent jamais ressusciter dans une commande.
      Object.keys(lu.produits || {}).forEach(function (ref) {
        if (DONNEES.produits[ref]) etat.produits[ref] = entier(lu.produits[ref]);
      });
      ['achats', 'offerts'].forEach(function (champ) {
        Object.keys(lu[champ] || {}).forEach(function (g) {
          if (!DONNEES.gammes[g]) return;
          Object.keys(lu[champ][g] || {}).forEach(function (n) {
            if (DONNEES.gammes[g].nuances.indexOf(n) !== -1) {
              etat[champ][g][n] = entier(lu[champ][g][n]);
            }
          });
        });
      });
      etat.salon = typeof lu.salon === 'string' ? lu.salon : '';
      etat.livraison = typeof lu.livraison === 'string' ? lu.livraison : '';
    } catch (err) {
      /* sessionStorage indisponible ou contenu illisible : on repart à zéro. */
    }
  }

  function sauver() {
    try { sessionStorage.setItem(CLE, JSON.stringify(etat)); } catch (err) {}
  }

  function entier(v) {
    var n = parseInt(v, 10);
    return isFinite(n) && n > 0 ? n : 0;
  }

  /* ---- Calculs ------------------------------------------------------ */

  function somme(objet) {
    return Object.keys(objet).reduce(function (t, c) { return t + objet[c]; }, 0);
  }

  /** La mécanique de l'offre : à partir du seuil, un tube offert par tube acheté. */
  function droitOfferts(gamme) {
    var achetes = somme(etat.achats[gamme]);
    return achetes >= DONNEES.seuil ? achetes : 0;
  }

  function resteARepartir(gamme) {
    return droitOfferts(gamme) - somme(etat.offerts[gamme]);
  }

  /** Total hors taxes, en centimes : aucun flottant n'intervient. */
  function totalCents() {
    var t = 0;
    Object.keys(etat.produits).forEach(function (ref) {
      t += DONNEES.produits[ref].prix * etat.produits[ref];
    });
    Object.keys(etat.achats).forEach(function (g) {
      t += DONNEES.gammes[g].prix * somme(etat.achats[g]);
    });
    return t;
  }

  function nbArticles() {
    var n = Object.keys(etat.produits).length;
    Object.keys(etat.achats).forEach(function (g) {
      n += Object.keys(etat.achats[g]).length;
    });
    return n;
  }

  function euros(cents) {
    return (cents / 100).toFixed(2).replace('.', ',') + ' €';
  }

  /* ---- Garde-fous --------------------------------------------------- */

  /** Tubes offerts sélectionnés au delà du droit acquis.
   *
   * On ne rogne plus la sélection dans le dos du salon : s'il retire des
   * tubes payants après avoir choisi ses cadeaux, il garde sa sélection sous
   * les yeux, le catalogue le lui dit, et l'envoi reste bloqué tant qu'il n'a
   * pas corrigé. Une correction silencieuse ferait disparaître des nuances
   * sans que personne ne s'en aperçoive avant la livraison.
   */
  function excesOfferts(gamme) {
    return Math.max(0, somme(etat.offerts[gamme]) - droitOfferts(gamme));
  }

  function excesTotal() {
    return Object.keys(DONNEES.gammes).reduce(function (t, g) {
      return t + excesOfferts(g);
    }, 0);
  }

  /* ---- Nuanciers ----------------------------------------------------- */

  var blocsGamme = Array.prototype.slice.call(document.querySelectorAll('[data-gamme]'));

  blocsGamme.forEach(function (bloc) {
    var gamme = bloc.getAttribute('data-gamme');

    bloc.querySelectorAll('.nuance').forEach(function (cellule) {
      var code = cellule.getAttribute('data-nuance');
      cellule.querySelector('[data-nuance-plus]').addEventListener('click', function () {
        etat.achats[gamme][code] = (etat.achats[gamme][code] || 0) + 1;
        rendre();
      });
      cellule.querySelector('[data-nuance-moins]').addEventListener('click', function () {
        if (!etat.achats[gamme][code]) return;
        etat.achats[gamme][code] -= 1;
        if (etat.achats[gamme][code] <= 0) delete etat.achats[gamme][code];
        rendre();
      });
    });

    var select = bloc.querySelector('[data-offerts-select]');
    DONNEES.gammes[gamme].nuances.forEach(function (code) {
      var o = document.createElement('option');
      o.value = code;
      o.textContent = code;
      select.appendChild(o);
    });

    bloc.querySelector('[data-offerts-ajout]').addEventListener('click', function () {
      if (resteARepartir(gamme) <= 0) return;
      var code = select.value;
      etat.offerts[gamme][code] = (etat.offerts[gamme][code] || 0) + 1;
      rendre();
    });

    bloc.querySelector('[data-offerts-miroir]').addEventListener('click', function () {
      // Le cas courant : le salon veut les mêmes nuances en offert. Le droit
      // étant égal au nombre acheté, la copie tombe toujours juste.
      etat.offerts[gamme] = {};
      var droit = droitOfferts(gamme);
      if (!droit) return;
      Object.keys(etat.achats[gamme]).forEach(function (c) {
        etat.offerts[gamme][c] = etat.achats[gamme][c];
      });
      rendre();
    });

    var filtre = bloc.querySelector('[data-filtre]');
    var filtreVide = bloc.querySelector('[data-filtre-vide]');
    if (filtre) {
      filtre.addEventListener('input', function () {
        var q = filtre.value.trim().toLowerCase()
          .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        var trouves = 0;
        bloc.querySelectorAll('.nuance').forEach(function (c) {
          var texte = c.textContent.toLowerCase()
            .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
          var ok = !q || texte.indexOf(q) !== -1;
          c.classList.toggle('est-masque', !ok);
          if (ok) trouves++;
        });
        // Une famille sans nuance visible n'a plus lieu d'être affichée ;
        // celles qui en gardent s'ouvrent d'elles-mêmes, et se referment
        // quand le champ est vidé — sauf si le salon les avait ouvertes.
        bloc.querySelectorAll('.famille').forEach(function (f) {
          var garde = f.querySelectorAll('.nuance:not(.est-masque)').length;
          f.classList.toggle('est-masque', !!q && !garde);
          if (q) {
            if (!f.dataset.avant) f.dataset.avant = f.open ? 'ouverte' : 'fermee';
            f.open = garde > 0;
          } else if (f.dataset.avant) {
            f.open = f.dataset.avant === 'ouverte';
            delete f.dataset.avant;
          }
        });
        filtreVide.hidden = !q || trouves > 0;
      });
    }

    bloc.querySelector('[data-offerts-liste]').addEventListener('click', function (ev) {
      var b = ev.target.closest('button[data-off-action]');
      if (!b) return;
      var code = b.getAttribute('data-off-code');
      var action = b.getAttribute('data-off-action');
      if (action === 'plus') {
        if (resteARepartir(gamme) <= 0) return;
        etat.offerts[gamme][code] = (etat.offerts[gamme][code] || 0) + 1;
      } else if (action === 'moins') {
        etat.offerts[gamme][code] -= 1;
        if (etat.offerts[gamme][code] <= 0) delete etat.offerts[gamme][code];
      } else {
        delete etat.offerts[gamme][code];
      }
      rendre();
    });
  });

  function rendreGamme(bloc) {
    var gamme = bloc.getAttribute('data-gamme');
    var achetes = somme(etat.achats[gamme]);
    var droit = droitOfferts(gamme);
    var reste = resteARepartir(gamme);

    bloc.querySelectorAll('.nuance').forEach(function (cellule) {
      var code = cellule.getAttribute('data-nuance');
      var q = etat.achats[gamme][code] || 0;
      cellule.querySelector('[data-nuance-qte]').textContent = q;
      cellule.classList.toggle('est-choisie', q > 0);
    });

    bloc.querySelector('[data-compte-achetes]').textContent = achetes;
    bloc.querySelector('[data-compte-mot]').textContent =
      achetes > 1 ? ' tubes achetés' : ' tube acheté';

    var blocOff = bloc.querySelector('[data-compte-bloc-offerts]');
    blocOff.hidden = droit === 0;
    bloc.querySelector('[data-compte-offerts]').textContent = somme(etat.offerts[gamme]);

    var msgReste = '';
    if (achetes > 0 && achetes < DONNEES.seuil) {
      var manque = DONNEES.seuil - achetes;
      msgReste = 'Encore ' + manque + ' tube' + (manque > 1 ? 's' : '')
        + ' pour déclencher l’offre';
    }
    bloc.querySelector('[data-compte-reste]').textContent = msgReste;

    // Le panneau reste ouvert tant qu'une nuance offerte est sélectionnée,
    // même si le droit est retombé à zéro : sinon le salon ne pourrait plus
    // corriger ce que le catalogue lui reproche.
    var choisis = somme(etat.offerts[gamme]);
    var exces = excesOfferts(gamme);
    var zone = bloc.querySelector('[data-offerts]');
    zone.hidden = droit === 0 && choisis === 0;

    bloc.querySelector('[data-offerts-solde]').textContent =
      choisis + ' coloration' + (choisis > 1 ? 's' : '') + ' offerte'
      + (choisis > 1 ? 's' : '') + ' sélectionnée' + (choisis > 1 ? 's' : '')
      + ' sur ' + droit + ' disponible' + (droit > 1 ? 's' : '');

    var alerte = bloc.querySelector('[data-offerts-alerte]');
    alerte.hidden = exces === 0;
    if (exces) {
      alerte.textContent = droit === 0
        ? 'Votre commande est repassée sous ' + DONNEES.seuil + ' tubes : retirez '
          + 'les ' + choisis + ' coloration' + (choisis > 1 ? 's' : '') + ' offerte'
          + (choisis > 1 ? 's' : '') + ' ou complétez vos achats.'
        : exces + ' coloration' + (exces > 1 ? 's' : '') + ' offerte'
          + (exces > 1 ? 's' : '') + ' de trop : retirez-en ' + exces
          + ' pour pouvoir envoyer la commande.';
    }
    zone.classList.toggle('offerts--exces', exces > 0);
    bloc.querySelector('[data-offerts-ajout]').disabled = reste <= 0;

    // Combien de tubes dans chaque famille repliée : la quantité choisie ne
    // doit pas disparaître parce qu'on a refermé la catégorie.
    bloc.querySelectorAll('[data-famille]').forEach(function (fam) {
      var t = 0;
      fam.querySelectorAll('.nuance').forEach(function (c) {
        t += etat.achats[gamme][c.getAttribute('data-nuance')] || 0;
      });
      var badge = fam.querySelector('[data-famille-choisies]');
      badge.hidden = t === 0;
      badge.textContent = t + ' tube' + (t > 1 ? 's' : '');
    });

    var liste = bloc.querySelector('[data-offerts-liste]');
    liste.textContent = '';
    Object.keys(etat.offerts[gamme]).forEach(function (code) {
      var li = document.createElement('li');
      li.className = 'offerts__l';
      li.innerHTML =
        '<span class="offerts__code">' + code + '</span>' +
        '<span class="pas">' +
          '<button type="button" class="pas__b" data-off-action="moins" data-off-code="' + code + '" aria-label="Retirer un tube offert ' + code + '">−</button>' +
          '<span class="pas__n pas__n--txt">' + etat.offerts[gamme][code] + '</span>' +
          '<button type="button" class="pas__b" data-off-action="plus" data-off-code="' + code + '" aria-label="Ajouter un tube offert ' + code + '">+</button>' +
        '</span>' +
        '<button type="button" class="p-retire" data-off-action="retire" data-off-code="' + code + '">Retirer</button>';
      liste.appendChild(li);
    });
  }

  /* ---- Cartes produit ------------------------------------------------ */

  document.querySelectorAll('.carte__action').forEach(function (zone) {
    var champ = zone.querySelector('[data-pas-valeur]');
    var bouton = zone.querySelector('[data-ajout]');

    function lire() {
      var n = parseInt(champ.value, 10);
      return isFinite(n) && n > 0 ? n : 1;
    }

    zone.querySelector('[data-pas-moins]').addEventListener('click', function () {
      champ.value = Math.max(1, lire() - 1);
    });
    zone.querySelector('[data-pas-plus]').addEventListener('click', function () {
      champ.value = lire() + 1;
    });
    champ.addEventListener('change', function () { champ.value = lire(); });

    bouton.addEventListener('click', function () {
      var ref = bouton.getAttribute('data-ajout');
      if (!DONNEES.produits[ref]) return;
      var qte = lire();
      etat.produits[ref] = (etat.produits[ref] || 0) + qte;
      champ.value = 1;
      bouton.classList.add('est-ajoute');
      bouton.textContent = 'Ajouté';
      setTimeout(function () {
        bouton.classList.remove('est-ajoute');
        bouton.textContent = 'Ajouter';
      }, 1100);
      rendre();
      pastilleAnime();
      confirmer(ref, qte);
    });
  });

  /* ---- Confirmations d'ajout ------------------------------------------ */

  /* Un bandeau discret, jamais bloquant : le salon enchaîne ses ajouts sans
     avoir à fermer quoi que ce soit. Les avis s'empilent et s'effacent seuls. */
  var zoneAvis = document.querySelector('[data-avis]');

  function confirmer(ref, qte) {
    var p = DONNEES.produits[ref];
    if (!p || !zoneAvis) return;

    var avis = document.createElement('div');
    avis.className = 'avis__item';
    avis.innerHTML =
      '<span class="avis__coche" aria-hidden="true">✓</span>' +
      '<span class="avis__txt"><strong>' + qte + ' × ' + p.nom + '</strong>' +
      '<span class="avis__fmt">' + p.fmt + '</span></span>' +
      '<button type="button" class="avis__lien">Voir ma commande</button>';

    avis.querySelector('.avis__lien').addEventListener('click', function () {
      retirerAvis(avis);
      ouvrir();
    });

    zoneAvis.appendChild(avis);
    // Au delà de trois, on perd la lisibilité : le plus ancien part aussitôt.
    // Retrait immédiat, et non par `retirerAvis` : celui-ci diffère la
    // suppression le temps de l'animation, et la boucle tournerait sans fin
    // si plusieurs ajouts tombaient dans le même cycle.
    while (zoneAvis.children.length > 3) zoneAvis.firstElementChild.remove();

    requestAnimationFrame(function () { avis.classList.add('est-la'); });
    setTimeout(function () { retirerAvis(avis); }, 3600);
  }

  function retirerAvis(avis) {
    if (!avis || avis.dataset.part) return;
    avis.dataset.part = '1';
    avis.classList.remove('est-la');
    setTimeout(function () {
      if (avis.parentNode) avis.parentNode.removeChild(avis);
    }, 260);
  }

  /* ---- Fiches à variantes -------------------------------------------- */

  /* Une seule carte, plusieurs puissances. Chaque puissance garde sa propre
     référence : le panier et le message WhatsApp les distinguent d'eux-mêmes. */
  document.querySelectorAll('[data-variantes]').forEach(function (carte) {
    var select = carte.querySelector('[data-var-select]');
    var prix = carte.querySelector('[data-var-prix]');
    var bouton = carte.querySelector('[data-ajout]');

    select.addEventListener('change', function () {
      var ref = select.value;
      var p = DONNEES.produits[ref];
      if (!p) return;
      bouton.setAttribute('data-ajout', ref);
      var entier = Math.floor(p.prix / 100);
      var cents = ('0' + (p.prix % 100)).slice(-2);
      prix.innerHTML = entier + ',<span class="prix__c">' + cents + '</span>';
      carte.setAttribute('data-ref', ref);
    });
  });

  /* ---- Panier -------------------------------------------------------- */

  var panier = document.querySelector('[data-panier]');
  var voile = document.querySelector('[data-voile]');
  var ouvreur = document.querySelector('[data-ouvre]');

  function ouvrir() {
    panier.hidden = false;
    voile.hidden = false;
    // Un souffle avant d'animer, sinon le navigateur saute la transition.
    requestAnimationFrame(function () {
      panier.classList.add('est-ouvert');
      voile.classList.add('est-visible');
    });
    panier.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    panier.querySelector('[data-ferme]').focus();
  }

  function fermer() {
    panier.classList.remove('est-ouvert');
    voile.classList.remove('est-visible');
    panier.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    setTimeout(function () {
      panier.hidden = true;
      voile.hidden = true;
    }, 260);
    ouvreur.focus();
  }

  ouvreur.addEventListener('click', ouvrir);
  panier.querySelector('[data-ferme]').addEventListener('click', fermer);
  voile.addEventListener('click', fermer);
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape' && panier.classList.contains('est-ouvert')) fermer();
  });

  // Le focus ne doit pas s'échapper du tiroir tant qu'il est ouvert.
  panier.addEventListener('keydown', function (ev) {
    if (ev.key !== 'Tab') return;
    var cibles = panier.querySelectorAll(
      'button:not([disabled]), input, select, a[href], [tabindex]:not([tabindex="-1"])');
    if (!cibles.length) return;
    var premier = cibles[0];
    var dernier = cibles[cibles.length - 1];
    if (ev.shiftKey && document.activeElement === premier) {
      ev.preventDefault(); dernier.focus();
    } else if (!ev.shiftKey && document.activeElement === dernier) {
      ev.preventDefault(); premier.focus();
    }
  });

  var blocs = panier.querySelector('[data-blocs]');
  var vide = panier.querySelector('[data-vide]');

  blocs.addEventListener('click', function (ev) {
    var b = ev.target.closest('button[data-p-action]');
    if (!b) return;
    var ref = b.getAttribute('data-p-ref');
    var action = b.getAttribute('data-p-action');
    if (action === 'plus') etat.produits[ref] += 1;
    else if (action === 'moins') {
      etat.produits[ref] -= 1;
      if (etat.produits[ref] <= 0) delete etat.produits[ref];
    } else if (action === 'retire') delete etat.produits[ref];
    else if (action === 'voir') {
      fermer();
      document.getElementById('colorations').scrollIntoView();
      return;
    }
    rendre();
  });

  panier.querySelector('[data-vider]').addEventListener('click', function () {
    etat.produits = {};
    Object.keys(DONNEES.gammes).forEach(function (g) {
      etat.achats[g] = {};
      etat.offerts[g] = {};
    });
    rendre();
  });

  var champSalon = panier.querySelector('[data-salon]');
  var champDate = panier.querySelector('[data-livraison]');

  champSalon.addEventListener('input', function () {
    etat.salon = champSalon.value.trim();
    sauver();
    majLien();
  });
  champDate.addEventListener('change', function () {
    etat.livraison = champDate.value;
    sauver();
    majLien();
  });

  // Pas de date passée : le champ lui-même interdit la saisie.
  (function () {
    var j = new Date();
    var iso = j.getFullYear() + '-'
      + String(j.getMonth() + 1).padStart(2, '0') + '-'
      + String(j.getDate()).padStart(2, '0');
    champDate.min = iso;
  })();

  function ligneProduit(ref) {
    var p = DONNEES.produits[ref];
    var q = etat.produits[ref];
    return '<div class="p-ligne">' +
      '<div><p class="p-ligne__nom">' + p.nom + '</p>' +
      '<p class="p-ligne__fmt">' + p.fmt + '</p></div>' +
      '<p class="p-ligne__st">' + euros(p.prix * q) + '</p>' +
      '<div class="p-ligne__bas">' +
        '<span class="pas">' +
          '<button type="button" class="pas__b" data-p-action="moins" data-p-ref="' + ref + '" aria-label="Retirer une unité de ' + p.nom + '">−</button>' +
          '<span class="pas__n pas__n--txt">' + q + '</span>' +
          '<button type="button" class="pas__b" data-p-action="plus" data-p-ref="' + ref + '" aria-label="Ajouter une unité de ' + p.nom + '">+</button>' +
        '</span>' +
        '<span class="p-ligne__u">' + euros(p.prix) + ' l’unité</span>' +
        '<button type="button" class="p-retire" data-p-action="retire" data-p-ref="' + ref + '">Retirer</button>' +
      '</div>' +
    '</div>';
  }

  function ligneGamme(gamme, offert) {
    var g = DONNEES.gammes[gamme];
    var table = offert ? etat.offerts[gamme] : etat.achats[gamme];
    var codes = Object.keys(table);
    if (!codes.length) return '';
    var total = somme(table);
    var puces = codes.map(function (c) {
      return '<li>' + c + ' × ' + table[c] + '</li>';
    }).join('');

    return '<div class="p-ligne' + (offert ? ' p-ligne--offert' : '') + '">' +
      '<div><p class="p-ligne__nom">' + g.nom + (offert ? ' — offertes' : '') + '</p>' +
      '<p class="p-ligne__fmt">' + total + ' tube' + (total > 1 ? 's' : '') +
      ' · 100 ml</p></div>' +
      '<p class="p-ligne__st">' + (offert ? '0,00 €' : euros(g.prix * total)) + '</p>' +
      '<ul class="p-nuances">' + puces + '</ul>' +
      '<div class="p-ligne__bas">' +
        '<span class="p-ligne__u">' + (offert ? 'Offert' : euros(g.prix) + ' le tube') + '</span>' +
        '<button type="button" class="p-retire" data-p-action="voir">Modifier les nuances</button>' +
      '</div>' +
    '</div>';
  }

  function rendrePanier() {
    var morceaux = [];

    var refs = Object.keys(etat.produits);
    if (refs.length) {
      morceaux.push('<div class="p-bloc"><h3 class="p-bloc__titre">Produits</h3>' +
        refs.map(ligneProduit).join('') + '</div>');
    }

    var achats = Object.keys(DONNEES.gammes)
      .map(function (g) { return ligneGamme(g, false); })
      .filter(Boolean).join('');
    if (achats) {
      morceaux.push('<div class="p-bloc"><h3 class="p-bloc__titre">Colorations</h3>' +
        achats + '</div>');
    }

    var cadeaux = Object.keys(DONNEES.gammes)
      .map(function (g) { return ligneGamme(g, true); })
      .filter(Boolean).join('');
    if (cadeaux) {
      morceaux.push('<div class="p-bloc"><h3 class="p-bloc__titre">Colorations offertes</h3>' +
        cadeaux + '</div>');
    }

    blocs.innerHTML = morceaux.join('');
    vide.hidden = morceaux.length > 0;
    panier.querySelector('[data-total]').textContent = euros(totalCents());
  }

  /* ---- Message WhatsApp ---------------------------------------------- */

  function dateFr(iso) {
    if (!iso) return '';
    var p = iso.split('-');
    return p.length === 3 ? p[2] + '/' + p[1] + '/' + p[0] : iso;
  }

  function message() {
    var L = [];
    L.push('Bonjour,');
    L.push('');
    L.push('Je souhaite passer la commande suivante auprès de Laly Cosmetics :');
    L.push('');
    if (etat.salon) {
      L.push('Salon : ' + etat.salon);
      L.push('');
    }
    L.push('Détail de la commande :');
    L.push('');

    Object.keys(etat.produits).forEach(function (ref) {
      var p = DONNEES.produits[ref];
      var q = etat.produits[ref];
      L.push('- ' + p.nom + ' ' + p.fmt + ' : ' + q + ' × ' + euros(p.prix)
        + ' = ' + euros(p.prix * q));
    });

    Object.keys(DONNEES.gammes).forEach(function (gamme) {
      var table = etat.achats[gamme];
      var codes = Object.keys(table);
      if (!codes.length) return;
      var g = DONNEES.gammes[gamme];
      var total = somme(table);
      L.push('- ' + g.nom + ' 100 ml : ' + total + ' × ' + euros(g.prix)
        + ' = ' + euros(g.prix * total));
      L.push('  Nuances : ' + codes.map(function (c) {
        return c + ' × ' + table[c];
      }).join(', '));
    });

    var cadeaux = Object.keys(DONNEES.gammes).filter(function (g) {
      return Object.keys(etat.offerts[g]).length > 0;
    });
    if (cadeaux.length) {
      L.push('');
      L.push('Colorations offertes :');
      L.push('');
      cadeaux.forEach(function (gamme) {
        var table = etat.offerts[gamme];
        var total = somme(table);
        L.push('- ' + DONNEES.gammes[gamme].nom + ' : ' + total + ' tube'
          + (total > 1 ? 's' : '') + ' offert' + (total > 1 ? 's' : '') + ' (0,00 €)');
        L.push('  Nuances : ' + Object.keys(table).map(function (c) {
          return c + ' × ' + table[c];
        }).join(', '));
      });
    }

    L.push('');
    L.push('Montant total HT : ' + euros(totalCents()));
    if (etat.livraison) {
      L.push('');
      L.push('Date de livraison souhaitée : ' + dateFr(etat.livraison));
    }
    L.push('');
    L.push('Pourriez-vous me confirmer la disponibilité des produits ainsi que la date de livraison ?');
    L.push('');
    L.push('Je vous remercie par avance.');
    L.push('');
    L.push('Bonne journée.');

    return L.join('\n');
  }

  var lienWa = panier.querySelector('[data-whatsapp]');

  function majLien() {
    var exces = excesTotal();
    var pret = nbArticles() > 0 && exces === 0;
    lienWa.setAttribute('aria-disabled', pret ? 'false' : 'true');
    lienWa.href = pret
      ? 'https://wa.me/' + DONNEES.tel + '?text=' + encodeURIComponent(message())
      : '#';
    var avis = panier.querySelector('[data-panier-alerte]');
    avis.hidden = exces === 0;
    if (exces) {
      avis.textContent = 'Vous avez sélectionné ' + exces + ' coloration'
        + (exces > 1 ? 's' : '') + ' offerte' + (exces > 1 ? 's' : '')
        + ' de trop. Corrigez la répartition dans la section Colorations '
        + 'pour envoyer la commande.';
    }
  }

  /* ---- Rendu global --------------------------------------------------- */

  function rendre() {
    blocsGamme.forEach(rendreGamme);
    rendrePanier();

    var n = nbArticles();
    var pastille = document.querySelector('[data-compteur]');
    pastille.textContent = n;
    pastille.hidden = n === 0;
    ouvreur.setAttribute('aria-label',
      n === 0 ? 'Ma commande, vide' : 'Ma commande, ' + n + ' référence' + (n > 1 ? 's' : ''));

    majLien();
    sauver();
  }

  function pastilleAnime() {
    var pastille = document.querySelector('[data-compteur]');
    if (!pastille) return;
    pastille.classList.remove('est-maj');
    void pastille.offsetWidth;          // force la relance de l'animation
    pastille.classList.add('est-maj');
  }

  /* ---- Recherche ------------------------------------------------------ */

  var champRech = document.querySelector('[data-rech]');

  if (champRech) {
    var vides = document.createElement('p');
    vides.className = 'sans-resultat';
    vides.hidden = true;
    vides.textContent = 'Aucune référence ne correspond à cette recherche.';
    champRech.closest('.entete').insertAdjacentElement('afterend', vides);

    champRech.addEventListener('input', function () {
      var q = champRech.value.trim().toLowerCase()
        .normalize('NFD').replace(/[̀-ͯ]/g, '');
      var trouves = 0;

      document.querySelectorAll('.carte').forEach(function (c) {
        var ok = !q || c.getAttribute('data-recherche').indexOf(q) !== -1;
        c.classList.toggle('est-masque', !ok);
        if (ok) trouves++;
      });

      // Un groupe ou une section sans carte visible n'a plus de raison d'être.
      document.querySelectorAll('[data-groupe]').forEach(function (g) {
        var reste = g.querySelectorAll('.carte:not(.est-masque)').length;
        g.classList.toggle('est-masque', q && !reste);
      });
      document.querySelectorAll('.section').forEach(function (s) {
        var reste = s.querySelectorAll('.carte:not(.est-masque)').length;
        var aGammes = s.querySelector('.gammes');
        s.classList.toggle('est-masque', !!q && !reste && !aGammes);
      });
      document.querySelectorAll('.gammes, .dilution').forEach(function (el) {
        el.classList.toggle('est-masque', !!q);
      });

      vides.hidden = !q || trouves > 0;
    });
  }

  /* ---- Navigation et confort ------------------------------------------ */

  var barre = document.querySelector('.entete');
  if (barre) {
    var mesurer = function () {
      document.documentElement.style.setProperty(
        '--barre', barre.getBoundingClientRect().height + 'px');
    };
    mesurer();
    window.addEventListener('resize', mesurer, { passive: true });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(mesurer);
  }

  var liens = Array.prototype.slice.call(document.querySelectorAll('.piste a[href^="#"]'));

  if (liens.length && 'IntersectionObserver' in window) {
    var parId = {};
    var cibles = [];
    liens.forEach(function (lien) {
      var s = document.querySelector(lien.getAttribute('href'));
      if (!s) return;
      parId[s.id] = lien;
      cibles.push(s);
    });

    var visibles = {};
    var marquer = function () {
      var active = cibles.filter(function (s) { return visibles[s.id]; })[0];
      liens.forEach(function (l) { l.removeAttribute('aria-current'); });
      if (!active || !parId[active.id]) return;
      var lien = parId[active.id];
      lien.setAttribute('aria-current', 'true');
      var piste = lien.parentElement;
      if (piste.scrollWidth > piste.clientWidth) {
        piste.scrollTo({
          left: lien.offsetLeft - piste.clientWidth / 2 + lien.offsetWidth / 2,
          behavior: 'smooth'
        });
      }
    };

    var obs = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (e) { visibles[e.target.id] = e.isIntersecting; });
      marquer();
    }, { rootMargin: '-25% 0px -60% 0px' });

    cibles.forEach(function (s) { obs.observe(s); });
  }

  var haut = document.querySelector('[data-haut]');
  if (haut) {
    haut.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    window.addEventListener('scroll', function () {
      haut.hidden = window.scrollY < 900;
    }, { passive: true });
  }

  var reduit = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!reduit && 'IntersectionObserver' in window) {
    var apparition = new IntersectionObserver(function (entrees, o) {
      entrees.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('est-la');
        o.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.04 });

    document.querySelectorAll('.groupe, .gamme, .offre__conditions')
      .forEach(function (el) {
        el.classList.add('js-paraitre');
        apparition.observe(el);
      });
  }

  /* ---- Impression ----------------------------------------------------- */

  /* Un <details> fermé ne s'ouvre pas de façon fiable en CSS seul : on les
     déplie avant l'impression, puis on rend à chacun son état. */
  (function () {
    var memoire = null;
    window.addEventListener('beforeprint', function () {
      var familles = document.querySelectorAll('[data-famille]');
      memoire = [];
      familles.forEach(function (f) { memoire.push(f.open); f.open = true; });
    });
    window.addEventListener('afterprint', function () {
      if (!memoire) return;
      document.querySelectorAll('[data-famille]').forEach(function (f, i) {
        f.open = memoire[i];
      });
      memoire = null;
    });
  })();

  /* ---- Démarrage ------------------------------------------------------ */

  charger();
  champSalon.value = etat.salon;
  champDate.value = etat.livraison;
  rendre();
})();
