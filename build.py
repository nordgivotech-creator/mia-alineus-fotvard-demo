"""Bygger hela demosajten: py build.py  (skriver alla .html-filer bredvid style.css och script.js).
Endast fakta som Mia själv publicerat används: tjänster, orter, titlar, telefon, e-post. Inga priser, omdömen eller medicinska löften."""
import json
import pathlib

OUT = pathlib.Path(__file__).parent
NAME = "Mia Alineus Fotvård"
PHONE, PHONE_HREF = "076-809 40 41", "+46768094041"
MAIL = "miaalineus.fotvard@gmail.com"
FB = "https://www.facebook.com/profile.php?id=61586364565331"
ORTER = [("Eslöv", "eslov"), ("Staffanstorp", "staffanstorp"), ("Veberöd", "veberod"), ("Genarp", "genarp"), ("Södra Sandby", "sodra-sandby"), ("Revinge", "revinge"), ("Lund", "lund")]
BEHANDLINGAR = [
    ("Förhårdnader", "Hård hud under och runt foten kan kännas obekvämt i skon. Mia tar hand om det vid hembesöket."),
    ("Nageltrång", "Berätta när du bokar var det besvär finns, så kan Mia planera besöket och ta med rätt utrustning."),
    ("Vårtor", "Mia kan titta på vårtor på fötterna. Hör av dig så går ni igenom vad som passar innan besöket."),
    ("Liktornar", "Små, tryckkänsliga förtjockningar. Mia hjälper dig med dem på plats hemma hos dig."),
]
ARTICLES = [
    dict(slug="infor-hembesoket", cat="Inför hembesöket", t="Så förbereder du för fotvård hemma", d="Ett par praktiska saker att stämma av när du bokar.", img="infor-hembesoket.webp", min=3,
         lead="Ett hembesök fungerar bäst när några småsaker är ordnade i förväg. Här är det som brukar vara bra att tänka på.",
         body=[("Välj en plats med bra ljus", "Sätt dig bekvämt på en stol eller i en soffa där Mia kommer åt dina fötter. Ett rum med bra belysning gör arbetet enklare."),
               ("Ha handdukar framme", "Lägg fram några rena handdukar. Fråga Mia vid bokningen om det är något mer hon vill att du har i ordning."),
               ("Berätta vad du vill ha hjälp med", "Beskriv besväret när du ringer eller mejlar, till exempel förhårdnader, nageltrång, vårtor eller liktornar. Då kan Mia förbereda sig."),
               ("Stäm av tid och pris i förväg", "Priser lämnas på förfrågan. Fråga vad besöket kostar när ni kommer överens om tid, så vet du vad som gäller.")],
         check=["Ange din ort och adress", "Beskriv besväret med några ord", "Fråga efter pris och tid", "Ha en bekväm sittplats med bra ljus", "Lägg fram rena handdukar"]),
    dict(slug="boka-at-en-narstaende", cat="Bokning", t="Boka fotvård åt en närstående", d="Så kan du hjälpa någon att ordna ett hembesök.", img="boka-at-en-narstaende.webp", min=3,
         lead="Många som behöver fotvård har svårt att själva ta sig till en mottagning. Du kan hjälpa till genom att ta den första kontakten.",
         body=[("Prata med personen först", "Stäm av att personen vill ha besöket och vad den vill ha hjälp med. Det är personens egna fötter, så önskemålen ska komma därifrån."),
               ("Ring eller mejla Mia", "Berätta vilken ort det gäller och att du bokar åt en närstående. Mia kan då svara på om hon kommer till orten och lämna prisuppgift."),
               ("Bestäm tid som passar båda", "Kom överens om en tid då personen är hemma och du kanske kan vara på plats eller nåbar i telefon."),
               ("Efteråt", "Fråga personen hur besöket kändes. Då vet ni om det är något ni vill ta med inför nästa gång.")],
         check=["Personen vill ha besöket", "Ort och adress är klara", "Du vet vad besväret gäller", "Ni har valt en tid som passar", "Du har frågat om pris"]),
    dict(slug="fotvard-i-din-ort", cat="Hembesök", t="Var gör Mia hembesök?", d="Se vilka orter Mia besöker och vad du kan ange i din förfrågan.", img="fotvard-i-din-ort.webp", min=2,
         lead="Mia utgår från Södra Sandby och kommer hem till dig i flera orter runt omkring.",
         body=[("Besöksområdet", "Mia erbjuder hembesök i Eslöv, Staffanstorp, Veberöd, Genarp, Södra Sandby, Revinge och Lund."),
               ("Fråga om din adress", "Ange din ort när du ringer eller mejlar. Mia kan då svara på om ett hembesök är möjligt och lämna prisuppgift."),
               ("Bor du utanför listan?", "Hör av dig ändå och fråga. Det är Mia som avgör om ett besök går att ordna.")],
         check=["Din ort", "Gatuadress", "Vad du vill ha hjälp med", "Önskad veckodag"]),
    dict(slug="infor-samtalet", cat="Bokning", t="Checklista inför samtalet med Mia", d="Det här är bra att ha i huvudet när du ringer eller mejlar.", img="infor-hembesoket.webp", min=2,
         lead="Ett kort samtal räcker långt om du har några uppgifter till hands. Så får du snabbare svar på om och när Mia kan komma.",
         body=[("Det Mia behöver veta", "Vilken ort du bor i, vad du vill ha hjälp med och om du bokar åt dig själv eller någon annan."),
               ("Det du kan fråga", "Fråga om pris, vilka dagar som fungerar och hur lång tid besöket brukar ta. Mia lämnar prisuppgift på förfrågan."),
               ("Ring eller mejla", "Vill du hellre skriva fungerar mejl lika bra. Skriv ort, besvär och några tider som passar.")],
         check=["Ort", "Besvär", "För dig eller någon annan", "Tider som passar", "Frågor om pris"]),
    dict(slug="hembesok-eller-mottagning", cat="Tips", t="Hembesök eller mottagning? Så väljer du", d="Några saker att väga in när du funderar på vad som passar dig.", img="boka-at-en-narstaende.webp", min=3,
         lead="Fotvård kan göras på en mottagning eller hemma hos dig. Det rätta valet beror på hur du har det i vardagen.",
         body=[("När hembesök passar", "Om resan till en mottagning är jobbig, tar tid eller kräver hjälp av någon annan kan det vara enklare att få besök hemma."),
               ("Det du behöver ordna hemma", "En bekväm sittplats, bra ljus och handdukar. Mia berättar om det är något mer."),
               ("Osäker?", "Ring och fråga. Mia kan berätta hur ett besök går till innan du bestämmer dig.")],
         check=["Hur tar jag mig till en mottagning?", "Har jag en bra plats hemma?", "Vill jag ha någon med mig?", "Vad kostar det?"]),
]
FAQ = [("Vad kostar ett besök?", "Priser lämnas på förfrågan. Kontakta Mia för en prisuppgift inför bokningen."),
       ("Kan jag boka åt en närstående?", "Ja, du kan kontakta Mia och fråga om ett hembesök åt en närstående. Stäm av med personen först."),
       ("Hur vet jag om Mia kommer till min ort?", "Se listan över besöksorter eller ange orten när du kontaktar Mia."),
       ("Vad behöver jag ha hemma?", "En bekväm sittplats med bra ljus och några rena handdukar. Fråga Mia om hon vill att något mer är i ordning."),
       ("Hur bokar jag?", "Ring eller mejla Mia, berätta ort och vad du vill ha hjälp med, och kom överens om en tid."),
       ("Vilken utbildning har Mia?", "Mia är certifierad undersköterska och diplomerad fotvårdare.")]


