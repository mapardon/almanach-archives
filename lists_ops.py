from files_ops import *

"""
  Functions relating to lists management (ins, del...)
"""

""" NB : De Rerum Filenamorum
Lorsqu'une opération sur un fichier doit être réalisée, son nom (et même
son chemin relatif) sont nécessaires. Or, du pdv de l'utilisateur, seul le
nom du fichier sans l'extension sera visible.
Il sera donc décidé de la convention suivante : lorsqu'on manipule un fichier
dissimulé à l'utilisateur (historiques...) ou un dossier, le chemin relatif
est enregistré dans une constante définie en début de ce fichier et c'est cet
identificateur qui sera utilisé dans le code (identificateur unique).
Autrement, principalement lorsqu'un nom de fichier sera demandé à l'utilisateur,
ce nom de fichier ne désignera que le nom du fichier sans l'extension. Cette
valeur sera convertie en chemin relatif le plus tard possible (les fonctions
ici définies) et sera désigné sous l'alias 'filename'.
Conversion : REPERTOIRE + "\\" + filename + ".txt"
Rmq : Une éventuelle vérification de la composition d'un nom (caractères
spéciaux...) est faite dans les fonctions de l'interface graphique (car cela
était plus simple pour lancer un message d'avertissement).
"""

""" BN2 : Schéma des données : 

Sur disque, les données sont sauvegardées grâce au module shelve, sous forme
d'un dictionnaire sérialisé.

Les données au sein du dictionnaire ont la forme suivante : mot_oz : [eq, score]
Où "score" représente le nombre de points déterminé par les interrogations.
"""


def serialize_entry(expr):
    """Another convention here (sorry)... Words will be stored entirely
    in lower case except for an "i" surrounded by 2 spaces (which will be
    supposed to be the first subject personal pronoun).
    In some terms, storage will be case insensitive."""
    expr = expr.strip()
    expr = expr.lower()
    expr = expr.replace(" i ", " I ")
    return expr


def is_regular_entry(word):
    word = word.strip() # might be useless
    res = bool(word)
    for c in word:
        res &= c not in "\t\n"
    return res


def is_empty(listname):
    """Check if list has no entry"""
    list_id = name_converter(listname)
    sentinel = bool()

    try:
        with shelve.open(list_id) as d:
            sentinel = len(d.keys()) == 0

    except Exception as e:
        write_down_feedback("verifying emptiness in {}".format(list_id), e)

    return sentinel


def search_entry(listname, word):
    """Returns translation (empty string if not found)
    rmk : search is based on 'term' word, not translation"""
    list_id = name_converter(listname)
    res = str()

    try:
        with shelve.open(list_id) as d:
            if word in d:
                res = d[word][0]

    except Exception as e:
        write_down_feedback("searching entry in {}".format(list_id), e)

    return res


def add_entry(listname, word, translation):
    list_id = name_converter(listname)
    ret = -2

    if not search_entry(listname, word):
        ret = 0

        try:
            with shelve.open(list_id) as d:
                d[word] = [translation, int()]

        except Exception as e:
            write_down_feedback("adding entry in {}".format(list_id), e)
            ret = -1

    return ret


def del_entry(listname, word):
    list_id = name_converter(listname)
    done = False

    if search_entry(listname, word):
        done = True

        try:
            with shelve.open(list_id) as d:
                del d[word]

        except Exception as e:
            write_down_feedback("deleting entry in {}".format(list_id), e)

    return done


def modify_entry(listname, word, new_tr):
    list_id = name_converter(listname)
    done = False

    if search_entry(listname, word):
        done = True

        try:
            with shelve.open(list_id) as d:
                d[word] = [new_tr, d[word][1]]

        except Exception as e:
            write_down_feedback("deleting entry in {}".format(list_id), e)

    return done


def random_choice(cur_listname):
    list_id = name_converter(cur_listname)
    keys_list = list()
    rd = str()

    try:
        with shelve.open(list_id) as db:
            for k in db.keys():
                keys_list.append(k)
            if len(keys_list) > 0:
                rd = random.choice(keys_list)

    except Exception as e:
        write_down_feedback("generating random entry with {}".format(list_id), e)

    return rd


    ### Evaluation, random selections

