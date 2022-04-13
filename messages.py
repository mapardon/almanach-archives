UNSUCCESSFUL_SEARCH = "Le terme spécifié n'a pas été trouvé. Vérifiez l'orthographe de votre entrée,\
 assurez-vous d'avoir sélectionné la bonne liste ou ajoutez d'abord ce mot."

NO_LIST_FOUND = "Sélectionnez ou créez une liste avant de commencer cette activité."

LIST_FOUND = "Une liste homonyme de votre répertoire empêche la récupération celle-ci."

EXP_ERR = "Un fichier texte nommé {}.txt existe déjà sur votre bureau \
supprimez-le ou renommer votre liste pour exporter."

CONSEILS = """Mathieu Company Limited© tient à rappeler, aussi géniale que soit
son application, que celle-ci ne garantit nullement de rendre
instantanément son utilisateur bilingue (et encore moins si l'application n'est
jamais utilisée).

En particulier, le concepteur n'offre aucune garantie quant à la réussite
d'une quelconque évaluation et décline toute responsabilité dans le cas contraire.

L'apprentissage d'une langue est un processus long, demande de l'investissement,
de la pratique et sollicite diverses compétences.

Almanach peut vous aider (et même avec certitude!) à réviser votre vocabulaire
mais ne se susbtitue en aucun cas à une étude plus exhaustive.

Astuce   Almanach a été initialement développé pour être un "mémo pratique" :
vous gambadez insoucieusement à travers les internets, lorsque tout à coup, vous
croisez un mot qui vous est inconnu.
Au lieu de le toiser de loin, telle une répugnante créature, avant de fuir
quelques instants plus tard et de l'oublier à jamais, consultez un dictionnaire
afin de connaître un équivalent (en français ou autre) et ajoutez-le à l'une de
vos listes!"""

BONNES_PRATIQUES = """Afin d'éviter la rencontre de certains problèmes facilement contournables
(compatibilité avec le système de fichiers de l'ordinateur, exécution du
programme...), le nommage des listes de vocabulaire est soumis à quelques
restrictions :

• Les noms de listes peuvent être composés de tout caractère alphanumérique(*)
ainsi que des caractères suivants : #, _, -, * et &

• Plusieurs listes ne devraient pas être identiquement nommées.

De plus, une limite de 15 caractères a été établie, étant de bonne pratique
de nommer un fichier avec clarté et concision ; Car ce qui se conçoit bien
s'énonce clairement (et les mots pour le dire arrivent aisément!).

(*) Il s'agit en principe des 10 chiffres du système décimal, des symboles
dérivés (fraction, nombre encerclé...) ainsi que des caractères des alphabets
latin et grec agrémentés de diacritiques (accents, tréma, cédille, tilde, ogonek,
brève, esprits...) ainsi que certains caractères spéciaux (eszett,
O-E entrelacé...).


NB1 : Le nommage d'une liste avec des caractères issus de systèmes d'écriture
autres que ceux décrits ci-dessus (hanzi, baybayin, hébreux...) pourrait être
refusé par le programme. Ces caractères risquent de générer des erreurs voire
l'interruption de l'application (communément appelée "bug" ou "crash") ceux-ci
n'étant pas reconnus comme tels.
Néanmoins, les listes peuvent recevoir des entrées constituées de n'importe quel
caractère (du moins tous ceux définis dans la codification utf-8).

NB2 : Les différentes saisies utilisateur (édition, évaluation) ont été
programmées de manière à être insensibles à la casse (mais bien aux diacritiques !!).

Toute erreur peut être signalée au concepteur : mathieu.pardon.20@gmail.com"""

MAN_PAGES = """Si vous avez atterri ici, c'est que vous êtes soit curieux (et
je me réjouis de l'intérêt que vous portez à Almanach !) soit vous avez été
confrontés à une erreur, en quel cas j'espère que vous trouverez réponses à vos
questions dans ces quelques lignes.

  #  Import & Export de fichiers
L'externalisation de listes se fait sous le support d'un fichier texte, un
fichier contenant uniquement une séquence de caractères (l'entièreté de la liste).

Lors de la création d'un tel fichier, Almanach utilise une certaine disposition
permettant de retrouver chaque mot et les traductions qui lui sont associées.
Tout fichier ne respectant pas cette disposition (qui aurait été l'objet de
modifications inappropiées ou n'étant tout simplement pas originaire d'Almanach)
ne pourrait être utilisé pour créer une nouvelle liste.

La disposition n'est pas très élaborée (vous devriez la déchiffrer en affichant
le contenu d'une liste externalisée). Néanmoins, pour éviter toute erreur
d'inattention, il est plus judicieux de laisser ce labeur aux fonctionnalités
idoines de l'application !

  #  Récupération de listes
Si jamais il vous était arrivé d'utiliser la fonctionnalité "Supprimer" par
inadvertance, pas de panique ! Almanach est doté d'un système de sauvegarde
temporaire des listes après suppression. Pour y accéder, entrez le code
"__REC0VER__" (sans les guillemets) dans le rectangle de saisie du menu principal
et appuyez ensuite sur "Nouvelle liste".
Le répertoire des listes supprimées est vidé une fois par mois, lors de votre
première connexion."""

LICENSE = """Merci d'avoir téléchargé Almanach

L'application que vous utilisez est le fruit du labeur et la propriété de
Mathieu Company Limited.

Almanach est libre d'utilisation et de diffusion. Néamoins, ce programme n'est
pas dépourvu de la moindre imperfection et ne s'en revendique nullement.
Pour ces raisons, il vous est demandé de ne pas le partager au-delà d'un cercle
strictement personnel, ni de vous l'approprier, auquel cas vous entrez en conflit
avec les droits sur la propriété intellectuelle et vous exposez à de lourdes
poursuites judiciaires.
Tout abus est punissable.

©2020 Mathieu Company Ltd


Logiciels, langage et bibliothèques utilisés :

# Python       : 3.8.5
# PyQt5        : 5.15.0
# PyCharm CE   : 2020.2
# cx_Freeze    : 6.2
# Inno Setup   : 6.0.5

# Actuelle version du programme : 1.4.4 (12-9-20)
  Dernières modifications : * (1.4.0) Menu "Évaluation" désormais menu "Étude" permettant d'afficher l'entièreté de
    la liste sélectionnée
  * (1.4.1) Possibilité de créer une liste depuis un fichier texte respectant la structure reconnue par l'application
  * (1.4.2) Nouvelle icône (ordi) donnant des renseignement sur diverses fonctionnalités de l'application
  * (1.4.3) Possibilité d'exporter une liste d'Almanach sous forme de fichier texte
  * (1.4.4) Ajout d'un oeuf de Pâques

Partenariat et sponsoring : mathieu.pardon.20@gmail.com

          Bruxelles, le 17 Août 2020
"""