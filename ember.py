from datetime import date, timedelta

START_YEAR = date.today().year
END_YEAR = START_YEAR + 9

# Goes in every UID. Subscribers match events across refreshes on it, so it has
# to stay put once published; swap in the domain the files are served from.
UID_DOMAIN = "grubitz.github.io"

# ----------------------------
# Easter (Gregorian Computus)
# ----------------------------
def gregorian_easter(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    month = (h + l - 7*m + 114) // 31
    day = ((h + l - 7*m + 114) % 31) + 1
    return date(year, month, day)

def next_weekday_after(d, weekday):
    days = (weekday - d.weekday() + 7) % 7
    if days == 0:
        days = 7
    return d + timedelta(days=days)

# ----------------------------
# Ember Day Calculation
# ----------------------------
def ember_days(year):
    easter = gregorian_easter(year)

    # Lent
    ash_wednesday = easter - timedelta(days=46)
    first_sunday_lent = ash_wednesday + timedelta(days=4)

    lent = [
        first_sunday_lent + timedelta(days=3),
        first_sunday_lent + timedelta(days=5),
        first_sunday_lent + timedelta(days=6),
    ]

    # Pentecost
    pentecost = easter + timedelta(days=49)

    pent = [
        pentecost + timedelta(days=3),
        pentecost + timedelta(days=5),
        pentecost + timedelta(days=6),
    ]

    # September
    # 1960 rubrics: the First Sunday of September is the first Sunday falling
    # within September, so the Ember week can land a week after Holy Cross.
    sept_1 = date(year, 9, 1)
    third_sunday_sept = sept_1 + timedelta(days=(6 - sept_1.weekday()) % 7 + 14)
    sept_wed = third_sunday_sept + timedelta(days=3)

    sept = [
        sept_wed,
        sept_wed + timedelta(days=2),
        sept_wed + timedelta(days=3),
    ]

    # Advent
    dec_anchor = date(year, 12, 13)
    dec_wed = next_weekday_after(dec_anchor, 2)

    advent = [
        dec_wed,
        dec_wed + timedelta(days=2),
        dec_wed + timedelta(days=3),
    ]

    return {
        "Lent": lent,
        "Pentecost": pent,
        "September": sept,
        "Advent": advent,
    }

# ----------------------------
# Holydays
# ----------------------------

# Feast key -> fixed (month, day), or an offset in days from Easter Sunday.
HOLYDAYS = {
    "circumcision": (1, 1),
    "epiphany": (1, 6),
    "presentation": (2, 2),
    "st_david": (3, 1),
    "st_joseph": (3, 19),
    "annunciation": (3, 25),
    "st_george": (4, 23),
    "st_adalbert": (4, 23),
    "st_stanislaus": (5, 8),
    "john_baptist": (6, 24),
    "peter_paul": (6, 29),
    "assumption": (8, 15),
    "nativity_bvm": (9, 8),
    "all_saints": (11, 1),
    "st_margaret_scotland": (11, 16),
    "st_andrew": (11, 30),
    "immaculate_conception": (12, 8),
    "christmas": (12, 25),
    "st_stephen": (12, 26),
    "easter": 0,
    "easter_monday": 1,
    "ascension": 39,
    "pentecost": 49,
    "whit_monday": 50,
    "corpus_christi": 60,
}

# Shared by every locale; national patrons come from the locale itself.
TRADITIONAL_CORE = (
    "christmas",
    "st_stephen",
    "circumcision",
    "epiphany",
    "easter",
    "easter_monday",
    "ascension",
    "pentecost",
    "whit_monday",
    "corpus_christi",
    "presentation",
    "annunciation",
    "assumption",
    "nativity_bvm",
    "immaculate_conception",
    "st_joseph",
    "john_baptist",
    "peter_paul",
    "all_saints",
)

# Obligation is set per bishops' conference, not per country, so England &
# Wales and Scotland are separate locales. "transfers" maps a feast to the
# weekdays (Mon=0, Sat=5) on which its obligation moves to the adjacent Sunday.
LOCALES = {
    "engwal": {
        "region": {"en": "England & Wales", "pl": "Anglia i Walia"},
        "patrons": ("st_david", "st_george"),
        "obligation": (
            "christmas",
            "epiphany",
            "ascension",
            "peter_paul",
            "assumption",
            "all_saints",
        ),
        "transfers": {
            "epiphany": (0, 5),
            "peter_paul": (0, 5),
            "assumption": (0, 5),
            "all_saints": (0, 5),
        },
    },
    "sco": {
        "region": {"en": "Scotland", "pl": "Szkocja"},
        "patrons": ("st_margaret_scotland", "st_andrew"),
        # Scotland never restored Epiphany; England & Wales did, in 2017.
        "obligation": (
            "christmas",
            "ascension",
            "peter_paul",
            "assumption",
            "all_saints",
        ),
        # All Saints moves off a Saturday but stays put on a Monday.
        "transfers": {
            "peter_paul": (0, 5),
            "assumption": (0, 5),
            "all_saints": (5,),
        },
    },
    "pol": {
        "region": {"en": "Poland", "pl": "Polska"},
        "patrons": ("st_adalbert", "st_stanislaus"),
        "obligation": (
            "christmas",
            "circumcision",
            "epiphany",
            "corpus_christi",
            "assumption",
            "all_saints",
        ),
        "transfers": {},
        # 1 January keeps the older title in the traditional tier and takes the
        # current one in the obligation the Polish bishops actually impose.
        "names": {
            "circumcision": {
                "en": "Mary, Mother of God",
                "pl": "\u015awi\u0119tej Bo\u017cej Rodzicielki Maryi",
            },
        },
    },
}

HOLYDAY_NAMES = {
    "en": {
        "circumcision": "Circumcision of the Lord",
        "epiphany": "Epiphany of the Lord",
        "presentation": "Presentation of the Lord (Candlemas)",
        "st_david": "St David",
        "st_joseph": "St Joseph",
        "annunciation": "Annunciation of the Lord",
        "st_george": "St George",
        "st_adalbert": "St Adalbert (Wojciech)",
        "st_stanislaus": "St Stanislaus of Szczepanów",
        "john_baptist": "Nativity of St John the Baptist",
        "peter_paul": "Ss Peter & Paul",
        "assumption": "Assumption of the Blessed Virgin Mary",
        "nativity_bvm": "Nativity of the Blessed Virgin Mary",
        "all_saints": "All Saints",
        "st_margaret_scotland": "St Margaret of Scotland",
        "st_andrew": "St Andrew",
        "immaculate_conception": "Immaculate Conception",
        "christmas": "Christmas Day",
        "st_stephen": "St Stephen (Second Day of Christmas)",
        "easter": "Easter Sunday",
        "easter_monday": "Easter Monday",
        "ascension": "Ascension of the Lord",
        "pentecost": "Pentecost",
        "whit_monday": "Whit Monday",
        "corpus_christi": "Corpus Christi",
    },
    "pl": {
        "circumcision": "Obrzezanie Pa\u0144skie",
        "epiphany": "Objawienie Pa\u0144skie (Trzech Kr\u00f3li)",
        "presentation": "Ofiarowanie Pa\u0144skie (Matki Bo\u017cej Gromnicznej)",
        "st_david": "\u015awi\u0119tego Dawida",
        "st_joseph": "\u015awi\u0119tego J\u00f3zefa",
        "annunciation": "Zwiastowanie Pa\u0144skie",
        "st_george": "\u015awi\u0119ty Jerzy",
        "st_adalbert": "\u015awi\u0119tego Wojciecha",
        "st_stanislaus": "\u015awi\u0119tego Stanis\u0142awa",
        "john_baptist": "Narodzenie \u015bw. Jana Chrzciciela",
        "peter_paul": "\u015awi\u0119tych Aposto\u0142\u00f3w Piotra i Paw\u0142a",
        "assumption": "Wniebowzi\u0119cie Naj\u015bwi\u0119tszej Maryi Panny",
        "nativity_bvm": "Narodzenie Naj\u015bwi\u0119tszej Maryi Panny",
        "all_saints": "Wszystkich \u015awi\u0119tych",
        "st_margaret_scotland": "\u015awi\u0119tej Ma\u0142gorzaty Szkockiej",
        "st_andrew": "\u015awi\u0119tego Andrzeja",
        "immaculate_conception": "Niepokalane Pocz\u0119cie Naj\u015bwi\u0119tszej Maryi Panny",
        "christmas": "Bo\u017ce Narodzenie",
        "st_stephen": "\u015awi\u0119tego Szczepana (drugi dzie\u0144 Bo\u017cego Narodzenia)",
        "easter": "Wielkanoc",
        "easter_monday": "Poniedzia\u0142ek Wielkanocny",
        "ascension": "Wniebowst\u0105pienie Pa\u0144skie",
        "pentecost": "Zes\u0142anie Ducha \u015awi\u0119tego (Zielone \u015awi\u0105tki)",
        "whit_monday": "Poniedzia\u0142ek Zes\u0142ania Ducha \u015awi\u0119tego",
        "corpus_christi": "Bo\u017ce Cia\u0142o",
    },
}

HOLYDAY_LABELS = {
    "en": {
        "obligation": "Holyday of Obligation",
        "transferred": "obligation transferred to Sun",
        "date_format": "%d %b",
        "calendar_name": "Holydays \u2014 {region}",
    },
    "pl": {
        "obligation": "\u015bwi\u0119to nakazane",
        "transferred": "obowi\u0105zek przeniesiony na niedziel\u0119",
        "date_format": "%d.%m",
        "calendar_name": "\u015awi\u0119ta \u2014 {region}",
    },
}


def holyday_dates(year):
    easter = gregorian_easter(year)
    return {
        key: date(year, *rule) if isinstance(rule, tuple) else easter + timedelta(days=rule)
        for key, rule in HOLYDAYS.items()
    }


def holydays(locale, year):
    """(date, feast key, tier, Sunday the obligation moved to or None), date order."""
    config = LOCALES[locale]
    dates = holyday_dates(year)
    events = []
    for key in dict.fromkeys(TRADITIONAL_CORE + config["patrons"] + config["obligation"]):
        d = dates[key]
        obligation = key in config["obligation"]
        moved = None
        if obligation and d.weekday() in config["transfers"].get(key, ()):
            moved = d + timedelta(days=1 if d.weekday() == 5 else -1)
        events.append((d, key, "Obligation" if obligation else "Traditional", moved))
    return sorted(events)


def holyday_summary(locale, lang, key, tier, moved):
    override = LOCALES[locale].get("names", {}).get(key)
    name = override[lang] if override else HOLYDAY_NAMES[lang][key]
    labels = HOLYDAY_LABELS[lang]
    if moved:
        return f"{name} ({labels['transferred']} {moved.strftime(labels['date_format'])})"
    if tier == "Obligation":
        return f"{name} ({labels['obligation']})"
    return name


# ----------------------------
# Translations
# ----------------------------

TRANSLATIONS = {
    "en": {
        "Lent": "Ember Day (Lent)",
        "Pentecost": "Ember Day (Pentecost)",
        "September": "Ember Day (September)",
        "Advent": "Ember Day (Advent)",
        "calendar_name": "Traditional Catholic Ember Days"
    },
    "pl": {
        "Lent": "Suche Dni (Wielki Post)",
        "Pentecost": "Suche Dni (Zielone Świątki)",
        "September": "Suche Dni (Wrzesień)",
        "Advent": "Suche Dni (Adwent)",
        "calendar_name": "Tradycyjne Suche Dni"
    },
}

# ----------------------------
# ICS Generation
# ----------------------------

def vevent(uid, d, summary, categories=None):
    lines = [
        "BEGIN:VEVENT",
        f"UID:{uid}@{UID_DOMAIN}",
        f"DTSTAMP:{date.today().strftime('%Y%m%d')}T000000Z",
        f"DTSTART;VALUE=DATE:{d.strftime('%Y%m%d')}",
        f"DTEND;VALUE=DATE:{(d + timedelta(days=1)).strftime('%Y%m%d')}",
        f"SUMMARY:{summary}",
    ]
    if categories:
        lines.append(f"CATEGORIES:{categories}")
    lines.append("END:VEVENT")
    return lines


def fold(line):
    """RFC 5545 folding: 75 octets per line, continuations start with a space."""
    data = line.encode("utf-8")
    if len(data) <= 75:
        return line

    chunks, start = [], 0
    while start < len(data):
        end = min(start + (75 if not chunks else 74), len(data))
        while end < len(data) and data[end] & 0xC0 == 0x80:  # never split a character
            end -= 1
        chunks.append(data[start:end].decode("utf-8"))
        start = end
    return "\r\n ".join(chunks)


def write_ics(filename, calendar_name, events):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Traditional Ember Days//EN",
        f"X-WR-CALNAME:{calendar_name}",
        # A rolling window: subscribers need to re-read to keep gaining years.
        "REFRESH-INTERVAL;VALUE=DURATION:P7D",
        "X-PUBLISHED-TTL:P7D",
    ]
    lines.extend(events)
    lines.append("END:VCALENDAR")

    with open(filename, "w", encoding="utf-8", newline="") as f:
        f.write("".join(fold(line) + "\r\n" for line in lines))