def e(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


def jl(o):
    return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def head(title, desc, rel="", ld=None, img="hero.webp"):
    return (f'<!doctype html><html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">'
            f'<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#26382c">'
            f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:image" content="{img}"><meta property="og:locale" content="sv_SE">'
            f'<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Crect width=%2732%27 height=%2732%27 rx=%278%27 fill=%27%2326382c%27/%3E%3Ctext x=%2716%27 y=%2723%27 font-size=%2720%27 text-anchor=%27middle%27 fill=%27%23faf7ef%27 font-family=%27Georgia%27%3EM%3C/text%3E%3C/svg%3E">'
            f'<link rel="stylesheet" href="style.css">{"".join(jl(x) for x in (ld or []))}</head>')


def top(active=""):
    def a(h, t, k):
        return f'<a href="{h}"{" aria-current=page" if active == k else ""}>{t}</a>'
    return ('<a class="skip" href="#innehall">Hoppa till innehållet</a><div class="notice">Inofficiell demo framtagen av Nordgivo Tech</div><div class="bar" id="bar"></div>'
            '<header class="top"><div class="wrap nav"><a class="brand" href="index.html" aria-label="Mia Alineus Fotvård, startsida"><span class="mono">M</span>Mia Alineus <span>Fotvård</span></a>'
            '<button class="burger" id="burger" aria-expanded="false" aria-controls="menu"><span class="sr">Meny</span><i></i><i></i></button>'
            f'<nav id="menu" aria-label="Huvudmeny">{a("index.html#behandlingar", "Behandlingar", "b")}{a("index.html#om-mia", "Om Mia", "o")}{a("index.html#omraden", "Orter", "r")}{a("blogg.html", "Blogg", "bl")}{a("kontakt.html", "Kontakt", "k")}'
            f'<a class="button sm" href="tel:{PHONE_HREF}">Ring Mia</a></nav></div></header>')


def foot():
    ol = "".join(f'<li><a href="fotvard-{s}.html">{n}</a></li>' for n, s in ORTER)
    return (f'<footer class="foot"><div class="wrap fg"><div><p class="brand sm"><span class="mono">M</span>Mia Alineus <span>Fotvård</span></p><p>Ambulerande fotvård med hembesök i Skåne.</p><p><a href="tel:{PHONE_HREF}">{PHONE}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p></div>'
            f'<div><h3>Besöksorter</h3><ul>{ol}</ul></div><div><h3>Läs mer</h3><ul><li><a href="blogg.html">Blogg</a></li><li><a href="kontakt.html">Kontakt och förfrågan</a></li><li><a href="index.html#fragor">Vanliga frågor</a></li><li><a href="{FB}">Mia på Facebook</a></li></ul></div></div>'
            '<div class="wrap fine"><span>Demoförslag för Mia Alineus Fotvård · framtaget av Nordgivo Tech · inget skickas och inga uppgifter sparas</span></div></footer>'
            f'<a class="callbar" href="tel:{PHONE_HREF}"><span>Ring Mia</span><b>{PHONE}</b></a><script src="script.js"></script></body></html>')


def biz():
    return {"@context": "https://schema.org", "@type": "HealthAndBeautyBusiness", "name": NAME, "telephone": PHONE_HREF, "email": MAIL, "sameAs": [FB],
            "description": "Ambulerande fotvård med hembesök i Eslöv, Staffanstorp, Veberöd, Genarp, Södra Sandby, Revinge och Lund.",
            "areaServed": [{"@type": "City", "name": n} for n, _ in ORTER],
            "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": b[0]}} for b in BEHANDLINGAR]}


