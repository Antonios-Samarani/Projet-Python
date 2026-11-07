def lire(file_path : str) :
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

def lire_tout(file_path : list[str]) :
    for p in file_path:
        yield from p.lire()