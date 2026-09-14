import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. SEITEN-KONFIGURATION & DUNKELGRÜNES DESIGN (CSS)
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
    
    .sudoku-grid {
        background-color: #142e1d;
        border: 2px solid #d69e2e;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-family: monospace;
        font-size: 1.2em;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Schneeflocken-Effekt
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
# 2. RÄTSEL-DATENBANK (Überarbeitet & Logisch optimiert)
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
        "puzzle_piece": "🧩 Fragment 1: Rahmenteil Oben-Links",
        "hint": "Ein kurzes, dreibuchstabiges Wort."
    },
    6: {
        "person": "Person C",
        "title": "Tag 6: Das magische Sudoku-Gitter 🔢",
        "type": "sudoku_puzzle",
        "story": "Ihr findet einen gefrorenen Monolithen. Die Struktur ist ein magisches 3x3-Quadrat, bei dem Zeilen, Spalten und Diagonalen jeweils 15 ergeben.",
        "question": "Trage die fehlenden Zahlen ein. In der Mitte steht fest die 5. Die Ecken enthalten die geraden Zahlen (2, 4, 6, 8) und die Rand-Mitten die ungeraden (1, 3, 7, 9). Löse das Raster!",
        "answer": None,
        "puzzle_piece": "🧩 Fragment 2: Rahmenteil Oben-Mitte",
        "hint": "Zentrum ist 5. Oben links = 8, Oben rechts = 6, Unten links = 2, Unten rechts = 4."
    },
    7: {
        "person": "Person A",
        "title": "Tag 7: Das Logikgitter der Schlucht 🗺️",
        "type": "logic_grid",
        "story": "Vor der Eisspalte müsst ihr anhand von Hinweisen herausfinden, welcher Elf (A, B, C) welchen Weg und welches Werkzeug gewählt hat.",
        "question": "Hinweise:\n1. Elf C war am schnellsten und wählte den gefährlichsten Weg (Eishöhlen-Weg) mit dem Eispickel.\n2. Elf A war langsamer als B und nahm den leichten Gletscher-Pfad.\n3. Elf B nahm folglich den Schlucht-Pfad mit den Schneeschuhen.\nOrdne die Wege korrekt zu!",
        "answer": None,
        "puzzle_piece": "🧩 Fragment 3: Rahmenteil Oben-Rechts",
        "hint": "Elf A = Gletscher-Pfad, Elf B = Schlucht-Pfad, Elf C = Eishöhlen-Weg."
    },
    8: {
        "person": "Person B",
        "title": "Tag 8: Das interaktive Morse-Terminal 📻",
        "type": "morse_terminal",
        "story": "Ein Funksignal hallt durch die Nebelwände. Nutze das Morse-Terminal, um das universelle Notsignal **SOS** abzusetzen!",
        "question": "Klicke die Tasten in der korrekten Reihenfolge: Drei mal Kurz (•), drei mal Lang (-), drei mal Kurz (•).",
        "answer": "...---...",
        "puzzle_piece": "🧩 Fragment 4: Rahmenteil Mitte-Links",
        "hint": "SOS = 3x Punkt, 3x Strich, 3x Punkt."
    },
    9: {
        "person": "Person C",
        "title": "Tag 9: Der Lichtstrahl-Spiegelpfad",
        "type": "mirror_puzzle",
        "story": "Ein Laserstrahl bricht durch den Nebel. Der Strahl kommt von Süden und muss nach Osten abgelenkt werden. Welcher Spiegelwinkel ist nötig?",
        "question": "Der Strahl soll von Süden kommend nach Osten gelenkt werden. Ein Spiegel mit der Ausrichtung '/' oder '\\' ist nötig. Finde die richtige Kombination für die 3 Spiegel (Tipp: Korrekt ist / \\ /).",
        "answer": "NO",
        "puzzle_piece": "🧩 Fragment 5: Zentrum-Teil",
        "hint": "Die Ausrichtung für Nord-Ost ist im System als 'NO' hinterlegt."
    },
    10: {
        "person": "Person A",
        "title": "Tag 10: Das interaktive Transporträtsel 🐺🐐🥬",
        "type": "river_crossing",
        "story": "Du stehst am Gletscherfluss mit Wolf, Ziege und Kohl. Du darfst immer nur einen Passagier mitnehmen.",
        "question": "Bringe alle sicher auf die andere Seite, ohne dass Fressfeinde unbeaufsichtigt gelassen werden!",
        "answer": "COMPLETED",
        "puzzle_piece": "🧩 Fragment 6: Rahmenteil Unten-Links",
        "hint": "Nimm zuerst die Ziege rüber, fahre allein zurück, nimm den Wolf rüber, bringe die Ziege wieder mit zurück..."
    },
    11: {
        "person": "Person B",
        "title": "Tag 11: Das Krypto-Zahlenschloss",
        "type": "text",
        "story": "Das Schloss vor dem Ausgang verlangt die Lösung eines Kombinatorik-Rätsels.",
        "question": "Wie viele verschiedene Möglichkeiten gibt es, 3 verschiedene Geschenke (A, B, C) unter den Elfen aufzuteilen? (Fakultät von 3 = 3!)\n\n**Eingabe:** Zahl eingeben.",
        "answer": "6",
        "puzzle_piece": "🧩 Fragment 7: Rahmenteil Unten-Mitte",
        "hint": "3 * 2 * 1 = 6."
    },
    12: {
        "person": "Person C",
        "title": "Tag 12: Das visuelle Puzzleteile-Haupttor 🧩",
        "type": "puzzle_assembly",
        "story": "Ihr habt alle 7 Fragmente gesammelt! Setzt sie im Master-Rahmen zusammen, um das Tor zu öffnen.",
        "question": "Klicke auf die Fragmente in der korrekten Reihenfolge (von Oben nach Unten / Mitte), um das Bild zu finalisieren.",
        "answer": "SOLVED",
        "puzzle_piece": "🏆 GEWONNEN: Die Werkstatt ist geöffnet!",
        "hint": "Klicke nacheinander auf die Teile 1 bis 7, um sie einzurasten."
    },
    13: {
        "person": "Person A",
        "title": "Tag 13: Das Zahnrad-Getriebe ⚙️",
        "type": "gear_puzzle",
        "story": "Die Hauptzahnräder der Werkstatt klemmen!",
        "question": "Stelle die benötigte Umdrehung des 12er-Rads ein (kgV von 12, 18, 24 = 72).",
        "answer": 6,
        "puzzle_piece": None,
        "hint": "72 / 12 = 6 Umdrehungen."
    },
    14: {
        "person": "Person B",
        "title": "Tag 14: Chaos in der Packstation",
        "type": "text",
        "story": "Sortiere die durcheinandergeratenen Buchstaben.",
        "question": "Entferne alle Buchstaben von 'MAGIE' aus 'ELFENMAGIE'.",
        "answer": "ELFEN",
        "puzzle_piece": None,
        "hint": "ELFENMAGIE - MAGIE = ELFEN."
    },
    15: {
        "person": "Person C",
        "title": "Tag 15: Rentierfutter-Mischstation ⚖️",
        "type": "scale_puzzle",
        "story": "Mische das Futter auf der Balkenwaage im exakten Verhältnis an.",
        "question": "Stelle Schieberegler so ein, dass exakt 50 kg entstehen (Hafer: 25, Sternenstaub: 10, Äpfel: 15).",
        "answer": {"hafer": 25, "staub": 10, "aepfel": 15},
        "puzzle_piece": None,
        "hint": "Hafer=25, Staub=10, Äpfel=15."
    },
    16: {
        "person": "Person A",
        "title": "Tag 16: Schalttafel für Notstrom",
        "type": "binary_switches",
        "story": "Aktiviere den Notstrom-Schaltkreis für die Binärzahl 25.",
        "question": "Schalte die passenden Schalter ein (16 + 8 + 1).",
        "answer": [True, True, False, False, True],
        "puzzle_piece": None,
        "hint": "Schalter 1 (16), 2 (8) und 5 (1) auf AN."
    },
    17: {
        "person": "Person B",
        "title": "Tag 17: Die Wunschzettel-Maschine",
        "type": "text",
        "story": "Kalibriere den Daten-Sortierer.",
        "question": "Bestimme den Median der Zahlenreihe: 12, 45, 7, 23, 89, 34, 19",
        "answer": "23",
        "puzzle_piece": None,
        "hint": "Sortiert: 7, 12, 19, [23], 34, 45, 89."
    },
    18: {
        "person": "Person C",
        "title": "Tag 18: Das Werkstatt-Schloss",
        "type": "text",
        "story": "Sichere das System ab.",
        "question": "Rechne: (Tag 13: 6) × (Tag 15 Sternenstaub: 10) + (Tag 17: 23)",
        "answer": "83",
        "puzzle_piece": None,
        "hint": "6 * 10 + 23 = 83."
    },
    19: {
        "person": "Person A",
        "title": "Tag 19: Flugrouten-Kalkulation",
        "type": "text",
        "story": "Berechne die optimalen Fluglinien.",
        "question": "Kürzeste Strecke (in km), um alle 4 Ecken eines 100x100km Quadrats nacheinander zu besuchen?",
        "answer": "300",
        "puzzle_piece": None,
        "hint": "3 Kanten abfliegen: 100 + 100 + 100 = 300 km."
    },
    20: {
        "person": "Person B",
        "title": "Tag 20: Polarlichter-Frequenz",
        "type": "frequency_tuner",
        "story": "Der Funkempfänger ist verstellt! Finde die Resonanzfrequenz.",
        "question": "Richte das Frequenz-Widget auf 87.5 MHz aus.",
        "answer": 87.5,
        "puzzle_piece": None,
        "hint": "Schieberegler auf 87.5 MHz einstellen."
    },
    21: {
        "person": "Person C",
        "title": "Tag 21: Rentiere anspannen",
        "type": "text",
        "story": "Berechne die Aufstellung der Rentiere.",
        "question": "Wie viele Anordnungen für 7 Rentiere hinter Rudolph? (Fakultät von 7 = 7!)",
        "answer": "5040",
        "puzzle_piece": None,
        "hint": "7 × 6 × 5 × 4 × 3 × 2 × 1 = 5040."
    },
    22: {
        "person": "Person A",
        "title": "Tag 22: Frachtraum-Ausgleich",
        "type": "text",
        "story": "Der Schlitten benötigt die finale Gewichtsanpassung.",
        "question": "Geladen: (3 × 150 kg) + (4 × 110 kg) = 890 kg. Wie viel kg fehlen bis zu 1000 kg?",
        "answer": "110",
        "puzzle_piece": None,
        "hint": "1000 - 890 = 110."
    },
    23: {
        "person": "Person B",
        "title": "Tag 23: Finale Startbereitschaft",
        "type": "text",
        "story": "Der Weihnachts-Countdown läuft!",
        "question": "Rechne: (Tag 3 Ergebnis: 8) + (Tag 18 Ergebnis: 83) + Basiszahl.",
        "answer": "91",
        "puzzle_piece": None,
        "hint": "8 + 83 = 91."
    },
    24: {
        "person": "Alle 3 gemeinsam",
        "title": "Tag 24: HEILIGABEND – Der Master-Code!",
        "type": "text",
        "story": "Hauptkontrollraum! Auf den Monitoren blinkt die Eingabe.",
        "question": "Fügt zusammen: Code Tag 3 (500) + Code Tag 12 (NORD12) + Code Tag 23 (583)",
        "answer": "500NORD12583",
        "puzzle_piece": "🏆 MEISTER-TITEL: RETTER VON WEIHNACHTEN!",
        "hint": "Schreibe die drei Teilstücke aneinander: 500NORD12583"
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
        "goat": "left",
        "cabbage": "left"
    }

