import json
import os

# ── Config ──────────────────────────────────────────────────────────────────
SRC_REZEPTE = "rezeptverzeichnis.json"
SRC_TEXTE   = "texte.json"
OUT_DIR     = "dist"
INDEX_OUT   = os.path.join(OUT_DIR, "index.html")
READER_DIR  = os.path.join(OUT_DIR, "rezept")

# ── Load data ────────────────────────────────────────────────────────────────
with open(SRC_REZEPTE, encoding="utf-8") as f:
    rezepte = json.load(f)

with open(SRC_TEXTE, encoding="utf-8") as f:
    t = json.load(f)

# Shortcuts für häufig genutzte Abschnitte
ti = t["index"]
tk = t["karten"]
tr = t["reader"]
ts = t["seite"]

# ── Shared styles (CSS variables + base) ────────────────────────────────────
SHARED_CSS = """
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --eggshell:   #f5f0e8;
    --eggshell-2: #ede7d9;
    --orange-1:   #f4956a;
    --orange-2:   #e8743f;
    --orange-pale:#fde8d8;
    --brown:      #6b4226;
    --text:       #3a2e27;
    --text-muted: #8a7060;
    --card-bg:    #faf7f2;
    --shadow:     0 2px 16px rgba(100,60,20,0.08);
  }

  html { font-size: 16px; }

  body {
    background: var(--eggshell);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    min-height: 100vh;
  }

  a { color: inherit; text-decoration: none; }
"""

# ── Index page ───────────────────────────────────────────────────────────────
def build_card(key, rezept):
    name  = rezept["name"]
    desc  = rezept.get("beschreibung", "")
    zeit  = rezept.get("zeit", "")
    port  = rezept.get("portionen", "")
    steps = len(rezept.get("schritte", []))
    url   = f"rezept/{key}/index.html"
    return f"""
    <a class="card" href="{url}">
      <div class="card-index">{key.replace("_", " ")}</div>
      <h2 class="card-name">{name}</h2>
      <p class="card-desc">{desc}</p>
      <div class="card-meta">
        <span>{tk["emoji_zeit"]} {zeit}</span>
        <span>{tk["emoji_portionen"]} {port} {tk["einheit_portionen"]}</span>
        <span>{tk["emoji_schritte"]} {steps} {tk["einheit_schritte"]}</span>
      </div>
      <div class="card-arrow">{tk["pfeil"]}</div>
    </a>"""

