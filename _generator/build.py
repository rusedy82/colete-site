# Generează site-ul de colete (prima variantă). Datele provizorii sunt în CONFIG.
import os, sys, shutil, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comanda import comanda_section

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    "nume": "Colete Europa",
    "tagline": "Transport colete",
    "tel_afisat": "0759 324 006",
    "tel_link": "+40759324006",
    "email": "corusglobalwork@gmail.com",
    "pret_txt": "30 € pentru orice colet de până la 20 kg, iar peste 20 kg plătești 1,70 € pe kilogram",
    "domeniu": "https://coleteeuropa.com",
}
C = CONFIG

# ---------- iconițe ----------
def icon(name, size=26, color="currentColor"):
    p = {
        "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
        "box": '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
        "truck": '<path d="M1 4h14v12H1zM15 9h4l4 4v3h-8z"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="18" r="2"/>',
        "pin": '<path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
        "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "euro": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5A4 4 0 0 0 9 11v2a4 4 0 0 0 6.5 2.5M7 11h6M7 13h6"/>',
        "home": '<path d="M3 11 12 4l9 7v9H3z"/><path d="M9 20v-6h6v6"/>',
        "scale": '<path d="M12 3v18M5 7h14M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
        "return": '<path d="M9 14 4 9l5-5"/><path d="M4 9h11a5 5 0 0 1 0 10h-3"/>',
        "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>',
        "msg": '<path d="M21 12a8 8 0 0 1-11.8 7L3 21l2-6A8 8 0 1 1 21 12z"/>',
        "arrow": '<path d="M4 12h16M14 6l6 6-6 6"/>',
        "menu": '<path d="M3 7h18M3 12h18M3 17h18"/>',
    }[name]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>')

# ---------- steaguri ----------
def flag(code):
    h = lambda *c: "".join(f'<rect y="{i*40/len(c)}" width="60" height="{40/len(c)+.5}" fill="{x}"/>' for i, x in enumerate(c))
    v = lambda *c: "".join(f'<rect x="{i*60/len(c)}" width="{60/len(c)+.5}" height="40" fill="{x}"/>' for i, x in enumerate(c))
    body = {
        "de": h("#000", "#DD0000", "#FFCE00"),
        "it": v("#009246", "#fff", "#CE2B37"),
        "fr": v("#0055A4", "#fff", "#EF4135"),
        "be": v("#000", "#FDDA24", "#EF3340"),
        "nl": h("#AE1C28", "#fff", "#21468B"),
        "at": h("#C8102E", "#fff", "#C8102E"),
        "hu": h("#CE2939", "#fff", "#477050"),
        "bg": h("#fff", "#00966E", "#D62612"),
        "rs": h("#C6363C", "#0C4076", "#fff"),
        "sk": h("#fff", "#0B4EA2", "#EE1C25") + '<path d="M14 7h14v14c0 6-7 10-7 10s-7-4-7-10z" fill="#EE1C25" stroke="#fff" stroke-width="1.5"/><path d="M21 10v16M17 14h8M16.5 18h9" stroke="#fff" stroke-width="2"/><path d="M14.5 25q3-4 6.5-1 3.5-3 6.5 1" fill="#0B4EA2"/>',
        "hr": h("#FF0000", "#fff", "#171796") + '<path d="M23.5 8.5h13v16.5c0 4-6.5 6.5-6.5 6.5s-6.5-2.5-6.5-6.5z" fill="#fff" stroke="#FF0000"/><rect x="24" y="9" width="4" height="4" fill="#FF0000"/><rect x="28" y="9" width="4" height="4" fill="#fff"/><rect x="32" y="9" width="4" height="4" fill="#FF0000"/><rect x="24" y="13" width="4" height="4" fill="#fff"/><rect x="28" y="13" width="4" height="4" fill="#FF0000"/><rect x="32" y="13" width="4" height="4" fill="#fff"/><rect x="24" y="17" width="4" height="4" fill="#FF0000"/><rect x="28" y="17" width="4" height="4" fill="#fff"/><rect x="32" y="17" width="4" height="4" fill="#FF0000"/><rect x="24" y="21" width="4" height="4" fill="#fff"/><rect x="28" y="21" width="4" height="4" fill="#FF0000"/><rect x="32" y="21" width="4" height="4" fill="#fff"/><path d="M24 25h12c-.5 3.5-6 6-6 6s-5.5-2.5-6-6z" fill="#FF0000"/>',
        "si": h("#fff", "#005DA4", "#ED1C24") + '<path d="M12 6h12v9c0 5-6 8-6 8s-6-3-6-8z" fill="#005DA4" stroke="#ED1C24" stroke-width="1.2"/><path d="M13 18l3-5 2 3 2-3 3 5" fill="#fff"/>',
        "ua": h("#0057B7", "#FFD700"),
        "es": '<rect width="60" height="40" fill="#AA151B"/><rect y="10" width="60" height="20" fill="#F1BF00"/>',
        "uk": ('<rect width="60" height="40" fill="#012169"/><path d="M0 0l60 40M60 0 0 40" stroke="#fff" stroke-width="8"/>'
               '<path d="M0 0l60 40M60 0 0 40" stroke="#C8102E" stroke-width="3"/>'
               '<path d="M30 0v40M0 20h60" stroke="#fff" stroke-width="12"/><path d="M30 0v40M0 20h60" stroke="#C8102E" stroke-width="7"/>'),
    }[code]
    return f'<svg class="flag" viewBox="0 0 60 40" preserveAspectRatio="none" aria-hidden="true">{body}</svg>'

