# Edda – Doula in Erkelenz & Kreis Heinsberg

Moderne, schlanke One-Page-Website für Edda Möller, Doula-Geburtsbegleitung in
Erkelenz und im gesamten Kreis Heinsberg (NRW).

Die Seite ersetzt die bisherige Jimdo-Website. Alle Texte, Fotos und
Kontaktdaten wurden von der bestehenden Seite übernommen und in ein neues,
ruhiges und modernes Design gebracht. Technisch ist die Seite bewusst simpel
gehalten: reines HTML/CSS/JavaScript, keine Build-Tools, kein Framework, kein
Backend, keine Cookies und kein Tracking.

## Struktur

```
index.html          Startseite (die eigentliche One-Page-Website)
impressum.html       Impressum (rechtlich erforderlich)
datenschutz.html      Datenschutzerklärung
robots.txt            Suchmaschinen-Steuerung
sitemap.xml           XML-Sitemap für Suchmaschinen
site.webmanifest       Web App Manifest (Icons, Theme-Farbe)
assets/
  css/style.css         Gesamtes Styling
  js/main.js            Mobiles Menü, Scroll-Animationen, Footer-Jahr
  fonts/                Selbst gehostete Schriftdateien (Lora, Inter)
  img/                  Optimierte Bilder (JPEG + WebP, mehrere Größen) und Icons
site-assets/
  originals/            Rohbilder in Originalqualität (Ausgangsmaterial)
  process_images.py     Skript zum Zuschneiden/Optimieren der Fotos
flyer/
  flyer.pdf / flyer-a4.png   Druckfertiger A4-Flyer (300 dpi) mit QR-Code
  flyer.html                 Browser-Ansicht zum Drucken
  generate_flyer.py          Erzeugt PNG/PDF neu aus Texten und Assets
```

## Design-Entscheidungen

- **Eine Seite, kein Klick-Marathon**: Navigation führt per Anker-Links zu
  Abschnitten auf derselben Seite (Über mich, Begleitung, Einsatzgebiet, FAQ,
  Kontakt). Impressum/Datenschutz sind aus rechtlichen Gründen eigene,
  schlanke Unterseiten.
- **Farben & Typografie**: warme, ruhige Terrakotta-/Cremetöne mit einem
  Salbeigrün als Sekundärfarbe. Überschriften in „Lora“ (klare, gut lesbare
  Serifenschrift mit geradem, ruhigem Schriftbild), Fließtext in „Inter“.
  Beide Schriften werden selbst gehostet (kein externer Aufruf zu Google
  Fonts).
- **Keine Cookies, kein Tracking**: bewusst wie auf der bisherigen Website.
  Es gibt keine Analyse-Skripte, keine eingebetteten Drittanbieter-Inhalte
  (auch keine Google-Maps-Einbettung) und keine Cookie-Banner, weil schlicht
  keine nicht-essenziellen Cookies gesetzt werden.
- **Kontakt ohne Formular**: Telefon-, WhatsApp-, SMS- und E-Mail-Links
  (`tel:`, `sms:`, `https://wa.me/…`, `mailto:`) statt eines Kontaktformulars –
  keine Serverlogik nötig, funktioniert auf jedem Hosting.

## SEO-Maßnahmen

- Fokus-Keywords in Title, Meta-Description, Überschriften und Bild-Alt-Texten:
  „Doula Erkelenz“, „Geburtsbegleitung Kreis Heinsberg“ sowie die Orte
  Heinsberg, Wegberg, Wassenberg, Hückelhoven, Geilenkirchen, Übach-Palenberg,
  Gangelt, Selfkant, Waldfeucht.
- Strukturierte Daten (JSON-LD) für `ProfessionalService` (Name, Adresse,
  Telefon, E-Mail, Einsatzgebiet) und `FAQPage` (häufige Fragen), damit Google
  die Seite als lokales Angebot einordnen und ggf. Rich Snippets anzeigen
  kann.
- `robots.txt` und `sitemap.xml` für saubere Indexierung.
- Ein eigener FAQ-Bereich deckt typische Suchanfragen ab („Was macht eine
  Doula?“, „Übernimmt die Krankenkasse die Kosten?“ usw.).
- Schnelle Ladezeiten durch optimierte, responsive Bilder (WebP + JPEG in
  mehreren Größen, `srcset`/`sizes`), selbst gehostete Schriften und
  vollständig statisches HTML ohne Frameworks.
- Halbwegs sprechende, kanonische URL-Struktur und `lang="de"`.

## Lokal ansehen

Da die Seite komplett statisch ist, reicht ein einfacher lokaler Webserver,
zum Beispiel:

```bash
cd /workspace
python3 -m http.server 8080
# dann im Browser: http://localhost:8080/
```

## Deployment

Die Seite besteht ausschließlich aus statischen Dateien und kann direkt auf
jedem Standard-Webhosting (z. B. das bisherige Hosting-Paket), bei Netlify,
GitHub Pages oder Cloudflare Pages veröffentlicht werden. Es ist kein
Build-Schritt notwendig – einfach den Inhalt dieses Repositories in das
Wurzelverzeichnis des Webspace kopieren.

**Vor dem Live-Schalten prüfen/anpassen:**

- Domain in `index.html`, `impressum.html`, `datenschutz.html` (`<link
  rel="canonical">`, Open-Graph-URLs) sowie in `CNAME`, `robots.txt`,
  `sitemap.xml` und `flyer/generate_flyer.py` auf die tatsächliche Ziel-Domain
  anpassen, falls sie von `https://edda-die-doula.com/` abweicht.
- Bei Google Search Console und ggf. Google Unternehmensprofil (Google Maps)
  hinterlegen, damit die lokale Auffindbarkeit zusätzlich gestärkt wird.

## Bilder neu erzeugen

Die Originalfotos liegen in `site-assets/originals/`. Mit
`site-assets/process_images.py` (benötigt Pillow: `pip install pillow`)
werden daraus die optimierten, responsiven Bilddateien in `assets/img/`
erzeugt:

```bash
pip install pillow
python3 site-assets/process_images.py
```

## A4-Flyer

Unter `flyer/` liegt ein druckfertiger A4-Flyer (PDF + 300-dpi-PNG) mit
Portrait, Kontaktdaten und QR-Code zur Website
`https://edda-die-doula.com/`. Neu erzeugen:

```bash
pip install pillow pymupdf qrcode
python3 flyer/generate_flyer.py
```

Der QR-Code (`flyer/qr-code.png`) wird dabei aus `SITE_URL` in
`flyer/generate_flyer.py` mit erzeugt – bei einem Domain- oder Adresswechsel
reichen also die Konstanten am Anfang des Skripts plus ein Neuaufruf.