def crumbs(*items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": h} for i, (n, h) in enumerate(items)]}


def faqld(f):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in f]}


def cta(t="Fråga om ett hembesök"):
    return (f'<section class="cta"><div class="wrap cta-in"><div><p class="label">Redo när du är det</p><h2>{t}</h2><p>Ring eller mejla Mia, berätta vilken ort det gäller och få prisuppgift.</p></div>'
            f'<div class="actions"><a class="button light" href="tel:{PHONE_HREF}">Ring {PHONE}</a><a class="button ghost" href="kontakt.html">Skriv en förfrågan</a></div></div></section>')


def card(a):
    return (f'<article class="story rv" data-cat="{e(a["cat"])}" data-t="{e((a["t"] + " " + a["d"]).lower())}"><a href="{a["slug"]}.html"><img src="{a["img"]}" width="420" height="360" alt="" loading="lazy"><div class="story-copy">'
            f'<p class="label">{e(a["cat"])} · {a["min"]} min</p><h3>{e(a["t"])}</h3><p>{e(a["d"])}</p><span class="read">Läs artikeln ↗</span></div></a></article>')


def ortsel():
    o = "".join(f'<option value="{s}">{n}</option>' for n, s in ORTER)
    return ('<div class="finder rv"><div><p class="label">Kommer Mia till dig?</p><h3>Välj din ort</h3></div><div class="fcol"><label for="ort">Jag bor i</label>'
            f'<select id="ort"><option value="">Välj ort …</option>{o}<option value="annan">Annan ort</option></select><p id="ortsvar" class="svar" aria-live="polite">Välj din ort så ser du direkt om den finns bland Mias besöksorter.</p></div></div>')


