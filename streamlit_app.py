import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. SEITEN-KONFIGURATION & EDLES, SCHLICHTES DESIGN (CSS)
# ==============================================================================
st.set_page_config(
    page_title="Nordpol-Expedition",
    page_icon="❄️",
    layout="wide"
)

# Schlichtes, elegantes Weihnachts-Design (Mattes Dunkelgrau + Warmgold)
st.markdown("""
    <style>
    /* Haupthintergrund: Schlicht, dunkel, matt */
    .stApp {
        background-color: #1a202c;
        color: #e2e8f0;
        font-family: 'Georgia', serif;
    }
    
    /* Elegant goldene Überschriften */
    h1, h2, h3 {
        color: #d69e2e !important;
        font-family: 'Georgia', serif;
        font-weight: normal;
        letter-spacing: 1px;
    }

    /* Subtile, edle Buttons */
    div.stButton > button {
        background-color: #2d3748;
        color: #e2e8f0;
        border-radius: 6px;
        border: 1px solid #4a5568;
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

    /* Dezent geprägte Infoboxen */
    .stAlert {
        border-radius: 8px;
        background-color: rgba(45, 55, 72, 0.5);
        border: 1px solid #4a5568;
    }
    
    /* Puzzle-Teil Auszeichnungsbox */
    .puzzle-card {
        border: 1px dashed #d69e2e;
        padding: 15px;
        border-radius: 8px;
        background-color: rgba(214, 158, 46, 0.05);
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Dezent rieselnde Schneeflocken (hohe Transparenz)
components.html("""
    <script src="https://unpkg.com/magic-snowflakes/dist/snowflakes.min.js"></script>
    <script>
        var snowflakes = new Snowflakes({
            color: '#ffffff',
            count: 15,
            minOpacity: 0.1,
            maxOpacity: 0.4
        });
    </script>
""", height=0)

# ==============================================================================
# 2. RÄTSEL- DATENBANK MIT PUZZLETEILEN & VISUELLEN RÄTSELN
# ==============================================================================
DOORS = {
    1: {
        "person": "Person A",
        "title": "Tag 1: Die verschlossene Kiste",
        "type": "lock_sliders",
        "image": "https://images.unsplash.com/photo-1543257580-7269da773bf5?w=600&q=80",
        "story": "Eine Holzschatulle liegt im Schnee. Auf dem Deckel ist ein Rätsel eingraviert.",
        "question": "Löse das Gravur-Rätsel: 3, 7, 15, 31, __. Übertrage den Code (4-stellig mit führenden Nullen) auf das Schloss.",
        "answer": [0, 0, 6, 3],
        "puzzle_piece": "🧩 Puzzleteil 1: 'KORDINATE NORD: 78° '",
        "hint": "Zahlenabstände verdoppeln sich (+4, +8, +16, +32). Das Ergebnis lautet 63."
    },
    2: {
        "person": "Person B",
        "title": "Tag 2: Das vergilbte Pergament",
        "type": "text",
        "image": "https://images.unsplash.com/photo-1516962215378-7fa2e137ae93?w=600&q=80",
        "story": "In der Kiste liegt eine alte Elfen-Chiffre.",
        "question": "Entschlüssele den Notsender-Code (Cäsar-Chiffre, 4 Stellen zurück im Alphabet): 'SIVX'",
        "answer": "NORD",
        "puzzle_piece": "🧩 Puzzleteil 2: 'SYMBOL: 🧭 COMPASS'",
        "hint": "S-4=N, I-4=O, V-4=R, X-4=D."
    },
    3: {
        "person": "Person C",
        "title": "Tag 3: Konsole des Schlittens",
        "type": "text",
        "image": None,
        "story": "Die Armaturen des Elfen-Schlittens müssen synchronisiert werden.",
        "question": "Berechne die Frequenz: (8 Rentiere) × (Code Tag 1: 63) - 4",
        "answer": "500",
        "puzzle_piece": "🧩 Puzzleteil 3: 'FREQUENZ: 500-MHZ'",
        "hint": "8 * 63 - 4 = 500"
    },
    4: {
        "person": "Person A",
        "title": "Tag 4: Sternenkarte",
        "type": "text",
        "image": None,
        "story": "Das Navigationssystem fordert die Eingabe des Kurses.",
        "question": "Addiere alle Primzahlen zwischen 10 und 25.",
        "answer": "60",
        "puzzle_piece": "🧩 Puzzleteil 4: 'KURS: 60° OST'",
        "hint": "11 + 13 + 17 + 19 = 60"
    },
    5: {
        "person": "Person B",
        "title": "Tag 5: Die Nebelwand",
        "type": "text",
        "image": None,
        "story": "Vor euch baut sich das undurchdringliche Nebel-Labyrinth auf.",
        "question": "Kombiniere Tag 2 + Tag 4 (z.B. ALPHA10).",
        "answer": "NORD60",
        "puzzle_piece": "🧩 Puzzleteil 5: 'GATE-KEY: NORD60'",
        "hint": "NORD + 60"
    },
    6: {
        "person": "Person C",
        "title": "Tag 6: Nikolaus-Schrein",
        "type": "text",
        "image": None,
        "story": "Ein steinerner Schrein versperrt den Pfad.",
        "question": "Welche Zahl steht in der Mitte (Feld X) eines magischen 3x3-Quadrats (Zahlen 1-9)?",
        "answer": "5",
        "puzzle_piece": "🧩 Puzzleteil 6: 'SIGIL: 5-STARS'",
        "hint": "Die Zahl 5 steht im magischen Quadrat immer im Zentrum."
    },
    7: {
        "person": "Person A",
        "title": "Tag 7: Die Weggabelung",
        "type": "text",
        "image": None,
        "story": "Vier Pfade tun sich auf. Das Eismuster weist den Weg.",
        "question": "Welche Pfadnummer folgt? 3, 6, 11, 18, 27, __",
        "answer": "38",
        "puzzle_piece": "🧩 Puzzleteil 7: 'PATH: RIGHT-38'",
        "hint": "+3, +5, +7, +9, +11..."
    },
    8: {
        "person": "Person B",
        "title": "Tag 8: Das Gletscher-Echo",
        "type": "audio_morse",
        "image": None,
        "story": "Ein akustisches Signal schallt durch die Eisspalten.",
        "question": "Entschlüssele den Morsecode (Tonsignal).",
        "answer": "SOS",
        "puzzle_piece": "🧩 Puzzleteil 8: 'SIGNAL: S.O.S'",
        "hint": "Drei kurz, drei lang, drei kurz."
    },
    9: {
        "person": "Person C",
        "title": "Tag 9: Die Spiegel-Grotte",
        "type": "text",
        "image": None,
        "story": "Lenke den Lichtstrahl ab.",
        "question": "Strahl startet OST. Spiegel-Reihenfolge: Links, Rechts, Links. Wohin zeigt der Strahl nun?",
        "answer": "NORD",
        "puzzle_piece": "🧩 Puzzleteil 9: 'MIRROR: NORTH'",
        "hint": "Ost -> Links(Nord) -> Rechts(Ost) -> Links(Nord)."
    },
    10: {
        "person": "Person A",
        "title": "Tag 10: Der gefrorene Kompass",
        "type": "text",
        "image": None,
        "story": "Justiere die Kompassnadel.",
        "question": "Berechne den Rest der Division: (2713) Modulo 360",
        "answer": "193",
        "puzzle_piece": "🧩 Puzzleteil 10: 'DEGREE: 193'",
        "hint": "2713 mod 360 = 193."
    },
    11: {
        "person": "Person B",
        "title": "Tag 11: Die Eisbrücke",
        "type": "text",
        "image": None,
        "story": "Tritt nur auf sichere Steine.",
        "question": "Summe aller Primfaktoren von 42? (42 = 2 × 3 × 7)",
        "answer": "12",
        "puzzle_piece": "🧩 Puzzleteil 11: 'BRIDGE-CODE: 12'",
        "hint": "2 + 3 + 7 = 12."
    },
    12: {
        "person": "Person C",
        "title": "Tag 12: Der Werkstatteingang",
        "type": "text",
        "image": None,
        "story": "Das Tor zur Werkstatt steht vor euch.",
        "question": "Tor-Code: Tag 9 + Tag 11.",
        "answer": "NORD12",
        "puzzle_piece": "🧩 Puzzleteil 12: 'MAIN-GATE: CLEAR'",
        "hint": "NORD + 12"
    },
    13: {
        "person": "Person A",
        "title": "Tag 13: Der Maschinensaal",
        "type": "text",
        "image": None,
        "story": "Die Zahnräder klemmen.",
        "question": "Zahnräder mit 12, 18, 24 Zähnen. Wie viele Umdrehungen macht Rad 1 (12 Zähne) bis alle wieder gleich stehen?",
        "answer": "6",
        "puzzle_piece": "🧩 Puzzleteil 13: 'GEAR-RATIO: 6'",
        "hint": "kgV(12,18,24) = 72. 72 / 12 = 6."
    },
    14: {
        "person": "Person B",
        "title": "Tag 14: Chaos in der Packstation",
        "type": "text",
        "image": None,
        "story": "Sortiere die Durcheinander geworfenen Buchstaben.",
        "question": "Entferne 'MAGIE' aus 'ELFENMAGIE'. Welches Wort bleibt?",
        "answer": "ELFEN",
        "puzzle_piece": "🧩 Puzzleteil 14: 'AUTH: ELFEN'",
        "hint": "E-L-F-E-N-M-A-G-I-E minus M-A-G-I-E."
    },
    15: {
        "person": "Person C",
        "title": "Tag 15: Das Rentier-Kraftfutter",
        "type": "text",
        "image": None,
        "story": "Mische das Futter im richtigen Verhältnis.",
        "question": "Verhältnis 5:2:3 (Hafer:Sternenstaub:Äpfel). Bei 50 kg Gesamtmenge: Wie viel kg Sternenstaub?",
        "answer": "10",
        "puzzle_piece": "🧩 Puzzleteil 15: 'DUST-AMOUNT: 10KG'",
        "hint": "50kg / 10 Teile = 5kg pro Teil. 2 Teile = 10kg."
    },
    16: {
        "person": "Person A",
        "title": "Tag 16: Batterien-Schalttafel",
        "type": "binary_switches",
        "image": None,
        "story": "Die Hauptenergie muss freigeschaltet werden.",
        "question": "Stelle die 5 Schalter so ein, dass sie binär der Zahl 25 entsprechen.",
        "answer": [True, True, False, False, True],
        "puzzle_piece": "🧩 Puzzleteil 16: 'POWER: 25-KW'",
        "hint": "16 + 8 + 1 = 25 (Ein, Ein, Aus, Aus, Ein)."
    },
    17: {
        "person": "Person B",
        "title": "Tag 17: Die Wunschzettel-Maschine",
        "type": "text",
        "image": None,
        "story": "Kalibriere den Daten-Sortierer.",
        "question": "Median der Reihe: 12, 45, 7, 23, 89, 34, 19?",
        "answer": "23",
        "puzzle_piece": "🧩 Puzzleteil 17: 'DATA-MEDIAN: 23'",
        "hint": "Sortiert: 7, 12, 19, [23], 34, 45, 89."
    },
    18: {
        "person": "Person C",
        "title": "Tag 18: Das Werkstatt-Schloss",
        "type": "text",
        "image": None,
        "story": "Sichere das System ab.",
        "question": "Rechne: (Tag 13: 6) × (Tag 15: 10) + (Tag 17: 23)",
        "answer": "83",
        "puzzle_piece": "🧩 Puzzleteil 18: 'SEC-CODE: 83'",
        "hint": "6 * 10 + 23 = 83."
    },
    19: {
        "person": "Person A",
        "title": "Tag 19: Flugrouten-Kalkulation",
        "type": "text",
        "image": None,
        "story": "Berechne die optimalen Fluglinien.",
        "question": "Kürzeste Strecke (in km), um alle 4 Ecken eines 100x100km Quadrats zu besuchen?",
        "answer": "300",
        "puzzle_piece": "🧩 Puzzleteil 19: 'DIST: 300-KM'",
        "hint": "3 Seiten des Quadrats: 100 + 100 + 100 = 300."
    },
    20: {
        "person": "Person B",
        "title": "Tag 20: Polarlichter-Frequenz",
        "type": "text",
        "image": None,
        "story": "Kopple den Schlitten an die Polarlichter an.",
        "question": "Übersetze den Morsecode '••• / --- / •••'",
        "answer": "SOS",
        "puzzle_piece": "🧩 Puzzleteil 20: 'LINK: ESTABLISHED'",
        "hint": "S-O-S"
    },
    21: {
        "person": "Person C",
        "title": "Tag 21: Rentiere anspannen",
        "type": "text",
        "image": None,
        "story": "Berechne die Aufstellung der Rentiere.",
        "question": "Wie viele Anordnungen gibt es für 7 Rentiere hinter Rudolph? (7!)",
        "answer": "5040",
        "puzzle_piece": "🧩 Puzzleteil 21: 'FORMATION: 5040'",
        "hint": "7 × 6 × 5 × 4 × 3 × 2 × 1 = 5040."
    },
    22: {
        "person": "Person A",
        "title": "Tag 22: Frachtraum-Ausgleich",
        "type": "text",
        "image": None,
        "story": "Der Schlitten benötigt die finale Gewichtsanpassung.",
        "question": "Geladen: (3 × 150 kg) + (4 × 110 kg). Wie viel kg fehlen bis exakt 1000 kg?",
        "answer": "110",
        "puzzle_piece": "🧩 Puzzleteil 22: 'WEIGHT: 110-KG'",
        "hint": "1000 - 890 = 110."
    },
    23: {
        "person": "Person B",
        "title": "Tag 23: Finale Startbereitschaft",
        "type": "text",
        "image": None,
        "story": "Der Weihnachts-Countdown läuft!",
        "question": "Rechne: (Tag 3: 500) + (Tag 18: 83)",
        "answer": "583",
        "puzzle_piece": "🧩 Puzzleteil 23: 'FINAL-KEY: 583'",
        "hint": "500 + 83 = 583."
    },
    24: {
        "person": "Alle 3 gemeinsam",
        "title": "Tag 24: HEILIGABEND – Der Master-Code!",
        "type": "text",
        "image": "https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=600&q=80",
        "story": "Ihr steht im Hauptkontrollraum! Auf den Monitoren blinkt die Aufforderung zur Eingabe des Master-Codes.",
        "question": "Kombiniert: Code Tag 3 (500) + Code Tag 12 (NORD12) + Code Tag 23 (583)",
        "answer": "500NORD12583",
        "puzzle_piece": "🏆 MEISTER-TITEL: RETTER VON WEIHNACHTEN!",
        "hint": "Setze die Codes ohne Leerzeichen zusammen."
    }
}

# ==============================================================================
# 3. SESSION STATE
# ==============================================================================
if "solved_doors" not in st.session_state:
    st.session_state.solved_doors = []

if "active_day" not in st.session_state:
    st.session_state.active_day = 1

# ==============================================================================
# 4. KOPFZEILE & FORTSCHRITT
# ==============================================================================
st.title("❄️ Nordpol-Expedition 2026")
st.caption("Ein mathematisch-logisches Escape-Abenteuer")

col_prog, col_stats = st.columns([3, 1])
with col_prog:
    progress = len(st.session_state.solved_doors) / 24
    st.progress(progress)
with col_stats:
    st.write(f"**Gefundene Puzzleteile:** {len(st.session_state.solved_doors)} / 24")

st.divider()

# ==============================================================================
# 5. TÜRCHEN-GRID
# ==============================================================================
cols = st.columns(6)
for i in range(1, 25):
    col = cols[(i - 1) % 6]
    if i in st.session_state.solved_doors:
        label = f"✓ Tag {i}"
    elif i == 24:
        label = f"★ Tag {i}"
    else:
        label = f"Tag {i}"
        
    if col.button(label, key=f"btn_{i}"):
        st.session_state.active_day = i

st.divider()

# ==============================================================================
# 6. RÄTSEL-FLÄCHE & PUZZLE-SAMMLUNG
# ==============================================================================
main_col, puzzle_col = st.columns([2, 1])

with main_col:
    day = st.session_state.active_day
    door = DOORS[day]

    st.subheader(f"{door['title']}")
    st.caption(f"Verantwortlich: **{door['person']}**")
    
    # Optionales Bild anzeigen
    if door["image"]:
        st.image(door["image"], use_column_width=True)
        
    st.info(f"📖 {door['story']}")
    st.markdown(f"**Aufgabe:** {door['question']}")

    # Eingabe-Logik
    if door["type"] == "lock_sliders":
        st.write("⚙️ **Stelle die Regler an der Schatulle ein:**")
        c1, c2, c3, c4 = st.columns(4)
        v1 = c1.number_input("R1", 0, 9, 0, key="n1")
        v2 = c2.number_input("R2", 0, 9, 0, key="n2")
        v3 = c3.number_input("R3", 0, 9, 0, key="n3")
        v4 = c4.number_input("R4", 0, 9, 0, key="n4")
        
        if st.button("Schloss prüfen 🗝️"):
            if [v1, v2, v3, v4] == door["answer"]:
                st.success("🎉 Das Schloss springt auf!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Das Schloss bleibt blockiert.")

    elif door["type"] == "binary_switches":
        st.write("⚡ **Kippschalter-Panel:**")
        b1, b2, b3, b4, b5 = st.columns(5)
        s1 = b1.checkbox("Schalter 1", key="cb1")
        s2 = b2.checkbox("Schalter 2", key="cb2")
        s3 = b3.checkbox("Schalter 3", key="cb3")
        s4 = b4.checkbox("Schalter 4", key="cb4")
        s5 = b5.checkbox("Schalter 5", key="cb5")
        
        if st.button("Schaltkreis aktivieren ⚡"):
            if [s1, s2, s3, s4, s5] == door["answer"]:
                st.success("🎉 Schaltung korrekt!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsche Schaltkombination.")

    elif door["type"] == "audio_morse":
        st.audio("https://upload.wikimedia.org/wikipedia/commons/1/1d/SOS_morse_code.ogg")
        ans = st.text_input("Gefundener Code:", key=f"input_{day}")
        if st.button("Code senden 📡"):
            if ans.strip().upper() == door["answer"]:
                st.success("🎉 Signal verifiziert!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsches Signal.")

    else:
        ans = st.text_input("Deine Lösung:", key=f"input_{day}")
        if st.button("Prüfen 🔍"):
            if ans.strip().upper() == door["answer"].upper():
                st.success("🎉 Richtig gelöst!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Das ist leider nicht korrekt.")

    with st.expander("💡 Hinweis anzeigen"):
        st.write(door["hint"])

# ------------------------------------------------------------------------------
# PUZZLETEIL-SAMMLUNG (SEITENLEISTE RECHTS)
# ------------------------------------------------------------------------------
with puzzle_col:
    st.subheader("🧩 Eure Puzzleteile")
    st.caption("Freigeschaltete Hinweise für Tag 24:")
    
    if not st.session_state.solved_doors:
        st.write("*Noch keine Puzzleteile gesammelt. Löst euer erstes Rätsel!*")
    else:
        # Sortiert anzeigen
        for d in sorted(st.session_state.solved_doors):
            st.markdown(f"<div class='puzzle-card'><b>Tag {d}:</b><br>{DOORS[d]['puzzle_piece']}</div>", unsafe_allow_html=True)
