#!/usr/bin/env python3
"""Builds index.html from the numbers below. Run: python3 build.py

Every number here was read on 2026-11-14 from the source named beside it.
Raw observations are in research/. Nothing is estimated unless it says so.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
CHECKED = "November 14, 2026"
PEOPLE, NIGHTS = 4, 5
GAS_MPG, GAS_PRICE = 20, 3.00  # the drive option; editable in the calculator

# Three weeks: pre = Dec 16-21, x = Christmas week Dec 21-26, f = a February week.
# Each week is (fare per person, hotel per night, car for the 5 days).
#   Fares: Google Flights, round trip from Houston IAH. Cars: Kayak, cheapest car.
#   Hotels: Booking.com, 2 adults + 2 children, average of the SAME hotels across weeks.
#   For the six mountain towns the Dec 16-21 hotel rate is the Christmas-week rate
#   times the price ratio at hotels listed in both weeks (research/dec16_raw.txt).
# snow = {week: (% of years with snow on the ground, typical inches, low-snow-year inches)}
#   from NOAA 1991-2020 daily normals on Dec 17, Dec 25 and Feb 10.
D = [
    dict(key="whitefish", name="Whitefish", state="Montana", elev=3100, feb="Feb 1–6",
         w=dict(pre=(419, 160, 176), x=(757, 179, 185), f=(419, 185, 176)),
         snow=dict(pre=(84, 5, 3), x=(92, 7, 4), f=(98, 13, 7)), temps=dict(pre=(28, 17), x=(28, 16), f=(33, 16)),
         travel="One stop to Kalispell, 6 to 9 hours, then a short drive.",
         nature="Glacier National Park next door: Lake McDonald under snow-covered peaks.",
         kids=[("Horse-drawn sleigh rides at Bar W Guest Ranch", "listed at $55 a person for 45 minutes, under 4 free (older price)"),
               ("Dog sledding in Olney", "all ages, and a family fits in one sled. December to March. No current price found"),
               ("Glacier National Park", "ranger-led snowshoe walks"),
               ("In town", "indoor ice rink and sledding. No tubing hill found")],
         verdict="Mountains and animals at half the elevation of the Colorado towns, and one of the three lowest prices on the page for Dec 16–21.",
         catch="Snow is on the ground on Dec 17 in 84% of years, against 97% in Steamboat. Christmas-week flights nearly double."),
    dict(key="duluth", name="Duluth", state="Minnesota", elev=1428, feb="Feb 1–6",
         w=dict(pre=(378, 205, 269), x=(586, 160, 260), f=(378, 169, 269)),
         snow=dict(pre=(87, 7, 3), x=(92, 8, 4), f=(99, 14, 9)), temps=dict(pre=(24, 9), x=(22, 7), f=(23, 4)),
         travel="One stop, about 5 hours.",
         nature="Lake Superior in winter: ice on the shore and the lift bridge lit at night.",
         kids=[("Bentleyville Tour of Lights", "a walk-through lights display on the waterfront, Nov 21 to Dec 26. Free; parking $12. Santa nightly through Dec 23"),
               ("Snow tubing at Spirit Mountain", "listed at $25 for two hours, ages 3 and up, no height minimum found. Projected opening Dec 4"),
               ("Christmas City Express train", "select dates through Dec 20")],
         verdict="The most Christmas for the least effort: nearly flat-land elevation, a free lights festival, and a tubing hill with no height rule.",
         catch="A lake city, not mountains. Coldest place here: lows of 4° to 9°."),
    dict(key="steamboat", name="Steamboat Springs", state="Colorado", elev=6695, feb="Feb 22–27",
         w=dict(pre=(448, 214, 277), x=(389, 326, 304), f=(379, 251, 323)),
         snow=dict(pre=(97, 13, 8), x=(99, 16, 11), f=(100, 26, 20)), temps=dict(pre=(29, 5), x=(28, 4), f=(33, 7)),
         travel="Nonstop from Houston in Christmas week and February (3 hr 8 min), one stop on Dec 16–21. Then a 28-minute drive.",
         nature="A wide, snowy ranch valley with the Yampa River through town and hot springs steaming in the cold.",
         kids=[("Snow tubing at Saddleback Ranch", "$50.88 per rider for 2 hours; age 4 and under free on a parent's tube"),
               ("Old Town Hot Springs pools", "$27 per child (3–14), $35 per adult. Closed Christmas Day"),
               ("Winter Carnival, Feb 2–7, 2027", "street events with horses pulling kids on skis (date from the GPT-6 Astra lane's source)")],
         verdict="The best mountain option: a 99% Christmas snow record, the lowest sleeping elevation of the Colorado ski towns, and a nonstop flight.",
         catch="6,695 ft. February here means Feb 22–27, because Feb 1–6 is Winter Carnival and prices like Christmas."),
    dict(key="jackson", name="Jackson Hole", state="Wyoming", elev=6237, feb="Feb 1–6",
         w=dict(pre=(508, 215, 244), x=(539, 282, 315), f=(539, 244, 213)),
         snow=dict(pre=(96, 15, 11), x=(98, 18, 14), f=(100, 30, 24)), temps=dict(pre=(27, 3), x=(27, 1), f=(31, 5)),
         travel="Nonstop from Houston on Dec 21 (3 hr 35 min); one stop on the other dates. Town is 15 minutes from the airport.",
         nature="The Teton range rising straight up from the valley, and thousands of wild elk wintering beside town.",
         kids=[("Horse-drawn sleigh ride among the elk herd", "$43 adult, $28 child (5–12), age 4 and under free. Season Dec 19 to Apr 3; closed Christmas Day"),
               ("Grand Teton National Park", "$35 per car for 7 days. Short snow walks and viewpoints"),
               ("Astoria Hot Springs kids' pool", "$19 per child, $26.25 per adult (from the GPT-6 Astra lane's source, not rechecked)")],
         verdict="The most memorable single activity on this page: the elk sleigh ride, with no height or age limit.",
         catch="6,237 ft. Snow King's tubing hill requires 42 inches. Snow record is from Moose, in the park 12 miles north."),
    dict(key="quebec", name="Quebec City", state="Quebec", elev=320, feb="Feb 1–6",
         w=dict(pre=(877, 146, 144), x=(1151, 154, 213), f=(813, 169, 164)),
         snow=dict(pre=None, x=(91, 10, None), f=(None, 22, None)), temps=None,
         travel="One stop, about 7 hours. Passports required.",
         nature="An old walled city above the frozen St. Lawrence, dressed for Christmas.",
         kids=[("Village Vacances Valcartier", "a winter playground with more than 35 lift-served snow slides. Opens Dec 18, 2026. Height rules for small children not confirmed"),
               ("Toboggan slide on Dufferin Terrace", "beside the Château Frontenac; about $10 for 3 rides (older price)"),
               ("German Christmas Market", "Nov 19 to Dec 23, Thursday to Sunday")],
         verdict="Nearly sea level and the most Christmas atmosphere, at the highest price.",
         catch="Flights run $813 to $1,151 a person. Snow figures are from the GLM lane, not NOAA. February hotel rate rests on 2 hotels."),
    dict(key="estes", name="Estes Park", state="Colorado", elev=7522, feb="Feb 1–6",
         w=dict(pre=(341, 169, 191), x=(361, 191, 435), f=(361, 153, 181)),
         snow=dict(pre=(71, 4, 2), x=(74, 4, 2), f=(76, 4, 2)), temps=dict(pre=(36, 16), x=(36, 15), f=(37, 15)),
         travel="Nonstop to Denver, 2 hr 45 min, then a 1 hr 21 min drive with no mountain pass.",
         nature="The front door of Rocky Mountain National Park. Elk wander through town.",
         kids=[("Sledding at Hidden Valley, inside the national park", "free with park entry. The hill is at 9,240 ft and had too little snow in parts of the last two winters"),
               ("Looking for elk and deer in town", "free")],
         verdict="The cheapest fly-to trip on the page in every week.",
         catch="7,522 ft, and the weakest snow in Colorado: bare ground in town 1 Christmas in 4."),
    dict(key="winterpark", name="Winter Park", state="Colorado", elev=9000, feb="Feb 1–6",
         w=dict(pre=(341, 268, 191), x=(361, 396, 435), f=(361, 280, 181)),
         snow=dict(pre=(98, 19, 14), x=(100, 22, 17), f=(100, 34, 29)), temps=dict(pre=(30, -1), x=(29, -2), f=(33, 1)),
         travel="Nonstop to Denver, then a 1 hr 32 min drive over Berthoud Pass.",
         nature="Deep-snow forest under the Continental Divide. The most snow on the ground of any town here.",
         kids=[("Hideaway Park sledding hill", "free, sleds provided"),
               ("Coca-Cola Tube Hill at the resort", "riders must be 36 inches tall and ride alone; no price or opening date posted yet")],
         verdict="The surest and deepest snow.",
         catch="9,000 ft, which is the height the CDC says not to sleep at on the first night up from sea level."),
    dict(key="breck", name="Breckenridge", state="Colorado", elev=9600, feb="Feb 1–6",
         w=dict(pre=(341, 323, 191), x=(361, 414, 435), f=(361, 357, 181)),
         snow=dict(pre=(95, 15, 10), x=(98, 17, 12), f=(100, 29, 21)), temps=dict(pre=(31, 2), x=(30, 2), f=(33, 3)),
         travel="Nonstop to Denver, then a 1 hr 43 min drive on I-70.",
         nature="A Victorian mining town under a wall of 13,000-foot peaks.",
         kids=[("Carter Park sledding hill", "free, with loaner sleds"),
               ("Gondola ride over the town", "free"),
               ("Ice skating", "$19 per child, $21 per adult with skates (last season's price)")],
         verdict="Pretty, with free kid activities.",
         catch="9,600 ft, the highest here: 30% less oxygen than Houston."),
    dict(key="redriver", name="Red River", state="New Mexico", elev=8667, feb="Feb 1–6", drive=True, miles=837,
         w=dict(pre=(0, 480, 0), x=(0, 652, 0), f=(0, 188, 0)),
         snow=dict(pre=(62, 6, 2), x=(66, 6, 3), f=(73, 7, 3)), temps=dict(pre=(35, 8), x=(34, 7), f=(36, 9)),
         travel="No flight. 837 miles from Conroe, 12 hr 44 min of driving each way before stops.",
         nature="A small ski town in a narrow canyon of the Sangre de Cristo mountains.",
         kids=[("Tubing at the ski area", "$30 a session, 42-inch minimum (from the GLM lane's source, not rechecked)")],
         verdict="The only drive-to option, and by far the cheapest in February.",
         catch="8,667 ft, a 66% Christmas snow record, a 13-hour drive, and December rates 2.5 to 3.5 times February's."),
]

# Dec 26-31 against Dec 21-26, same hotels: (hotel before, hotel after, fare before, fare after, places left before, after)
PEAK = [("Steamboat Springs", 365, 481, 389, 1080, 287, 142), ("Jackson Hole", 281, 351, 539, 815, 32, 31),
        ("Estes Park", 170, 187, 361, 389, 203, 179), ("Breckenridge", 352, 531, 361, 389, 329, 240),
        ("Winter Park", 440, 593, 361, 389, 186, 123), ("Red River", 492, 527, None, None, 33, 12)]

AI_VS_LIVE = [
    ("Steamboat hotel, per night", "$450 / $250", "$326 / $251"),
    ("Steamboat flight, per person", "$750 / $450", "$389 / $379"),
    ("Steamboat: February saving, flights and hotel", "$2,200", "$415"),
    ("Jackson Hole hotel, per night", "$425 / $250", "$282 / $244"),
    ("Jackson Hole flight, per person", "$800 / $500", "$539 / $539"),
    ("Winter Park hotel, per night", "$400 / $240", "$396 / $280"),
    ("Denver flight, per person", "$350 / $250", "$361 / $361"),
]

SOURCES = [
    ("NOAA 1991–2020 daily climate normals, by weather station (snow odds, snow depth, temperatures)", "https://www.ncei.noaa.gov/data/normals-daily/1991-2020/access/"),
    ("NOAA white Christmas map and station list", "https://www.climate.gov/news-features/understanding-climate/interactive-map-are-you-dreaming-white-christmas"),
    ("Google Flights, Houston (IAH) round trips for each date window", "https://www.google.com/travel/flights"),
    ("Booking.com search results for each town and date window", "https://www.booking.com/"),
    ("Kayak car rental search at each arrival airport", "https://www.kayak.com/cars"),
    ("Google Maps driving times", "https://www.google.com/maps"),
    ("CDC, Travel to High Altitudes", "https://wwwnc.cdc.gov/travel/page/travel-to-high-altitudes"),
    ("National Elk Refuge sleigh rides, rates and season", "https://www.nersleighrides.com/rates-and-location-2020/"),
    ("Saddleback Ranch snow tubing", "https://saddlebackranch.net/winter-activities/snow-tubing/"),
    ("Old Town Hot Springs rates", "https://oldtownhotsprings.org/rates/"),
    ("Winter Park Coca-Cola Tube Hill", "https://www.winterparkresort.com/things-to-do/activities/coca-cola-tubing"),
    ("Snow King Mountain winter hours", "https://snowkingmountain.com/?p=12156"),
    ("Bentleyville Tour of Lights, Duluth", "https://www.bentleyvilleusa.org/"),
    ("Spirit Mountain tubing, Duluth", "https://www.spiritmt.com/tubing"),
    ("Bar W Guest Ranch, Whitefish", "https://glaciermt.com/listing/bar-w-guest-ranch"),
    ("Village Vacances Valcartier winter playground", "https://www.valcartier.com/en/activities/winter-playground/"),
    ("National Park Service, Hidden Valley sledding", "https://www.nps.gov/places/romo_sleddinghiddenvalley.htm"),
    ("Denver Gazette, Hidden Valley snowpack, Dec 30, 2025", "https://www.denvergazette.com/outtherecolorado/2025/12/30/images-of-rocky-mountain-national-parks-ski-area-turned-sledding-hill-show-how-bad-snowpack-is/"),
]

WEEKS = [("pre", "Dec 16–21"), ("x", "Dec 21–26"), ("f", "February")]

# ------------------------------------------------------------- derived ---
def money(n):
    return f"${n:,.0f}"


def e(s):
    return html.escape(str(s), quote=True)


def oxygen_less(ft):
    """Percent less oxygen pressure than sea level, standard atmosphere."""
    return round((1 - (1 - 2.25577e-5 * ft * 0.3048) ** 5.25588) * 100)


GAS = round(837 * 2 / GAS_MPG * GAS_PRICE)
for d in D:
    d["ox"] = oxygen_less(d["elev"])
    d["t"] = {}
    d["parts"] = {}
    for k, _ in WEEKS:
        fare, lodge, car = d["w"][k]
        travel = GAS if d.get("drive") else fare * PEOPLE
        d["parts"][k] = (travel, lodge * NIGHTS, car)
        d["t"][k] = travel + lodge * NIGHTS + car
    d["best"] = min(d["t"], key=d["t"].get)

by = {d["key"]: d for d in D}
maxtotal = max(max(d["t"].values()) for d in D)
cheapest_pre = sum(d["best"] == "pre" for d in D)
cheapest_feb = sum(d["best"] == "f" for d in D)
WK = dict(WEEKS)


def snow_txt(s):
    if not s:
        return "not checked"
    odds, depth, _ = s
    return (f"{odds}% of years" if odds is not None else "odds not checked") + f", {depth} in typical"


# -------------------------------------------------------------- pieces ---
def option(rank, key, week, title, gives):
    d = by[key]
    s = d["snow"][week]
    label = d["feb"] if week == "f" else WK[week]
    return f"""
        <article class="option">
          <p class="eyebrow">Option {rank} · {e(title)}</p>
          <h3>{e(d['name'])}, {e(label)}</h3>
          <p class="option__price">{money(d['t'][week])}</p>
          <dl class="facts">
            <div><dt>Elevation</dt><dd>{d['elev']:,} ft</dd></div>
            <div><dt>Oxygen vs Houston</dt><dd>{d['ox']}% less</dd></div>
            <div><dt>Snow on the ground</dt><dd>{s[0]}% of years</dd></div>
            <div><dt>Typical depth</dt><dd>{s[1]} in</dd></div>
          </dl>
          <p><strong>You get.</strong> {e(d['verdict'])}</p>
          <p><strong>You give up.</strong> {e(gives)}</p>
          <p><a href="#{key}">Details and kid activities</a></p>
        </article>"""


def bars():
    out = []
    for i, d in enumerate(D, 1):
        rows = "".join(
            f'<div class="bar bar--{k}" data-w="{d["t"][k] / maxtotal * 100:.1f}"><span>{money(d["t"][k])}</span></div>' for k, _ in WEEKS)
        out.append(f"""
      <div class="barrow">
        <div class="barrow__name">{i}. {e(d['name'])}<span class="sub">{d['elev']:,} ft</span></div>
        <div class="barrow__bars">{rows}</div>
      </div>""")
    return "".join(out)


def master_rows():
    out = []
    for i, d in enumerate(D, 1):
        cells = ""
        for k, _ in WEEKS:
            star = " best" if d["best"] == k else ""
            cells += f'<td class="tot {k}{star}">{money(d["t"][k])}</td>'
        sx, sf = d["snow"]["x"], d["snow"]["f"]
        out.append(f"""
        <tr>
          <th scope="row"><a href="#{d['key']}">{i}. {e(d['name'])}</a><span class="sub">{e(d['state'])}</span></th>
          <td>{d['elev']:,} ft<span class="sub">{d['ox']}% less oxygen</span></td>
          {cells}
          <td>{sx[0]}%</td>
          <td>{sx[1]} in → {sf[1]} in</td>
        </tr>""")
    return "".join(out)


def cards():
    out = []
    for i, d in enumerate(D, 1):
        kids = "".join(f"<li><strong>{e(a)}:</strong> {e(b)}.</li>" for a, b in d["kids"])
        alt = "ok" if d["elev"] < 5000 else ("mid" if d["elev"] < 8000 else "warn")
        prices = "".join(
            f'<div><dt>{e(d["feb"] if k == "f" else lab)}</dt><dd class="{k}">{money(d["t"][k])}</dd></div>' for k, lab in WEEKS)
        out.append(f"""
      <article class="place" id="{d['key']}">
        <header class="place__head">
          <p class="eyebrow">#{i} · {e(d['state'])}</p>
          <h3>{e(d['name'])}</h3>
          <p>{e(d['verdict'])}</p>
        </header>
        <dl class="facts facts--3">{prices}</dl>
        <p class="alt alt--{alt}"><strong>{d['elev']:,} ft · {d['ox']}% less oxygen than Houston.</strong></p>
        <p><strong>Snow on the ground.</strong> Dec 17: {snow_txt(d['snow']['pre'])}. Christmas Day: {snow_txt(d['snow']['x'])}. February: {snow_txt(d['snow']['f'])}.</p>
        <p><strong>Getting there.</strong> {e(d['travel'])}</p>
        <p><strong>What makes it special.</strong> {e(d['nature'])}</p>
        <ul class="kidlist">{kids}</ul>
        <p class="catch"><strong>The catch.</strong> {e(d['catch'])}</p>
      </article>""")
    return "".join(out)


def line_rows():
    out = []
    for d in D:
        for j, (k, lab) in enumerate(WEEKS):
            fare, lodge, car = d["w"][k]
            travel, stay, _ = d["parts"][k]
            head = f'<th scope="row" rowspan="3">{e(d["name"])}</th>' if j == 0 else ""
            tr = f'{money(travel)}<span class="sub">{"gas" if d.get("drive") else money(fare) + " × 4"}</span>'
            out.append(f"""
        <tr>{head}<td class="{k} wk">{e(d['feb'] if k == 'f' else lab)}</td><td>{tr}</td><td>{money(stay)}<span class="sub">{money(lodge)} × 5</span></td><td>{money(car) if car else '—'}</td><td class="tot">{money(d['t'][k])}</td></tr>""")
    return "".join(out)


def peak_rows():
    out = []
    for n, a, b, f1, f2, r1, r2 in PEAK:
        fly = "—" if f1 is None else f"{money(f1)} → {money(f2)}"
        out.append(f'<tr><th scope="row">{e(n)}</th><td>{money(a)} → {money(b)}<span class="sub">+{round((b / a - 1) * 100)}% a night</span></td><td>{fly}</td><td>{r1} → {r2}</td></tr>')
    return "".join(out)


def snow_rows():
    out = []
    for d in D:
        cells = ""
        for k, _ in WEEKS:
            s = d["snow"][k]
            t = d["temps"][k] if d["temps"] else None
            if s:
                odds = f"{s[0]}%" if s[0] is not None else "—"
                low = f"{s[2]} in" if s[2] is not None else "—"
                cells += f'<td class="{k}">{odds}</td><td class="{k}">{s[1]} in</td><td class="{k}">{low}</td>'
            else:
                cells += f'<td class="{k}">—</td><td class="{k}">—</td><td class="{k}">—</td>'
            cells += f'<td class="{k}">{t[0]}° / {t[1]}°</td>' if t else f'<td class="{k}">—</td>'
        out.append(f'<tr><th scope="row">{e(d["name"])}<span class="sub">{d["elev"]:,} ft</span></th>{cells}</tr>')
    return "".join(out)


def ai_rows():
    return "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td class="tot">{e(c)}</td></tr>' for a, b, c in AI_VS_LIVE)


def source_items():
    return "".join(f'<li><a href="{e(u)}" rel="noopener">{e(t)}</a></li>' for t, u in SOURCES)


calc_data = {d["key"]: dict(name=d["name"], feb=d["feb"], drive=bool(d.get("drive")), miles=d.get("miles", 0), w=d["w"]) for d in D}
wf, du, sb, jk = by["whitefish"], by["duluth"], by["steamboat"], by["jackson"]
lanes_file = ROOT / "research/lanes.html"
LANES = lanes_file.read_text() if lanes_file.exists() else ""

PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <meta name="color-scheme" content="light dark">
  <title>Snow Trip: Where and When?</title>
  <meta name="description" content="Nine snow destinations from Houston, priced for three weeks, with NOAA snow records and elevation.">
  <link rel="icon" href="icon.svg" type="image/svg+xml">
  <link rel="preload" href="assets/fonts/inter-variable.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <main id="main">

    <section class="hero">
      <div class="container stack">
        <p class="eyebrow">Family snow trip · 2 adults, 2 kids, 5 nights from Houston</p>
        <h1>Where and when for the snow trip?</h1>
        <p class="lede">Two decisions: which week, and which place. The short answer is the week before Christmas, Dec 16–21, in Whitefish or Duluth. The one option that puts you in the snow on Christmas morning for a fair price is Steamboat Springs.</p>
        <nav class="jump" aria-label="On this page">
          <a href="#options">1. The three options</a>
          <a href="#week">2. Which week</a>
          <a href="#place">3. Which place</a>
          <a href="#ranked">4. All nine, ranked</a>
          <a href="#details">5. The detail</a>
        </nav>
        <p class="caption muted">Every price is a live quote read on {CHECKED}, for flights, hotel and rental car for four people and five nights. Food and activities are left out because they cost the same in any week.</p>
      </div>
    </section>

    <section class="section" id="options">
      <div class="container stack">
        <h2>1. The three options worth choosing between</h2>
        <p>Nine places and three weeks make 27 combinations. These three are the ones that win on something.</p>
        <div class="options">{option(1, 'whitefish', 'pre', 'Mountains, low elevation', 'Being there on Christmas morning. Snow is a little less certain than in Colorado. Flights have one stop and take 6 to 9 hours.')}{option(2, 'duluth', 'pre', 'Most Christmas, lowest elevation', 'Mountain scenery. It is the coldest place on the list. Snow is on the ground that week in 87% of years.')}{option(3, 'steamboat', 'x', 'In the snow on Christmas morning', f'About {money(sb["t"]["x"] - wf["t"]["pre"])} more than Whitefish, and a sleeping elevation of 6,695 ft. The hot springs pools are closed on Christmas Day.')}
        </div>
        <div class="callout stack stack--tight">
          <p><strong>How to choose.</strong> If waking up in the snow on Dec 25 is the point, it is Option 3. If the point is snow, animals and Christmas lights sometime in December, Options 1 and 2 cost {money(sb['t']['x'] - du['t']['pre'])} to {money(sb['t']['x'] - wf['t']['pre'])} less and sit far lower.</p>
          <p><strong>Not recommended in any plan:</strong> a stay that runs past Dec 26, and Presidents Day week (Feb 12–17). Both price well above the weeks shown here.</p>
        </div>
      </div>
    </section>

    <section class="section section--alt" id="week">
      <div class="container stack">
        <h2>2. Which week</h2>
        <div class="weeks">
          <article class="week week--pre">
            <h3>Dec 16–21</h3>
            <p class="eyebrow">the week before</p>
            <p><strong>Cost.</strong> Cheaper than Christmas week in all 9 places, and within $200 of February in 6 of them. Hotels in the mountain towns run 12% to 34% under Christmas week.</p>
            <p><strong>Snow.</strong> The four snow-sure mountain towns 95% to 98%. Whitefish 84%, Duluth 87%. About 3 inches thinner than Christmas Day.</p>
            <p><strong>What is different.</strong> Home for Christmas morning. Elk sleigh rides start Dec 19 and Quebec's snow park opens Dec 18, so the end of the stay catches both.</p>
          </article>
          <article class="week week--x">
            <h3>Dec 21–26</h3>
            <p class="eyebrow">Christmas week</p>
            <p><strong>Cost.</strong> Flights to Denver and Steamboat cost about the same as February. Flights to Whitefish, Duluth and Quebec City rise 31% to 81% over the week before.</p>
            <p><strong>Snow.</strong> Best December odds: 98% to 100% in four mountain towns, 92% in Whitefish and Duluth.</p>
            <p><strong>What is different.</strong> The only week you wake up there on Dec 25. Steamboat's hot springs and Jackson's elk sleigh rides are closed that day.</p>
          </article>
          <article class="week week--peak">
            <h3>Dec 26–31</h3>
            <p class="eyebrow">the real peak</p>
            <p><strong>Cost.</strong> Avoid. The Steamboat nonstop goes from $389 to $1,080 a person and mountain hotels rise 7% to 51%.</p>
            <p><strong>Snow.</strong> Same as Christmas week.</p>
            <p><strong>What is different.</strong> Fewest rooms left of any week.</p>
          </article>
          <article class="week week--f">
            <h3>February</h3>
            <p class="eyebrow">a non-holiday week</p>
            <p><strong>Cost.</strong> Cheapest week in {cheapest_feb} of 9 places, usually by less than $200. Red River is the exception: $1,191 against $2,651.</p>
            <p><strong>Snow.</strong> The deepest of the winter: about 60% more on the ground than at Christmas in the snow-sure towns, and 98% to 100% everywhere but Estes Park and Red River.</p>
            <p><strong>What is different.</strong> No Christmas events. Skip Feb 12–17. In Steamboat use Feb 22–27, after Winter Carnival.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section" id="place">
      <div class="container stack">
        <h2>3. Which place</h2>
        <p>Total for each place in each week, in the ranked order explained in section 4.</p>
        <div class="legend"><span class="key key--pre">Dec 16–21</span><span class="key key--x">Christmas week, Dec 21–26</span><span class="key key--f">February</span></div>
        <div class="bars" aria-hidden="true">{bars()}
        </div>
        <div class="tablewrap" tabindex="0" role="region" aria-label="All nine places: elevation, cost by week and snow">
          <table class="num">
            <thead><tr><th scope="col">Place, in ranked order</th><th scope="col">Elevation</th><th scope="col" class="pre">Dec 16–21</th><th scope="col" class="x">Dec 21–26</th><th scope="col" class="f">February</th><th scope="col">Snow on Dec 25</th><th scope="col">Depth, Dec 25 → Feb</th></tr></thead>
            <tbody>{master_rows()}
            </tbody>
          </table>
        </div>
        <p class="caption muted">The cheapest week for each place is outlined. "Snow on Dec 25" is the share of years from 1991 to 2020 with at least an inch on the ground (NOAA). Oxygen is the air pressure at that elevation compared with sea level.</p>
        <ul class="notes">
          <li><strong>The low places are cheap the week before Christmas</strong> and expensive in Christmas week, because their flights jump. Whitefish costs {money(wf['t']['x'] - wf['t']['pre'])} more in Christmas week.</li>
          <li><strong>The Colorado towns are the reverse on flights:</strong> the Denver fare is $341 to $361 in all three weeks. Their gap is hotels and the rental car ($435 at Denver in Christmas week, $181 to $191 otherwise).</li>
          <li><strong>Elevation and snow certainty pull in opposite directions.</strong> The places above 6,000 ft have the 95%-plus snow records, except Estes Park and Red River. The low places are 84% to 92% in December.</li>
        </ul>
      </div>
    </section>

    <section class="section section--alt" id="ranked">
      <div class="container stack">
        <h2>4. All nine, ranked for kids aged 4 to 7</h2>
        <p>Ranked on elevation first, then how sure the snow is, how hard the trip is with small children, and what they can actually do there.</p>
        <div class="places">{cards()}
        </div>
        <h3>Tubing hills and height</h3>
        <p>Rules found for a child between 36 and 42 inches tall:</p>
        <ul class="notes">
          <li><strong>Can ride:</strong> Spirit Mountain in Duluth (ages 3 and up), Saddleback Ranch in Steamboat (age 4 and under shares a parent's tube), Winter Park's Coca-Cola Tube Hill (36 inches and up).</li>
          <li><strong>Cannot ride under 42 inches:</strong> Snow King in Jackson, Red River, Mount Norquay in Banff.</li>
          <li><strong>No height rule:</strong> the elk sleigh ride in Jackson, and the sleigh and dog sled rides near Whitefish.</li>
          <li><strong>Opening dates:</strong> none of the mountain tubing hills has published one for this season. Saddleback Ranch says a bookable slot online means it is open. Snow King opens when there is enough snow; its page shows Dec 20 last season.</li>
        </ul>
        <p class="caption muted">Also suggested by the AI researchers and not priced: Banff (4,540 ft, needs passports), West Yellowstone, Tahoe City, and Santa Fe (ruled out: 9% chance of snow in town at Christmas).</p>
      </div>
    </section>

    <section class="section" id="details">
      <div class="container stack">
        <h2>5. The detail behind the numbers</h2>
        <p>Open any of these to check the working.</p>

        <details class="more">
          <summary>Run your own numbers</summary>
          <div class="stack">
            <p>Change the family size, the nights or any rate. The starting values are the quotes on this page.</p>
            <form class="calc" id="calc">
              <div class="calc__inputs">
                <label>Destination<select id="c-dest"></select></label>
                <label>Travelers<input id="c-people" type="number" min="1" max="12" value="4" inputmode="numeric"></label>
                <label>Nights<input id="c-nights" type="number" min="1" max="14" value="5" inputmode="numeric"></label>
                <label>Lodging tax and fees, %<input id="c-tax" type="number" min="0" max="40" value="0" inputmode="decimal"></label>
                <label>Food and activities per day, whole family<input id="c-daily" type="number" min="0" max="2000" step="10" value="0" inputmode="numeric"></label>
              </div>
              <div class="tablewrap">
                <table class="num" aria-live="polite">
                  <thead><tr><th scope="col">Line</th><th scope="col" class="pre">Dec 16–21</th><th scope="col" class="x">Dec 21–26</th><th scope="col" class="f" id="c-feblabel">February</th></tr></thead>
                  <tbody id="c-body"></tbody>
                </table>
              </div>
              <div class="calc__rates">
                <p class="caption muted">Rates used, editable:</p>
                <label>Fare per person, Dec 16–21<input id="c-fare-pre" type="number" min="0"></label>
                <label>Fare per person, Christmas<input id="c-fare-x" type="number" min="0"></label>
                <label>Fare per person, February<input id="c-fare-f" type="number" min="0"></label>
                <label>Hotel per night, Dec 16–21<input id="c-lodge-pre" type="number" min="0"></label>
                <label>Hotel per night, Christmas<input id="c-lodge-x" type="number" min="0"></label>
                <label>Hotel per night, February<input id="c-lodge-f" type="number" min="0"></label>
                <label>Car for 5 days, Dec 16–21<input id="c-car-pre" type="number" min="0"></label>
                <label>Car for 5 days, Christmas<input id="c-car-x" type="number" min="0"></label>
                <label>Car for 5 days, February<input id="c-car-f" type="number" min="0"></label>
              </div>
            </form>
            <noscript><p class="callout">The calculator needs JavaScript. Every number it starts from is in the next table.</p></noscript>
          </div>
        </details>

        <details class="more">
          <summary>Cost line by line: flights, hotel and car for every place and week</summary>
          <div class="stack">
            <div class="tablewrap" tabindex="0" role="region" aria-label="Cost line items">
              <table class="num">
                <thead><tr><th scope="col">Place</th><th scope="col">Week</th><th scope="col">Travel</th><th scope="col">Lodging</th><th scope="col">Car</th><th scope="col">Total</th></tr></thead>
                <tbody>{line_rows()}
                </tbody>
              </table>
            </div>
            <p class="caption muted">Red River is a drive: 837 miles each way at {GAS_MPG} mpg and ${GAS_PRICE:.2f} a gallon. Lodging is before tax.</p>
          </div>
        </details>

        <details class="more">
          <summary>Why Dec 26–31 and Presidents Day week are out</summary>
          <div class="stack">
            <p>Staying Dec 26–31 instead of Dec 21–26 changes the same trip like this:</p>
            <div class="tablewrap" tabindex="0" role="region" aria-label="Dec 21 to 26 against Dec 26 to 31">
              <table class="num">
                <thead><tr><th scope="col">Destination</th><th scope="col">Hotel per night</th><th scope="col">Flight per person</th><th scope="col">Places still bookable</th></tr></thead>
                <tbody>{peak_rows()}</tbody>
              </table>
            </div>
            <p class="caption muted">Each comparison uses the hotels listed in both of its weeks, so the Dec 21–26 rate here differs a little from the main table. Only the six mountain towns were checked for this week.</p>
            <p>Presidents Day week, Feb 12–17: the same 11 Steamboat hotels averaged $396 a night against $339 for Dec 21–26, and the nonstop flight is $546 against $389.</p>
          </div>
        </details>

        <details class="more">
          <summary>Snow and temperature records for all three weeks</summary>
          <div class="stack">
            <p>30-year records from NOAA weather stations, not forecasts. "Low year" is the depth that 1 winter in 4 falls below.</p>
            <div class="tablewrap" tabindex="0" role="region" aria-label="Snow and temperature records">
              <table class="num">
                <thead>
                  <tr><th rowspan="2" scope="col">Town</th><th colspan="4" scope="colgroup" class="pre">Dec 17</th><th colspan="4" scope="colgroup" class="x">Dec 25</th><th colspan="4" scope="colgroup" class="f">Feb 10</th></tr>
                  <tr><th scope="col">Years with snow</th><th scope="col">Typical</th><th scope="col">Low year</th><th scope="col">High / low °F</th><th scope="col">Years with snow</th><th scope="col">Typical</th><th scope="col">Low year</th><th scope="col">High / low °F</th><th scope="col">Years with snow</th><th scope="col">Typical</th><th scope="col">Low year</th><th scope="col">High / low °F</th></tr>
                </thead>
                <tbody>{snow_rows()}</tbody>
              </table>
            </div>
            <p class="caption muted">Jackson Hole's record is from Moose, in Grand Teton National Park. Winter Park's temperatures are from Fraser and Breckenridge's from Dillon. Quebec City is not in NOAA's data; its figures come from the GLM lane's station records and were not rechecked.</p>
          </div>
        </details>

        <details class="more">
          <summary>How these numbers were checked</summary>
          <div class="stack">
            <p>Five AI models were each given the same brief through Ringer. Their output had to pass an automated check: at least 8 destinations, numbers in every field, and source links that load. Then every price on this page was read separately from live booking sites, and every snow figure from NOAA's station files.</p>
            <ul class="notes">
              <li><strong>GPT-6 Astra passed.</strong> Its snow figures matched NOAA. Its hotel and flight prices were labeled as estimates, and the live quotes show they were too pessimistic about Christmas:</li>
            </ul>
            <div class="tablewrap" tabindex="0" role="region" aria-label="AI estimate against live quote">
              <table class="num">
                <thead><tr><th scope="col">Christmas / February</th><th scope="col">GPT-6 Astra estimate</th><th scope="col">Live quote, {CHECKED}</th></tr></thead>
                <tbody>{ai_rows()}</tbody>
              </table>
            </div>
            <ul class="notes">
              {LANES}
              <li><strong>Three activity prices were spot-checked</strong> against the operators' own pages (elk sleigh ride, Saddleback tubing, Old Town Hot Springs). All three matched.</li>
            </ul>
          </div>
        </details>

        <details class="more">
          <summary>Limits of this comparison</summary>
          <ul class="notes">
            <li>Hotel comparisons use 6 to 13 hotels per town: the ones Booking.com listed first in each week being compared. Small samples; treat a gap under $200 as a tie.</li>
            <li>For the six mountain towns, the Dec 16–21 hotel rate is the Christmas-week rate multiplied by the price ratio at hotels listed in both weeks. Breckenridge's ratio rests on 6 hotels.</li>
            <li>Rates are before lodging tax and resort fees. Flights exclude bags.</li>
            <li>Prices marked "older price" are from past seasons. Activity prices other than the three spot-checked ones come from pages the AI lanes cited or from tourism sites.</li>
            <li>Snow records describe 1991–2020. Colorado's early season was thin in December 2025.</li>
            <li>The oxygen figures are standard-atmosphere pressure at each town's elevation compared with sea level.</li>
            <li>The altitude guidance is the CDC's general advice for travelers, not medical advice for your children.</li>
          </ul>
        </details>

        <details class="more">
          <summary>Sources</summary>
          <div class="stack">
            <ul class="notes sources">{source_items()}</ul>
            <p class="caption muted">Raw price observations, NOAA station data and the AI output are in the <a href="https://github.com/brandoncordoba/snow-trip/tree/main/research">research folder</a>.</p>
          </div>
        </details>
      </div>
    </section>
  </main>
  <footer class="site-footer"><div class="container"><p class="caption muted">Prepared {CHECKED}. Prices are quotes on that date, not offers.</p></div></footer>
  <script id="calc-data" type="application/json">{json.dumps(dict(dest=calc_data, mpg=GAS_MPG, gas=GAS_PRICE))}</script>
  <script src="app.js" defer></script>
</body>
</html>
"""

(ROOT / "index.html").write_text(PAGE)
print("wrote index.html", len(PAGE), "bytes; cheapest week: pre", cheapest_pre, "feb", cheapest_feb)
for d in D:
    print(f"{d['name']:18} {d['elev']:>5} ft ox-{d['ox']}%  pre {d['t']['pre']:>6,}  xmas {d['t']['x']:>6,}  feb {d['t']['f']:>6,}  best {d['best']}")