# ---------- date: țări și servicii ----------
TARI = [
    dict(slug="colete-anglia", cod="uk", tara="Anglia", in_="în Anglia", kw="colete Anglia",
         orase=["Londra", "Birmingham", "Manchester", "Leicester", "Luton", "Nottingham"],
         nota="Pentru Marea Britanie, după Brexit, coletele au nevoie de o declarație vamală cu conținutul și valoarea lor. Te ajutăm s-o completezi corect la ridicare, ca să nu se blocheze coletul la graniță."),
    dict(slug="colete-germania", cod="de", tara="Germania", in_="în Germania", kw="colete Germania",
         orase=["München", "Berlin", "Frankfurt", "Stuttgart", "Nürnberg", "Köln"]),
    dict(slug="colete-italia", cod="it", tara="Italia", in_="în Italia", kw="colete Italia",
         orase=["Roma", "Milano", "Torino", "Bologna", "Padova", "Verona"]),
    dict(slug="colete-spania", cod="es", tara="Spania", in_="în Spania", kw="colete Spania",
         orase=["Madrid", "Barcelona", "Valencia", "Castellón", "Zaragoza", "Alicante"]),
    dict(slug="colete-franta", cod="fr", tara="Franța", in_="în Franța", kw="colete Franța",
         orase=["Paris", "Lyon", "Marseille", "Strasbourg", "Lille", "Nice"]),
    dict(slug="colete-belgia", cod="be", tara="Belgia", in_="în Belgia", kw="colete Belgia",
         orase=["Bruxelles", "Antwerpen", "Gent", "Liège", "Charleroi"]),
    dict(slug="colete-olanda", cod="nl", tara="Olanda", in_="în Olanda", kw="colete Olanda",
         orase=["Amsterdam", "Rotterdam", "Haga", "Utrecht", "Eindhoven"]),
    dict(slug="colete-austria", cod="at", tara="Austria", in_="în Austria", kw="colete Austria",
         orase=["Viena", "Linz", "Graz", "Salzburg", "Innsbruck"]),
    dict(slug="colete-ungaria", cod="hu", tara="Ungaria", in_="în Ungaria", kw="colete Ungaria",
         orase=["Budapesta", "Debrețin", "Szeged", "Győr", "Pécs", "Miskolc"]),
    dict(slug="colete-bulgaria", cod="bg", tara="Bulgaria", in_="în Bulgaria", kw="colete Bulgaria",
         orase=["Sofia", "Plovdiv", "Varna", "Burgas", "Ruse"]),
    dict(slug="colete-serbia", cod="rs", tara="Serbia", in_="în Serbia", kw="colete Serbia",
         orase=["Belgrad", "Novi Sad", "Niš", "Kragujevac", "Subotica"],
         nota="Serbia nu face parte din Uniunea Europeană, așa că pentru colete este nevoie de o declarație vamală cu conținutul și valoarea lor. Te ajutăm s-o completezi la ridicare."),
    dict(slug="colete-slovacia", cod="sk", tara="Slovacia", in_="în Slovacia", kw="colete Slovacia",
         orase=["Bratislava", "Košice", "Nitra", "Žilina", "Trnava"]),
    dict(slug="colete-croatia", cod="hr", tara="Croația", in_="în Croația", kw="colete Croația",
         orase=["Zagreb", "Split", "Rijeka", "Osijek", "Zadar"]),
    dict(slug="colete-slovenia", cod="si", tara="Slovenia", in_="în Slovenia", kw="colete Slovenia",
         orase=["Ljubljana", "Maribor", "Celje", "Kranj", "Koper"]),
    dict(slug="colete-ucraina", cod="ua", tara="Ucraina", in_="în Ucraina", kw="colete Ucraina",
         orase=["Cernăuți", "Odesa", "Kiev", "Lviv", "Ivano-Frankivsk"],
         nota="Ucraina nu face parte din Uniunea Europeană, așa că pentru colete este nevoie de o declarație vamală cu conținutul și valoarea lor. Te ajutăm s-o completezi la ridicare și îți confirmăm la telefon în ce zone livrăm."),
]
T = {t["cod"]: t for t in TARI}

