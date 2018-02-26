
def get_original_line(fname, idx):
    original = []
    with open(fname, "r", encoding="utf8") as f:
        content = f.readlines()
        for line in content:
            original.append(line)

    return original.__getitem__(idx)
