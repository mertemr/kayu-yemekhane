import re
import string
from utils.date_renamer import get_date_from_title

replace_table = {
    "İ": "i",
    "Ç": "ç",
    "Ş": "ş",
    "Ğ": "ğ",
    "Ü": "ü",
    "Ö": "ö",
    "I": "ı",
}

rep = dict((re.escape(k), v) for k, v in replace_table.items())
pattern = re.compile("|".join(rep.keys()))

whitespace_pattern = re.compile(r"\s{2,}")

def filter_table(table: list[str]) -> list[str]:
    cleaned_list = list(map(lambda x: whitespace_pattern.sub(" ", x), table))
    title_map = []
    
    liste = []
    
    skip_next_line = False
    
    for i,item in enumerate(cleaned_list):  # Satır gruplama
        if skip_next_line:
            skip_next_line = False
            continue
        
        if cleaned_list[-1] != item:
            if re.search(r"YEMEK LİSTE", cleaned_list[i+1]):
                liste.append(("menu", " ".join([item, cleaned_list[i+1]])))
                skip_next_line = True
                continue
        
        if re.search(r"^[\d]+", item):
            liste.append(("zaman", item))
            continue
        
        liste.append(("yemek", item))
    
    for i, line in enumerate(liste.copy()):
        dt, dc = line  # dt: data type, dc: data content
        if dt == "zaman" and liste[i+1][0] == "zaman":
            dc = " ".join([dc, liste[i+1][1]])
            liste[i+1] = ("zaman", dc)
            liste.pop(i)
    
    for i, line in enumerate(liste):
        dt, dc = line
        if dt == "zaman":
            liste[i] = (dt, get_date_from_title(dc).isoformat())
    
    for i, line in enumerate(liste):
        dt, dc = line
        print(dc)
        dc = pattern.sub(lambda m: str(rep[re.escape(m.group(0))]), dc)
        title_map.append((dt, dc.lower()))
    yield from title_map