SERVICII = [
    dict(slug="ridicare-colete-de-la-adresa", ic="home", titlu="Ridicare colete de la adresă",
         scurt="Venim după colet acasă, la birou sau unde îți e mai simplu. Nu cari nimic la vreun depozit și nu stai la coadă.",
         lung=["Spune-ne adresa și ziua în care ești acasă. Șoferul trece pe la tine, cântărește coletul pe loc și îți spune prețul final înainte să-l ia.",
               "Ridicăm din toată țara, de la un singur colet până la mai multe pachete pentru aceeași familie. Primești numărul de urmărire pe loc, ca să știi mereu unde e coletul."]),
    dict(slug="colete-mari-si-voluminoase", ic="scale", titlu="Colete mari și voluminoase",
         scurt="Cutii mari, genți de voiaj, televizoare, biciclete sau mobilă mică. Spune-ne dimensiunile și îți dăm prețul la telefon.",
         lung=["Nu tot ce trimiți încape într-o cutie standard. Luăm și colete mari: bagaje, electrocasnice mici, biciclete, cărucioare sau piese de mobilier demontate.",
               "Prețul e același ca la orice colet: 30 € până la 20 kg, iar peste 20 kg 1,70 € pe kilogram. De exemplu, un colet de 50 kg costă 85 €. Îl cântărim la ridicare și afli suma exactă înainte să plece."]),
    dict(slug="colete-din-europa-in-romania", ic="return", titlu="Colete din Europa în România",
         scurt="Merge și invers: ridicăm coletul de la adresa ta din străinătate și îl livrăm acasă, în România.",
         lung=["Lucrezi în străinătate și vrei să trimiți ceva acasă? Ridicăm coletul de la adresa ta din țara în care ești și îl ducem direct la ușa familiei, în România.",
               "Funcționează pe toate rutele noastre, cu aceleași reguli: preț spus dinainte, număr de urmărire și livrare la adresă."]),
]
S = {s["slug"]: s for s in SERVICII}

def kw(href, text):
    return f'<a class="kw" href="{href}.html">{text}</a>'

