# -*- coding: utf-8 -*-

import os, shutil, datetime, shelve, random, math
import dbm.dumb

REPERTOIRE = "voc_lists"
TRASH = "deleted_lists"
MAINTENANCE = "maintenance_stuffs"
FEEDBACK = MAINTENANCE + "\\" + "exec_feedback.txt"
DELETIONS = MAINTENANCE + "\\" + "delete_times.txt"
DATE = datetime.datetime.now().strftime
S_FORMAT = '%d-%m-%Y'
L_FORMAT = '%Y-%m-%d @ %H:%M:%S'


###  Initializations (directories), lists management


def write_down_feedback(msg, exc):
    try:
        with open(FEEDBACK, 'a') as f:
            if exc == "__initz__":
                f.write(DATE(L_FORMAT) + " * initialization : {}\n".format(msg))
            else:
                f.write(DATE(L_FORMAT) + " * following error occurred while {} : {}\n".format(msg, exc))

    except Exception as e:
        with open("EMERGENCY.txt", 'w') as f:
            f.write("Following error occurred while trying to report error : {}.\nInitial error : {}, {}\n".format(e, msg, exc))


def init_util_dirs():
    try:
        if not os.path.exists(MAINTENANCE):
            os.mkdir(MAINTENANCE)

        if not os.path.exists(FEEDBACK):
            with open(FEEDBACK, 'w') as f:
                f.write(DATE(L_FORMAT) + " FEEDBACK initialized\n")

        if not os.path.exists(DELETIONS):
            with open(DELETIONS, 'w') as fic:
                fic.write(DATE(S_FORMAT))

        if not os.path.exists(REPERTOIRE):
            os.mkdir(REPERTOIRE)
            write_down_feedback("REPERTOIRE dir created", "__initz__")

        if not os.path.exists(TRASH):
            os.mkdir(TRASH)
            write_down_feedback("TRASH dir created", "__initz__")

    except Exception as e:
        write_down_feedback("doing initializations", e)


def clear_trash():
    # Once a month
    cur_month = int(DATE('%m'))

    try:
        with open(DELETIONS) as f:
            last_month = int(f.readline().split("-")[1])

        if cur_month != last_month:
            for f in os.listdir(TRASH):
                os.remove(TRASH + "\\" + f)

            with open(DELETIONS, 'w') as f:
                f.write(DATE(S_FORMAT))

    except Exception as e:
        write_down_feedback("clearing trash", e)


def delete_file(filename):
    """ more exactly : move it to the trash"""
    res = int()

    try:
        # we previously made sure there was NO homonyms
        # do the moving
        for ext in [".dat", ".dir", ".bak"]:
            shutil.move(REPERTOIRE + "\\" + filename + ext, TRASH)

    except Exception as e:
        write_down_feedback("deleting list", e)
        res = -1

    return res


def name_converter(filename):
    return REPERTOIRE + "\\" + filename


def create_file(filename):
    # rmk : we previously checked that the chain is valid (not homonym...)
    ret = int()
    try:
        d = shelve.open(name_converter(filename))
        d.close()

    except Exception as e:
        write_down_feedback("adding new list", e)
        ret = -1

    return ret


def rename(oldname, newname):
    try:
        for ext in [".dat", ".dir", ".bak"]:
            shutil.move(REPERTOIRE + "\\" + oldname + ext, REPERTOIRE + "\\" + newname + ext)

    except Exception as e:
        write_down_feedback("renaming", e)


def resurrect(filename):
    # more exactly : move it to the trash
    try:
        for ext in [".dat", ".dir", ".bak"]:
            shutil.move(TRASH + "\\" + filename + ext, REPERTOIRE)

    except Exception as e:
        write_down_feedback("recovering list", e)


def is_regular_filename(name):
    res = bool(name)
    for c in name:
        res &= c.isalnum() or c == '#' or c == '_' or c == '&' or c == '-' or c == '*'
    return res


def is_homonym(name, oz_names):
    return name.lower() in [n.lower() for n in oz_names]


# IMPORT -- EXPORT
# IMPORT : cf lists_ops


def file_export(cur_filename):
    ret = int()
    dest = os.path.expanduser("~/Desktop/{}".format(cur_filename + ".txt"))

    if os.path.exists(dest):
        ret = -2

    else:
        try:
            with shelve.open(name_converter(cur_filename)) as hydra:
                with open(dest, 'w', encoding='utf-8') as f:
                    for k in sorted(hydra.keys()):
                        f.write("{}\t{}\n".format(k, hydra[k][0]))

        except Exception as e:
            write_down_feedback("exporting list ({})".format(cur_filename), e)
            os.remove(dest)
            ret = -1

    return ret


if __name__ == '__main__':

    print("Bonjour UpyLab!")
