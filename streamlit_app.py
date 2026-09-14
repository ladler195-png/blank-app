import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. SEITEN-KONFIGURATION & DUNKELGRÜNES DESIGN (CSS)
# ==============================================================================
st.set_page_config(
    page_title="Weihnachtlicher Rätsel-Adventskalender",
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
# 2. RÄTSEL-DATENBANK (AKT 1 BIS 4 - VOLLSTÄNDIG ÜBERARBEITET)
# ==============================================================================
DOORS = {
    # AKT 1: ZUHAUSE & AUFTAKT (1-4)
    1: {
        "title": "Tag 1: Die mysteriöse Holzbox",
        "type": "text",
        "story": "Es klingelt an der Haustür. Ihr öffnet, aber niemand ist da – stattdessen liegt auf der Fußmatte eine schwere, eisige Holzbox. Auf dem Absender steht Nordpol.",
        "question": "Ihr untersucht die Box und findet an der Seite einen Code, ein Gedicht und dann die Aufgabe:\n> *„Vier kleine Ziffern im winterlichen Schnee... Zacken eines Weihnachtssterns plus Rentiere mal zwei.“*\n\nWie lautet der 4-stellige Zahlencode?",
        "answer": "0026",
        "puzzle_piece": None,
        "hint": "Zähle die Zacken eines klassischen Weihnachtssterns und addiere die Rentiere (inkl. Rudolf), dann multipliziere mit zwei."
    },
    2: {
        "title": "Tag 2: Das vergilbte Pergament",
        "type": "text",
        "story": "Das Schloss springt auf! Im Inneren liegt ein steif gefrorenes Pergament mit der verschlüsselten Nachricht: *„SIVX“*.",
        "question": "Entschlüssele das Codewort (jeder Buchstabe exakt 4 Schritte im Alphabet nach links).",
        "answer": "NORD",
        "puzzle_piece": None,
        "hint": "Gehe im Alphabet jeden Buchstaben 4 Schritte zurück."
    },
    3: {
        "title": "Tag 3: Das Rentier-Experten-Rätsel",
        "type": "text",
        "story": "Der Elfen-Schlitten erwacht zum Leben! Doch das Armaturenbrett verlangt einen Zündcode.",
        "question": "Wie viele Buchstaben hat das englische Wort für die winterliche Rentier-Augenfarbe (blau = 4) multipliziert mit der Anzahl der Geweih-Geschlechter im Winter (2)?",
        "answer": "8",
        "puzzle_piece": None,
        "hint": "Blue = 4 Buchstaben. Beide Geschlechter tragen im Winter Geweih = 2. 4 * 2 = 8."
    },
    4: {
        "title": "Tag 4: Das Navigationssystem & die Koordinaten",
        "type": "text",
        "story": "Das Navigationssystem benötigt die exakten Kurs-Koordinaten.",
        "question": "Breitengrad: 90 Grad Nordpol minus 10. Längengrad: Quersumme des Jahres 2026 mal 10.",
        "answer": "80100",
        "puzzle_piece": None,
        "hint": "90-10 = 80. Quersumme von 2026 (2+0+2+6 = 10) * 10 = 100. Zusammen: 80100."
    },
    
    # AKT 2: DAS LABYRINTH (5-12)
    5: {
        "title": "Tag 5: Das Nebel-Tor & Fragment 1",
        "type": "text",
        "story": "Der Schlitten stoppt vor einer massiven Nebelwand aus blauem Eis.",
        "question": "Welchen Aggregatzustand nimmt Wasser bei klarem Frost an?",
        "answer": "EIS",
        "puzzle_piece": "🧩 Fragment 1: **E**",
        "hint": "Ein kurzes, dreibuchstabiges Wort."
    },
    6: {
        "title": "Tag 6: Das magische Sudoku-Gitter 🔢",
        "type": "sudoku_puzzle",
        "story": "Ihr findet ein magisches 3x3-Sudoku-Inkassofeld, bei dem jede Zeile, Spalte und Diagonale exakt dieselle Summe ergeben muss. Nutze das interaktive Gitter unten.",
        "question": "Fülle die Felder so aus, dass das Sudoku mathematisch aufgeht.",
        "answer": "VALID",
        "puzzle_piece": "🧩 Fragment 2: **X**",
        "hint": "Magische Summe ist 15. Die Mitte ist festgesetzt auf 5."
    },
    7: {
        "title": "Tag 7: Das Logikgitter der Schlucht 🗺️",
        "type": "logic_grid",
        "story": "Vor der Eisspalte müsst ihr anhand von Hinweisen herausfinden, welcher Elf welchen Weg gewählt hat. Die Hinweise sind komplexer als gedacht: Drei Elfen (A, B, C) und drei Werkzeuge (Eispickel, Seil, Laterne) auf drei Wegen (Gletscher-Pfad, Schlucht-Pfad, Eishöhlen-Weg).",
        "question": "Hinweise:\n1. Der Elf mit dem Eispickel nahm weder den Gletscher- noch den Schlucht-Pfad.\n2. Elf A nahm den Gletscher-Pfad.\n3. Elf B hatte kein Seil.\nWelchen Weg nahm folglich Elf C, der den Eispickel trug?",
        "answer": "EISHÖHLEN-WEG",
        "puzzle_piece": "🧩 Fragment 3: **P**",
        "hint": "Schließe über Ausschlussverfahren aus, welche Wege belegt sind."
    },
    8: {
        "title": "Tag 8: Das interaktive Morse-Terminal 📻",
        "type": "morse_terminal",
        "story": "Ein Funksignal hallt durch die Nebelwände. Nutze das Morse-Terminal, um das universelle Notsignal **SOS** abzusetzen!",
        "question": "Klicke die Tasten in der korrekten Reihenfolge: Drei mal Kurz (•), drei mal Lang (-), drei mal Kurz (•).",
        "answer": "...---...",
        "puzzle_piece": "🧩 Fragment 4: **E**",
        "hint": "SOS = 3x Punkt, 3x Strich, 3x Punkt."
    },
    9: {
        "title": "Tag 9: Der Lichtstrahl-Spiegelpfad",
        "type": "mirror_puzzle",
        "story": "Ein Laserstrahl bricht durch den Nebel. Der Strahl kommt von Süden und muss nach Osten abgelenkt werden.",
        "question": "Bringe die drei Spiegel in die richtige Kombination, damit der Strahl umgelenkt wird.",
        "answer": "NO",
        "puzzle_piece": "🧩 Fragment 5: **D**",
        "hint": "Ein schräger Spiegel '/' lenkt einen von unten kommenden Strahl nach rechts ab."
    },
    10: {
        "title": "Tag 10: Das interaktive Transporträtsel (Wolf, Ziege, Kohl) 🐺🐐🥬",
        "type": "river_crossing",
        "story": "Du stehst am Gletscherfluss mit Wolf, Ziege und Kohl. Du darfst im Boot immer nur einen Passagier mitnehmen.",
        "question": "Bringe alle sicher auf die andere Seite, ohne dass Fressfeinde unbeaufsichtigt gelassen werden!",
        "answer": "COMPLETED",
        "puzzle_piece": "🧩 Fragment 6: **I**",
        "hint": "Nimm zuerst die Ziege rüber, fahre allein zurück, nimm den Wolf rüber..."
    },
    11: {
        "title": "Tag 11: Das Krypto-Zahlenschloss",
        "type": "text",
        "story": "Das Schloss vor dem Ausgang verlangt die Lösung eines Kombinatorik-Rätsels.",
        "question": "Wie viele verschiedene Möglichkeiten gibt es, 3 verschiedene Geschenke unter den Elfen aufzuteilen? (Fakultät von 3 = 3!)\n\n**Eingabe:** Zahl eingeben.",
        "answer": "6",
        "puzzle_piece": "🧩 Fragment 7: **T**",
        "hint": "3 * 2 * 1 = 6."
    },
    12: {
        "title": "Tag 12: Das geheime Lösungswort & Notiz 🧩",
        "type": "text",
        "story": "Ihr habt alle Fragmente von Tag 5 bis 11 gesammelt. Auf jedem Fragment stand ein Buchstabe! Zudem gab es einen System-Override-Token für Notfälle im Speicher: `OVERRIDE99!`",
        "question": "Setzt die gesammelten Buchstaben von Tag 5 bis 11 in der richtigen Reihenfolge zu einem 7-stelligen Lösungswort zusammen und tippt es ein.",
        "answer": "EXPEDIT",
        "puzzle_piece": "🏆 GEWONNEN: Das Tor zur Werkstatt ist geöffnet!",
        "hint": "Die Buchstaben aus den Fragmenten (Tag 5 bis 11) ergeben hintereinander gelesen ein passendes Wort."
    },
    
    # AKT 3: DIE WERKSTATT-RETTUNG (13-21)
    13: {
        "title": "Tag 13: Das synchrone Tri-Ventil-Netzwerk ⚙️",
        "type": "gear_puzzle",
        "story": "Ihr betretet die riesige Hauptmaschinerie. Das Haupt-Dampfnetz ist auf drei voneinander abhängige Ventile aufgeteilt. Ein restriktives Druck-Gleichungssystem muss gelöst werden.",
        "question": "Löse das Gleichungssystem für die Ventile A, B und C:\n1. A + B + C = 42\n2. B = 2C\n3. A × C = 160",
        "answer": {"a": 10, "b": 20, "c": 16},
        "puzzle_piece": None,
        "hint": "Setze B = 2C in die erste Gleichung ein..."
    },
    14: {
        "title": "Tag 14: Das interaktive Logistik-Constraint-Gitter der Rutschen 📦",
        "type": "package_sort",
        "story": "Die Förderbänder rotieren im Hyper-Modus. Vier Spezial-Pakete (Alpha, Beta, Gamma, Delta) müssen interaktiv per Schieberegler auf vier Express-Rutschen (1 bis 4) verteilt werden, entsprechend strenger Werkstatt-Regeln.",
        "question": "Axiome:\n1. Paket Alpha liegt auf einer ungeraden Rutsche, aber nicht auf Rutsche 1.\n2. Rutsche von Beta ist doppelt so hoch wie Gamma.\n3. Delta liegt auf einer höheren Rutsche als Beta.\n4. Gamma liegt auf Rutsche 1.",
        "answer": {"alpha": 3, "beta": 2, "gamma": 1, "delta": 4},
        "puzzle_piece": None,
        "hint": "Gamma = 1 -> Beta = 2 -> Delta = 4 -> Alpha = 3."
    },
    15: {
        "title": "Tag 15: Die interaktive Wunschzettel-Maschine 📜",
        "type": "wish_machine",
        "story": "Hier werden alle Kinderwünsche verarbeitet. Das Haupt-Datenband hängt fest und erfordert das Berechnen und Eintippen des nächsten Reihen-Glieds.",
        "question": "Analysiere die Code-Reihe der Wunschzettel-Maschine: 4, 9, 19, 39, 79, ?\nErmittle das nächste logische Glied über das interaktive Steuerpult.",
        "answer": "159",
        "puzzle_piece": None,
        "hint": "Jedes Glied wird verdoppelt und 1 addiert."
    },
    16: {
        "title": "Tag 16: Das binäre Logikgitter des Notfallkellers ⚡",
        "type": "binary_switches",
        "story": "Der Stromkreis im Keller ist mit einer Sicherheits-Schaltlogik abgesichert. Der Not-Trafo muss mit einer präzisen binären Last hochfahren.",
        "question": "Berechne die Zielzahl: Addition aus dem Wunschzettel-Ergebnis an zweiter Stelle (9) und der Anzahl der verbleibenden Tage bis Heiligabend (9), mal 3 minus 6 = **48**. Aktiviere die passenden Relais.",
        "answer": [True, True, False, False, False, False],
        "puzzle_piece": None,
        "hint": "32 + 16 = 48."
    },
    17: {
        "title": "Tag 17: Die interaktive Signal-Frequenz 📻",
        "type": "frequency_tuner",
        "story": "Am alten Radio-Kontrolltisch blinkt eine Notwarnung. Die Polarlichter stören den Hauptkanal. Stelle die Frequenz über den interaktiven Regler ein.",
        "question": "Berechne den Frequenz-Wert ($((24 + (2 \\times 4)) \\times 3) - 7$) und stelle den Regler auf diesen exakten MHz-Wert ein.",
        "answer": 89.0,
        "puzzle_piece": None,
        "hint": "(24 + 8) * 3 - 7 = 96 - 7 = 89 MHz."
    },
    18: {
        "title": "Tag 18: Das interaktive Hangar-Zahlenwort-Rätsel 🔐",
        "type": "hangar_puzzle",
        "story": "Das elektronische Master-Schloss des Hangars verlangt ein klassisches Zahlenwort-Rätsel, gesteuert über digitale Ziffern-Wahlräder.",
        "question": "Rätsel:\n> *„Ich bin eine zweistellige Zahl. Meine Zehnerziffer entspricht der halben Leistung des Ventil-Werts A (Tag 13: 10), und meine Einerziffer entspricht der Anzahl der Buchstaben im Wort NORDPOL (7).“*\nStelle den Code am Schloss ein.",
        "answer": 57,
        "puzzle_piece": None,
        "hint": "Hälfte von 10 = 5. Buchstaben in NORDPOL = 7. Ergibt 57."
    },
    19: {
        "title": "Tag 19: Das Rentier-Aufstellungs-Raster (3 Reihen à 2 Plätze) 🦌",
        "type": "reindeer_puzzle",
        "story": "Das Raster ist in 3 Reihen mit jeweils 2 Plätzen unterteilt, und Comet sitzt fest auf Platz 1.",
        "question": "Wie viele mathematisch valide Aufstellungen der Rentiere auf den Plätzen 2 bis 6 erfüllen exakt die Bedingungen?",
        "answer": "12",
        "puzzle_piece": None,
        "hint": "Analysiere die fixen Blöcke und schließe verbotene Nachbarn aus."
    },
    20: {
        "title": "Tag 20: Die alchemistische Sternenstaub-Waage ⚖️",
        "type": "scale_puzzle",
        "story": "Mische das Spezialfutter auf der Balkenwaage für den langen Flug an.",
        "question": "Stelle die Regler für Hafer, Sternenstaub und Elfen-Essenz so ein, dass exakt 75 kg entstehen.\n\nStaub ist doppelt so schwer wie Hafer\nEssenz ist 15 kg leichter als Staub",
        "answer": {"hafer": 18, "staub": 36, "essenz": 21},
        "puzzle_piece": None,
        "hint": "x + 2x + (2x - 15) = 75 => x = 18."
    },
    21: {
        "title": "Tag 21: Der interaktive Routen-Algorithmus ✈️",
        "type": "route_planner",
        "story": "Jetzt geht es um die finale Flug-Effizienz! Der Navigationscomputer der Rentiere berechnet die optimale Route über die Zeitzonen. Nutze den interaktiven Routenplaner.",
        "question": "Ermittle die Differenz (Ersparnis) zwischen der teuersten Route (A->B->C = 270) und dem effizienten Express-Modus (A->C = 240).",
        "answer": 30,
        "puzzle_piece": None,
        "hint": "270 - 240 = 30."
    },
    
    # AKT 4: DAS HARDCORE-FINALE (22-24)
    22: {
        "title": "Tag 22: Das verdeckte Easter-Egg (System-Override) 🕵️‍♂️",
        "type": "text",
        "story": "Das Haupt-Terminal blockiert den Start mit einer Firewall. Der Code von Tag 12 wird verlangt.",
        "question": "Gib den bei Tag 12 gefundenen Override-Token ein.",
        "answer": "OVERRIDE99!",
        "puzzle_piece": None,
        "hint": "Erinnere dich an die Zusatz-Notiz im Speicher von Tag 12."
    },
    23: {
        "title": "Tag 23: Das mechanische Zahnrad-Gleichgewicht ⚙️",
        "type": "gear_ratio_puzzle",
        "story": "Die Hauptschotten verriegeln sich durch ein Vier-Zahnrad-System.",
        "question": "Stelle die Zahnrad-Übersetzung so ein, dass am Hauptausgang exakt 144 Umdrehungen pro Minute (RPM) ankommen (Eingabe = 36).",
        "answer": 4,
        "puzzle_piece": None,
        "hint": "144 / 36 = 4."
    },
    24: {
        "title": "Tag 24: HEILIGABEND – Die Turing-Zustandsmaschine 💻",
        "type": "text",
        "story": "Der Start-Countdown läuft! Die finale Start-KI läuft auf einer virtuellen Turing-Maschine.",
        "question": "Zustandsvektor: $q_0 = 10, q_1 = 11$, multipliziert mit dem Faktor 4. Wie lautet das Ergebnis?",
        "answer": "84",
        "puzzle_piece": "🏆 HARDCORE MEISTER-TITEL: SYSTEM OVERRIDE ERFOLGREICH!",
        "hint": "(10 + 11) * 4 = 84."
    }
}

# ==============================================================================
# 3. SESSION STATE INITIALISIERUNG
# ==============================================================================
if "solved_doors" not in st.session_state:
    st.session_state.solved_doors = []

if "active_day" not in st.session_state:
    st.session_state.active_day = 1

if "mirror_state" not in st.session_state:
    st.session_state.mirror_state = ["\\", "/", "\\"]

if "morse_buffer" not in st.session_state:
    st.session_state.morse_buffer = ""

if "river" not in st.session_state:
    st.session_state.river = {
        "boat": "left",
        "wolf": "left",
        "ziege": "left",
        "kohl": "left"
    }

# ==============================================================================
# 4. KOPFZEILE & FORTSCHRITT
# ==============================================================================
st.title("🎄 Weihnachtlicher Rätsel-Adventskalender")
st.caption("Das mathematisch-logische Advents-Abenteuer mit System-Override")

col_prog, col_stats = st.columns([3, 1])
with col_prog:
    progress = len(st.session_state.solved_doors) / 24
    st.progress(progress)
with col_stats:
    st.write(f"**Gelöste Türchen:** {len(st.session_state.solved_doors)} / 24")

st.divider()

# ==============================================================================
# 5. TÜRCHEN-GRID
# ==============================================================================
cols = st.columns(6)
for i in range(1, 25):
    col = cols[(i - 1) % 6]
    
    if i <= 4:
        prefix = "📦 "
    elif 5 <= i <= 12:
        prefix = "🌀 "
    elif 13 <= i <= 21:
        prefix = "⚙️ "
    else:
        prefix = "🔥 "
        
    label = f"✅ {prefix}Tag {i}" if i in st.session_state.solved_doors else f"{prefix}Tag {i}"
        
    if col.button(label, key=f"btn_{i}"):
        st.session_state.active_day = i

st.divider()

# ==============================================================================
# 6. RÄTSEL-FLÄCHE & DYNAMISCHES LAYOUT
# ==============================================================================
show_sidebar = 5 <= st.session_state.active_day <= 12

if show_sidebar:
    main_col, puzzle_col = st.columns([2, 1])
else:
    main_col = st.container()

with main_col:
    day = st.session_state.active_day
    door = DOORS[day]

    st.subheader(door['title'])
    st.info(f"📖 {door['story']}")
    st.markdown(f"**Aufgabe:** {door['question']}")

    # Standard-Text-Eingabe
    if door["type"] == "text":
        ans = st.text_input("Deine Lösung:", key=f"txt_{day}")
        if st.button("Antwort einreichen 🚀", key=f"chk_{day}"):
            if ans.strip().upper() == str(door["answer"]).upper():
                st.success("🎉 Richtig gelöst!")
                if door["puzzle_piece"]:
                    st.markdown(f"<div class='puzzle-card'>{door['puzzle_piece']}</div>", unsafe_allow_html=True)
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Das ist leider nicht korrekt.")

    # TAG 6: SUDOKU (INTERAKTIV)
    elif door["type"] == "sudoku_puzzle":
        st.write("🔢 **Interaktives 3x3 Magisches Quadrat (Sudoku):**")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            f1 = st.text_input("Zeile 1, Spalte 1 (Wert: 8)", value="8", disabled=True)
            f4 = st.text_input("Zeile 2, Spalte 1 (Wert: 3)", value="3", disabled=True)
            f7 = st.text_input("Zeile 3, Spalte 1 (Wert: 4)", value="4", disabled=True)
        with sc2:
            f2 = st.text_input("Z1, S2 (Fehlt)", key="sud_f2")
            f5 = st.text_input("Z2, S2 (Mitte: 5)", value="5", disabled=True)
            f8 = st.text_input("Z3, S2 (Fehlt)", key="sud_f8")
        with sc3:
            f3 = st.text_input("Zeile 1, Spalte 3 (Wert: 6)", value="6", disabled=True)
            f6 = st.text_input("Zeile 2, Spalte 3 (Wert: 7)", value="7", disabled=True)
            f9 = st.text_input("Zeile 3, Spalte 3 (Wert: 2)", value="2", disabled=True)
            
        if st.button("Sudoku prüfen 🔢", key=f"chk_{day}"):
            if f2.strip() == "1" and f8.strip() == "9":
                st.success("🎉 Hervorragend! Jede Zeile, Spalte und Diagonale ergibt exakt 15.")
                st.markdown(f"<div class='puzzle-card'>{door['puzzle_piece']}</div>", unsafe_allow_html=True)
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Die Zahlenwerte sind noch nicht korrekt platziert.")

    # TAG 7: LOGIKGITTER
    elif door["type"] == "logic_grid":
        ans_lg = st.text_input("Deine Lösung (Name des Weges):", key="lg_input")
        if st.button("Logikgitter auswerten 🗺️", key=f"chk_{day}"):
            if ans_lg.strip().upper() in ["EISHÖHLEN-WEG", "EISHOHLEN-WEG", "EISHÖHLE"]:
                st.success("🎉 Richtig gelöst!")
                st.markdown(f"<div class='puzzle-card'>{door['puzzle_piece']}</div>", unsafe_allow_html=True)
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsch.")

    # TAG 8: MORSE-TERMINAL
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
                st.markdown(f"<div class='puzzle-card'>{door['puzzle_piece']}</div>", unsafe_allow_html=True)
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsches Signal.")

    # TAG 9: SPIEGEL-RÄTSEL
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
            st.success("🟢 Korrekt ausgerichtet!")
            st.markdown(f"<div class='puzzle-card'>{door['puzzle_piece']}</div>", unsafe_allow_html=True)
            if st.button("Aktivieren 🔦", key=f"chk_{day}"):
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()

    # TAG 10: TRANSPORT-RÄTSEL (WOLF, ZIEGE, KOHL)
    elif door["type"] == "river_crossing":
        st.write("🐺🐐🥬 **Fluss-Transport-Steuerung (Wolf, Ziege, Kohl):**")
        r = st.session_state.river
        st.write(f"📍 **Linkes Ufer:** {[k for k, v in r.items() if v == 'left' and k != 'boat']}")
        st.write(f"🛶 **Boot Position:** Ufer {r['boat'].upper()}")
        st.write(f"📍 **Rechtes Ufer:** {[k for k, v in r.items() if v == 'right' and k != 'boat']}")
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            item_to_move = st.selectbox("Passagier mitnehmen:", ["Niemand (leer fahren)", "wolf", "ziege", "kohl"], key="river_item")
        with col_act2:
            if st.button("Ufer wechseln 🛶", key="river_move"):
                target = "right" if r["boat"] == "left" else "left"
                r["boat"] = target
                if item_to_move != "Niemand (leer fahren)":
                    r[item_to_move] = target
                if r["wolf"] == r["ziege"] and r["boat"] != r["wolf"]:
                    st.error("💀 Der Wolf hat die Ziege gefressen! Zurückgesetzt.")
                    st.session_state.river = {"boat": "left", "wolf": "left", "ziege": "left", "kohl": "left"}
                elif r["ziege"] == r["kohl"] and r["boat"] != r["ziege"]:
                    st.error("💀 Die Ziege hat den Kohlkopf gefressen! Zurückgesetzt.")
                    st.session_state.river = {"boat": "left", "wolf": "left", "ziege": "left", "kohl": "left"}
                st.rerun()
        if st.button("Zurücksetzen 🔄", key="river_reset"):
            st.session_state.river = {"boat": "left", "wolf": "left", "ziege": "left", "kohl": "left"}
            st.rerun()
        if r["wolf"] == "right" and r["ziege"] == "right" and r["kohl"] == "right":
            st.success("🎉 Alle sicher drüben!")
            st.markdown(f"<div class='puzzle-card'>{door['puzzle_piece']}</div>", unsafe_allow_html=True)
            if day not in st.session_state.solved_doors:
                st.session_state.solved_doors.append(day)
                st.rerun()

    # TAG 13: TRI-VENTIL-GLEICHUNGSSYSTEM
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

    # TAG 14: INTERAKTIVES PAKET-LEITSYSTEM
    elif door["type"] == "package_sort":
        st.write("📦 **Interaktives Paket-Leitsystem (Rutschen 1-4 zuweisen):**")
        p_alpha = st.selectbox("Paket Alpha", [1, 2, 3, 4], index=0, key="pa")
        p_beta = st.selectbox("Paket Beta", [1, 2, 3, 4], index=1, key="pb")
        p_gamma = st.selectbox("Paket Gamma", [1, 2, 3, 4], index=0, key="pg")
        p_delta = st.selectbox("Paket Delta", [1, 2, 3, 4], index=3, key="pd")
        
        if st.button("Rutschen-Konfiguration prüfen 📦", key=f"chk_{day}"):
            if p_alpha == 3 and p_beta == 2 and p_gamma == 1 and p_delta == 4:
                st.success("🎉 Perfekt! Alle Axiome und Paket-Regeln wurden fehlerfrei erfüllt.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Die Rutschen-Belegung widerspricht den logischen Axiomen.")

    # TAG 15: WUNSCHZETTEL-MASCHINE (INTERAKTIV)
    elif door["type"] == "wish_machine":
        st.write("📜 **Interaktives Wunschzettel-Rechenmodul:**")
        w_input = st.number_input("Nächsten Wert in der Reihe ermitteln:", min_value=0, max_value=500, value=0, key="wish_num")
        if st.button("Wunschzettel-Reihe berechnen 📜", key=f"chk_{day}"):
            if w_input == 159:
                st.success("🎉 Richtig! Das Muster (Multiplikation mit 2 und Addition von 1) wurde erfolgreich berechnet.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falscher Wert.")

    # TAG 16: STARKSTROM-RELAY NETZWERK
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

    # TAG 17: FREQUENZ-REGLER
    elif door["type"] == "frequency_tuner":
        st.write("📻 **Interaktiver Radio-Notkanal Resonanz-Tuner:**")
        fa = st.slider("Frequenz-Regler (MHz)", 50.0, 150.0, 70.0, step=0.5, key="fa_slide")
        st.markdown(f"**Aktuell eingestellt:** `{fa} MHz`")
        
        if st.button("Frequenz synchronisieren 📡", key=f"chk_{day}"):
            if abs(fa - 89.0) < 0.1:
                st.success("🎉 Resonanzpunkt perfekt getroffen! Der Notkanal steht klar im Äther.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Das Signal ist noch verrauscht.")

    # TAG 18: HANGAR-SCHLOSS
    elif door["type"] == "hangar_puzzle":
        st.write("🔐 **Interaktives Hangar-Zahlenwahl-Schloss:**")
        hangar_code = st.slider("Wähle die zweistellige Kombination", 10, 99, 10, key="hangar_slider")
        st.markdown(f"**Aktuell gewählt:** `{hangar_code}`")
        if st.button("Schloss entriegeln 🔐", key=f"chk_{day}"):
            if hangar_code == 57:
                st.success("🎉 Korrekt! Das Hangar-Tor schwingt auf.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Das Schloss bleibt verschlossen.")

    # TAG 19: RENTIER-AUFSTELLUNGS-RASTER
    elif door["type"] == "reindeer_puzzle":
        st.write("🦌 **Rentier-Aufstellungs-Raster (3 Reihen à 2 Plätze):**")
        ans_count = st.text_input("Wie viele valide Kombinationsmöglichkeiten gibt es insgesamt?", key="reindeer_count_ans")
        
        if st.button("Aufstellung verifizieren 🦌", key=f"chk_{day}"):
            if ans_count.strip() == "12":
                st.success("🎉 Perfekt! 12 valide Permutationen exakt errechnet.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsche Anzahl an Kombinationen.")

    # TAG 20: ALCHEMISTISCHE WAAGE (Sauberes Layout ohne Klammern)
    elif door["type"] == "scale_puzzle":
        st.write("⚖️ **Sternenstaub-Waage (Einheitliches Mischsystem):**")
        st.markdown("Stelle die Regler so ein, dass exakt 75 kg erreicht werden:")
        w_hafer = st.slider("Hafer (kg)", 0, 50, 10, key="w_h")
        w_staub = st.slider("Sternenstaub (kg)", 0, 50, 10, key="w_s")
        w_essenz = st.slider("Elfen-Essenz (kg)", 0, 50, 10, key="w_e")
        
        total_weight = w_hafer + w_staub + w_essenz
        st.write(f"Gesamtgewicht: **{total_weight} kg** (Ziel: 75 kg)")
        
        if st.button("Waage ausbalancieren ⚖️", key=f"chk_{day}"):
            if w_hafer == 18 and w_staub == 36 and w_essenz == 21 and total_weight == 75:
                st.success("🎉 Die Waage ist perfekt im Gleichgewicht!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Die Gewichte stimmen nicht mit den Alchemie-Regeln überein.")

    # TAG 21: ROUTEN-PLANER (INTERAKTIV)
    elif door["type"] == "route_planner":
        st.write("✈️ **Interaktiver Routen-Differenz-Rechner:**")
        r_val = st.number_input("Ersparnis-Wert eingeben:", min_value=0, max_value=500, value=0, key="route_num")
        if st.button("Routen-Effizienz bestätigen ✈️", key=f"chk_{day}"):
            if r_val == 30:
                st.success("🎉 Korrekt! Die optimale Flug-Effizienz ist berechnet.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falscher Wert.")

    # TAG 23: ZAHNRAD-ÜBERSETZUNG
    elif door["type"] == "gear_ratio_puzzle":
        st.write("⚙️ **Zahnrad-Übersetzung:**")
        factor = st.slider("Übersetzungsfaktor", 1, 10, 1, key="gear_slider")
        rpm_out = 36 * factor
        st.write(f"Eingabe: 36 RPM × Faktor {factor} = **{rpm_out} RPM** (Ziel: 144 RPM)")
        
        if st.button("Zahnräder einkuppeln ⚙️", key=f"chk_{day}"):
            if factor == 4:
                st.success("🎉 Perfekte Übersetzung! Die Schotten öffnen sich.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsche Drehzahl.")

# Optionale Anzeige der Fragmente / Hinweise in der Seitenleiste (Tage 5-12)
if show_sidebar:
    with puzzle_col:
        st.markdown("### 🧩 Deine Fragmente")
        st.markdown("Sammle alle Hinweise aus den Toren 5 bis 12:")
        for d_num in range(5, 13):
            if d_num in st.session_state.solved_doors:
                st.success(f"{DOORS[d_num]['puzzle_piece']}")
            else:
                st.info(f"Tag {d_num}: *Noch gesperrt*")
