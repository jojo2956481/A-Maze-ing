import sys


def is_valide(item):
    if item.count("=") != 1:
        return False
    name, value = item.split("=")
    if not name:
        return False
    if name in ["WIDTH", "HEIGHT"]:
        return value.isdigit()
    if name in ["ENTRY", "EXIT"]:
        parts = value.split(",")
        if len(parts) != 2:
            return False
        return all(p.isdigit() for p in parts)
    if name in ["OUTPUT_FILE"]:
        if not value.endswith(".txt"):
            return False
    if name in ["PERFECT"]:
        if value not in ["True", "False"]:
            return False
    return True


def pars_args(args):
    inventory = {}
    if args:
        for item in args:
            if not is_valide(item):
                print("Error invalide Key, value")
                return
            name, value = item.split("=")
            inventory[name] = value.strip()
            # print(inventory[name])
        return inventory


def read_file():
    args = sys.argv[1:]
    try:
        with open(args[0], "r") as f:
            contenue = f.read()
            if contenue:
                lst = contenue.splitlines()
                return lst
            return print("file empty")
    except IOError as e:
        return print(f"ERROR: {e}")


def check_dict(dictionaire):
    valide_key = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}
    optional_keys = {"SEED"}
    for name in dictionaire:
        if name not in valide_key and name not in optional_keys:
            print("Error invalide Key, value")
            return False

    keys = set(dictionaire.keys())

    if not valide_key.issubset(keys):
        print("Error invalide Key, value")
        return False
    entry = dictionaire["ENTRY"]
    exit = dictionaire["EXIT"]
    if entry == exit:
        print("Error invalide Key, value")
        return False
    e_w, e_h = map(int, entry.split(","))
    o_w, o_h = map(int, exit.split(","))
    if e_h > int(dictionaire["HEIGHT"]) or o_h > int(dictionaire["HEIGHT"]):
        
        return False
    if e_w > int(dictionaire["WIDTH"]) or o_w > int(dictionaire["WIDTH"]):
        print("Error invalide Key, value")
        return False
    return True


def pars_dict():
    data = read_file()
    dictionaire = pars_args(data)
    if not dictionaire:
        return
    if check_dict(dictionaire):
        return dictionaire


if __name__ == "__main__":
    dictionaire = pars_dict()
    if dictionaire:
        print(dictionaire)
