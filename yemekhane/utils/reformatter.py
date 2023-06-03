import re

from utils.date_renamer import get_date_from_title


def rename_items(items: list) -> list:
    renamed_list = []
    
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

    for line in items:
        dt, dc = line
        dc = pattern.sub(lambda m: str(rep[re.escape(m.group(0))]), dc)
        renamed_list.append((dt, dc.title()))
        
    return renamed_list

def edit_lists(lists):
    new = []
    
    for _list in lists:
        for i in _list:
            if i[0] == 'menu':
                menu_ismi = i[1]
                new.append({'isim': menu_ismi, 'veri': []})
            elif i[0] == 'zaman':
                zaman = i[1]
                new[-1]['veri'].append({'tarih': zaman, 'yemekler': []})
            elif i[0] == 'yemek':
                new[-1]['veri'][-1]['yemekler'].append(i[1])
        
        return new


def split_menus(items: list) -> list:
    splitted = []
    sublist = []
    
    for i in items:
        if i[0] == 'menu':
            if sublist:
                splitted.append(sublist)
                sublist = []
        sublist.append(i)
    
    splitted.append(sublist)
    return splitted

def filter_table(table: list[str]):
    """
    Horrifying Data Revival Function
    ------------------------------
    This function is used to resurrect data from a terrifying state.
    Here's a joke that came to my mind when I spent 3 hours fixing this code:
    Once upon a time, the data was lost in a nightmare.
    It was a chaotic mess, things were misplaced, and even ghosts were haunting it!
    But fear not, for I arrived as the heroic programmer and breathed new life into the data.
    At the end of this horrifying tale, the data is now neatly organized and living happily ever after.
    So, here I am, ready to take on the challenge of spooky data!
    """
    cleaned_list = list(map(lambda x: re.sub(r"\s{2,}", " ", x), table))
    
    data = []
    skip_next_line = False
    for i,item in enumerate(cleaned_list):  # Satır gruplama
        if skip_next_line:
            skip_next_line = False
            continue
        
        if cleaned_list[-1] != item:
            if re.search(r"YEMEK LİSTE", cleaned_list[i+1]):
                data.append(("menu", " ".join([item, cleaned_list[i+1]])))
                skip_next_line = True
                continue
        
        if re.search(r"^[\d]+", item):
            data.append(("zaman", item))
            continue
        
        data.append(("yemek", item))
    
    #? dt: data type, dc: data content
    dt: str
    dc: str
    
    for i, line in enumerate(data.copy()):
        dt, dc = line
        if dt == "zaman" and data[i+1][0] == "zaman":
            dc = " ".join([dc, data[i+1][1]])
            data[i+1] = ("zaman", dc)
            data.pop(i)
    
    for i, line in enumerate(data):
        dt, dc = line
        if dt == "zaman":
            data[i] = (dt, get_date_from_title(dc).isoformat())
    
    renamed_list = rename_items(data)
    
    sm = split_menus(renamed_list)
    MENU = []
    
    for i, menu in enumerate(sm):
        # Checking if menu is smaller than 5 items
        # Probably an error
        length = len(menu) - 1
        if length < 5:
            name = menu[0][1]
            value = menu[-1][1]
            MENU.append({
                "isim": name,
                "hata": value
            })
            sm.pop(i)
        
    edited = edit_lists(sm)
    MENU.extend(edited)
    
    return MENU
