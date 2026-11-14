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

# ---------------------------------------------------------------- inputs ---
# Lodging: average nightly rate (before tax) across the SAME hotels in both
# windows, Booking.com, 2 adults + 2 children, 1 room. See research/booking_raw.txt.
# Flights: Google Flights, round trip per person from Houston (IAH), United fare.
# Car: Kayak, cheapest economy car for the 5 days, at the arrival airport.
D = [
    dict(key="steamboat", name="Steamboat Springs", state="Colorado", airport="HDN",
         feb_label="Feb 22–27", elev=6695,
         lodge_x=326, lodge_f=251, lodge_n=9, lodge_cheaper=6,
         fly_x=389, fly_f=379, car_x=304, car_f=323, drive=False,
         peak_lodge=(365, 481), peak_fly=1080, rooms=(287, 142, 215),
         snow="STEAMBOAT SPRINGS, CO US", temps="STEAMBOAT SPRINGS, CO US",
         travel="Nonstop from Houston, 3 hr 8 min, then a 28-minute drive.",
         nature="A wide, snowy ranch valley with the Yampa River running through town and hot springs steaming in the cold.",
         kids=[
             ("Snow tubing at Saddleback Ranch", "$50.88 per rider for 2 hours; age 4 and under free on a parent's tube"),
             ("Old Town Hot Springs pools", "$27 per child (3–14), $35 per adult. Closed Christmas Day"),
             ("Winter Carnival, Feb 2–7, 2027", "Street events with horses pulling kids on skis. February only (date from the GPT-6 Astra lane's source)"),
         ],
         verdict="Best overall. Lowest sleeping elevation of the Colorado ski towns, a 99% snow record, a nonstop flight both ways, and a Christmas markup under $400.",
         note="February uses Feb 22–27 here because Feb 1–6 is Winter Carnival week, when the same hotels cost as much as Christmas."),
    dict(key="jackson", name="Jackson Hole", state="Wyoming", airport="JAC",
         feb_label="Feb 1–6", elev=6237,
         lodge_x=282, lodge_f=244, lodge_n=11, lodge_cheaper=9,
         fly_x=539, fly_f=539, car_x=315, car_f=213, drive=False,
         peak_lodge=(281, 351), peak_fly=815, rooms=(32, 31, 37),
         snow="MOOSE, WY US", temps="MOOSE, WY US",
         travel="Nonstop from Houston on Dec 21 (3 hr 35 min); one stop on the February dates. Town is 15 minutes from the airport.",
         nature="The Teton range rising straight up from the valley, and thousands of wild elk wintering beside town.",
         kids=[
             ("Horse-drawn sleigh ride among the elk herd", "$43 adult, $28 child (5–12), age 4 and under free. Closed Christmas Day; season Dec 19–Apr 3"),
             ("Grand Teton National Park", "$35 per car for 7 days. Short snow walks and viewpoints"),
             ("Astoria Hot Springs kids' pool", "$19 per child, $26.25 per adult (from the GPT-6 Astra lane's source, not rechecked)"),
         ],
         verdict="Most memorable for nature. The elk sleigh ride is the one activity on this page a 4-year-old can do that exists nowhere else.",
         note="Snow record is from Moose, inside Grand Teton National Park, 12 miles north. The town of Jackson holds less snow."),
    dict(key="estes", name="Estes Park", state="Colorado", airport="DEN",
         feb_label="Feb 1–6", elev=7522,
         lodge_x=191, lodge_f=153, lodge_n=11, lodge_cheaper=9,
         fly_x=361, fly_f=361, car_x=435, car_f=181, drive=False,
         peak_lodge=(170, 187), peak_fly=389, rooms=(203, 179, 316),
         snow="ESTES PARK 3 SSE, CO US", temps="ESTES PARK 3 SSE, CO US",
         travel="Nonstop to Denver, 2 hr 45 min, then a 1 hr 21 min drive with no mountain pass.",
         nature="The front door of Rocky Mountain National Park. Elk wander through town.",
         kids=[
             ("Sledding at Hidden Valley, inside the national park", "Free with park entry. The hill sits at 9,240 ft and had too little snow to sled in parts of the last two winters"),
             ("Looking for elk and deer in town", "Free"),
         ],
         verdict="Cheapest by about $650, but the weakest snow among the Colorado towns: 1 Christmas in 4 has bare ground in town.",
         note=""),
    dict(key="breck", name="Breckenridge", state="Colorado", airport="DEN",
         feb_label="Feb 1–6", elev=9600,
         lodge_x=414, lodge_f=357, lodge_n=6, lodge_cheaper=4,
         fly_x=361, fly_f=361, car_x=435, car_f=181, drive=False,
         peak_lodge=(352, 531), peak_fly=389, rooms=(329, 240, 596),
         snow="BRECKENRIDGE, CO US", temps="DILLON 1 E, CO US",
         travel="Nonstop to Denver, then a 1 hr 43 min drive on I-70.",
         nature="A Victorian mining town under a wall of 13,000-foot peaks.",
         kids=[
             ("Carter Park sledding hill", "Free, with loaner sleds"),
             ("Gondola ride over the town", "Free"),
             ("Ice skating", "$19 per child, $21 per adult with skates (last season's price)"),
         ],
         verdict="Pretty, with free kid activities, but the town sits at 9,600 ft. That is above the height the CDC says not to sleep at on your first night up from sea level.",
         note="Temperatures are from Dillon, 9 miles away, because the Breckenridge station does not report them."),
    dict(key="winterpark", name="Winter Park", state="Colorado", airport="DEN",
         feb_label="Feb 1–6", elev=9000,
         lodge_x=396, lodge_f=280, lodge_n=7, lodge_cheaper=6,
         fly_x=361, fly_f=361, car_x=435, car_f=181, drive=False,
         peak_lodge=(440, 593), peak_fly=389, rooms=(186, 123, 241),
         snow="WINTER PARK, CO US", temps="FRASER, CO US",
         travel="Nonstop to Denver, then a 1 hr 32 min drive over Berthoud Pass.",
         nature="Deep-snow forest under the Continental Divide. The most snow on the ground of any town here.",
         kids=[
             ("Hideaway Park sledding hill", "Free, sleds provided"),
             ("Coca-Cola Tube Hill at the resort", "Riders must be 36 inches tall and ride alone; price not posted yet"),
         ],
         verdict="The surest snow, but 9,000 ft is high for a first night, and February is $834 cheaper here.",
         note="Temperatures are from Fraser, 4 miles down the valley."),
    dict(key="redriver", name="Red River", state="New Mexico", airport=None,
         feb_label="Feb 1–6", elev=8667,
         lodge_x=652, lodge_f=188, lodge_n=6, lodge_cheaper=6,
         fly_x=0, fly_f=0, car_x=0, car_f=0, drive=True, miles=837, drive_time="12 hr 44 min",
         peak_lodge=(492, 527), peak_fly=None, rooms=(33, 12, 129),
         snow="RED RIVER, NM US", temps="RED RIVER, NM US",
         travel="No flight. 837 miles from Conroe, 12 hr 44 min of driving each way before stops.",
         nature="A small ski town in a narrow canyon of the Sangre de Cristo mountains.",
         kids=[("Town sledding and tubing", "Not price-checked")],
         verdict="The only drive-to option. Christmas week is nearly sold out and what is left costs 3.5 times the February rate.",
         note="What is left for Christmas is mostly townhouses and cabins, so the nightly rate is for a larger unit than a hotel room."),
]
GAS_MPG, GAS_PRICE = 20, 3.00  # assumption for the drive option; editable in the calculator
PEOPLE, NIGHTS = 4, 5

