# draw_frontpage.py — composes the 25 November 2026 front page with PIL.
# Own code, written for news-image-20261125. Run: python3 draw_frontpage.py
# Output: entry.png, 1024x1024, a dense newspaper front page.
# All headlines below were verified against wire/search reports of 25 Nov 2026.
# Lead is fresh 25 Nov news (Hormuz tankers), NOT the 24 Nov COP31 lead.
# Layout follows the 24 Nov entry: top bar, huge masthead, lead, two
# featured stories, three columns of region sections with black headers,
# and a footer ticker. An assert catches any overflow.

from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (255, 255, 255)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (74, 74, 74)
RULE = (150, 145, 132)

# Bundled fonts (in this repo's fonts/); fall back to the system copies.
def _font(name):
    local = os.path.join(HERE, "fonts", name)
    if os.path.exists(local):
        return local
    return os.path.join("/usr/share/fonts/truetype/dejavu", name)

SERIF_B = _font("DejaVuSerif-Bold.ttf")
SERIF = _font("DejaVuSerif.ttf")
SANS = _font("DejaVuSans.ttf")
SANS_B = _font("DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_one_line(draw, text, fnt, max_w):
    """Truncate text with an ellipsis so it fits max_w on one line."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    short = text
    while short and draw.textlength(short + "\u2026", font=fnt) > max_w:
        short = short[:-1]
    return short + "\u2026"


def draw_center(draw, text, fnt, y, fill=INK):
    draw.text((W // 2, y), text, font=fnt, fill=fill, anchor="ma")


def rule(draw, y, x0, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
LEAD = {
    "kicker": "IRAN WAR  •  STRAIT OF HORMUZ",
    "headline": "TWO TANKERS ABLAZE AFTER MINES HIT HORMUZ",
    "deck": ("Two oil tankers explode and catch fire in the Strait of Hormuz after "
             "striking naval mines, the IRGC says — as Houthis hit a Saudi refinery "
             "and Brent crude jumps to $91.46 a barrel."),
}

FEATURED = [
    {
        "kicker": "IRAN WAR  •  YEMEN",
        "headline": "Houthis hit Saudi refinery as Riyadh counts its wounded",
        "deck": ("Rebels say they struck the Ras Tanura refinery; a day earlier a "
                 "drone hit a Riyadh tower, injuring 11."),
    },
    {
        "kicker": "WAR IN UKRAINE",
        "headline": "Ukraine's drones sink Russian warship off Libya",
        "deck": ("Sea drones hit a Russian corvette at Benghazi; two Libyan officers "
                 "die, and the LNA vows retaliation."),
    },
]

# (section, [(headline, deck), ...]) — three columns, sections in order.
COLUMNS = [
    [
        ("AMERICAS", [
            ("Trump unveils tariffs of up to 20% on China and EU",
             "New duties follow a Section 301 probe into subsidies."),
            ("US GDP grows 4.3% in Q3",
             "Economy beats forecasts as inflation stays high at 3.8%."),
            ("CIA and spy chief's systems breached",
             "Unclassified networks hit in a cyberattack, sources say."),
            ("Democrats clinch 259 House seats",
             "Largest House majority since 1990, AP calls it."),
            ("Thanksgiving storm threatens 250m Americans",
             "Macy's parade balloons at risk in its 100th year."),
        ]),
        ("AFRICA", [
            ("Sudan drones kill 19 civilians",
             "RSF strikes hit two cities, rights lawyers say."),
            ("Senegal regains Africa Cup title",
             "Sports court restores 2025 crown to Senegal."),
            ("Funding cuts threaten AIDS fight",
             "UN warns decades of progress are at risk."),
        ]),
    ],
    [
        ("EUROPE", [
            ("Ukraine drones set two Russian refineries ablaze",
             "Syzran and Kuibyshev hit; one killed, 145 downed."),
            ("Zelensky: Ukraine needs €115bn aid for 2027",
             "Kyiv seeks funds as US pauses Patriot supplies."),
            ("Poland seeks permanent US base",
             "After two Russian airspace incursions in four days."),
            ("Russian strikes kill two in Odesa",
             "Kyiv apartment block hit; child among the injured."),
            ("490,334 Russian soldiers dead, leaked data show",
             "BBC analysis of leaked government statistics."),
        ]),
        ("TECH & SCIENCE", [
            ("Huawei convicted on 10 of 12 counts",
             "Brooklyn jury finds bank fraud and trade-secret theft."),
            ("Asian stocks plunge as AI rout deepens",
             "KOSPI -6.2%, Nikkei -2.8%; Nvidia falls 5%."),
            ("Dell posts record $54.9bn quarter",
             "AI server revenue up 291% to $22.0bn."),
            ("Amazon says AI agents hacked a server",
             "Attackers used AI agents to exploit a new flaw."),
            ("Roche breast cancer drug wins FDA nod",
             "Wilserdly is the first new hormone therapy in 20 years."),
        ]),
    ],
    [
        ("MIDDLE EAST", [
            ("Israel kills Hamas security chief in Gaza",
             "Abuelouf, his wife and two children killed, medics say."),
            ("Pope decries COP31 failure",
             "Leo XIV: extreme events grow 'increasingly frequent'."),
            ("Brent crude jumps to $91.46 a barrel",
             "Oil up ~$29 on the year as Hormuz fears mount."),
            ("World court rules Myanmar committed genocide",
             "Rohingya ruling faces a geopolitical test."),
        ]),
        ("ASIA-PACIFIC", [
            ("Solomons sign pact barring foreign bases",
             "Australia treaty shores up Pacific security."),
            ("Shenzhou-24 docks with Tiangong",
             "Pakistan's first astronaut reaches orbit with China."),
            ("Australia inflation hits 4.9%",
             "Fuel prices drive the rise; RBA expected to hold."),
            ("Abrego Garcia reaches Spain",
             "Deported Salvadoran ends 20-month legal fight."),
        ]),
        ("SPORT & CULTURE", [
            ("Ezra Frech wins Dancing With the Stars",
             "Mirrorball after a freestyle on a prosthetic leg."),
            ("Packers visit Rams in first Thanksgiving Eve game",
             "NFL's holiday stretch opens on Netflix."),
            ("Blade Runner 2099 premieres today",
             "Michelle Yeoh leads Prime Video's new series."),
            ("2Chainz hurt in head-on crash",
             "Rapper injured in a collision, reports say."),
        ]),
    ],
]

TICKER = ("BRENT $91.46 AS HORMUZ BURNS  •  DOW CLOSES ABOVE 50,000 FOR THE FIRST TIME  •  "
          "SHENZHOU-24 DOCKS WITH TIANGONG  •  HUAWEI CONVICTED IN NEW YORK  •  "
          "MACY'S PARADE BALLOONS AT RISK IN 100TH YEAR")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 24                      # side margin
    x1 = W - mx
    # outer border
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)

    y = 16
    # ---- top bar -------------------------------------------------------
    d.text((mx, y), "WEDNESDAY 25 NOVEMBER 2026", font=font(SANS_B, 15), fill=INK)
    rt = "ONE DAY  •  THE WORLD IN FULL"
    d.text((x1, y), rt, font=font(SANS_B, 15), fill=INK, anchor="ra")
    y += 22
    rule(d, y, mx, x1, 2)
    y += 6

    # ---- masthead ------------------------------------------------------
    # Fit the masthead to the page width (shrink until it fits).
    _msize = 96
    while _msize > 40 and d.textlength("THE WORLD TODAY", font=font(SERIF_B, _msize)) > x1 - mx:
        _msize -= 2
    draw_center(d, "THE WORLD TODAY", font(SERIF_B, _msize), y)
    y += _msize - 2
    draw_center(d, "The world's news of Wednesday 25 November 2026 — in one page",
                font(SERIF, 19), y, fill=GREY)
    y += 26
    rule(d, y, mx, x1, 3)
    y += 10

    # ---- lead story ----------------------------------------------------
    d.text((mx, y), LEAD["kicker"], font=font(SANS_B, 15), fill=RED)
    y += 21
    for line in wrap(d, LEAD["headline"], font(SANS_B, 38), x1 - mx):
        d.text((mx, y), line, font=font(SANS_B, 38), fill=INK)
        y += 42
    y += 2
    for line in wrap(d, LEAD["deck"], font(SERIF, 17), x1 - mx - 10):
        d.text((mx, y), line, font=font(SERIF, 17), fill=GREY)
        y += 21
    y += 6
    rule(d, y, mx, x1, 2)
    y += 8

    # ---- featured row: two stories side by side ------------------------
    col_w = (x1 - mx - 24) // 2
    row_top = y
    max_y = row_top
    for i, s in enumerate(FEATURED):
        cx = mx + i * (col_w + 24)
        cy = row_top
        d.text((cx, cy), s["kicker"], font=font(SANS_B, 12), fill=RED)
        cy += 18
        for line in wrap(d, s["headline"], font(SANS_B, 20), col_w)[:2]:
            d.text((cx, cy), line, font=font(SANS_B, 20), fill=INK)
            cy += 24
        cy += 2
        for line in wrap(d, s["deck"], font(SERIF, 14), col_w)[:2]:
            d.text((cx, cy), line, font=font(SERIF, 14), fill=GREY)
            cy += 17
        max_y = max(max_y, cy)
    d.line([(mx + col_w + 12, row_top), (mx + col_w + 12, max_y)],
           fill=RULE, width=1)
    y = max_y + 4
    rule(d, y, mx, x1, 2)
    y += 8

    # ---- region columns -------------------------------------------------
    cols = 3
    gutter = 18
    gw = (x1 - mx - (cols - 1) * gutter) // cols
    grid_top = y
    max_y = grid_top
    for ci, sections in enumerate(COLUMNS):
        gx = mx + ci * (gw + gutter)
        cy = grid_top
        for sec_name, stories in sections:
            # black section header bar
            d.rectangle([gx, cy, gx + gw, cy + 22], fill=INK)
            d.text((gx + 6, cy + 3), sec_name, font=font(SANS_B, 14), fill=PAPER)
            cy += 22 + 4
            for head, deck in stories:
                for line in wrap(d, head, font(SANS_B, 14), gw)[:2]:
                    d.text((gx, cy), line, font=font(SANS_B, 14), fill=INK)
                    cy += 16
                d.text((gx, cy), fit_one_line(d, deck, font(SERIF, 11), gw),
                       font=font(SERIF, 11), fill=GREY)
                cy += 13
            cy += 3
        max_y = max(max_y, cy)
    y = max_y
    rule(d, y, mx, x1, 2)
    y += 8

    # ---- footer ticker ---------------------------------------------------
    for line in wrap(d, TICKER, font(SANS_B, 13), x1 - mx):
        d.text((mx, y), line, font=font(SANS_B, 13), fill=INK)
        y += 17
    y += 4
    assert y <= H - 12, f"layout overflow: content ends at {y}, canvas is {H}"
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    import os as _os
    n_lead = 1
    n_feat = len(FEATURED)
    n_grid = sum(len(st) for col in COLUMNS for _, st in col)
    print(f"saved {out} {img.size}, {_os.path.getsize(out)} bytes, content ends at y={y}")
    print(f"stories: {n_lead} lead + {n_feat} featured + {n_grid} grid = "
          f"{n_lead + n_feat + n_grid} (+ ticker)")


if __name__ == "__main__":
    main()