def index():
    tre = "".join(f'<button class="tc rv" aria-expanded="false"><span class="n">0{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p><span class="pl" aria-hidden="true">+</span></button>' for i, (t, d) in enumerate(BEHANDLINGAR))
    orter = "".join(f'<li><a href="fotvard-{s}.html">{n}</a></li>' for n, s in ORTER)
    mq = "".join(f"<span>{n}</span>" for n, _ in ORTER) * 4
    steps = [("Kontakta Mia", "Ring eller mejla och berätta vilken ort du bor på och vad du vill ha hjälp med."), ("Stäm av tid och pris", "Fråga vad besöket kostar och kom överens med Mia om en tid som passar."), ("Ta emot Mia hemma", "Mia kommer till den adress ni har kommit överens om och utför fotvården på plats.")]
    st = "".join(f'<li class="rv"><h3>{t}</h3><p>{d}</p></li>' for t, d in steps)
    fq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in FAQ)
    arts = "".join(card(a) for a in ARTICLES[:3])
    return (head("Mia Alineus Fotvård | Fotvård hemma hos dig i Skåne", "Ambulerande fotvård med hembesök i Eslöv, Staffanstorp, Veberöd, Genarp, Södra Sandby, Revinge och Lund. Certifierad undersköterska och diplomerad fotvårdare.", ld=[biz(), faqld(FAQ)])
            + "<body>" + top() + '<main id="innehall">'
            '<section class="hero"><div class="wrap hg"><div class="intro"><p class="label chip">Ambulerande fotvård i Skåne</p><h1>Fotvård hemma <em>hos dig.</em></h1>'
            '<p class="lede">Mia Alineus kommer hem till dig och utför fotvårdsbehandling på plats. Du slipper resa, och du får en lugn stund i din egen hemmiljö.</p>'
            f'<div class="actions"><a class="button" href="kontakt.html">Fråga om en tid <span aria-hidden="true">↘</span></a><a class="link" href="tel:{PHONE_HREF}">eller ring {PHONE}</a></div>'
            '<ul class="trust"><li>Certifierad undersköterska</li><li>Diplomerad fotvårdare</li><li>Hembesök i 7 orter</li></ul></div>'
            '<div class="ph"><div class="hero-photo" role="img" aria-label="Fotvård hemma"></div><div class="float"><b>Hembesök</b><span>Södra Sandby · Lund · Eslöv m.fl.</span></div></div></div></section>'
            f'<div class="mq" aria-hidden="true"><div>{mq}</div></div>'
            f'<section id="behandlingar" class="sec"><div class="wrap"><div class="shead rv"><p class="label">Behandlingar</p><h2>Det här hjälper Mia dig med</h2><p>Klicka på ett kort för mer information. Priser lämnas på förfrågan.</p></div><div class="tg">{tre}</div></div></section>'
            f'<section id="omraden" class="sec tint"><div class="wrap">{ortsel()}<ul class="places rv">{orter}</ul></div></section>'
            '<section id="om-mia" class="sec"><div class="wrap two"><div class="rv"><p class="label">Om Mia</p><h2>Närvarande och noggrann, hemma hos dig</h2></div><div class="rv"><p class="lede">Med utgångspunkt i Södra Sandby erbjuder Mia fotvård vid hembesök. Du kan höra av dig för egen del eller hjälpa en närstående att boka.</p>'
            '<ul class="cred"><li><b>Certifierad</b> undersköterska</li><li><b>Diplomerad</b> fotvårdare</li><li><b>Hembesök</b> i sju orter i Skåne</li></ul></div></div></section>'
            f'<section class="sec dark"><div class="wrap two"><div class="rv"><p class="label">Från första kontakt till hembesök</p><h2>Så går det till</h2></div><ol class="steps">{st}</ol></div></section>'
            f'<section class="sec"><div class="wrap"><div class="shead row rv"><div><p class="label">Blogg</p><h2>Fotvård i vardagen</h2></div><a class="link" href="blogg.html">Alla artiklar ↗</a></div><div class="stories">{arts}</div></div></section>'
            f'<section id="fragor" class="sec tint"><div class="wrap two"><div class="rv"><p class="label">Vanliga frågor</p><h2>Frågor och svar</h2></div><div class="faq rv">{fq}</div></div></section>'
            + cta() + "</main>" + foot())


