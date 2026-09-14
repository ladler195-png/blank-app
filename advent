import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. SEITEN-KONFIGURATION & SIDEBAR-NAVIGATION (DUNKELGRÜNES DESIGN)
# ==============================================================================
st.set_page_config(
    page_title="Nordpol-Expedition",
    page_icon="🎄",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0b1b10;
        color: #e2e8f0;
        font-family: 'Georgia', serif;
    }
    
    h1, h2, h3 {
        color: #d69e2e !important;
        font-family: 'Georgia', serif;
        font-weight: normal;
        letter-spacing: 1px;
    }

    div.stButton > button {
        background-color: #142e1d;
        color: #e2e8f0;
        border-radius: 6px;
        border: 1px solid #2d5a3a;
        font-weight: bold;
        width: 100%;
        padding: 8px;
        transition: all 0.2s ease;
    }
    
    div.stButton > button:hover {
        background-color: #b7791f;
        color: #ffffff;
        border-color: #d69e2e;
    }

    .stAlert {
        border-radius: 8px;
        background-color: rgba(20, 46, 29, 0.7);
        border: 1px solid #2d5a3a;
    }
    
    .puzzle-card {
        border: 1px dashed #d69e2e;
        padding: 10px;
        border-radius: 8px;
        background-color: rgba(214, 158, 46, 0.08);
        margin-top: 8px;
        font-size: 0.9em;
    }
    
    .morse-screen {
        background-color: #050d08;
        border: 2px solid #2d5a3a;
        border-radius: 6px;
        padding: 15px;
        font-family: monospace;
        font-size: 1.5em;
        color: #d69e2e;
        text-align: center;
        letter-spacing: 4px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

components.html("""
    <script src="https://unpkg.com/magic-snowflakes/dist/snowflakes.min.js"></script>
    <script>
        var snowflakes = new Snowflakes({
            color: '#ffffff',
            count: 15,
            minOpacity: 0.1,
            maxOpacity: 0.35
        });
    </script>
""", height=0)

# ==============================================================================
# 2. RÄTSEL-DATENBANK
# ==============================================================================
DOORS = {
    1: {
        "person": "Person A",
        "title": "Tag 1: Die mysteriöse Holzbox",
        "type": "lock_sliders",
        "story": "Es klingelt an der Haustür. Ihr öffnet, aber niemand ist da – stattdessen liegt auf der Fußmatte eine schwere, eisige Holzbox mit dem Absender „Nordpol“.",
        "question": "Knacke das 4-stellige Zahlenschloss mithilfe des Reims:\n> *„Vier kleine Ziffern im winterlichen Schnee... Zacken eines Weihnachtssterns plus Rentiere mal zwei.“*",
        "answer": [0, 0, 2, 6],
        "puzzle_piece": None,
        "hint": "Zähle die Zacken des Weihnachtssterns und addiere die Rentiere, dann multipliziere mit zwei."
    },
    2: {
        "person": "Person B",
        "title": "Tag 2: Das vergilbte Pergament",
        "type": "text",
        "story": "Das Schloss springt auf! Im Inneren liegt ein steif gefrorenes Pergament mit der verschlüsselten Nachricht: *„SIVX“*.",
        "question": "Entschlüssele das Codewort (jeder Buchstabe 4 Schritte im Alphabet nach links).",
        "answer": "NORD",
        "puzzle_piece": None,
        "hint": "Gehe im Alphabet jeden Buchstaben 4 Schritte zurück."
    },
    3: {
        "person": "Person C",
        "title": "Tag 3: Das Rentier-Experten-Rätsel",
        "type": "text",
        "story": "Der Elfen-Schlitten erwacht zum Leben! Doch das Armaturenbrett verlangt einen Zündcode.",
        "question": "Wie viele Buchstaben hat das englische Wort für die winterliche Rentier-Augenfarbe (blau = 4) multipliziert mit der Anzahl der Geweih-Geschlechter im Winter (2)?",
        "answer": "8",
        "puzzle_piece": None,
        "hint": "Blue = 4 Buchstaben. Beide Geschlechter tragen im Winter Geweih = 2. 4 * 2 = 8."
    },
    4: {
        "person": "Person A",
        "title": "Tag 4: Das Navigationssystem & die Koordinaten",
        "type": "text",
        "story": "Das Navigationssystem benötigt die exakten Kurs-Koordinaten.",
        "question": "Breitengrad: 90 Grad Nordpol minus 10. Längengrad: Quersumme des Jahres 2026 mal 10.",
        "answer": "80100",
        "puzzle_piece": None,
        "hint": "90-10 = 80. Quersumme von 2026 (2+0+2+6 = 10) * 10 = 100. Zusammen: 80100."
    },
    5: {
        "person": "Person B",
        "title": "Tag 5: Das Nebel-Tor & Fragment 1",
        "type": "text",
        "story": "Der Schlitten stoppt vor einer massiven Nebelwand aus blauem Eis.",
        "question": "Welchen Aggregatzustand nimmt Wasser bei klarem Frost an?",
        "answer": "EIS",
        "puzzle_piece": "🧩 Fragment 1: **E**",
        "hint": "Ein kurzes, dreibuchstabiges Wort."
    },
    6: {
        "person": "Person C",
        "title": "Tag 6: Das magische Sudoku-Gitter 🔢",
        "type": "sudoku_puzzle",
        "story": "Ihr findet ein magisches 3x3-Sudoku, bei dem Zeilen, Spalten und Diagonalen exakt 15 ergeben. Die Mitte ist 5.",
        "question": "Trage die fehlenden Zahlen in die leeren Felder ein (Zeile 1: 8, ?, 6 | Zeile 2: 3, 5, 7 | Zeile 3: 4, ?, 2). Welcher Wert fehlt oben in der Mitte?",
        "answer": "1",
        "puzzle_piece": "🧩 Fragment 2: **X**",
        "hint": "Die Summe jeder Zeile muss 15 ergeben (8 + ? + 6 = 15)."
    },
    7: {
        "person": "Person A",
        "title": "Tag 7: Das Logikgitter der Schlucht 🗺️",
        "type": "logic_grid",
        "story": "Vor der Eisspalte müsst ihr anhand von Hinweisen herausfinden, welcher Elf welchen Weg gewählt hat.",
        "question": "Hinweise:\n1. Der Elf mit dem Eispickel nahm den gefährlichsten Weg.\n2. Elf A nahm den Gletscher-Pfad.\n3. Elf B nahm den Schlucht-Pfad.\nWelchen Weg nahm folglich Elf C mit dem Eispickel?",
        "answer": "EISHÖHLEN-WEG",
        "puzzle_piece": "🧩 Fragment 3: **P**",
        "hint": "Schließe durch Ausschlussverfahren aus, welche Wege A und B belegt haben."
    },
    8: {
        "person": "Person B",
        "title": "Tag 8: Das interaktive Morse-Terminal 📻",
        "type": "morse_terminal",
        "story": "Ein Funksignal hallt durch die Nebelwände. Nutze das Morse-Terminal, um das universelle Notsignal **SOS** abzusetzen!",
        "question": "Klicke die Tasten in der korrekten Reihenfolge: Drei mal Kurz (•), drei mal Lang (-), drei mal Kurz (•).",
        "answer": "...---...",
        "puzzle_piece": "🧩 Fragment 4: **E**",
        "hint": "SOS = 3x Punkt, 3x Strich, 3x Punkt."
    },
    9: {
        "person": "Person C",
        "title": "Tag 9: Der Lichtstrahl-Spiegelpfad",
        "type": "mirror_puzzle",
        "story": "Ein Laserstrahl bricht durch den Nebel. Der Strahl kommt von Süden und muss nach Osten abgelenkt werden.",
        "question": "Bringe die Spiegel in die richtige Kombination, damit der Strahl von Süden nach Osten umgelenkt wird.",
        "answer": "NO",
        "puzzle_piece": "🧩 Fragment 5: **D**",
        "hint": "Ein schräger Spiegel '/' lenkt einen von unten kommenden Strahl nach rechts (Osten) ab."
    },
    10: {
        "person": "Person A",
        "title": "Tag 10: Das interaktive Transporträtsel 🐺🐐🥬",
        "type": "river_crossing",
        "story": "Du stehst am Gletscherfluss mit Wolf, Ziege und Kohl. Du darfst immer nur einen Passagier mitnehmen.",
        "question": "Bringe alle sicher auf die andere Seite, ohne dass Fressfeinde unbeaufsichtigt gelassen werden!",
        "answer": "COMPLETED",
        "puzzle_piece": "🧩 Fragment 6: **I**",
        "hint": "Nimm zuerst die Ziege rüber, fahre allein zurück, nimm den Wolf rüber..."
    },
    11: {
        "person": "Person B",
        "title": "Tag 11: Das Krypto-Zahlenschloss",
        "type": "text",
        "story": "Das Schloss vor dem Ausgang verlangt die Lösung eines Kombinatorik-Rätsels.",
        "question": "Wie viele verschiedene Möglichkeiten gibt es, 3 verschiedene Geschenke unter den Elfen aufzuteilen? (Fakultät von 3 = 3!)\n\n**Eingabe:** Zahl eingeben.",
        "answer": "6",
        "puzzle_piece": "🧩 Fragment 7: **T**",
        "hint": "3 * 2 * 1 = 6."
    },
    12: {
        "person": "Person C",
        "title": "Tag 12: Das geheime Lösungswort & Notiz 🧩",
        "type": "text",
        "story": "Ihr habt alle Fragmente von Tag 5 bis 11 gesammelt. Unten links auf jedem Fragment stand ein Buchstabe! (Zusatz-Notiz im System-Speicher: *'Override-Token für Notfälle entdeckt: OVERRIDE99!'*)",
        "question": "Setzt die gesammelten Buchstaben von Tag 5 bis 11 in der richtigen Reihenfolge zu einem 7-stelligen Lösungswort zusammen und tippt es ein.",
        "answer": "EXPEDIT",
        "puzzle_piece": "🏆 GEWONNEN: Das Tor zur Werkstatt ist geöffnet!",
        "hint": "Die Buchstaben aus den Fragmenten (Tag 5 bis 11) ergeben hintereinander gelesen ein Wort rund um unsere Reise."
    },
    13: {
        "person": "Chef-Elf Barnaby",
        "title": "Tag 13: Das synchrone Tri-Ventil-Netzwerk ⚙️",
        "type": "gear_puzzle",
        "story": "Ihr betretet die riesige, dampfgeschwängerte Hauptmachinerie der Fabrik. Ober-Elf Barnaby stürzt herbei, Schweißperlen auf der Stirn: *'Das Haupt-Dampfnetz ist auf drei voneinander abhängige Ventile aufgeteilt. Ein einfacher Multiplikator reicht hier nicht – wir haben ein restriktives Druck-Gleichungssystem! Das System bricht zusammen, wenn die Summe aller Ventile exakt 42 beträgt, Ventil B genau doppelt so stark geöffnet ist wie Ventil C, und das Produkt aus A und C genau 160 ergibt.'*",
        "question": "Löse das Gleichungssystem für die Ventile A, B und C:\n1. $A + B + C = 42$\n2. $B = 2C$\n3. $A \\times C = 160$",
        "answer": {"a": 10, "b": 20, "c": 16},
        "puzzle_piece": None,
        "hint": "Setze B = 2C in die erste Gleichung ein: A + 3C = 42. Da A = 160 / C ist..."
    },
    14: {
        "person": "Logistik-Leitstand R-04",
        "title": "Tag 14: Das Logistik-Constraint-Gitter der Rutschen 📦",
        "type": "package_sort",
        "story": "Die Förderbänder rotieren im Hyper-Modus. Um den Datenstau von Roboter R-04 zu beheben, verlangt das Terminal ein knallhartes Logikgitter. Vier Spezial-Pakete (Alpha, Beta, Gamma, Delta) müssen anhand von vier strikten Werkstatt-Regeln auf vier Express-Rutschen (1 bis 4) verteilt werden.",
        "question": "Axiome:\n1. Paket Alpha liegt auf einer ungeraden Rutsche, aber nicht auf Rutsche 1.\n2. Rutsche von Beta ist doppelt so hoch wie Gamma.\n3. Delta liegt auf einer höheren Rutsche als Beta.\n4. Gamma liegt auf Rutsche 1.\nWelche Rutsche gehört zu **Delta**?",
        "answer": "4",
        "puzzle_piece": None,
        "hint": "Gamma = 1 -> Beta = 2. Delta muss höher sein als 2 (also 3 oder 4). Da Alpha ungerade (nicht 1) ist, bleibt für Alpha nur 3. Also landet Delta auf 4."
    },
    15: {
        "person": "Chef-Elf Barnaby",
        "title": "Tag 15: Die magische Wunschzettel-Maschine 📜",
        "type": "text",
        "story": "Ihr erreicht den Zentralraum der Wunschzettelmaschine. Barnaby seufzt erleichtert: *'Hier werden alle Kinderwünsche verarbeitet, aber das Haupt-Datenband hängt fest! Wir müssen den Sortier-Code für den Stapel berechnen.'*\nDas Terminal zeigt: Ein Wunschzettel-Paket besteht aus Zetteln, die nach einer bestimmten Ziffernfolge sortiert werden müssen.",
        "question": "Analysiere die Code-Reihe der Wunschzettel-Maschine: 4, 9, 19, 39, 79, ?\nWelche Zahl bildet das nächste logische Glied dieser Reihe?",
        "answer": "159",
        "puzzle_piece": None,
        "hint": "Jedes Glied wird verdoppelt und 1 addiert: (4*2)+1=9, (9*2)+1=19, (19*2)+1=39, (39*2)+1=79, (79*2)+1=159."
    },
    16: {
        "person": "Chef-Elf Barnaby",
        "title": "Tag 16: Das binäre Logikgitter des Notfallkellers ⚡",
        "type": "binary_switches",
        "story": "Der Stromkreis im Keller ist mit einer Sicherheits-Schaltlogik abgesichert. Barnaby funkt: *'Wir müssen den Not-Trafo mit einer präzisen binären Last hochfahren!'*",
        "question": "Berechne die Zielzahl: Addition aus dem Wunschzettel-Ergebnis an zweiter Stelle (9) und der Anzahl der verbleibenden Tage bis Heiligabend (9), mal 3 minus 6 = **48**. Schalte die 6 Starkstrom-Relais (32, 16, 8, 4, 2, 1) für die Zahl 48.",
        "answer": [True, True, False, False, False, False],
        "puzzle_piece": None,
        "hint": "32 + 16 = 48. Aktiviere die entsprechenden Relais."
    },
    17: {
        "person": "Radio-Kontrolltisch",
        "title": "Tag 17: Die geheimnisvolle Signal-Frequenz 📻",
        "type": "frequency_tuner",
        "story": "Am alten Radio-Kontrolltisch des Funkraums blinkt eine Notwarnung. Die Polarlichter stören den Hauptkanal. Ein Post-it des diensthabenden Funk-Elfs klebt am Gehäuse: *'Die Ziel-Frequenz für den Notkanal entspricht genau der Summe der Betriebsstunden einer vollen Schicht (24) plus dem doppelten Wert des Wunschzettel-Startwerts (4), mal 3 minus 7!'*",
        "question": "Berechne den Frequenz-Wert ($((24 + (2 \\times 4)) \\times 3) - 7$) und stelle beide Reaktor-Regler (Alpha und Beta) auf diesen exakten MHz-Wert ein.",
        "answer": {"fa": 89.0, "fb": 89.0},
        "puzzle_piece": None,
        "hint": "(24 + 8) * 3 - 7 = 96 - 7 = 89 MHz. (Stelle den Regler auf 89.0 ein)."
    },
    18: {
        "person": "Hangar-Sicherheits-Schloss",
        "title": "Tag 18: Das Hangar-Zahlenwort-Rätsel 🔐",
        "type": "text",
        "story": "Das elektronische Master-Schloss des Hangars verlangt kein normales Passwort, sondern ein klassisches Zahlenwort-Rätsel aus den Werkstatt-Akten, um Diebe abzuhalten.",
        "question": "Das Rätsel lautet:\n> *„Ich bin eine zweistellige Zahl. Meine Zehnerziffer entspricht der halben Leistung des Ventil-Werts A (Tag 13: 10), und meine Einerziffer entspricht der Anzahl der Buchstaben im Wort NORDPOL (7).“*\nWie lautet der Code?",
        "answer": "57",
        "puzzle_piece": None,
        "hint": "Hälfte von 10 = 5. Anzahl der Buchstaben in NORDPOL = 7. Zusammengefügt: 57."
    },
    19: {
        "person": "Rentier-Planungsstation",
        "title": "Tag 19: Das Rentier-Aufstellungs-Raster (3 Reihen à 2 Plätze) 🦌",
        "type": "reindeer_puzzle",
        "story": "Barnaby steht vor der großen Rentier-Wandtafel. Das Raster ist nun in **3 Reihen mit jeweils 2 Plätzen** unterteilt. **Comet (☄️)** sitzt unumstößlich fest auf **Platz 1 (ganz oben links)**. Um den perfekten Flug zu garantieren, müssen die 5 übrigen Rentiere (Cupid, Dancer, Prancer, Blitz, Donner) nach strikten Regeln eingetragen werden:\n1. Prancer (⭐) muss direkt vor Dancer (💃) fliegen.\n2. Blitz (⚡) und Donner (🌩️) dürfen wegen statischer Entladung niemals in derselben Reihe (nebeneinander) stehen.",
        "question": "Wie viele mathematisch valide Aufstellungen der Rentiere auf den Plätzen 2 bis 6 erfüllen exakt diese Bedingungen?",
        "answer": "12",
        "puzzle_piece": None,
        "hint": "Analysiere die fixen Blöcke (Prancer vor Dancer) und schließe die verbotenen Quer-Nachbarn von Blitz und Donner aus."
    },
    20: {
        "person": "Person B",
        "title": "Tag 20: Die alchemistische Sternenstaub-Waage ⚖️",
        "type": "scale_puzzle",
        "story": "Mische das Spezialfutter auf der Balkenwaage für den langen Flug an.",
        "question": "Stelle die Regler für Hafer, Sternenstaub und Elfen-Essenz so ein, dass exakt 75 kg entstehen (Staub ist doppelt so schwer wie Hafer; Essenz ist 15 kg leichter als Staub).",
        "answer": {"hafer": 18, "staub": 36, "essenz": 21},
        "puzzle_piece": None,
        "hint": "x + 2x + (2x - 15) = 75 => x = 18 (Hafer), 36 (Staub), 21 (Essenz)."
    },
    21: {
        "person": "Flugleitstand-Terminal",
        "title": "Tag 21: Der effizienteste Routen-Algorithmus ✈️",
        "type": "text",
        "story": "Jetzt geht es um die finale Flug-Effizienz! Der Navigationscomputer der Rentiere berechnet die optimale Route über die Zeitzonen. Um den Treibstoff (Magie-Staub) zu sparen, muss die kürzeste Gesamtdistanz im Kurven-Graph ermittelt werden.",
        "question": "Ein Flugknoten hat 3 Stationen: Start (A) -> Zwischenstopp Nordpol (B) -> Ziel Grönland (C). Die Verbindung A->B kostet 120 Einheiten Magie, B->C kostet 150 Einheiten, und ein direkter Express-Modus A->C kostet 240 Einheiten. Wie hoch ist die Differenz (Ersparnis) zwischen der teuersten Route (A->B->C) und dem effizienten Express-Modus (A->C)?",
        "answer": "30",
        "puzzle_piece": None,
        "hint": "A->B->C = 120 + 150 = 270. Express A->C = 240. Differenz: 270 - 240 = 30."
    },
    22: {
        "person": "System-Administrator R-01",
        "title": "Tag 22: Das verdeckte Easter-Egg (System-Override) 🕵️‍♂️",
        "type": "text",
        "story": "Das Haupt-Terminal blockiert den Systemstart mit einer Firewall. Der Code, den ihr damals bei Tag 12 im System-Speicher entdeckt habt, wird jetzt als Master-Override verlangt!",
        "question": "Gib den bei Tag 12 gefundenen Override-Token ein.",
        "answer": "OVERRIDE99!",
        "puzzle_piece": None,
        "hint": "Erinnere dich an die Zusatz-Notiz im Speicher von Tag 12 (OVERRIDE99!)."
    },
    23: {
        "person": "Chef-Elf Barnaby",
        "title": "Tag 23: Das mechanische Zahnrad-Gleichgewicht ⚙️",
        "type": "gear_ratio_puzzle",
        "story": "Die Hauptschotten verriegeln sich durch ein mechanisches Vier-Zahnrad-System. Die Umdrehungen müssen exakt abgestimmt werden.",
        "question": "Stelle die Zahnrad-Übersetzung so ein, dass am Hauptausgang exakt 144 Umdrehungen pro Minute (RPM) ankommen (Eingabe-RPM = 36, Übersetzungsfaktor = ?).",
        "answer": "4",
        "puzzle_piece": None,
        "hint": "36 mal welcher Faktor ergibt 144? (144 / 36 = ?)"
    },
    24: {
        "person": "Turing-Master-KI",
        "title": "Tag 24: HEILIGABEND – Die Turing-Zustandsmaschine 💻",
        "type": "text",
        "story": "Der Start-Countdown läuft! Die finale Start-KI läuft auf einer virtuellen Turing-Maschine, deren Zustandsvektor vervollständigt werden muss.",
        "question": "Eine Turing-Maschine mit 2 Zuständen ($q_0, q_1$) verarbeitet das Band. Wenn der Startvektor $q_0$ bei Eingabe von 1 in Zustand $q_1$ übergeht und das Band invertiert (0), wie lautet die binäre Zustandssumme ($q_0 = 10, q_1 = 11$, multipliziert mit dem Faktor 4)?",
        "answer": "84",
        "puzzle_piece": "🏆 HARDCORE MEISTER-TITEL: SYSTEM OVERRIDE ERFOLGREICH!",
        "hint": "(10 + 11) * 4 = 21 * 4 = 84."
    }
}

# ==============================================================================
# 3. SESSION STATE INITIALISIERUNG
# ==============================================================================
if "solved_doors" not in st.session_state:
    st.session_state.solved_doors = []

if "mirror_state" not in st.session_state:
    st.session_state.mirror_state = ["\\", "/", "\\"]

if "morse_buffer" not in st.session_state:
    st.session_state.morse_buffer = ""

if "river" not in st.session_state:
    st.session_state.river = {
        "boat": "left",
        "wolf": "left",
        "goat": "left",
        "cabbage": "left"
    }

# ==============================================================================
# 4. SIDEBAR NAVIGATION (VARIANTE 2)
# ==============================================================================
st.sidebar.title("🎄 Nordpol-Expedition")
st.sidebar.caption("Variante 2: Sidebar-Navigation")

# Fortschrittsanzeige in der Sidebar
progress = len(st.session_state.solved_doors) / 24
st.sidebar.progress(progress)
st.sidebar.write(f"**Gelöste Türchen:** {len(st.session_state.solved_doors)} / 24")
st.sidebar.divider()

# Selectbox oder Radio für die Türchenauswahl in der Sidebar
day_options = [f"Tag {i} {'✅' if i in st.session_state.solved_doors else '🔒'}" for i in range(1, 25)]
selected_option = st.sidebar.selectbox("Wähle ein Türchen:", day_options)
day = int(selected_option.split(" ")[1])

st.sidebar.divider()
if st.sidebar.button("Fortschritt zurücksetzen 🔄"):
    st.session_state.solved_doors = []
    st.rerun()

# ==============================================================================
# 5. HAUPTSEITE & RÄTSEL-AUSFÜHRUNG
# ==============================================================================
show_sidebar_content = 5 <= day <= 12

if show_sidebar_content:
    main_col, puzzle_col = st.columns([2, 1])
else:
    main_col = st.container()

with main_col:
    door = DOORS[day]

    st.subheader(f"{door['title']}")
    st.caption(f"Verantwortlich: **{door['person']}**")
    
    st.info(f"📖 {door['story']}")
    st.markdown(f"**Aufgabe:** {door['question']}")

    # --- SONDER-WIDGETS ---
    if door["type"] == "sudoku_puzzle":
        s_input = st.text_input("Fehlende Zahl oben in der Mitte eintragen:", key="s_in")
        if st.button("Sudoku bestätigen 🔢", key=f"chk_{day}"):
            if s_input.strip() == "1":
                st.success("🎉 Richtig!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsch.")

    elif door["type"] == "logic_grid":
        ans_lg = st.text_input("Deine Lösung (Weg):", key="lg_input")
        if st.button("Logikgitter auswerten 🗺️", key=f"chk_{day}"):
            if ans_lg.strip().upper() in ["EISHÖHLEN-WEG", "EISHOHLEN-WEG", "EISHÖHLE"]:
                st.success("🎉 Richtig gelöst!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsch.")

    elif door["type"] == "morse_terminal":
        st.write("📻 **Interaktives Morse-Terminal:**")
        st.markdown(f"<div class='morse-screen'>{st.session_state.morse_buffer if st.session_state.morse_buffer else '--- SIGNAL BEREIT ---'}</div>", unsafe_allow_html=True)
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        if m_col1.button("• Kurz", key="morse_dot"):
            st.session_state.morse_buffer += "."
            st.rerun()
        if m_col2.button("- Lang", key="morse_dash"):
            st.session_state.morse_buffer += "-"
            st.rerun()
        if m_col3.button("Löschen ⌫", key="morse_clear"):
            st.session_state.morse_buffer = ""
            st.rerun()
        if m_col4.button("Signal senden 📡", key=f"chk_{day}"):
            if st.session_state.morse_buffer == "...---...":
                st.success("🎉 SOS-Signal erfolgreich!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsches Signal.")

    elif door["type"] == "river_crossing":
        st.write("🐺🐐🥬 **Fluss-Transport-Steuerung:**")
        r = st.session_state.river
        st.write(f"📍 **Linkes Ufer:** {[k for k, v in r.items() if v == 'left' and k != 'boat']}")
        st.write(f"🛶 **Boot Position:** Ufer {r['boat'].upper()}")
        st.write(f"📍 **Rechtes Ufer:** {[k for k, v in r.items() if v == 'right' and k != 'boat']}")
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            item_to_move = st.selectbox("Passagier mitnehmen:", ["Niemand (leer fahren)", "wolf", "goat", "cabbage"], key="river_item")
        with col_act2:
            if st.button("Ufer wechseln 🛶", key="river_move"):
                target = "right" if r["boat"] == "left" else "left"
                r["boat"] = target
                if item_to_move != "Niemand (leer fahren)":
                    r[item_to_move] = target
                if r["wolf"] == r["goat"] and r["boat"] != r["wolf"]:
                    st.error("💀 Der Wolf hat die Ziege gefressen! Zurückgesetzt.")
                    st.session_state.river = {"boat": "left", "wolf": "left", "goat": "left", "cabbage": "left"}
                elif r["goat"] == r["cabbage"] and r["boat"] != r["goat"]:
                    st.error("💀 Die Ziege hat den Kohlkopf gefressen! Zurückgesetzt.")
                    st.session_state.river = {"boat": "left", "wolf": "left", "goat": "left", "cabbage": "left"}
                st.rerun()
        if st.button("Zurücksetzen 🔄", key="river_reset"):
            st.session_state.river = {"boat": "left", "wolf": "left", "goat": "left", "cabbage": "left"}
            st.rerun()
        if r["wolf"] == "right" and r["goat"] == "right" and r["cabbage"] == "right":
            st.success("🎉 Alle sicher drüben!")
            if day not in st.session_state.solved_doors:
                st.session_state.solved_doors.append(day)
                st.rerun()

    elif door["type"] == "mirror_puzzle":
        st.write("🔦 **Laser-Spiegel-Ausrichtung:**")
        m_col1, m_col2, m_col3 = st.columns(3)
        if m_col1.button(f"Spiegel A: [ {st.session_state.mirror_state[0]} ]", key="m1"):
            st.session_state.mirror_state[0] = "/" if st.session_state.mirror_state[0] == "\\" else "\\"
            st.rerun()
        if m_col2.button(f"Spiegel B: [ {st.session_state.mirror_state[1]} ]", key="m2"):
            st.session_state.mirror_state[1] = "/" if st.session_state.mirror_state[1] == "\\" else "\\"
            st.rerun()
        if m_col3.button(f"Spiegel C: [ {st.session_state.mirror_state[2]} ]", key="m3"):
            st.session_state.mirror_state[2] = "/" if st.session_state.mirror_state[2] == "\\" else "\\"
            st.rerun()
        if st.session_state.mirror_state == ["/", "\\", "/"]:
            st.success("🟢 Korrekt!")
            if st.button("Aktivieren 🔦", key=f"chk_{day}"):
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()

    elif door["type"] == "gear_puzzle":
        st.write("⚙️ **Tri-Ventil-Konsolen:** Stelle die drei Ventile A, B und C exakt ein.")
        va = st.slider("Ventil A", 1, 30, 10, key="va_s")
        vb = st.slider("Ventil B", 1, 30, 10, key="vb_s")
        vc = st.slider("Ventil C", 1, 30, 10, key="vc_s")
        
        st.markdown(f"**Aktueller Status:** A = {va}, B = {vb}, C = {vc}")
        st.write(f"• Summe (A+B+C) = {va+vb+vc} (Ziel: 42)")
        st.write(f"• Verhältnis (B - 2C) = {vb - 2*vc} (Ziel: 0)")
        st.write(f"• Produkt (A × C) = {va*vc} (Ziel: 160)")
        
        if st.button("Ventil-System kalibrieren ⚙️", key=f"chk_{day}"):
            if va == 10 and vb == 20 and vc == 16:
                st.success("🎉 Hervorragend! Das Gleichungssystem ist perfekt gelöst.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Die Bedingungen des Gleichungssystems sind noch nicht erfüllt.")

    elif door["type"] == "package_sort":
        st.write("📦 **Intelligentes Paket-Leitsystem:**")
        st.markdown("Basierend auf den Logik-Axiomen: Welche Rutsche (1 bis 4) gehört zu Paket **Delta**?")
        ans_delta = st.text_input("Rutschen-Nummer für Paket Delta eingeben:", key="delta_input")
        if st.button("Logik-Prüfung ausführen 📦", key=f"chk_{day}"):
            if ans_delta.strip() == "4":
                st.success("🎉 Richtig kombiniert!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsche Zuordnung.")

    elif door["type"] == "binary_switches":
        st.write("⚡ **Notfall-Keller SPS-Schaltpult (Zielzahl: 48):**")
        b1, b2, b3, b4, b5, b6 = st.columns(6)
        s1 = b1.checkbox("32", key="cb1")
        s2 = b2.checkbox("16", key="cb2")
        s3 = b3.checkbox("8", key="cb3")
        s4 = b4.checkbox("4", key="cb4")
        s5 = b5.checkbox("2", key="cb5")
        s6 = b6.checkbox("1", key="cb6")
        
        curr_val = (32 if s1 else 0) + (16 if s2 else 0) + (8 if s3 else 0) + (4 if s4 else 0) + (2 if s5 else 0) + (1 if s6 else 0)
        st.metric("Aktueller Relais-Wert", f"{curr_val}", delta=f"Ziel: 48")
        
        if st.button("SPS-Schaltkreis zünden ⚡", key=f"chk_{day}"):
            if curr_val == 48:
                st.success("🎉 Relais-Konfiguration exakt bestätigt!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error(f"❌ Wert inkorrekt ({curr_val}). Benötigt: 48.")

    elif door["type"] == "frequency_tuner":
        st.write("📻 **Radio-Notkanal Resonanz-Tuner:**")
        fa = st.slider("Frequenz-Regler (MHz)", 50.0, 150.0, 70.0, step=0.5, key="fa_slide")
        st.markdown(f"**Aktuell eingestellt:** `{fa} MHz`")
        
        if st.button("Frequenz synchronisieren 📡", key=f"chk_{day}"):
            if abs(fa - 89.0) < 0.1:
                st.success("🎉 Resonanzpunkt perfekt getroffen! Der Notkanal steht klar im Äther.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Das Signal ist noch verrauscht. Überprüfe die Rechnungsformel im Text.")

    elif door["type"] == "scale_puzzle":
        st.write("⚖️ **Alchemistische Präzisionswaage (Ziel: 75 kg):**")
        w_hafer = st.slider("Hafer (kg)", 0, 50, 10, key="wh")
        w_staub = st.slider("Sternenstaub (kg)", 0, 50, 10, key="ws")
        w_essenz = st.slider("Elfen-Essenz (kg)", 0, 50, 10, key="we")
        
        total_w = w_hafer + w_staub + w_essenz
        st.metric("Gesamtgewicht", f"{total_w} kg", delta=f"Ziel: 75 kg")
        
        if st.button("Waage arretieren ⚖️", key=f"chk_{day}"):
            if w_hafer == 18 and w_staub == 36 and w_essenz == 21:
                st.success("🎉 Algebraisch exaktes Mischungsverhältnis!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Die Mischungsbedingungen sind nicht erfüllt.")

    elif door["type"] == "gear_ratio_puzzle":
        st.write("⚙️ **Zahnrad-Übersetzungs-Konsole:**")
        factor = st.slider("Wähle den Übersetzungsfaktor", 1, 10, 1, key="gear_factor")
        output_rpm = 36 * factor
        st.metric("Ausgangs-Umdrehungen (RPM)", f"{output_rpm}", delta="Ziel: 144 RPM")
        if st.button("Zahnrad-System einkuppeln ⚙️", key=f"chk_{day}"):
            if output_rpm == 144:
                st.success("🎉 Perfekt! Das Zahnrad-System läuft exakt mit 144 RPM.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error(f"❌ Aktuell {output_rpm} RPM. Benötigt werden exakt 144 RPM.")

    elif door["type"] == "lock_sliders":
        c1, c2, c3, c4 = st.columns(4)
        v1 = c1.number_input("Stelle 1", 0, 9, 0, key=f"n1_{day}")
        v2 = c2.number_input("Stelle 2", 0, 9, 0, key=f"n2_{day}")
        v3 = c3.number_input("Stelle 3", 0, 9, 0, key=f"n3_{day}")
        v4 = c4.number_input("Stelle 4", 0, 9, 0, key=f"n4_{day}")
        if st.button("Schloss prüfen 🗝️", key=f"chk_{day}"):
            if [int(v1), int(v2), int(v3), int(v4)] == door["answer"]:
                st.success("🎉 Schloss geöffnet!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsch.")

    else:
        if door["type"] not in ["sudoku_puzzle", "logic_grid", "morse_terminal", "river_crossing", "mirror_puzzle", "gear_puzzle", "package_sort", "binary_switches", "frequency_tuner", "scale_puzzle", "lock_sliders", "reindeer_puzzle", "gear_ratio_puzzle"]:
            ans = st.text_input("Deine Lösung:", key=f"input_{day}")
            if st.button("Prüfen 🔍", key=f"chk_{day}"):
                user_clean = ans.strip().replace(" ", "").upper()
                target_clean = str(door["answer"]).strip().replace(" ", "").upper()
                if user_clean == target_clean:
                    st.success("🎉 Richtig gelöst!")
                    if day not in st.session_state.solved_doors:
                        st.session_state.solved_doors.append(day)
                        if day == 24:
                            st.balloons()
                        st.rerun()
                else:
                    st.error("❌ Leider nicht korrekt.")

    with st.expander("💡 Hinweis anzeigen"):
        st.write(door["hint"])

# ==============================================================================
# FRAGMENT-ANZEIGE IN DER SEITENLEISTE (FÜR TAG 5 BIS 12)
# ==============================================================================
if show_sidebar_content:
    with puzzle_col:
        st.subheader("🌀 Puzzleteil-Fragmente")
        st.caption("Sammle hier die Buchstaben (Tag 5 bis 12):")
        
        lab_pieces = [d for d in st.session_state.solved_doors if 5 <= d <= 12 and DOORS[d]["puzzle_piece"]]
        
        if not lab_pieces:
            st.write("*Noch keine Fragmente gesammelt.*")
        else:
            for d in sorted(lab_pieces):
                st.markdown(f"<div class='puzzle-card'><b>Tag {d}:</b><br>{DOORS[d]['puzzle_piece']}</div>", unsafe_allow_html=True)
                
        st.write("---")
        st.metric("Gefundene Fragmente", f"{len(lab_pieces)} / 8")