# The week before Christmas week, Dec 14-19 (research/booking_dec14_raw.txt, flights_cars_raw.txt).
# lodge = (Dec 21-26, Dec 14-19) average at the same n hotels; fly = United fare per person; snow = NOAA Dec 17.
DEC14 = dict(
    steamboat=dict(lodge=(340, 158, 10), fly=522, car=243, odds=96.6, depth=13, low=8, flag="No nonstop that week: one stop on United"),
    jackson=dict(lodge=(278, 188, 12), fly=485, car=234, odds=95.8, depth=15, low=11, flag="One stop. Elk sleigh rides do not start until Dec 19"),
    estes=dict(lodge=(176, 148, 9), fly=361, car=174, odds=71.3, depth=4, low=2, flag=""),
    breck=dict(lodge=(373, 268, 3), fly=361, car=174, odds=95.3, depth=15, low=10, flag="Only 3 hotels matched"),
    winterpark=dict(lodge=(435, 265, 9), fly=361, car=174, odds=98.4, depth=19, low=14, flag=""),
    redriver=dict(lodge=(652, 301, 6), fly=0, car=0, odds=61.9, depth=6, low=2, flag=""),
)

# Presidents Day week check (Feb 12-17): same hotels.
PRES = dict(steamboat_lodge=(339, 396, 11), hdn_fly=546, den_fly=341)  # research/booking_presidents_raw.txt

# What the GPT lane estimated before live prices were checked.
AI_VS_LIVE = [
    ("Steamboat hotel, per night", "$450 / $250", "$326 / $251"),
    ("Steamboat flight, per person", "$750 / $450", "$389 / $379"),
    ("Steamboat: February saving, flights and hotel", "$2,200", "$415"),
    ("Jackson Hole hotel, per night", "$425 / $250", "$282 / $244"),
    ("Jackson Hole flight, per person", "$800 / $500", "$539 / $539"),
    ("Winter Park hotel, per night", "$400 / $240", "$396 / $280"),
    ("Denver flight, per person", "$350 / $250", "$361 / $361"),
]

ALSO = [
    ("Banff, Alberta", "On all three AI lists. Canadian Rockies, sleigh rides, only 4,600 ft. Needs passports and a 1 hr 45 min drive from Calgary. Not price-checked."),
    ("West Yellowstone, Montana", "Geysers in the snow by heated snowcoach ($160 per child, $190 per adult for the day). A long, cold day for a 4-year-old."),
    ("Tahoe City, California", "Lake scenery and milder cold. 83% snow record, and rain is possible at lake level."),
    ("Santa Fe, New Mexico", "Drivable in 13 hours, but only a 9% chance of snow on the ground in town at Christmas. Ruled out."),
]