def kontakt():
    o = "".join(f'<option>{n}</option>' for n, _ in ORTER)
    return (head("Kontakt och förfrågan | " + NAME, "Ring eller mejla Mia Alineus Fotvård och fråga om hembesök. Berätta ort och vad du vill ha hjälp med.", ld=[biz(), crumbs(("Start", "index.html"), ("Kontakt", "kontakt.html"))])
            + "<body>" + top("k") + '<main id="innehall" class="wrap page"><p class="label">Kontakt</p><h1 class="h1s">Fråga om ett hembesök</h1><p class="lede">Ring eller mejla Mia, eller fyll i formuläret så öppnas ett färdigt mejl i din mejlapp. Inget skickas förrän du själv trycker på skicka.</p>'
            f'<div class="cg"><form id="req" class="form" novalidate><label for="f-n">Ditt namn</label><input id="f-n" required autocomplete="name"><label for="f-o">Ort</label><select id="f-o" required><option value="">Välj ort …</option>{o}<option>Annan ort</option></select>'
            '<label for="f-b">Vad vill du ha hjälp med?</label><select id="f-b"><option>Förhårdnader</option><option>Nageltrång</option><option>Vårtor</option><option>Liktornar</option><option>Annat / osäker</option></select>'
            '<label class="chk"><input type="checkbox" id="f-c"> Jag bokar åt en närstående</label><label for="f-m">Meddelande och önskade tider</label><textarea id="f-m" rows="4"></textarea><button class="button" type="submit">Förbered mejl till Mia</button><p class="mut" id="fmsg" aria-live="polite"></p></form>'
            f'<aside class="side"><h2>Eller kontakta Mia direkt</h2><p><a class="button" href="tel:{PHONE_HREF}">Ring {PHONE}</a></p><p><a href="mailto:{MAIL}">{MAIL}</a></p><p><a href="{FB}">Mia på Facebook</a></p><h3>Bra att ange</h3><ul class="cred"><li>Din ort och adress</li><li>Vad du vill ha hjälp med</li><li>Om det är åt dig själv eller någon annan</li></ul><p class="mut">Priser lämnas på förfrågan.</p></aside></div></main>'
            + foot())


def blogg():
    cats = ["Alla"] + sorted({a["cat"] for a in ARTICLES})
    ch = "".join(f'<button class="fc{" on" if c == "Alla" else ""}" data-c="{e(c)}">{e(c)}</button>' for c in cats)
    return (head("Blogg | " + NAME, "Praktiska guider för dig som funderar på att boka fotvård hemma.", ld=[crumbs(("Start", "index.html"), ("Blogg", "blogg.html"))])
            + "<body>" + top("bl") + '<main id="innehall" class="wrap page"><p class="label">Blogg</p><h1 class="h1s">Fotvård i vardagen</h1><p class="lede">Praktiska guider för dig som funderar på att boka fotvård hemma.</p>'
            f'<div class="filters"><div class="chips" role="group" aria-label="Kategori">{ch}</div><label class="sr" for="q">Sök</label><input id="q" type="search" placeholder="Sök i artiklarna …"></div>'
            f'<div class="stories" id="list">{"".join(card(a) for a in ARTICLES)}</div><p id="none" class="mut" hidden>Inga artiklar matchade.</p></main>' + cta() + foot())