# ---------- bucăți comune ----------
def header():
    return f'''<div class="live"><div class="wrap"><span class="dot"></span>Răspundem acum<span class="hide-m"> · Ridicăm de la adresă</span></div></div>
<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="{C["nume"]}, pagina principală">
      <span class="mark">{icon("box", 26, "#FF6A00")}</span>
      <span><b>{C["nume"]}</b><small>{C["tagline"]} · România ⇄ Europa</small></span>
    </a>
    <nav class="menu nav-desktop" aria-label="Meniu principal"><div class="wrap">
      <a href="index.html#comanda">Trimite colet</a><a href="index.html#tari">Țări</a><a href="index.html#servicii">Servicii</a><a href="index.html#pret">Preț</a>
      <a href="index.html#cum">Cum funcționează</a><a href="index.html#intrebari">Întrebări</a><a href="index.html#contact">Contact</a>
    </div></nav>
    <a class="call-dot" href="tel:{C["tel_link"]}" aria-label="Sună la {C["tel_afisat"]}">{icon("phone", 24, "#fff")}</a>
    <button class="menu-btn" type="button" aria-label="Meniu" aria-expanded="false" id="menu-btn">{icon("menu", 26, "#0A1A33")}</button>
  </div>
</header>'''

def sticky():
    return f'''<div class="sticky"><a href="tel:{C["tel_link"]}"><span class="ring">{icon("phone", 24, "#fff")}</span><span><small>Sună sau scrie-ne</small><b>{C["tel_afisat"]}</b></span></a></div>'''

def footer():
    tari = "".join(f'<li><a href="{t["slug"]}.html">Colete {t["tara"]}</a></li>' for t in TARI)
    serv = "".join(f'<li><a href="{s["slug"]}.html">{s["titlu"]}</a></li>' for s in SERVICII)
    return f'''<footer><div class="wrap">
  <div class="cols">
    <div><h4>{C["nume"]}</h4><p>Transport internațional de colete între România și Europa, de la ușă la ușă.</p></div>
    <div><h4>Țări</h4><ul>{tari}</ul></div>
    <div><h4>Servicii</h4><ul>{serv}</ul></div>
    <div><h4>Contact</h4><ul><li><a href="tel:{C["tel_link"]}">{C["tel_afisat"]}</a></li><li><a href="mailto:{C["email"]}">{C["email"]}</a></li></ul></div>
  </div>
  <p class="legal">© 2026 {C["nume"]}. Toate drepturile rezervate.</p>
</div></footer>
{sticky()}
<script>
(function(){{var b=document.getElementById("menu-btn"),m=document.querySelector("nav.menu");
if(!b||!m)return;b.addEventListener("click",function(){{var o=m.classList.toggle("open");b.setAttribute("aria-expanded",o)}});
m.addEventListener("click",function(e){{if(e.target.tagName==="A"){{m.classList.remove("open");b.setAttribute("aria-expanded","false")}}}});}})();
</script>'''

def page(title, desc, path, body):
    canon = C["domeniu"] + "/" + ("" if path == "index.html" else path)
    return f'''<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#0A1A33">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap">
<link rel="stylesheet" href="style.css">
</head>
<body>
{header()}
<main>
{body}
</main>
{footer()}
</body>
</html>
'''

def faq_html(items):
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)

def price_block():
    return f'''<div class="hazard"></div>
<div class="price">
  <p class="lbl">Prețul întreg</p>
  <p class="big">30 €</p>
  <p class="per">orice colet până la 20 kg, de la ușă la ușă</p>
  <p class="big2">1,70 € <span>/ kg</span></p>
  <p class="per">pentru coletele de peste 20 kg</p>
  <ul class="ticks">
    <li>Ridicarea de la adresa ta e inclusă</li>
    <li>Livrarea la adresa destinatarului e inclusă</li>
    <li>Prețul final îl afli înainte să plece coletul</li>
    <li>Număr de urmărire pentru fiecare colet</li>
  </ul>
</div>'''