# utils for test_sheet generation

def get_list_size(cur_listname):
    list_id = name_converter(cur_listname)
    res = int()

    try:
        with shelve.open(list_id) as db:
            res = len(db)

    except Exception as e:
        write_down_feedback("computing len of {}".format(list_id), e)

    return res


def unknown_outcome(z):
    """ formula : param positif, renvoie des valeurs de 0.5 à 0+
    génère le nombre associé au score du mot et vérifie la sélection
    par appel à random.random() """
    def formula(x): return 1/2 if x < 4 else 1/(math.ceil(math.log(x, 2) + 2))
    v = 1 - formula(-z) if z < 0 else formula(z)
    return v > random.random()


def generate_quiz(nb_questions, mode, cur_listname):
    """ rappel : mode "True" = réponse à fournir en fr (langue originelle)
    schéma des données : disk = {"en" : ["fr", score]} ; interro = {"q" : ["sol", update]}"""
    list_id = name_converter(cur_listname)
    max_len = get_list_size(cur_listname)
    supervised_nb_q = (max_len < nb_questions) and max_len or nb_questions
    test_sheet = dict()

    try:
        with shelve.open(list_id) as db:
            # read keys for base of choices
            keys = [k for k in db]
            while len(test_sheet) < supervised_nb_q:

                oz = random.choice(keys)
                if oz not in test_sheet and unknown_outcome(db[oz][1]):
                    if mode:
                        test_sheet[oz] = [db[oz][0], int()]
                    else:
                        test_sheet[db[oz][0]] = [oz, int()]

    except Exception as e:
        write_down_feedback("generating testsheet with {}.".format(list_id), e)

    return test_sheet


def update_scores(test_sheet, mode, cur_listname):
    list_id = name_converter(cur_listname)

    try:
        with shelve.open(list_id) as db:
            for k in test_sheet:
                if mode: # keys = oz word
                    db[k] = [db[k][0], db[k][1] + test_sheet[k][1]]
                else: # keys = og word
                    db[test_sheet[k][0]] = [db[test_sheet[k][0]][0], db[test_sheet[k][0]][1] + test_sheet[k][1]]

    except Exception as e:
        write_down_feedback("updating scores with {}".format(list_id), e)


def list_chopper(list_2_chop):
    """lim == nb columns
    renvoie les colonnes de mots / leur trad
    et le nombre de pages nécessaire"""

    try:
        LIM = 23 # à priori fixé

        # compose selections + convert into bunches
        with shelve.open(name_converter(list_2_chop)) as db:
            x = sorted(db.keys())
            n_pg = math.ceil(len(x)/LIM)

            words = ['\n'.join([k for k in x[i*LIM:min(len(x), (i+1)*LIM)]]) for i in range(n_pg)]
            trads = ['\n'.join([db[k][0] for k in x[i*LIM:min(len(x), (i+1)*LIM)]]) for i in range(n_pg)]
            del x

    except Exception as e:
        write_down_feedback("reading list for display w list {}".format(list_2_chop), e)
        words, trads = list(), list()
        n_pg = -1

    return words, trads, n_pg


# IMPORT (needed add entry)


def file_import(fileid, filename):
    ret = -1

    if not create_file(filename):
        ret = 0
        try:
            with open(fileid, 'r', encoding='utf-8') as f:
                buf = f.readline()
                while buf and not ret:
                    if buf.count('\t') > 1:
                        ret = -1
                    elif buf.strip():
                        ret = add_entry(filename, buf.split('\t')[0], buf.split('\t')[1].strip())
                    buf = f.readline()

                if ret == -1:
                    raise Exception("Inconsistent format found in file")

        except Exception as e:
            ret = -1
            write_down_feedback("importing list", e)
            for ext in [".dat", ".dir", ".bak"]:
                os.remove(REPERTOIRE + "\\" + filename + ext)

    return ret


if __name__ == '__main__':

    # test deletion
    u, v, n = list_chopper("Anglais1")
    print(u, n)