def article(a):
    secs = "".join(f'<h2 id="s{i}">{e(h)}</h2><p>{e(p)}</p>' for i, (h, p) in enumerate(a["body"]))
    ck = "".join(f"<li>{e(c)}</li>" for c in a["check"])
    rel = "".join(card(x) for x in ARTICLES if x["slug"] != a["slug"])[:0] + "".join(card(x) for x in [y for y in ARTICLES if y["slug"] != a["slug"]][:3])
    ld = [crumbs(("Start", "index.html"), ("Blogg", "blogg.html"), (a["t"], a["slug"] + ".html")),
          {"@context": "https://schema.org", "@type": "Article", "headline": a["t"], "description": a["d"], "image": a["img"], "author": {"@type": "Person", "name": "Mia Alineus"}, "publisher": {"@type": "Organization", "name": NAME}}]
    return (head(f'{a["t"]} | {NAME}', a["d"], ld=ld, img=a["img"]) + "<body>" + top("bl")
            + f'<main id="innehall" class="wrap art"><a class="back" href="blogg.html">← Till bloggen</a><p class="label">{e(a["cat"])} · {a["min"]} min läsning</p><h1 class="h1s">{e(a["t"])}</h1><p class="lede">{e(a["lead"])}</p>'
            f'<img class="ahero" src="{a["img"]}" width="840" height="520" alt="">'
            f'<div class="ag"><aside class="toc" aria-label="Innehåll"><b>I artikeln</b><ol id="toc"></ol></aside><div class="prose">{secs}<div class="box"><h3>Checklista</h3><ul class="cred">{ck}</ul></div>'
            f'<p><a class="button" href="kontakt.html">Fråga om ett hembesök ↘</a></p></div></div></main>'
            f'<section class="sec tint"><div class="wrap"><div class="shead rv"><h2>Fler artiklar</h2></div><div class="stories">{rel}</div></div></section>' + foot())


def ort(n, s):
    nar = [x for x in ORTER if x[1] != s][:4]
    nl = ", ".join(x[0] for x in nar)
    f = [(f"Kommer Mia till {n}?", f"Ja, {n} finns bland Mias besöksorter. Ange din adress när du kontaktar henne så bekräftar hon tid och pris."), ("Vad kostar ett besök?", "Priser lämnas på förfrågan."), ("Vad behöver jag ha hemma?", "En bekväm sittplats med bra ljus och några rena handdukar.")]
    ld = [biz(), faqld(f), crumbs(("Start", "index.html"), (f"Fotvård i {n}", f"fotvard-{s}.html"))]
    fq = "".join(f"<details><summary>{e(q)}</summary><p>{e(x)}</p></details>" for q, x in f)
    return (head(f"Fotvård i {n} | Hembesök av Mia Alineus", f"Fotvård hemma i {n}. Mia Alineus är certifierad undersköterska och diplomerad fotvårdare och kommer hem till dig.", ld=ld) + "<body>" + top("r")
            + f'<main id="innehall" class="wrap page"><p class="label">Hembesök i {n}</p><h1 class="h1s">Fotvård hemma i {n}</h1><p class="lede">Mia kommer hem till dig i {n} och utför fotvårdsbehandling på plats. Hon är certifierad undersköterska och diplomerad fotvårdare.</p>'
            f'<div class="actions"><a class="button" href="kontakt.html">Fråga om ett hembesök i {n} ↘</a><a class="link" href="tel:{PHONE_HREF}">ring {PHONE}</a></div>'
            f'<div class="two sp"><div><h2>Det här hjälper Mia med</h2><ul class="cred">{"".join(f"<li>{b[0]}</li>" for b in BEHANDLINGAR)}</ul><p class="mut">Priser lämnas på förfrågan.</p></div><div><h2>Frågor om {n}</h2><div class="faq">{fq}</div></div></div>'
            f'<p class="mut">Mia besöker även {nl} med flera orter. <a href="index.html#omraden">Se alla orter</a>.</p></main>' + cta() + foot())


def main():
    pages = {"index.html": index(), "kontakt.html": kontakt(), "blogg.html": blogg()}
    for a in ARTICLES:
        pages[a["slug"] + ".html"] = article(a)
    for n, s in ORTER:
        pages[f"fotvard-{s}.html"] = ort(n, s)
    for k, v in pages.items():
        (OUT / k).write_text(v, encoding="utf-8")
    sm = "".join(f"<url><loc>{k}</loc></url>" for k in pages)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>', encoding="utf-8")
    (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n# Demo: släpps efter godkännande\n", encoding="utf-8")
    print(len(pages), "sidor byggda")


main()