SOURCES = [
    ("NOAA 1991–2020 daily climate normals, by weather station (snow odds, snow depth, temperatures)", "https://www.ncei.noaa.gov/data/normals-daily/1991-2020/access/"),
    ("NOAA white Christmas map and station list", "https://www.climate.gov/news-features/understanding-climate/interactive-map-are-you-dreaming-white-christmas"),
    ("Google Flights, Houston (IAH) round trips for each date window", "https://www.google.com/travel/flights"),
    ("Bentleyville Tour of Lights, Duluth", "https://www.bentleyvilleusa.org/"),
    ("Spirit Mountain tubing, Duluth", "https://www.spiritmt.com/tubing"),
    ("Village Vacances Valcartier winter playground", "https://www.valcartier.com/en/activities/winter-playground/"),
    ("Bar W Guest Ranch, Whitefish", "https://glaciermt.com/listing/bar-w-guest-ranch"),
    ("Snow King Mountain winter hours", "https://snowkingmountain.com/?p=12156"),
    ("Winter Park Coca-Cola Tube Hill", "https://www.winterparkresort.com/things-to-do/activities/coca-cola-tubing"),
    ("Booking.com search results for each town and date window", "https://www.booking.com/"),
    ("Kayak car rental search at DEN, HDN and JAC", "https://www.kayak.com/cars"),
    ("Google Maps driving times", "https://www.google.com/maps"),
    ("CDC, Travel to High Altitudes", "https://wwwnc.cdc.gov/travel/page/travel-to-high-altitudes"),
    ("National Elk Refuge sleigh rides, rates and season", "https://www.nersleighrides.com/rates-and-location-2020/"),
    ("Saddleback Ranch snow tubing", "https://saddlebackranch.net/winter-activities/snow-tubing/"),
    ("Old Town Hot Springs rates", "https://oldtownhotsprings.org/rates/"),
    ("National Park Service, Hidden Valley sledding", "https://www.nps.gov/places/romo_sleddinghiddenvalley.htm"),
    ("Denver Gazette, Hidden Valley snowpack, Dec 30, 2025", "https://www.denvergazette.com/outtherecolorado/2025/12/30/images-of-rocky-mountain-national-parks-ski-area-turned-sledding-hill-show-how-bad-snowpack-is/"),
]

# ------------------------------------------------------------- derived ---
normals = {r["name"]: r for r in json.loads((ROOT / "research/noaa_normals.json").read_text())}


def money(n):
    return f"${n:,.0f}"


def e(s):
    return html.escape(str(s), quote=True)


for d in D:
    if d["drive"]:
        gas = round(d["miles"] * 2 / GAS_MPG * GAS_PRICE)
        d["travel_x"] = d["travel_f"] = gas
        d["car_x"] = d["car_f"] = 0
    else:
        d["travel_x"] = d["fly_x"] * PEOPLE
        d["travel_f"] = d["fly_f"] * PEOPLE
    d["stay_x"] = d["lodge_x"] * NIGHTS
    d["stay_f"] = d["lodge_f"] * NIGHTS
    d["total_x"] = d["travel_x"] + d["stay_x"] + d["car_x"]
    d["total_f"] = d["travel_f"] + d["stay_f"] + d["car_f"]
    d["diff"] = d["total_x"] - d["total_f"]
    d["pct"] = round(d["diff"] / d["total_f"] * 100)
    s = normals[d["snow"]]
    t = normals[d["temps"]]
    d["n"] = dict(odds_x=s["cover_dec"], odds_f=s["cover_feb"], depth_x=s["depth50_dec"], depth_f=s["depth50_feb"],
                  low_x=s["depth25_dec"], low_f=s["depth25_feb"], hi_x=t["hi_dec"], lo_x=t["lo_dec"], hi_f=t["hi_feb"], lo_f=t["lo_feb"])

by = {d["key"]: d for d in D}
sb = by["steamboat"]
maxtotal = max(d["total_x"] for d in D)

# -------------------------------------------------------------- pieces ---
def cost_rows():
    out = []
    for d in D:
        trav = "Gas" if d["drive"] else "Flights"
        out.append(f"""
        <tr>
          <th scope="row">{e(d['name'])}<span class="sub">{e(d['state'])} · {e(d['feb_label'])}</span></th>
          <td>{money(d['travel_x'])}<span class="sub">{trav}</span></td>
          <td>{money(d['stay_x'])}<span class="sub">{money(d['lodge_x'])} × 5</span></td>
          <td>{money(d['car_x']) if d['car_x'] else '—'}</td>
          <td class="tot x">{money(d['total_x'])}</td>
          <td>{money(d['travel_f'])}</td>
          <td>{money(d['stay_f'])}<span class="sub">{money(d['lodge_f'])} × 5</span></td>
          <td>{money(d['car_f']) if d['car_f'] else '—'}</td>
          <td class="tot f">{money(d['total_f'])}</td>
          <td class="diff">+{money(d['diff'])}<span class="sub">+{d['pct']}%</span></td>
        </tr>""")
    return "".join(out)


def bars():
    out = []
    for d in sorted(D, key=lambda d: d["diff"]):
        out.append(f"""
      <div class="barrow">
        <div class="barrow__name">{e(d['name'])}</div>
        <div class="barrow__bars">
          <div class="bar bar--x" data-w="{d['total_x'] / maxtotal * 100:.1f}"><span>{money(d['total_x'])}</span></div>
          <div class="bar bar--f" data-w="{d['total_f'] / maxtotal * 100:.1f}"><span>{money(d['total_f'])}</span></div>
        </div>
        <div class="barrow__diff">+{money(d['diff'])}</div>
      </div>""")
    return "".join(out)


