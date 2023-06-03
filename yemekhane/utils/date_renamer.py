import difflib
import re
from datetime import date

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

    try:  # get month number from dict
        d, m, y = map(int, splitted[:3])
        date_ = date(y, m, d)
    except ValueError:  # if month name is wrong, try to find the closest match
        d, m, y = splitted[:3]
        try:
            closest = difflib.get_close_matches(m.upper(), months.keys(), n=1)[0]
            m = months[closest]
            date_ = date(int(y), m, int(d))
        except IndexError:  # f**k it, just use today's month
            date_ = date(int(y), date.today().month, int(d))
    return date_
