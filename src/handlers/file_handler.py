import csv
import os

def get_base_path():
    # Vai até a raiz do projeto, subindo 2 níveis
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def read_usernames_from_file(filename: str) -> list[str]:
    base_path = get_base_path()

    filepath = os.path.join(base_path, filename)
    dev_path = os.path.join(base_path, "src", "data", filename)

    if os.path.exists(filepath):
        final_path = filepath
    elif os.path.exists(dev_path):
        final_path = dev_path
    else:
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath} ou {dev_path}")

    _, ext = os.path.splitext(final_path)

    if ext.lower() == ".txt":
        return _read_from_txt(final_path)
    elif ext.lower() == ".csv":
        return _read_from_csv(final_path)
    else:
        raise ValueError("Formato de arquivo não suportado. Use .txt ou .csv.")

def _read_from_txt(filepath: str) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def _read_from_csv(filepath: str) -> list[str]:
    usernames = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                usernames.append(row[0].strip())
    return usernames