def peak_rows():
    out = []
    for d in D:
        a, b = d["peak_lodge"]
        up = round((b / a - 1) * 100)
        fly = "—" if d["peak_fly"] is None else f"{money(d['fly_x'])} → {money(d['peak_fly'])}"
        r = d["rooms"]
        out.append(f"""
        <tr>
          <th scope="row">{e(d['name'])}</th>
          <td>{money(a)} → {money(b)}<span class="sub">+{up}% a night</span></td>
          <td>{fly}</td>
          <td>{r[0]} → {r[1]}</td>
        </tr>""")
    return "".join(out)


def dec14_rows():
    out = []
    for d in D:
        x = DEC14[d["key"]]
        travel = d["travel_x"] if d["drive"] else x["fly"] * PEOPLE
        total = travel + x["lodge"][1] * NIGHTS + x["car"]
        x["total"] = total
        vf = total - d["total_f"]
        flag = f'<span class="sub">{e(x["flag"])}</span>' if x["flag"] else ""
        out.append(f"""
        <tr>
          <th scope="row">{e(d['name'])}{flag}</th>
          <td class="tot">{money(total)}<span class="sub">hotel {money(x['lodge'][1])} a night</span></td>
          <td>−{money(d['total_x'] - total)}</td>
          <td>{'−' if vf < 0 else '+'}{money(abs(vf))}</td>
          <td>{x['odds']:.0f}%<span class="sub">{d['n']['odds_x']:.0f}% on Dec 25</span></td>
          <td>{x['depth']} in<span class="sub">{d['n']['depth_x']:.0f} in on Dec 25</span></td>
        </tr>""")
    return "".join(out)


def snow_rows():
    out = []
    for d in D:
        n = d["n"]
        out.append(f"""
        <tr>
          <th scope="row">{e(d['name'])}<span class="sub">{d['elev']:,} ft</span></th>
          <td class="x">{n['odds_x']:.0f}%</td><td class="f">{n['odds_f']:.0f}%</td>
          <td class="x">{n['depth_x']:.0f} in</td><td class="f">{n['depth_f']:.0f} in</td>
          <td class="x">{n['low_x']:.0f} in</td><td class="f">{n['low_f']:.0f} in</td>
          <td class="x">{n['hi_x']:.0f}° / {n['lo_x']:.0f}°</td><td class="f">{n['hi_f']:.0f}° / {n['lo_f']:.0f}°</td>
        </tr>""")
    return "".join(out)


def cards():
    out = []
    for i, d in enumerate(D, 1):
        n = d["n"]
        kids = "".join(f"<li><strong>{e(a)}.</strong> {e(b)}.</li>" for a, b in d["kids"])
        alt = "ok" if d["elev"] < 8000 else "warn"
        altword = "Under the CDC's 8,000 ft caution line" if d["elev"] < 8000 else ("Above 9,000 ft: the CDC says not to sleep this high on day one from sea level" if d["elev"] >= 9000 else "Above the CDC's 8,000 ft caution line")
        note = f'<p class="caption muted">{e(d["note"])}</p>' if d["note"] else ""
        out.append(f"""
      <article class="place" id="{d['key']}">
        <header class="place__head">
          <p class="eyebrow">#{i} · {e(d['state'])}</p>
          <h3>{e(d['name'])}</h3>
          <p>{e(d['verdict'])}</p>
        </header>
        <dl class="facts">
          <div><dt>Christmas week</dt><dd>{money(d['total_x'])}</dd></div>
          <div><dt>{e(d['feb_label'])}</dt><dd>{money(d['total_f'])}</dd></div>
          <div><dt>Snow on Dec 25</dt><dd>{n['odds_x']:.0f}%</dd></div>
          <div><dt>Typical depth</dt><dd>{n['depth_x']:.0f} in → {n['depth_f']:.0f} in</dd></div>
        </dl>
        <p class="alt alt--{alt}"><strong>{d['elev']:,} ft.</strong> {altword}.</p>
        <p><strong>Getting there.</strong> {e(d['travel'])}</p>
        <p><strong>What makes it special.</strong> {e(d['nature'])}</p>
        <ul class="kidlist">{kids}</ul>
        {note}
      </article>""")
    return "".join(out)


def ai_rows():
    return "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td class="tot">{e(c)}</td></tr>' for a, b, c in AI_VS_LIVE)


def also_items():
    return "".join(f"<li><strong>{e(a)}.</strong> {e(b)}</li>" for a, b in ALSO)


def source_items():
    return "".join(f'<li><a href="{e(u)}" rel="noopener">{e(t)}</a></li>' for t, u in SOURCES)


calc_data = {d["key"]: dict(name=d["name"], feb=d["feb_label"], drive=d["drive"], miles=d.get("miles", 0),
                            fx=d["fly_x"], ff=d["fly_f"], lx=d["lodge_x"], lf=d["lodge_f"], cx=d["car_x"], cf=d["car_f"]) for d in D}