def why_block():
    return f'''<div class="why">
  <h2>De ce să trimiți cu noi</h2>
  <ul class="checks">
    <li>Ridicăm coletul de la ușa ta, din toată țara</li>
    <li>Livrăm direct la adresa destinatarului din Europa</li>
    <li>30 € până la 20 kg, 1,70 €/kg peste 20 kg</li>
    <li>Plecări săptămânale pe fiecare rută</li>
    <li>Număr de urmărire pentru fiecare colet</li>
    <li>Și invers: colete din Europa în România</li>
  </ul>
  <a class="btn" href="tel:{C["tel_link"]}">{icon("phone", 22, "#fff")} Sună acum {C["tel_afisat"]}</a>
</div>'''

# ---------- pagina principală ----------
def index():
    tiles = "".join(f'<a class="tile" href="{t["slug"]}.html">{flag(t["cod"])}<b>{t["tara"]}</b><span>{", ".join(t["orase"][:3])}</span></a>' for t in TARI)
    cards = "".join(f'''<div class="card"><span class="ic">{icon(s["ic"], 28, "#fff")}</span><div>
      <h3>{s["titlu"]}</h3><p>{s["scurt"]}</p>
      <a class="more" href="{s["slug"]}.html">Detalii {icon("arrow", 22)}</a></div></div>''' for s in SERVICII)
    faq = [
        ("Cât costă să trimit un colet în străinătate?", f"Prețul este {C['pret_txt']}. Ridicarea și livrarea la adresă sunt incluse. Cântărim coletul la ridicare și afli suma exactă înainte să plece."),
        ("În cât timp ajunge coletul?", "Depinde de țară și de ziua în care pleacă cursa. Îți spunem data estimată de livrare când rezervi, iar cu numărul de urmărire vezi oricând unde e coletul."),
        ("Ce nu am voie să trimit?", "Nu transportăm bani, bijuterii de valoare, arme, substanțe periculoase sau inflamabile ori produse interzise de lege. Pentru Anglia sunt reguli în plus la alimente; întreabă-ne înainte să faci pachetul."),
        ("Cum trebuie ambalat coletul?", "Într-o cutie sau o geantă închisă bine, cu lucrurile fragile învelite separat. Scrie pe colet numele și telefonul destinatarului. Dacă nu ești sigur, te ajutăm la ridicare."),
        ("Ridicați colete și din orașul meu?", "Ridicăm din toată țara. Sună-ne, spune-ne localitatea și îți confirmăm ziua în care trecem pe la tine."),
        ("Pot trimite un colet din străinătate în România?", f"Da. Ridicăm coletul de la adresa ta din Europa și îl livrăm acasă, în România. Vezi {kw('colete-din-europa-in-romania', 'colete din Europa în România')}."),
    ]
    body = f'''
<div class="hero"><div class="wrap">
  <span class="eyebrow pill">Transport colete România ⇄ Europa</span>
  <h1>Trimite colete în <em>toată Europa</em>, de la ușă la ușă</h1>
  <p class="sub">Ridicăm coletul de acasă și îl livrăm direct la adresă</p>
  <p class="lead">{C["nume"]} duce coletele tale în {kw("colete-anglia","Anglia")}, {kw("colete-germania","Germania")}, {kw("colete-italia","Italia")}, {kw("colete-spania","Spania")}, {kw("colete-franta","Franța")} și în alte țări din Europa, inclusiv în {kw("colete-ungaria","Ungaria")} și în țările din jurul ei: {kw("colete-austria","Austria")}, {kw("colete-slovacia","Slovacia")}, {kw("colete-croatia","Croația")}, {kw("colete-slovenia","Slovenia")}, {kw("colete-serbia","Serbia")} și {kw("colete-ucraina","Ucraina")}, plus {kw("colete-bulgaria","Bulgaria")}. {kw("ridicare-colete-de-la-adresa","Ridicăm coletul de la adresa ta")}, îl cântărim pe loc și îți spunem prețul final înainte să plece. Trimitem și {kw("colete-mari-si-voluminoase","colete mari și voluminoase")}, iar pe aceleași rute aducem {kw("colete-din-europa-in-romania","colete din Europa în România")}.</p>
  <div class="cta-row">
    <a class="btn" href="tel:{C["tel_link"]}">{icon("phone", 24, "#fff")}<span><small>Sună acum</small>{C["tel_afisat"]}</span></a>
    <a class="btn ghost" href="#comanda">Trimite un colet</a>
  </div>
  <p class="note">Îți răspunde un om, nu un robot. Afli prețul înainte să trimiți ceva.</p>
  <div class="chips">
    <span class="chip">{icon("home", 18)} Ridicare de la adresă</span>
    <span class="chip">{icon("euro", 18)} 30 € până la 20 kg</span>
    <span class="chip">{icon("clock", 18)} Plecări săptămânale</span>
    <span class="chip">{icon("card", 18)} Cash sau card</span>
  </div>
  <div class="feats">
    <div class="feat"><span class="ic">{icon("pin", 28, "#fff")}</span><div><b>Venim la tine</b><span>acasă sau la birou</span></div></div>
    <div class="feat"><span class="ic">{icon("truck", 28, "#fff")}</span><div><b>Livrare la adresă</b><span>direct la destinatar</span></div></div>
    <div class="feat"><span class="ic">{icon("shield", 28, "#fff")}</span><div><b>Preț clar</b><span>fără taxe ascunse</span></div></div>
  </div>
</div></div>

<section id="tari" class="band"><div class="wrap">
  <div class="head"><h2>Trimitem colete în aceste țări</h2><p>Alege țara ca să vezi orașele în care livrăm și detaliile rutei.</p></div>
  <div class="grid">{tiles}</div>
</div></section>

{comanda_section(C, TARI, icon)}
<section id="servicii"><div class="wrap">
  <div class="head"><span class="eyebrow pill">Servicii</span><h2 style="margin-top:14px">Transport colete, cum îți e mai simplu</h2></div>
  <div class="cards">{cards}</div>
</div></section>

<section id="pret" class="dark"><div class="wrap">
  <div class="two">
    <div>{price_block()}</div>
    <div>
      <h2>Fără surprize la preț</h2>
      <p style="margin-top:14px;color:#C9D4E6">Orice colet de până la 20 kg costă 30 €. Peste 20 kg plătești 1,70 € pe kilogram. Ridicarea și livrarea la adresă sunt incluse. Cântărim coletul când îl ridicăm și îți spunem suma exactă înainte să plece. Nu există taxe de deplasare și nici costuri care apar după.</p>
      <div class="cta-row"><a class="btn" href="tel:{C["tel_link"]}">{icon("phone", 22, "#fff")} Cere prețul</a></div>
    </div>
  </div>
</div></section>

<section id="cum"><div class="wrap">
  <div class="head"><span class="eyebrow pill">Cum funcționează</span><h2 style="margin-top:14px">Patru pași, de la tine până la destinatar</h2></div>
  <div class="steps">
    <div class="step"><div><h3>Ne suni sau ne scrii</h3><p>Ne spui ce trimiți, în ce țară și de unde ridicăm. Primești prețul estimat pe loc.</p><span class="tag">2 minute la telefon</span></div></div>
    <div class="step"><div><h3>Ridicăm coletul de la tine</h3><p>Șoferul vine la adresa ta, cântărește coletul și îți spune prețul final.</p><span class="tag">În ziua stabilită</span></div></div>
    <div class="step"><div><h3>Coletul pleacă spre destinație</h3><p>Primești numărul de urmărire și vezi pe unde e coletul.</p><span class="tag">Plecări săptămânale</span></div></div>
    <div class="step"><div><h3>Livrăm la adresă</h3><p>Destinatarul e sunat înainte și primește coletul direct la ușă.</p><span class="tag">De la ușă la ușă</span></div></div>
  </div>
</div></section>

<section><div class="wrap">{why_block()}</div></section>

<section id="intrebari"><div class="wrap">
  <div class="head"><span class="eyebrow pill">Întrebări frecvente</span><h2 style="margin-top:14px">Transport colete în Europa: întrebări și răspunsuri</h2></div>
  <div class="faq">{faq_html(faq)}</div>
</div></section>

<section id="contact" class="final"><div class="wrap">
  <span class="eyebrow pill">Contact</span>
  <h2 style="margin-top:14px">Ai un colet de trimis? Sună acum.</h2>
  <p style="margin-top:12px;color:var(--muted)">Spune-ne ce trimiți și în ce țară. Îți dăm prețul pe loc.</p>
  <a class="phone-big" href="tel:{C["tel_link"]}">{C["tel_afisat"]}</a>
  <p><a class="kw" href="mailto:{C["email"]}" style="font-weight:600">{C["email"]}</a></p>
</div></section>
'''
    return page(f"Transport colete România Europa, de la ușă la ușă | {C['nume']}",
                f"Transport colete din România în Anglia, Germania, Italia, Spania, Ungaria, Austria, Bulgaria și toată Europa. Ridicare de la adresă, livrare la ușă. 30 € până la 20 kg.",
                "index.html", body)