def generate_ics(lang_code):
    events = []
    for year in range(START_YEAR, END_YEAR + 1):
        for season, dates in ember_days(year).items():
            for d in dates:
                events.extend(
                    vevent(f"ember-{season.lower()}-{d:%Y%m%d}", d, TRANSLATIONS[lang_code][season])
                )

    write_ics(
        f"ember-{lang_code}.ics",
        TRANSLATIONS[lang_code]["calendar_name"],
        events,
    )


def generate_holydays_ics(locale, lang_code):
    labels = HOLYDAY_LABELS[lang_code]
    events = []
    for year in range(START_YEAR, END_YEAR + 1):
        for d, key, tier, moved in holydays(locale, year):
            events.extend(
                vevent(
                    f"{locale}-{key}-{d:%Y}",
                    d,
                    holyday_summary(locale, lang_code, key, tier, moved),
                    tier,
                )
            )

    write_ics(
        f"{locale}-{lang_code}.ics",
        labels["calendar_name"].format(region=LOCALES[locale]["region"][lang_code]),
        events,
    )

# ----------------------------
# Run
# ----------------------------

def _self_check():
    # 2026 checked against a published 1962 ordo; 2025 and 2027 are the other
    # years here where the "Wednesday after 14 September" shortcut is a week early.
    expected = {
        2025: ("Lent", date(2025, 3, 12), "September", date(2025, 9, 24)),
        2026: ("Lent", date(2026, 2, 25), "September", date(2026, 9, 23)),
        2027: ("Lent", date(2027, 2, 17), "September", date(2027, 9, 22)),
    }
    for year, (s1, d1, s2, d2) in expected.items():
        got = ember_days(year)
        assert got[s1][0] == d1, (year, s1, got[s1][0], d1)
        assert got[s2][0] == d2, (year, s2, got[s2][0], d2)
    assert ember_days(2026)["Advent"][0] == date(2026, 12, 16)
    assert ember_days(2026)["Pentecost"][0] == date(2026, 5, 27)

    engwal_2026 = {key: (d, tier, moved) for d, key, tier, moved in holydays("engwal", 2026)}
    assert engwal_2026["ascension"] == (date(2026, 5, 14), "Obligation", None)
    # 15 Aug 2026 is a Saturday, 29 Jun 2026 a Monday: obligation moves either way.
    assert engwal_2026["assumption"][2] == date(2026, 8, 16)
    assert engwal_2026["peter_paul"][2] == date(2026, 6, 28)
    assert engwal_2026["christmas"] == (date(2026, 12, 25), "Obligation", None)
    # 15 Aug 2027 is itself a Sunday.
    assert holyday_dates(2027)["assumption"].weekday() == 6
    assert {key: moved for _, key, _, moved in holydays("engwal", 2027)}["assumption"] is None
    # Feasts in both tiers are emitted once, as Obligation.
    assert engwal_2026["all_saints"][1] == "Obligation"
    for locale, config in LOCALES.items():
        keys = set(TRADITIONAL_CORE) | set(config["patrons"]) | set(config["obligation"])
        assert len(holydays(locale, 2026)) == len(keys), locale
        for lang in HOLYDAY_NAMES:
            assert config["region"][lang]
            for key in keys:
                assert holyday_summary(locale, lang, key, "Traditional", None)

    # Scotland 2026, against the published diocesan list.
    sco_2026 = {
        key: (moved or d)
        for d, key, tier, moved in holydays("sco", 2026)
        if tier == "Obligation"
    }
    assert sco_2026 == {
        "ascension": date(2026, 5, 14),
        "peter_paul": date(2026, 6, 28),
        "assumption": date(2026, 8, 16),
        "all_saints": date(2026, 11, 1),
        "christmas": date(2026, 12, 25),
    }
    # 1 Nov 2027 is a Monday: England & Wales move it, Scotland do not.
    assert holyday_dates(2027)["all_saints"].weekday() == 0
    moved_2027 = lambda loc: {key: moved for _, key, _, moved in holydays(loc, 2027)}
    assert moved_2027("engwal")["all_saints"] == date(2027, 10, 31)
    assert moved_2027("sco")["all_saints"] is None
    assert "st_andrew" in dict.fromkeys(
        key for _, key, _, _ in holydays("sco", 2026)
    )

    pol_2026 = {
        key: tier for _, key, tier, _ in holydays("pol", 2026)
    }
    assert pol_2026["corpus_christi"] == "Obligation"
    assert pol_2026["peter_paul"] == "Traditional"  # obligation abrogated in 2003
    assert pol_2026["st_adalbert"] == "Traditional"
    assert "st_george" not in pol_2026
    assert holyday_summary("pol", "en", "circumcision", "Obligation", None) == (
        "Mary, Mother of God (Holyday of Obligation)"
    )
    assert holyday_summary("engwal", "en", "circumcision", "Traditional", None) == (
        "Circumcision of the Lord"
    )

    # UIDs must be stable across runs and unique within a calendar.
    assert vevent("x", date(2026, 1, 1), "s")[1] == f"UID:x@{UID_DOMAIN}"
    for locale in LOCALES:
        uids = [
            f"{locale}-{key}-{d:%Y}"
            for year in range(2026, 2036)
            for d, key, _, _ in holydays(locale, year)
        ]
        assert len(uids) == len(set(uids)), locale
    ember_uids = [
        f"ember-{season.lower()}-{d:%Y%m%d}"
        for year in range(2026, 2036)
        for season, dates in ember_days(year).items()
        for d in dates
    ]
    assert len(ember_uids) == len(set(ember_uids))

    assert fold("SUMMARY:short") == "SUMMARY:short"
    folded = fold("SUMMARY:" + "\u015a" * 60)
    assert all(len(part.encode("utf-8")) <= 75 for part in folded.split("\r\n"))
    assert folded.replace("\r\n ", "") == "SUMMARY:" + "\u015a" * 60


if __name__ == "__main__":
    _self_check()
    for lang in TRANSLATIONS.keys():
        generate_ics(lang)
    for locale in LOCALES:
        for lang in HOLYDAY_NAMES:
            generate_holydays_ics(locale, lang)

    print("ICS files generated.")