def build_index(rezepte):
    cards = "\n".join(build_card(k, v) for k, v in rezepte.items())
    count = len(rezepte)
    return f"""<!DOCTYPE html>
<html lang="{ts["sprache"]}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{ts["titel"]}</title>
  <style>
{SHARED_CSS}

    /* ── Header ── */
    header {{
      background: linear-gradient(135deg, var(--orange-1) 0%, var(--orange-2) 100%);
      padding: 3.5rem 2rem 2.5rem;
      text-align: center;
      position: relative;
      overflow: hidden;
    }}
    header::before {{
      content: '';
      position: absolute;
      inset: 0;
      background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='30' cy='30' r='1.5' fill='rgba(255,255,255,0.15)'/%3E%3C/svg%3E") repeat;
    }}
    header h1 {{
      font-family: 'Playfair Display', serif;
      font-size: clamp(2rem, 5vw, 3.2rem);
      color: #fff;
      letter-spacing: -0.02em;
      position: relative;
    }}
    header p {{
      color: rgba(255,255,255,0.85);
      margin-top: 0.5rem;
      font-size: 0.95rem;
      position: relative;
    }}
    .badge {{
      display: inline-block;
      background: rgba(255,255,255,0.2);
      color: #fff;
      border-radius: 999px;
      padding: 0.15rem 0.75rem;
      font-size: 0.8rem;
      margin-top: 0.75rem;
      position: relative;
    }}

    /* ── Grid ── */
    main {{
      max-width: 960px;
      margin: 0 auto;
      padding: 3rem 1.5rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1.5rem;
    }}

    /* ── Card ── */
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--eggshell-2);
      border-radius: 16px;
      padding: 1.75rem;
      display: block;
      transition: transform 0.2s, box-shadow 0.2s;
      box-shadow: var(--shadow);
      position: relative;
      overflow: hidden;
    }}
    .card::after {{
      content: '';
      position: absolute;
      top: 0; right: 0;
      width: 80px; height: 80px;
      background: radial-gradient(circle at top right, var(--orange-pale), transparent 70%);
    }}
    .card:hover {{
      transform: translateY(-4px);
      box-shadow: 0 8px 28px rgba(100,60,20,0.13);
    }}
    .card-index {{
      font-size: 0.72rem;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--orange-2);
      margin-bottom: 0.5rem;
    }}
    .card-name {{
      font-family: 'Playfair Display', serif;
      font-size: 1.45rem;
      line-height: 1.2;
      color: var(--text);
      margin-bottom: 0.75rem;
    }}
    .card-desc {{
      font-size: 0.88rem;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 1.25rem;
    }}
    .card-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      font-size: 0.78rem;
      color: var(--text-muted);
    }}
    .card-meta span {{
      background: var(--eggshell-2);
      padding: 0.2rem 0.6rem;
      border-radius: 999px;
    }}
    .card-arrow {{
      position: absolute;
      bottom: 1.5rem;
      right: 1.5rem;
      color: var(--orange-1);
      font-size: 1.1rem;
      transition: transform 0.2s;
    }}
    .card:hover .card-arrow {{ transform: translateX(4px); }}

    footer {{
      text-align: center;
      padding: 2rem;
      font-size: 0.78rem;
      color: var(--text-muted);
    }}
  </style>
</head>
<body>
  <header>
    <h1>{ti["header_titel"]}</h1>
    <p>{ti["header_untertitel"]}</p>
    <span class="badge">{count} {ti["badge_einheit"]}</span>
  </header>
  <main>
    <div class="grid">
      {cards}
    </div>
  </main>
  <footer>{ti["footer"]}</footer>
</body>
</html>"""