fewer = [d for d in D if d["rooms"][0] < d["rooms"][2]]
PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <meta name="color-scheme" content="light dark">
  <title>Snow Trip: Christmas or February?</title>
  <meta name="description" content="Six snow destinations from Houston, priced for Christmas week and for February, with NOAA snow records.">
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
        <h1>Christmas week or February?</h1>
        <p class="lede">You are both right. February is cheaper everywhere we looked. But the expensive week is the one <em class="strongem">after</em> Christmas, and in Steamboat Springs the week <em class="strongem">before</em> it costs {money(sb['diff'])} more than February.</p>
        <ul class="tiles" role="list">
          <li class="tile"><span class="tile__num">+{money(sb['diff'])}</span><span class="tile__label">What Dec 21–26 costs over Feb 22–27 in Steamboat, for flights, hotel and car ({sb['pct']}% more)</span></li>
          <li class="tile"><span class="tile__num">{sb['n']['odds_x']:.0f}%</span><span class="tile__label">Of Christmases with snow on the ground in Steamboat, 1991–2020 (NOAA)</span></li>
          <li class="tile"><span class="tile__num">{money(sb['fly_x'])} → {money(sb['peak_fly'])}</span><span class="tile__label">The same nonstop flight to Steamboat if you leave Dec 26 instead of Dec 21</span></li>
          <li class="tile"><span class="tile__num">16 in → 26 in</span><span class="tile__label">Typical snow on the ground in Steamboat: Christmas Day against February 10 (NOAA)</span></li>
        </ul>
        <p class="caption muted">Every price is a live quote read on {CHECKED}. Prices will move; the gaps between weeks are the point.</p>
      </div>
    </section>

    <section class="section">
      <div class="container stack">
        <h2>The recommendation</h2>
        <div class="callout stack stack--tight">
          <p><strong>Steamboat Springs, Dec 21–26, home on the 26th.</strong> About {money(sb['total_x'])} for flights, hotel and car, against {money(sb['total_f'])} in late February. The {money(sb['diff'])} difference buys a white Christmas with a 99% snow record.</p>
          <p><strong>If the {money(sb['diff'])} is better spent elsewhere:</strong> the same trip on Feb 22–27 has 10 more inches of snow on the ground and warmer afternoons.</p>
          <p><strong>If being there on Christmas morning is not the point:</strong> Dec 14–19 is the cheapest snow-sure week priced. Winter Park comes to $2,943 and Jackson Hole to $3,114, both under their February totals.</p>
          <p><strong>If the trip needs to stay at low elevation:</strong> Duluth ($2,806) or Whitefish ($2,652) for Dec 16–21. Both are 3,100 ft or lower, and both cost far more in Christmas week because of flights.</p>
          <p><strong>Not recommended in any plan:</strong> any stay that runs past Dec 26, and Presidents Day week (Feb 12–17), which prices like Christmas.</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container stack">
        <h2>What each trip costs</h2>
        <p>Flights, lodging and rental car for four people and five nights. Food and activities cost the same in either week, so they are left out. Lodging is the average of the same hotels in both weeks, before tax.</p>
        <div class="legend"><span class="key key--x">Christmas week, Dec 21–26</span><span class="key key--f">February</span></div>
        <div class="bars" aria-hidden="true">{bars()}
        </div>
        <div class="tablewrap" tabindex="0" role="region" aria-label="Cost by destination, Christmas week against February">
          <table class="num">
            <thead>
              <tr><th rowspan="2" scope="col">Destination</th><th colspan="4" scope="colgroup" class="x">Christmas week · Dec 21–26</th><th colspan="4" scope="colgroup" class="f">February</th><th rowspan="2" scope="col">Christmas costs more by</th></tr>
              <tr><th scope="col">Travel</th><th scope="col">Lodging</th><th scope="col">Car</th><th scope="col">Total</th><th scope="col">Travel</th><th scope="col">Lodging</th><th scope="col">Car</th><th scope="col">Total</th></tr>
            </thead>
            <tbody>{cost_rows()}
            </tbody>
          </table>
        </div>
        <ul class="notes">
          <li><strong>Flights cost the same in both weeks.</strong> Houston to Denver on United is $361 either way. The gap is lodging and the rental car.</li>
          <li><strong>Rental cars at Denver are the surprise:</strong> $435 for Christmas week against $181 in February.</li>
          <li><strong>February won at most hotels, not all.</strong> Of the {sum(d['lodge_n'] for d in D)} hotels compared, {sum(d['lodge_cheaper'] for d in D)} were cheaper in February.</li>
          <li><strong>Steamboat in February means Feb 22–27.</strong> Feb 1–6 is Winter Carnival, when the same hotels averaged $379 a night against $375 at Christmas.</li>
          <li><strong>Red River is a drive:</strong> 837 miles each way, with gas at {GAS_MPG} mpg and ${GAS_PRICE:.2f} a gallon.</li>
        </ul>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container stack">
        <h2>The week that is really peak season</h2>
        <p>Peak pricing starts on December 26. Staying Dec 26–31 instead of Dec 21–26 changes the same trip like this:</p>
        <div class="tablewrap" tabindex="0" role="region" aria-label="Dec 21 to 26 against Dec 26 to 31">
          <table class="num">
            <thead><tr><th scope="col">Destination</th><th scope="col">Hotel per night</th><th scope="col">Flight per person</th><th scope="col">Places still bookable</th></tr></thead>
            <tbody>{peak_rows()}
            </tbody>
          </table>
        </div>
        <p class="caption muted">Hotel rates are averages of the same hotels in both weeks. Flights are United nonstop from Houston. "Places still bookable" is Booking.com's count for a family of four. Each comparison uses the hotels listed in both of its weeks, so the Dec 21–26 rate here differs a little from the cost table above.</p>
        <h3>The February week to skip</h3>
        <p>Presidents Day week, Feb 12–17, prices like Christmas: the same {PRES['steamboat_lodge'][2]} Steamboat hotels averaged ${PRES['steamboat_lodge'][1]} a night for Feb 12–17 against ${PRES['steamboat_lodge'][0]} for Dec 21–26, and the nonstop flight is ${PRES['hdn_fly']} against $389.</p>
      </div>
    </section>

    <section class="section">
      <div class="container stack">
        <h2>A third option: the week before, Dec 14–19</h2>
        <p>With no school calendar to work around, the week before Christmas week is open. The same hotels cost 16% to 54% less than Dec 21–26, and Denver rental cars drop from $435 to $174. You would be home for Christmas morning instead of waking up in the snow.</p>
        <div class="tablewrap" tabindex="0" role="region" aria-label="Dec 14 to 19 against Christmas week and February">
          <table class="num">
            <thead><tr><th scope="col">Destination</th><th scope="col">Dec 14–19 total</th><th scope="col">Against Dec 21–26</th><th scope="col">Against February</th><th scope="col">Years with snow on Dec 17</th><th scope="col">Typical depth Dec 17</th></tr></thead>
            <tbody>{dec14_rows()}
            </tbody>
          </table>
        </div>
        <ul class="notes">
          <li><strong>Every fly-to destination except Steamboat comes out cheaper than February,</strong> Jackson Hole by the most ($475). Against Christmas week, Jackson Hole saves $767.</li>
          <li><strong>Steamboat saves less than its hotels suggest.</strong> Hotels fall from $340 to $158 a night, but the nonstop flight is not on sale that week and the one-stop fare is $522 a person, against $389 nonstop on Dec 21.</li>
          <li><strong>Snow is up to 3 inches thinner than on Christmas Day</strong> and the odds of snow on the ground are 1 to 4 points lower. In a low-snow year Steamboat has 8 inches on Dec 17.</li>
          <li><strong>Not everything is open yet.</strong> Jackson's elk sleigh rides start Dec 19. Check opening dates for tubing hills before booking.</li>
        </ul>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container stack">
        <h2>Staying low: snow without the altitude</h2>
        <p>Every town above sits at 6,200 ft or higher, where each breath carries 21% to 30% less oxygen than in Houston. These three have a strong snow record at 3,100 ft or lower. Same method: four people, five nights, flights, the same hotels in each week, and a rental car.</p>
        <div class="tablewrap" tabindex="0" role="region" aria-label="Low-elevation destinations by week">
          <table class="num">
            <thead><tr><th scope="col">Destination</th><th scope="col">Dec 16–21</th><th scope="col" class="x">Christmas week · Dec 21–26</th><th scope="col" class="f">Feb 1–6</th></tr></thead>
            <tbody>
        <tr>
          <th scope="row">Duluth, Minnesota<span class="sub">1,428 ft · 5% less oxygen than Houston</span></th>
          <td class="tot">$2,806<span class="sub">$378 fare · $205 a night</span><span class="sub">snow 87% · 7 in</span></td><td class="tot">$3,404<span class="sub">$586 fare · $160 a night</span><span class="sub">snow 92% · 8 in</span></td><td class="tot">$2,626<span class="sub">$378 fare · $169 a night</span><span class="sub">snow 99% · 14 in</span></td>
        </tr>
        <tr>
          <th scope="row">Whitefish, Montana<span class="sub">3,100 ft · 11% less oxygen than Houston</span></th>
          <td class="tot">$2,652<span class="sub">$419 fare · $160 a night</span><span class="sub">snow 84% · 5 in</span></td><td class="tot">$4,108<span class="sub">$757 fare · $179 a night</span><span class="sub">snow 92% · 7 in</span></td><td class="tot">$2,777<span class="sub">$419 fare · $185 a night</span><span class="sub">snow 98% · 13 in</span></td>
        </tr>
        <tr>
          <th scope="row">Quebec City, Quebec<span class="sub">320 ft · 1% less oxygen than Houston</span></th>
          <td class="tot">$4,382<span class="sub">$877 fare · $146 a night</span><span class="sub">snow not checked</span></td><td class="tot">$5,587<span class="sub">$1,151 fare · $154 a night</span><span class="sub">snow 91% · 10 in</span></td><td class="tot">$4,261<span class="sub">$813 fare · $169 a night</span><span class="sub">snow about 22 in</span></td>
        </tr>
            </tbody>
          </table>
        </div>
        <p class="caption muted">Snow is NOAA's share of years with snow on the ground and the typical depth on Dec 17, Dec 25 and Feb 10. Quebec City is not in NOAA's data; its figures come from the GLM lane's station records and were not rechecked. Its February hotel rate rests on only 2 matched hotels.</p>
        <ul class="notes">
          <li><strong>Here Christmas week costs far more, and the reason is flights.</strong> Fares to these small airports jump for Dec 21–26: Duluth $378 to $586, Whitefish $419 to $757. Whitefish costs $1,456 more in Christmas week than the week before.</li>
          <li><strong>The week before Christmas is the value week.</strong> Duluth is $2,806 and Whitefish $2,652 for Dec 16–21, both under any Colorado total on this page except Estes Park.</li>
          <li><strong>Snow is less certain in mid-December than in the mountains:</strong> 84% to 87% of years on Dec 17, with 5 to 7 inches typical. By February it is 98% or better.</li>
          <li><strong>Quebec City is the lowest and the most expensive:</strong> flights run $813 to $1,151 a person, and passports are needed.</li>
        </ul>
        <div class="places">
          <article class="place">
            <header class="place__head"><p class="eyebrow">Minnesota · 1,428 ft</p><h3>Duluth</h3><p>The most Christmas for the least effort: a lakefront city with a free lights festival and a tubing hill with no height rule.</p></header>
            <ul class="kidlist">
              <li><strong>Bentleyville Tour of Lights.</strong> A walk-through lights display on the Lake Superior waterfront, Nov 21 to Dec 26. Free; parking $12. Santa is there nightly through Dec 23.</li>
              <li><strong>Snow tubing at Spirit Mountain.</strong> Listed at $25 for two hours, ages 3 and up, no height minimum found. The ski area's projected opening is Dec 4.</li>
              <li><strong>Christmas City Express train.</strong> Select dates through Dec 20.</li>
            </ul>
            <p><strong>Getting there.</strong> One stop, about 5 hours.</p>
            <p class="caption muted">Cold: average high 22° to 24°, low 4° to 9°. Hotels cost more on Dec 16–21 than in Christmas week because that stay includes a festival weekend.</p>
          </article>
          <article class="place">
            <header class="place__head"><p class="eyebrow">Montana · 3,100 ft</p><h3>Whitefish</h3><p>The mountain-and-animals choice at half the elevation of the Colorado towns, on the edge of Glacier National Park.</p></header>
            <ul class="kidlist">
              <li><strong>Horse-drawn sleigh rides at Bar W Guest Ranch.</strong> Listed at $55 a person for 45 minutes, under 4 free (older price).</li>
              <li><strong>Dog sledding in Olney.</strong> All ages; a family fits in one sled. Season December to March. No current price found.</li>
              <li><strong>Glacier National Park.</strong> Ranger-led snowshoe walks and Lake McDonald in the snow.</li>
              <li><strong>In town.</strong> Indoor ice rink and sledding. No tubing hill found.</li>
            </ul>
            <p><strong>Getting there.</strong> One stop to Kalispell, 6 to 9 hours, then a short drive.</p>
            <p class="caption muted">Milder than Duluth: average high 28°, low 16° to 17° in December.</p>
          </article>
          <article class="place">
            <header class="place__head"><p class="eyebrow">Quebec · 320 ft</p><h3>Quebec City</h3><p>Nearly sea level, with an old walled city dressed for Christmas. The priciest trip here.</p></header>
            <ul class="kidlist">
              <li><strong>Village Vacances Valcartier.</strong> A winter playground with more than 35 lift-served snow slides. Opens Dec 18, 2026. Height rules for small children not confirmed.</li>
              <li><strong>Toboggan slide on Dufferin Terrace.</strong> Beside the Château Frontenac; about $10 for 3 rides (older price).</li>
              <li><strong>German Christmas Market.</strong> Nov 19 to Dec 23, Thursday to Sunday.</li>
            </ul>
            <p><strong>Getting there.</strong> One stop, about 7 hours. Passports required.</p>
          </article>
        </div>
        <h3>Tubing hills and height</h3>
        <p>Rules found for a child between 36 and 42 inches tall:</p>
        <ul class="notes">
          <li><strong>Can ride:</strong> Winter Park's Coca-Cola Tube Hill (36 inches and up), Spirit Mountain in Duluth (ages 3 and up), Saddleback Ranch in Steamboat (age 4 and under shares a parent's tube).</li>
          <li><strong>Cannot ride under 42 inches:</strong> Snow King in Jackson, Red River, Mount Norquay in Banff.</li>
          <li><strong>No height rule:</strong> the elk sleigh ride in Jackson, and the sleigh and dog sled rides near Whitefish.</li>
          <li><strong>Opening dates:</strong> none of the mountain tubing hills has published one for this season. Saddleback Ranch says a bookable slot online means it is open. Snow King opens when there is enough snow and its page shows Dec 20 last season. Frisco, near Breckenridge, projects Nov 26.</li>
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="container stack">
        <h2>Will there be snow?</h2>
        <p>These are 30-year records from NOAA weather stations in each town, not forecasts. "Low-snow year" is the depth that 1 winter in 4 falls below.</p>
        <div class="tablewrap" tabindex="0" role="region" aria-label="Snow and temperature records, December 25 against February 10">
          <table class="num">
            <thead>
              <tr><th rowspan="2" scope="col">Town</th><th colspan="2" scope="colgroup">Years with snow on the ground</th><th colspan="2" scope="colgroup">Typical depth</th><th colspan="2" scope="colgroup">Low-snow year</th><th colspan="2" scope="colgroup">Average high / low °F</th></tr>
              <tr><th scope="col" class="x">Dec 25</th><th scope="col" class="f">Feb 10</th><th scope="col" class="x">Dec 25</th><th scope="col" class="f">Feb 10</th><th scope="col" class="x">Dec 25</th><th scope="col" class="f">Feb 10</th><th scope="col" class="x">Dec 25</th><th scope="col" class="f">Feb 10</th></tr>
            </thead>
            <tbody>{snow_rows()}
            </tbody>
          </table>
        </div>
        <ul class="notes">
          <li><strong>In the four snow-sure towns, February has about 60% more snow on the ground</strong> and afternoons 2 to 4 degrees warmer.</li>
          <li><strong>Christmas snow is still close to certain</strong> in Steamboat, Winter Park, Breckenridge and Grand Teton: 98% or better, and at least 11 inches even in a low-snow year.</li>
          <li><strong>Estes Park and Red River are the gamble:</strong> bare ground on 1 Christmas in 4 and 1 in 3.</li>
        </ul>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container stack">
        <h2>What the dollars do not show</h2>
        <div class="tablewrap" tabindex="0" role="region" aria-label="Non-cost comparison">
          <table class="plain">
            <thead><tr><th scope="col"></th><th scope="col" class="x">Christmas week · Dec 21–26</th><th scope="col" class="f">February week</th></tr></thead>
            <tbody>
              <tr><th scope="row">Waking up to snow on Christmas morning</th><td>Yes. This is the only week that delivers it.</td><td>No.</td></tr>
              <tr><th scope="row">Closed on Dec 25</th><td>Steamboat's hot springs pools and Jackson's elk sleigh rides. Do them on another day.</td><td>Nothing.</td></tr>
              <tr><th scope="row">Choice of places to stay</th><td>Booking is 5 weeks out. Fewer places left than February in {len(fewer)} of 6 towns.</td><td>11 to 14 weeks out. More choice everywhere except Steamboat.</td></tr>
              <tr><th scope="row">Snow to play in</th><td>16 inches typical in Steamboat.</td><td>26 inches typical in Steamboat.</td></tr>
              <tr><th scope="row">Cold</th><td>High 28°, low 4° in Steamboat.</td><td>High 33°, low 7°.</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container stack">
        <h2>Run your own numbers</h2>
        <p>Change the family size, the nights or any rate. The starting values are the quotes above.</p>
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
              <thead><tr><th scope="col">Line</th><th scope="col" class="x">Christmas week</th><th scope="col" class="f" id="c-feblabel">February</th><th scope="col">Difference</th></tr></thead>
              <tbody id="c-body"></tbody>
            </table>
          </div>
          <div class="calc__rates">
            <p class="caption muted">Rates used, editable:</p>
            <label>Fare per person, Christmas<input id="c-fx" type="number" min="0" step="1"></label>
            <label>Fare per person, February<input id="c-ff" type="number" min="0" step="1"></label>
            <label>Hotel per night, Christmas<input id="c-lx" type="number" min="0" step="1"></label>
            <label>Hotel per night, February<input id="c-lf" type="number" min="0" step="1"></label>
            <label>Car for 5 days, Christmas<input id="c-cx" type="number" min="0" step="1"></label>
            <label>Car for 5 days, February<input id="c-cf" type="number" min="0" step="1"></label>
          </div>
        </form>
        <noscript><p class="callout">The calculator needs JavaScript. Every number it starts from is in the cost table above.</p></noscript>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container stack">
        <h2>The six places, ranked for kids aged 4 to 7</h2>
        <p>Ranked on snow certainty, altitude, travel time with small children, and what they will remember.</p>
        <div class="places">{cards()}
        </div>
        <h3>Also suggested, not priced</h3>
        <ul class="notes">{also_items()}</ul>
      </div>
    </section>

    <section class="section">
      <div class="container stack">
        <h2>How these numbers were checked</h2>
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
          <!--LANES-->
          <li><strong>Three activity prices were spot-checked</strong> against the operators' own pages (elk sleigh ride, Saddleback tubing, Old Town Hot Springs). All three matched.</li>
        </ul>
        <h3>Limits</h3>
        <ul class="notes">
          <li>Hotel comparisons use 6 to 11 hotels per town: the ones Booking.com listed first in both weeks with a Christmas rate under $700 a night. Small samples; treat a gap under $200 as a tie.</li>
          <li>Rates are before lodging tax and resort fees. Flights exclude bags.</li>
          <li>Activity prices other than the three spot-checked ones come from the pages the GPT-6 Astra lane cited.</li>
          <li>Rental cars were priced for Dec 14–19, Christmas week and February, not for Dec 26–31 outside Denver.</li>
          <li>The oxygen figures are standard-atmosphere pressure at each town's elevation compared with sea level.</li>
          <li>Snow records describe 1991–2020. Colorado's early season was thin in December 2025.</li>
          <li>The altitude guidance is the CDC's general advice for travelers, not medical advice for your children.</li>
        </ul>
        <h3>Sources</h3>
        <ul class="notes sources">{source_items()}</ul>
        <p class="caption muted">Raw price observations, NOAA station data and the AI output are in the <a href="https://github.com/brandoncordoba/snow-trip/tree/main/research">research folder</a>.</p>
      </div>
    </section>
  </main>
  <footer class="site-footer"><div class="container"><p class="caption muted">Prepared {CHECKED}. Prices are quotes on that date, not offers.</p></div></footer>
  <script id="calc-data" type="application/json">{json.dumps(dict(dest=calc_data, mpg=GAS_MPG, gas=GAS_PRICE))}</script>
  <script src="app.js" defer></script>
</body>
</html>
"""

lanes_file = ROOT / "research/lanes.html"
PAGE = PAGE.replace("<!--LANES-->", lanes_file.read_text() if lanes_file.exists() else "")
(ROOT / "index.html").write_text(PAGE)
print("wrote index.html", len(PAGE), "bytes")
for d in D:
    print(f"{d['name']:18} xmas {d['total_x']:>6,}  feb {d['total_f']:>6,}  diff {d['diff']:>5,} ({d['pct']}%)  snow {d['n']['odds_x']:.0f}%/{d['n']['odds_f']:.0f}%  depth {d['n']['depth_x']}/{d['n']['depth_f']}")
