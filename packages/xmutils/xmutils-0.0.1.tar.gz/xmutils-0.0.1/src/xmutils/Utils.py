import os


def mkdir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def searchFiles(root_path: str, exclude: list = []):
    if not os.path.exists(root_path):
        raise FileExistsError(f"No such directory: {root}")
    for root, dirs, files in os.walk(root_path):
        if exclude and os.path.basename(root) in exclude:
            continue
        for file in files:
            yield os.path.join(root, file)


def searchFileFromSuffix(root_path: str, suffix: str, exclude: list = []):
    for file in searchFiles(root_path, exclude):
        _ = os.path.basename(file).split('.')
        if _[-1] == suffix:
            yield file