if "puzzle_assembled" not in st.session_state:
    st.session_state.puzzle_assembled = False

# ==============================================================================
# 4. KOPFZEILE & FORTSCHRITT
# ==============================================================================
st.title("🎄 Nordpol-Expedition 2026")
st.caption("Das mathematisch-logische Advents-Abenteuer (Optimierte Version)")

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
    
    prefix = "🌀 " if 5 <= i <= 11 else ""
    label = f"🎁 {prefix}Tag {i}" if i in st.session_state.solved_doors else f"{prefix}Tag {i}"
        
    if col.button(label, key=f"btn_{i}"):
        st.session_state.active_day = i

st.divider()

# ==============================================================================
# 6. RÄTSEL-FLÄCHE & LABYRINTH-SAMMLUNG
# ==============================================================================
main_col, puzzle_col = st.columns([2, 1])

with main_col:
    day = st.session_state.active_day
    door = DOORS[day]

    st.subheader(f"{door['title']}")
    st.caption(f"Verantwortlich: **{door['person']}**")
    
    st.info(f"📖 {door['story']}")
    st.markdown(f"**Aufgabe:** {door['question']}")

    # --- SONDER-WIDGETS ---
    
    # TAG 6: SUDOKU (Klar und visuell)
    if door["type"] == "sudoku_puzzle":
        st.markdown("""
            <div class='sudoku-grid'>
            [ 8 ] [ 1 ] [ 6 ]<br>
            [ 3 ] [ 5 ] [ 7 ]<br>
            [ 4 ] [ 9 ] [ 2 ]
            </div>
        """, unsafe_allow_html=True)
        st.write("🔢 **Trage die Summen-Bestätigung ein (Jede Reihe ergibt 15):**")
        s_input = st.text_input("Tippe die Summe ein (15):", key="s_in")
        if st.button("Sudoku bestätigen 🔢", key=f"chk_{day}"):
            if s_input.strip() == "15":
                st.success("🎉 Perfekt! Das magische Sudoku ist bestätigt!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsche Summe. Es müssen genau 15 sein.")

    # TAG 7: LOGIKGITTER
    elif door["type"] == "logic_grid":
        st.write("🗺️ **Logikgitter-Auswahl:**")
        elf_a_weg = st.selectbox("Welchen Weg nahm Elf A?", ["-", "Schlucht-Pfad", "Gletscher-Pfad", "Eishöhlen-Weg"], key="lg_a")
        elf_b_weg = st.selectbox("Welchen Weg nahm Elf B?", ["-", "Schlucht-Pfad", "Gletscher-Pfad", "Eishöhlen-Weg"], key="lg_b")
        elf_c_weg = st.selectbox("Welchen Weg nahm Elf C?", ["-", "Schlucht-Pfad", "Gletscher-Pfad", "Eishöhlen-Weg"], key="lg_c")
        
        if st.button("Logikgitter auswerten 🗺️", key=f"chk_{day}"):
            if elf_a_weg == "Gletscher-Pfad" and elf_b_weg == "Schlucht-Pfad" and elf_c_weg == "Eishöhlen-Weg":
                st.success("🎉 Logikgitter fehlerfrei gelöst!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Die Zuordnung stimmt noch nicht. Siehe Hinweise.")

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
                st.success("🎉 SOS-Signal erfolgreich übertragen!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error(f"❌ Falsches Signal ('{st.session_state.morse_buffer}'). Benötigt: ...---...")

    # TAG 10: TRANSPORT-RÄTSEL (Stabil & korrigiert)
    elif door["type"] == "river_crossing":
        st.write("🐺🐐🥬 **Fluss-Transport-Steuerung:**")
        r = st.session_state.river
        
        st.write(f"📍 **Linkes Ufer:** {[k for k, v in r.items() if v == 'left' and k != 'boat']}")
        st.write(f"🛶 **Boot Position:** Ufer {r['boat'].upper()}")
        st.write(f"📍 **Rechtes Ufer:** {[k for k, v in r.items() if v == 'right' and k != 'boat']}")
        
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            item_to_move = st.selectbox("Wer kommt mit ins Boot?", ["Niemand (leer fahren)", "wolf", "goat", "cabbage"], key="river_item")
        with col_act2:
            if st.button("Ufer wechseln 🛶", key="river_move"):
                target = "right" if r["boat"] == "left" else "left"
                r["boat"] = target
                if item_to_move != "Niemand (leer fahren)":
                    r[item_to_move] = target
                
                # Fress-Regeln
                if r["wolf"] == r["goat"] and r["boat"] != r["wolf"]:
                    st.error("💀 Der Wolf hat die Ziege gefressen! Zurückgesetzt.")
                    st.session_state.river = {"boat": "left", "wolf": "left", "goat": "left", "cabbage": "left"}
                elif r["goat"] == r["cabbage"] and r["boat"] != r["goat"]:
                    st.error("💀 Die Ziege hat den Kohlkopf gefressen! Zurückgesetzt.")
                    st.session_state.river = {"boat": "left", "wolf": "left", "goat": "left", "cabbage": "left"}
                st.rerun()

        if st.button("Spielstand zurücksetzen 🔄", key="river_reset"):
            st.session_state.river = {"boat": "left", "wolf": "left", "goat": "left", "cabbage": "left"}
            st.rerun()

        if r["wolf"] == "right" and r["goat"] == "right" and r["cabbage"] == "right":
            st.success("🎉 Alle sicher drüben!")
            if day not in st.session_state.solved_doors:
                st.session_state.solved_doors.append(day)
                st.rerun()

    # TAG 12: PUZZLE-ZUSAMMENBAU (Stabiles Matrix-Einrasten)
    elif door["type"] == "puzzle_assembly":
        st.write("🧩 **Puzzleteile-Masterrahmen:** Setze die 7 Fragmente in der richtigen Reihenfolge zusammen.")
        
        p1 = st.checkbox("Teil 1: Oben-Links einrasten", key="pz1")
        p2 = st.checkbox("Teil 2: Oben-Mitte einrasten", key="pz2")
        p3 = st.checkbox("Teil 3: Oben-Rechts einrasten", key="pz3")
        p4 = st.checkbox("Teil 4: Mitte-Links einrasten", key="pz4")
        p5 = st.checkbox("Teil 5: Zentrum-Teil einrasten", key="pz5")
        p6 = st.checkbox("Teil 6: Unten-Links einrasten", key="pz6")
        p7 = st.checkbox("Teil 7: Unten-Mitte einrasten", key="pz7")
        
        if st.button("Puzzle-Vollständigkeit prüfen 🏆", key=f"chk_{day}"):
            if p1 and p2 and p3 and p4 and p5 and p6 and p7:
                st.success("🎉 Das Tor ist komplett zusammengesetzt und öffnet sich!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Es fehlen noch Teile im Rahmen.")

    # STANDARD-WIDGETS FÜR ANDERE TAGE
    elif door["type"] == "mirror_puzzle":
        st.write("🔦 **Laser-Spiegel-Ausrichtung:** Klicke auf die Spiegel, um die Ausrichtung zu ändern.")
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
            st.success("🟢 Strahlenverlauf korrekt!")
            if st.button("Lichtstrahl aktivieren 🔦", key=f"chk_{day}"):
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
        else:
            st.warning("🔴 Strahl wird noch falsch reflektiert.")

    elif door["type"] == "gear_puzzle":
        rot = st.slider("⚙️ Umdrehungen des 12er-Rads:", 1, 12, 1, key="rot_slider")
        if st.button("Zahnräder einrasten ⚙️", key=f"chk_{day}"):
            if rot == door["answer"]:
                st.success("🎉 Synchronisiert!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Noch nicht synchron.")

    elif door["type"] == "scale_puzzle":
        w_hafer = st.slider("🌾 Hafer (kg)", 0, 50, 20, key="w_h")
        w_staub = st.slider("✨ Sternenstaub (kg)", 0, 50, 5, key="w_s")
        w_aepfel = st.slider("🍎 Äpfel (kg)", 0, 50, 10, key="w_a")
        if st.button("Futter-Mischung wiegen ⚖️", key=f"chk_{day}"):
            if w_hafer == 25 and w_staub == 10 and w_aepfel == 15:
                st.success("🎉 Perfektes Verhältnis!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsches Mischungsverhältnis.")

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
                st.error("❌ Falscher Code.")

    elif door["type"] == "binary_switches":
        b1, b2, b3, b4, b5 = st.columns(5)
        s1 = b1.checkbox("Schalter 1 (16)", key="cb1")
        s2 = b2.checkbox("Schalter 2 (8)", key="cb2")
        s3 = b3.checkbox("Schalter 3 (4)", key="cb3")
        s4 = b4.checkbox("Schalter 4 (2)", key="cb4")
        s5 = b5.checkbox("Schalter 5 (1)", key="cb5")
        if st.button("Schaltkreis aktivieren ⚡", key=f"chk_{day}"):
            if [s1, s2, s3, s4, s5] == door["answer"]:
                st.success("🎉 Stromkreis aktiv!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsche Schaltung.")

    elif door["type"] == "frequency_tuner":
        freq = st.slider("📻 Empfänger (MHz):", 80.0, 100.0, 92.0, step=0.5, key="freq_slider")
        if st.button("Signal-Frequenz feststellen 📡", key=f"chk_{day}"):
            if abs(freq - door["answer"]) < 0.1:
                st.success("🎉 Glasklarer Empfang!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Nur Rauschen.")

    else:
        if door["type"] not in ["sudoku_puzzle", "logic_grid", "morse_terminal", "river_crossing", "puzzle_assembly"]:
            ans = st.text_input("Deine Lösung:", key=f"input_{day}")
            if st.button("Prüfen 🔍", key=f"chk_{day}"):
                user_clean = ans.strip().replace(" ", "").upper()
                target_clean = str(door["answer"]).strip().replace(" ", "").upper()
                if user_clean == target_clean:
                    st.success("🎉 Richtig gelöst!")
                    if day not in st.session_state.solved_doors:
                        st.session_state.solved_doors.append(day)
                        st.rerun()
                else:
                    st.error("❌ Leider nicht korrekt.")

    with st.expander("💡 Hinweis anzeigen"):
        st.write(door["hint"])

# ==============================================================================
# SEITENLEISTE (FRAGMENT-SAMMLUNG)
# ==============================================================================
with puzzle_col:
    st.subheader("🌀 Labyrinth-Puzzleteile")
    st.caption("Sammlertasche für das Haupttor:")
    
    lab_pieces = [d for d in st.session_state.solved_doors if DOORS[d]["puzzle_piece"]]
    
    if not lab_pieces:
        st.write("*Noch keine Puzzleteile gefunden.*")
    else:
        for d in sorted(lab_pieces):
            st.markdown(f"<div class='puzzle-card'><b>Tag {d}:</b><br>{DOORS[d]['puzzle_piece']}</div>", unsafe_allow_html=True)
            
    st.write("---")
    st.metric("Gefundene Fragmente", f"{len(lab_pieces)} / 7")
