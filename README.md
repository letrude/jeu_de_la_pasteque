# 🥝 Le jeu de la pastèque --- Clone Python du Suika Game

Le jeu de la pastèque est une réinterprétation du célèbre **Suika Game**, développée
en Python avec **Pygame** et **Pymunk**.\
Votre objectif : **faire tomber des fruits**, **les fusionner**, et
**éviter qu'ils dépassent le toit** !

## 🎮 Fonctionnalités

-   Physique réaliste grâce à Pymunk\
-   Système de fusion : deux fruits identiques → un fruit plus gros\
-   Graphismes cartoon (ombres, yeux, bouche)\
-   Murs + toit détectant la fin de partie\
-   Contrôles simples : souris + clic / espace\
-   Score automatique basé sur les fusions\
-   Écran Game Over si un fruit passe au-dessus de la limite

## 📦 Dépendances

Le script tente d'installer automatiquement les libs manquantes, mais
voici la liste :

-   Python ≥ 3.8\
-   `numpy`\
-   `pygame`\
-   `pymunk`

Installation :

``` bash
pip install numpy pygame pymunk
```

## ▶️ Lancer le jeu

``` bash
python pasteque.py
```

## 🕹️ Commandes

  |Action                      |Touche / Souris|
  |--------------------------- |-------------------------------|
  |Lâcher un fruit             |Clic gauche / Espace / Entrée|
  |Déplacer le fruit suivant   |Bouger la souris|
  |Quitter                     |`Q`, `ESC`|

## 🍎 Règles du jeu

-   Deux fruits identiques fusionnent.\
-   Chaque fusion donne des points.\
-   Si un fruit dépasse le toit après collision → **Game Over**.

## 🧠 Structure interne

-   Classes : `Particle`, `PreParticle`, `Wall`, `Roof`.\
-   Physique : gravité, friction, élasticité.\
-   Graphismes cartoon via Pygame.