from datetime import date, timedelta
import re

months = {
    "OCAK": 1,
    "ŞUBAT": 2,
    "MART": 3,
    "NİSAN": 4,
    "MAYIS": 5,
    "HAZİRAN": 6,
    "TEMMUZ": 7,
    "AĞUSTOS": 8,
    "EYLÜL": 9,
    "EKİM": 10,
    "KASIM": 11,
    "ARALIK": 12,
}

rep = dict((re.escape(k), v) for k, v in months.items())
pattern = re.compile("|".join(rep.keys()))

def get_date_from_title(title: str) -> date:
    replaced = pattern.sub(lambda m: str(rep[re.escape(m.group(0))]), title)
    splitted = replaced.split(" ")
    d,m,y = map(int, splitted[:3])
    
    return date(y, m, d)