# ---------- pagini de țară ----------
def tara_page(t):
    alte = [x for x in TARI if x is not t]
    links_alte = ", ".join(kw(x["slug"], x["kw"]) for x in alte[:4])
    orase = "".join(f"<span>{o}</span>" for o in t["orase"])
    nota = f"<h2>Ce trebuie să știi pentru {t['tara']}</h2><p>{t['nota']}</p>" if t.get("nota") else ""
    faq = [
        (f"Cât costă un colet {t['in_']}?", f"Prețul este {C['pret_txt']}. Ridicarea din România și livrarea la adresa din {t['tara']} sunt incluse."),
        (f"În ce orașe din {t['tara']} livrați?", f"Livrăm în toată țara, inclusiv în {', '.join(t['orase'])}. Dacă localitatea ta nu apare aici, sună-ne și îți confirmăm."),
        (f"Pot trimite colete și din {t['tara']} în România?", f"Da. Ridicăm coletul de la adresa ta din {t['tara']} și îl livrăm acasă, în România. Detalii la {kw('colete-din-europa-in-romania','colete din Europa în România')}."),
    ]
    body = f'''
<div class="hero"><div class="wrap">
  <p class="crumbs"><a href="index.html">Acasă</a> / Colete {t["tara"]}</p>
  <span class="eyebrow pill" style="margin-top:14px">Transport colete România – {t["tara"]}</span>
  <h1>Transport colete <em>România – {t["tara"]}</em></h1>
  <p class="sub">Ridicăm de la adresa ta și livrăm direct la ușă {t["in_"]}</p>
  <p class="lead">Trimite {kw(t["slug"], t["kw"])} fără să mergi la vreun depozit. {kw("ridicare-colete-de-la-adresa","Ridicăm coletul de acasă")} de oriunde din România, îl cântărim pe loc și îl livrăm la adresa destinatarului {t["in_"]}. Luăm și {kw("colete-mari-si-voluminoase","colete mari")}, iar pe aceeași rută aducem {kw("colete-din-europa-in-romania","colete din " + t["tara"] + " în România")}.</p>
  <div class="cta-row"><a class="btn" href="tel:{C["tel_link"]}">{icon("phone", 24, "#fff")}<span><small>Sună acum</small>{C["tel_afisat"]}</span></a></div>
</div></div>

<section><div class="wrap"><div class="two">
  <div class="prose">
    <h2 style="margin-top:0">Orașe în care livrăm {t["in_"]}</h2>
    <p>Livrăm la adresă în toată țara. Cele mai cerute orașe:</p>
    <div class="cities">{orase}</div>
    <h2>Cum trimiți un colet {t["in_"]}</h2>
    <p>Ne suni și ne spui ce trimiți, adresa de ridicare din România și adresa din {t["tara"]}. Primești prețul estimat pe loc. În ziua stabilită, șoferul ridică coletul de la tine și îl cântărește, iar tu primești prețul final și numărul de urmărire.</p>
    <p>Coletul pleacă cu următoarea cursă spre {t["tara"]}. Înainte de livrare, destinatarul e sunat și primește coletul direct la ușă.</p>
    {nota}
    <h2>Preț colete {t["tara"]}</h2>
    <p>Prețul este {C["pret_txt"]}. Ridicarea și livrarea la adresă sunt incluse, nu ai taxe ascunse și afli suma exactă înainte să plece coletul.</p>
    <h2>Trimitem și în alte țări</h2>
    <p>Pe lângă {t["tara"]}, avem curse și pentru {links_alte}.</p>
    <h2>Întrebări frecvente</h2>
    <div class="faq">{faq_html(faq)}</div>
  </div>
  {why_block()}
</div></div></section>
'''
    return page(f"Transport colete România {t['tara']}, de la ușă la ușă | {C['nume']}",
                f"Transport colete România – {t['tara']}: ridicare de la adresă, livrare la ușă în {', '.join(t['orase'][:3])} și în toată țara. 30 € până la 20 kg.",
                t["slug"] + ".html", body)

