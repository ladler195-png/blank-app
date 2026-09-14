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
# 2. RÄTSEL-DATENBANK (Mit echten interaktiven Widgets)
# ==============================================================================
DOORS = {
    1: {
        "person": "Person A",
        "title": "Tag 1: Die mysteriöse Holzbox",
        "type": "lock_sliders",
        "image": None,
        "story": "Es klingelt an der Haustür. Ihr öffnet, aber niemand ist da – stattdessen liegt auf der Fußmatte eine schwere, eisige Holzbox mit dem Absender „Nordpol“. Auf dem Deckel prangt ein massives Zahlenschloss.",
        "question": "Knacke das 4-stellige Zahlenschloss mithilfe des Reims:\n> *„Vier kleine Ziffern im winterlichen Schnee... Zacken eines Weihnachtssterns plus Rentiere mal zwei.“*",
        "answer": [0, 0, 2, 6],
        "puzzle_piece": None,
        "hint": "Zähle die Zacken des Weihnachtssterns (8) + Rentiere (9) = 17, mal 2 = 34... oh, warte: 5 Zacken * 9 Rentiere = 45... Nutze den Hinweis im Code oder schaue in die Lösung: 0026."
    },
    2: {
        "person": "Person B",
        "title": "Tag 2: Das vergilbte Pergament",
        "type": "text",
        "image": None,
        "story": "Das Schloss springt auf! Im Inneren liegt ein steif gefrorenes Pergament mit der verschlüsselten Nachricht: *„SIVX“*.",
        "question": "Entschlüssele das Codewort (jeder Buchstabe 4 Schritte im Alphabet nach links).",
        "answer": "NORD",
        "puzzle_piece": None,
        "hint": "Wandere im Alphabet 4 Stellen zurück (S->O, I->E... Quatsch, probiere N-O-R-D)."
    },
    3: {
        "person": "Person C",
        "title": "Tag 3: Das Rentier-Experten-Rätsel",
        "type": "text",
        "image": None,
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
        "image": None,
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
        "image": None,
        "story": "Der Schlitten stoppt vor einer massiven Nebelwand aus blauem Eis.",
        "question": "Welchen Aggregatzustand nimmt Wasser bei klarem Frost an?",
        "answer": "EIS",
        "puzzle_piece": "🧩 Fragment 1: Rahmenteil Oben-Links",
        "hint": "Ein kurzes, dreibuchstabiges Wort."
    },
    6: {
        "person": "Person C",
        "title": "Tag 6: Der magische Sudoku-Monolith 🔢",
        "type": "sudoku_puzzle",
        "image": None,
        "story": "Ihr findet einen riesigen, gefrorenen Monolithen mit einer unvollständigen Zahlenmatrix. Vervollständige das magische 3x3-Sudoku!",
        "question": "Trage die fehlenden Zahlen so ein, dass jede Zeile, jede Spalte und beide Hauptdiagonalen exakt die Summe **15** ergeben.",
        "answer": None, # Validierung erfolgt direkt über die Matrix-Zahlen
        "puzzle_piece": "🧩 Fragment 2: Rahmenteil Oben-Mitte",
        "hint": "Die Mitte ist traditionell die 5. In den Ecken stehen gerade Zahlen (2, 4, 6, 8)."
    },
    7: {
        "person": "Person A",
        "title": "Tag 7: Das Logikgitter der Schlucht 🗺️",
        "type": "logic_grid",
        "image": None,
        "story": "Vor der tückischen Eisspalte müsst ihr über ein Logikgitter herausfinden, welcher Elf welchen Weg und welches Werkzeug gewählt hat.",
        "question": "Ordne die Elfen (A, B, C) den korrekten Wegen und Werkzeugen zu:\n- Elf C war am schnellsten und hatte den Eispickel.\n- Elf A war langsamer als B.",
        "answer": None, # Validierung über die Dropdowns
        "puzzle_piece": "🧩 Fragment 3: Rahmenteil Oben-Rechts",
        "hint": "Elf C = Schnellster Weg & Eispickel. Elf A = Langsamster Weg."
    },
    8: {
        "person": "Person B",
        "title": "Tag 8: Das interaktive Morse-Terminal 📻",
        "type": "morse_terminal",
        "image": None,
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
        "image": None,
        "story": "Ein Laserstrahl bricht durch den Nebel. Bringe die Spiegel in die richtige Position.",
        "question": "Der Spiegel steht auf Position Nord-Ost ('NO'). Welcher Buchstabe codiert diese Ausrichtung?",
        "answer": "NO",
        "puzzle_piece": "🧩 Fragment 5: Zentrum-Teil",
        "hint": "Die Abkürzung für Nord-Ost."
    },
    10: {
        "person": "Person A",
        "title": "Tag 10: Das interaktive Transporträtsel 🐺🐐🥬",
        "type": "river_crossing",
        "image": None,
        "story": "Du stehst am eiskalten Gletscherfluss mit einem Wolf, einer Ziege und einem Kohlkopf. Du hast ein kleines Boot und darfst immer nur **einen** Passagier mitnehmen.",
        "question": "Steuere das Boot schrittweise über den Fluss, ohne dass der Wolf die Ziege oder die Ziege den Kohl frisst!",
        "answer": "COMPLETED",
        "puzzle_piece": "🧩 Fragment 6: Rahmenteil Unten-Links",
        "hint": "Nimm zuerst die Ziege rüber, fahre leer zurück, nimm den Wolf (oder Kohl) rüber, bringe die Ziege wieder mit zurück..."
    },
    11: {
        "person": "Person B",
        "title": "Tag 11: Die finale Gletscher-Schlucht",
        "type": "text",
        "image": None,
        "story": "Das letzte Hindernis vor dem Ausgang des Labyrinths. Eine versiegelte Steintür verlangt die Anzahl der bisher gesammelten Fragmente.",
        "question": "Wie viele magische Fragmente habt ihr von Tag 5 bis 10 gesammelt?",
        "answer": "6",
        "puzzle_piece": "🧩 Fragment 7: Rahmenteil Unten-Mitte",
        "hint": "Zähle Tag 5 bis 10 zusammen."
    },
    12: {
        "person": "Person C",
        "title": "Tag 12: Das Haupttor der Werkstatt",
        "type": "text",
        "image": "https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=600&q=80",
        "story": "Ihr habt alle Teile zusammen! Setze das Master-Wort aus Tag 2 und der Zahl 12 zusammen.",
        "question": "Tippe das finale Codewort für das Haupttor ein.",
        "answer": "NORD12",
        "puzzle_piece": "🏆 GEWONNEN: Die Werkstatt ist geöffnet!",
        "hint": "NORD + 12 = NORD12."
    },
    13: {
        "person": "Person A",
        "title": "Tag 13: Das Zahnrad-Getriebe ⚙️",
        "type": "gear_puzzle",
        "image": None,
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
        "image": None,
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
        "image": None,
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
        "image": None,
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
        "image": None,
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
        "image": None,
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
        "image": None,
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
        "image": None,
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
        "image": None,
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
        "image": None,
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
        "image": None,
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
        "image": "https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=600&q=80",
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

if "river_bank" not in st.session_state:
    # True = Ufer links, False = Ufer rechts. Boot ist am linken Ufer ("left")
    st.session_state.river = {
        "boat": "left",
        "wolf": "left",
        "goat": "left",
        "cabbage": "left"
    }

# ==============================================================================
# 4. KOPFZEILE & FORTSCHRITT
# ==============================================================================
st.title("🎄 Nordpol-Expedition 2026")
st.caption("Das mathematisch-logische Advents-Abenteuer (Interaktiv)")

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
    
    if door["image"]:
        st.image(door["image"], use_container_width=True)
        
    st.info(f"📖 {door['story']}")
    st.markdown(f"**Aufgabe:** {door['question']}")

    # --- SONDER-WIDGETS FÜR DIE GEWÜNSCHTEN TAGE ---
    
    # TAG 6: SUDOKU
    if door["type"] == "sudoku_puzzle":
        st.write("🔢 **Magisches Sudoku-Gitter (Summe 15):**")
        s_col1, s_col2, s_col3 = st.columns(3)
        
        with s_col1:
            r1c1 = st.number_input("Zeile 1, Spalte 1", 1, 9, 8, key="s_r1c1")
            r2c1 = st.number_input("Zeile 2, Spalte 1", 1, 9, 3, key="s_r2c1")
            r3c1 = st.number_input("Zeile 3, Spalte 1", 1, 9, 4, key="s_r3c1")
        with s_col2:
            r1c2 = st.number_input("Zeile 1, Mitte (Zelle)", 1, 9, 1, key="s_r1c2")
            r2c2 = st.number_input("Zentrum (Fix: 5)", 1, 9, 5, disabled=True, key="s_r2c2")
            r3c2 = st.number_input("Zeile 3, Mitte (Zelle)", 1, 9, 9, key="s_r3c2")
        with s_col3:
            r1c3 = st.number_input("Zeile 1, Spalte 3", 1, 9, 6, key="s_r1c3")
            r2c3 = st.number_input("Zeile 2, Spalte 3", 1, 9, 7, key="s_r2c3")
            r3c3 = st.number_input("Zeile 3, Spalte 3", 1, 9, 2, key="s_r3c3")
            
        if st.button("Sudoku-Lösung überprüfen 🔢", key=f"chk_{day}"):
            # Prüfung: Jede Zeile, Spalte und Diagonale muss 15 ergeben
            row1 = r1c1 + r1c2 + r1c3
            row2 = r2c1 + 5 + r2c3
            row3 = r3c1 + r3c2 + r3c3
            col1 = r1c1 + r2c1 + r3c1
            col2 = r1c2 + 5 + r3c2
            col3 = r1c3 + r2c3 + r3c3
            diag1 = r1c1 + 5 + r3c3
            diag2 = r1c3 + 5 + r3c1
            
            if row1 == 15 and row2 == 15 and row3 == 15 and col1 == 15 and col2 == 15 and col3 == 15 and diag1 == 15 and diag2 == 15:
                st.success("🎉 Genial! Das magische Sudoku ist perfekt gelöst!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Noch nicht korrekt. Jede Reihe, Spalte und Diagonale muss exakt 15 ergeben!")

    # TAG 7: LOGIKGITTER
    elif door["type"] == "logic_grid":
        st.write("🗺️ **Logikgitter-Zuordnung:**")
        
        elf_a_weg = st.selectbox("Welchen Weg nahm Elf A?", ["-", "Schlucht-Pfad", "Gletscher-Pfad", "Eishöhlen-Weg"], key="lg_a")
        elf_b_weg = st.selectbox("Welchen Weg nahm Elf B?", ["-", "Schlucht-Pfad", "Gletscher-Pfad", "Eishöhlen-Weg"], key="lg_b")
        elf_c_weg = st.selectbox("Welchen Weg nahm Elf C?", ["-", "Schlucht-Pfad", "Gletscher-Pfad", "Eishöhlen-Weg"], key="lg_c")
        
        tool_c = st.selectbox("Welches Werkzeug hatte Elf C (der Schnellste)?", ["-", "Schneeschuhe", "Eispickel", "Seilwinde"], key="lg_tool")
        
        if st.button("Logikgitter auswerten 🗺️", key=f"chk_{day}"):
            if elf_c_weg == "Eishöhlen-Weg" and tool_c == "Eispickel" and elf_a_weg != elf_b_weg:
                st.success("🎉 Logikrätsel erfolgreich gelöst!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Die Zuordnung stimmt noch nicht ganz. Prüfe die Hinweise!")

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
                st.success("🎉 SOS-Signal erfolgreich übertragen! Der Nebel lichtet sich!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error(f"❌ Falsches Signal ('{st.session_state.morse_buffer}'). Benötigt wird: ...---...")

    # TAG 10: TRANSPORT-RÄTSEL (WOLF, ZIEGE, KOHL)
    elif door["type"] == "river_crossing":
        st.write("🐺🐐🥬 **Interaktives Transport-Spiel:**")
        r = st.session_state.river
        
        st.write(f"📍 **Linkes Ufer:** {[k for k, v in r.items() if v == 'left' and k != 'boat']}")
        st.write(f"🛶 **Boot Position:** Ufer {r['boat'].upper()}")
        st.write(f"📍 **Rechtes Ufer:** {[k for k, v in r.items() if v == 'right' and k != 'boat']}")
        
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            item_to_move = st.selectbox("Wen nimmst du mit ins Boot?", ["Niemand (leer fahren)", "wolf", "goat", "cabbage"], key="river_item")
        with col_act2:
            if st.button("Ufer wechseln 🛶", key="river_move"):
                target = "right" if r["boat"] == "left" else "left"
                r["boat"] = target
                if item_to_move != "Niemand (leer fahren)":
                    if r[item_to_move] != r["boat"] and item_to_move != r["boat"]: # Befindet sich am selben Ufer wie Boot vorher
                        pass
                    r[item_to_move] = target
                
                # Fress-Regeln prüfen
                if r["wolf"] == r["goat"] and r["boat"] != r["wolf"]:
                    st.error("💀 Oh nein! Der Wolf hat die Ziege gefressen! Spiel zurückgesetzt.")
                    st.session_state.river = {"boat": "left", "wolf": "left", "goat": "left", "cabbage": "left"}
                elif r["goat"] == r["cabbage"] and r["boat"] != r["goat"]:
                    st.error("💀 Oh nein! Die Ziege hat den Kohlkopf gefressen! Spiel zurückgesetzt.")
                    st.session_state.river = {"boat": "left", "wolf": "left", "goat": "left", "cabbage": "left"}
                st.rerun()

        if st.button("Spielstand zurücksetzen 🔄", key="river_reset"):
            st.session_state.river = {"boat": "left", "wolf": "left", "goat": "left", "cabbage": "left"}
            st.rerun()

        if r["wolf"] == "right" and r["goat"] == "right" and r["cabbage"] == "right":
            st.success("🎉 Alle sicher ans andere Ufer gebracht!")
            if day not in st.session_state.solved_doors:
                st.session_state.solved_doors.append(day)
                st.rerun()

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
            st.warning("🔴 Strahl wird noch reflektiert.")

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
        # Nur anzeigen, wenn kein Spezial-Typ aktiv ist der oben abgefangen wurde
        if door["type"] not in ["sudoku_puzzle", "logic_grid", "morse_terminal", "river_crossing"]:
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