# ── Reader page ──────────────────────────────────────────────────────────────
def build_reader(key, rezept):
    name    = rezept["name"]
    desc    = rezept.get("beschreibung", "")
    zeit    = rezept.get("zeit", "")
    port    = rezept.get("portionen", "")
    steps   = rezept.get("schritte", [])
    zutaten = rezept.get("zutaten", [])

    steps_html = "\n".join(
        f'<li><span class="step-num">{i+1:02d}</span><p>{s}</p></li>'
        for i, s in enumerate(steps)
    )
    zutaten_html = "\n".join(
        f'<li>{z}</li>' for z in zutaten
    )

    return f"""<!DOCTYPE html>
<html lang="{ts["sprache"]}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} – {ts["titel"]}</title>
  <style>
{SHARED_CSS}

    /* ── Top bar ── */
    .topbar {{
      background: var(--card-bg);
      border-bottom: 1px solid var(--eggshell-2);
      padding: 0.9rem 2rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
      position: sticky;
      top: 0;
      z-index: 10;
    }}
    .back-btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      color: var(--orange-2);
      font-size: 0.88rem;
      font-weight: 500;
      transition: gap 0.15s;
    }}
    .back-btn:hover {{ gap: 0.6rem; }}
    .topbar-sep {{ color: var(--eggshell-2); }}
    .topbar-title {{
      font-family: 'Playfair Display', serif;
      font-size: 0.95rem;
      color: var(--text-muted);
    }}

    /* ── Hero ── */
    .hero {{
      background: linear-gradient(135deg, var(--orange-pale) 0%, var(--eggshell) 60%);
      padding: 3rem 2rem 2rem;
      border-bottom: 1px solid var(--eggshell-2);
    }}
    .hero-index {{
      font-size: 0.72rem;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--orange-2);
      margin-bottom: 0.5rem;
    }}
    .hero h1 {{
      font-family: 'Playfair Display', serif;
      font-size: clamp(2rem, 4vw, 3rem);
      line-height: 1.1;
      color: var(--text);
      max-width: 600px;
    }}
    .hero-desc {{
      margin-top: 0.75rem;
      color: var(--text-muted);
      font-size: 0.95rem;
      max-width: 540px;
      line-height: 1.7;
    }}
    .hero-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-top: 1.25rem;
    }}
    .pill {{
      background: rgba(232,116,63,0.12);
      color: var(--orange-2);
      border-radius: 999px;
      padding: 0.25rem 0.85rem;
      font-size: 0.8rem;
      font-weight: 500;
    }}

    /* ── Layout ── */
    .layout {{
      max-width: 1000px;
      margin: 0 auto;
      padding: 2.5rem 1.5rem;
      display: grid;
      grid-template-columns: 1fr 280px;
      gap: 2.5rem;
      align-items: start;
    }}
    @media (max-width: 700px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .sidebar {{ order: -1; }}
    }}

    /* ── Steps ── */
    section h2 {{
      font-family: 'Playfair Display', serif;
      font-size: 1.4rem;
      margin-bottom: 1.5rem;
      padding-bottom: 0.5rem;
      border-bottom: 2px solid var(--orange-pale);
      color: var(--text);
    }}
    .steps-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }}
    .steps-list li {{
      display: flex;
      gap: 1rem;
      align-items: flex-start;
      background: var(--card-bg);
      border: 1px solid var(--eggshell-2);
      border-radius: 12px;
      padding: 1rem 1.25rem;
      transition: border-color 0.2s;
    }}
    .steps-list li:hover {{ border-color: var(--orange-1); }}
    .step-num {{
      font-family: 'Playfair Display', serif;
      font-size: 1.5rem;
      color: var(--orange-1);
      line-height: 1;
      min-width: 2rem;
      font-style: italic;
    }}
    .steps-list p {{
      font-size: 0.93rem;
      line-height: 1.65;
      color: var(--text);
      padding-top: 0.15rem;
    }}

    /* ── Sidebar ── */
    .sidebar {{
      background: var(--card-bg);
      border: 1px solid var(--eggshell-2);
      border-radius: 16px;
      padding: 1.5rem;
      position: sticky;
      top: 70px;
    }}
    .sidebar h3 {{
      font-family: 'Playfair Display', serif;
      font-size: 1.1rem;
      margin-bottom: 1rem;
      color: var(--text);
    }}
    .zutaten-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }}
    .zutaten-list li {{
      font-size: 0.875rem;
      color: var(--text-muted);
      padding: 0.35rem 0;
      border-bottom: 1px solid var(--eggshell-2);
      display: flex;
      align-items: center;
      gap: 0.5rem;
      line-height: 1.4;
    }}
    .zutaten-list li::before {{
      content: '·';
      color: var(--orange-1);
      font-size: 1.2rem;
      line-height: 0;
      flex-shrink: 0;
    }}
    .zutaten-list li:last-child {{ border-bottom: none; }}
  </style>
</head>
<body>
  <nav class="topbar">
    <a class="back-btn" href="{tr["zurueck_link"]}">{tr["zurueck_text"]}</a>
    <span class="topbar-sep">|</span>
    <span class="topbar-title">{name}</span>
  </nav>

  <div class="hero">
    <div class="hero-index">{key.replace("_", " ")}</div>
    <h1>{name}</h1>
    <p class="hero-desc">{desc}</p>
    <div class="hero-pills">
      <span class="pill">{tk["emoji_zeit"]} {zeit}</span>
      <span class="pill">{tk["emoji_portionen"]} {port} {tk["einheit_portionen"]}</span>
      <span class="pill">{tk["emoji_schritte"]} {len(steps)} {tk["einheit_schritte"]}</span>
    </div>
  </div>

  <div class="layout">
    <section>
      <h2>{tr["abschnitt_zubereitung"]}</h2>
      <ol class="steps-list">
        {steps_html}
      </ol>
    </section>
    <aside class="sidebar">
      <h3>{tr["abschnitt_zutaten"]}</h3>
      <ul class="zutaten-list">
        {zutaten_html}
      </ul>
    </aside>
  </div>
</body>
</html>"""

# ── Write files ──────────────────────────────────────────────────────────────
os.makedirs(OUT_DIR, exist_ok=True)

with open(INDEX_OUT, "w", encoding="utf-8") as f:
    f.write(build_index(rezepte))
print(f"✓ {INDEX_OUT}")

for key, rezept in rezepte.items():
    out_dir = os.path.join(READER_DIR, key)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(build_reader(key, rezept))
    print(f"✓ {out_path}")

print("\n✅ Build fertig! Alle Dateien in /dist")