# ---------- pagini de serviciu ----------
def serviciu_page(s):
    tari = ", ".join(kw(t["slug"], t["tara"]) for t in TARI)
    alte = " și ".join(kw(x["slug"], x["titlu"].lower()) for x in SERVICII if x is not s)
    paras = "".join(f"<p>{p}</p>" for p in s["lung"])
    body = f'''
<div class="hero"><div class="wrap">
  <p class="crumbs"><a href="index.html">Acasă</a> / {s["titlu"]}</p>
  <span class="eyebrow pill" style="margin-top:14px">Transport colete Europa</span>
  <h1>{s["titlu"]}</h1>
  <p class="lead" style="margin-top:12px">{s["scurt"]}</p>
  <div class="cta-row"><a class="btn" href="tel:{C["tel_link"]}">{icon("phone", 24, "#fff")}<span><small>Sună acum</small>{C["tel_afisat"]}</span></a></div>
</div></div>
<section><div class="wrap"><div class="two">
  <div class="prose">
    <h2 style="margin-top:0">Cum funcționează</h2>
    {paras}
    <h2>În ce țări</h2>
    <p>Serviciul e disponibil pe toate rutele noastre: {tari}.</p>
    <h2>Preț</h2>
    <p>Prețul este {C["pret_txt"]}. Ridicarea și livrarea la adresă sunt incluse.</p>
    <h2>Alte servicii</h2>
    <p>Vezi și {alte}.</p>
  </div>
  {why_block()}
</div></div></section>
'''
    return page(f"{s['titlu']} | {C['nume']}", s["scurt"], s["slug"] + ".html", body)

# ---------- scriere ----------
os.makedirs(OUT, exist_ok=True)
files = {"index.html": index()}
for t in TARI: files[t["slug"] + ".html"] = tara_page(t)
for s in SERVICII: files[s["slug"] + ".html"] = serviciu_page(s)
for name, content in files.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f: f.write(content)
shutil.copy(os.path.join(HERE, "style.css"), os.path.join(OUT, "style.css"))
urls = "".join(f"  <url><loc>{C['domeniu']}/{'' if n == 'index.html' else n}</loc></url>\n" for n in files)
open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {C['domeniu']}/sitemap.xml\n")
fav = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0A1A33"/><g transform="translate(12 12) scale(1.67)" fill="none" stroke="#FF6A00" stroke-width="2" stroke-linejoin="round"><path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/></g></svg>'
open(os.path.join(OUT, "favicon.svg"), "w").write(fav)
print(len(files), "pagini")
