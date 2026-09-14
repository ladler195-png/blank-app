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

# Sehr dunkles Tannengrün (#0b1b10) + warmes Weihnachts-Gold (#d69e2e)
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
# 2. RÄTSEL- DATENBANK (Puzzleteile nur im Labyrinth: Tage 5, 7, 8, 9, 10, 11)
# ==============================================================================
DOORS = {
    1: {
        "person": "Person A",
        "title": "Tag 1: Die mysteriöse Holzbox",
        "type": "lock_sliders",
        "image": None,
        "story": "Es klingelt an der Haustür. Ihr öffnet, aber niemand ist da stattdessen liegt auf der Fußmatte eine schwere, eisige Holzbox mit dem Absender „Nordpol“. Auf dem Deckel prangt ein massives Zahlenschloss und ein eingravierter Reimgedicht-Hinweis.",
        "question": "Knacke das 4-stellige Zahlenschloss mithilfe des Reims:
        \n\n> *„Vier kleine Ziffern im winterlichen Schnee,
        \n> hör gut zu, was ich dir steh:\n> Nimm die Ecken eines weisen Weihnachtssterns,
        \n> plus die treuen Rentiere des Nordpols fern.
        \n> Multipliziere das Ganze mit zwei,\n> dann ist die erste Hürde vorbei.“*",
        "answer": [0, 0, 2, 6],
        "puzzle_piece": None,
        "hint": "Ein Weihnachtsstern hat 5 Ecken. Es gibt 8 Rentiere. Rechne (5 + 8) * 2 "
    },
    2: {
        "person": "Person B",
        "title": "Tag 2: Das vergilbte Pergament",
        "type": "text",
        "image": None,
        "story": "Das Schloss der Holzbox springt auf! Ihr öffnet den Deckel und findet im Inneren ein altes, steif gefrorenes Pergament mit einer Elfen-Chiffre: *„SIVX“*.",
        "question": "Entschlüssele das Codewort: 'SIVX'. Wie lautet das Lösungswort?",
        "answer": "NORD",
        "puzzle_piece": None,
        "hint": "Cäsar-Chiffre, 4 Stellen im Alphabet zurückschieben"
    },
    3: {
        "person": "Person C",
        "title": "Tag 3: Konsole des Schlittens",
        "type": "text",
        "image": None,
        "story": "Die Armaturen des Elfen-Schlittens müssen synchronisiert werden.",
        "question": "Berechne die Frequenz: (8 Rentiere) × (Code Tag 1: 63) - 4",
        "answer": "500",
        "puzzle_piece": None,
        "hint": "8 * 63 - 4 = 500"
    },
    4: {
        "person": "Person A",
        "title": "Tag 4: Sternenkarte",
        "type": "text",
        "image": None,
        "story": "Das Navigationssystem fordert die Eingabe des Kurses.",
        "question": "Addiere alle Primzahlen zwischen 10 und 25 (11, 13, 17, 19, 23).",
        "answer": "83",
        "puzzle_piece": None,
        "hint": "11 + 13 + 17 + 19 + 23 = 83"
    },
    # --- START NEBEL-LABYRINTH (Tage 5 - 11 sammeln 6 Puzzleteile) ---
    5: {
        "person": "Person B",
        "title": "Tag 5: Eingang zum Nebel-Labyrinth 🌀",
        "type": "text",
        "image": None,
        "story": "Ihr betretet das Nebel-Labyrinth. Hier verstecken sich 6 wertvolle Labyrinth-Scherben!",
        "question": "Kombiniere Tag 2 (NORD) + Tag 4 (83) ohne Leerzeichen.",
        "answer": "NORD83",
        "puzzle_piece": "🧩 Labyrinth-Teil 1: 'KARTEN-FRAGMENT ALPHA'",
        "hint": "NORD + 83"
    },
    6: {
        "person": "Person C",
        "title": "Tag 6: Nikolaus-Schrein im Labyrinth",
        "type": "text",
        "image": None,
        "story": "Ein steinerner Schrein versperrt eine Weggabelung im Nebel.",
        "question": "Welche Zahl steht in der Mitte (Feld X) eines magischen 3x3-Quadrats (Zahlen 1-9)?",
        "answer": "5",
        "puzzle_piece": None,
        "hint": "Die Zahl 5 steht im magischen Quadrat immer im Zentrum."
    },
    7: {
        "person": "Person A",
        "title": "Tag 7: Die Pfad-Verzweigung",
        "type": "text",
        "image": None,
        "story": "Vier Pfade tun sich auf. Das Eismuster am Boden weist den Weg.",
        "question": "Welche Pfadnummer folgt? 3, 6, 11, 18, 27, __",
        "answer": "38",
        "puzzle_piece": "🧩 Labyrinth-Teil 2: 'KOMPASS-Richtung RECHTS'",
        "hint": "+3, +5, +7, +9, +11..."
    },
    8: {
        "person": "Person B",
        "title": "Tag 8: Das Gletscher-Echo",
        "type": "text",
        "image": None,
        "story": "Ein verzerrendes Echosignal hallt durch die Nebelwände.",
        "question": "Wie lautet das Notsignal bei Schiffen/Expeditionen?",
        "answer": "SOS",
        "puzzle_piece": "🧩 Labyrinth-Teil 3: 'NOTFALL-SIGNAL S.O.S'",
        "hint": "Drei Buchstaben: S-O-S"
    },
    9: {
        "person": "Person C",
        "title": "Tag 9: Der Lichtstrahl-Spiegelpfad 🔦",
        "type": "mirror_puzzle",
        "image": None,
        "story": "Richte die Spiegel so aus, dass der Lichtstrahl durch das Nebel-Labyrinth geleitet wird!",
        "question": "Klicke auf die Spiegel, um sie zu drehen, bis der Laserstrahl den Kristallsensor trifft.",
        "answer": "SOLVED",
        "puzzle_piece": "🧩 Labyrinth-Teil 4: 'OPTISCHE LINSE NORD'",
        "hint": "Der Strahl startet nach OSTE (rechts), wird nach NORDEN (oben) abgelenkt, geht dann weiter."
    },
    10: {
        "person": "Person A",
        "title": "Tag 10: Der gefrorene Kompass",
        "type": "text",
        "image": None,
        "story": "Justiere die Kompassnadel tiefer im Labyrinth.",
        "question": "Berechne den Rest der Division (Modulo): 2713 Modulo 360",
        "answer": "193",
        "puzzle_piece": "🧩 Labyrinth-Teil 5: 'WINKEL-GRAD 193°'",
        "hint": "2713 mod 360 = 193."
    },
    11: {
        "person": "Person B",
        "title": "Tag 11: Die Eisbrücke des Labyrinths",
        "type": "text",
        "image": None,
        "story": "Tritt nur auf die tragenden Eissteine, um die Schlucht zu überqueren.",
        "question": "Summe aller Primfaktoren von 42 (42 = 2 × 3 × 7)?",
        "answer": "12",
        "puzzle_piece": "🧩 Labyrinth-Teil 6: 'BRÜCKEN-SCHLÜSSEL 12'",
        "hint": "2 + 3 + 7 = 12."
    },
    # --- ENDE LABYRINTH / HAUPTTOR ---
    12: {
        "person": "Person C",
        "title": "Tag 12: Der Ausgang – Werkstatt-Haupttor 🚪",
        "type": "text",
        "image": None,
        "story": "Ihr habt den Labyrinth-Ausgang erreicht! Aber das Haupttor benötigt das vereinte Labyrinth-Wissen (Teil 1 bis 6).",
        "question": "Kombination: Wort aus Tag 9 (NORD) + Summe aus Tag 11 (12).",
        "answer": "NORD12",
        "puzzle_piece": None,
        "hint": "NORD12"
    },
    13: {
        "person": "Person A",
        "title": "Tag 13: Das Zahnrad-Getriebe ⚙️",
        "type": "gear_puzzle",
        "image": None,
        "story": "Die Hauptzahnräder der Werkstatt klemmen! Dreht die Übersetzung manuell.",
        "question": "Stelle die benötigte Umdrehung des 12er-Rads ein, damit alle Markierungen wieder synchron stehen (kgV von 12, 18, 24).",
        "answer": 6,
        "puzzle_piece": None,
        "hint": "72 / 12 = 6 Umdrehungen."
    },
    14: {
        "person": "Person B",
        "title": "Tag 14: Chaos in der Packstation",
        "type": "text",
        "image": None,
        "story": "Sortiere die Durcheinander geworfenen Buchstaben.",
        "question": "Entferne alle Buchstaben von 'MAGIE' aus 'ELFENMAGIE'. Welcher Name bleibt übrig?",
        "answer": "ELFEN",
        "puzzle_piece": None,
        "hint": "ELFENMAGIE - MAGIE = ELFEN."
    },
    15: {
        "person": "Person C",
        "title": "Tag 15: Rentierfutter-Mischstation ⚖️",
        "type": "scale_puzzle",
        "image": None,
        "story": "Mische das Futter auf der Balkenwaage im genauen Verhältnis (5 Teile Hafer : 2 Teile Sternenstaub : 3 Teile Äpfel).",
        "question": "Stellt die Schieberegler so ein, dass exakt 50 kg Futter angemischt werden.",
        "answer": {"hafer": 25, "staub": 10, "aepfel": 15},
        "puzzle_piece": None,
        "hint": "Hafer = 25 kg, Sternenstaub = 10 kg, Äpfel = 15 kg."
    },
    16: {
        "person": "Person A",
        "title": "Tag 16: Schalttafel für Notstrom",
        "type": "binary_switches",
        "image": None,
        "story": "Die Hauptenergie muss freigeschaltet werden. Stellt die Binärzahl 25 ein.",
        "question": "Aktiviert die richtigen Schalter für den Gesamtwert 25 (16 + 8 + 1).",
        "answer": [True, True, False, False, True],
        "puzzle_piece": None,
        "hint": "Schalter 1 (16) = EIN, Schalter 2 (8) = EIN, Schalter 5 (1) = EIN."
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
        "story": "Der Funkempfänger ist verstellt! Findet die exakte Resonanzfrequenz der Polarlichter.",
        "question": "Richtet das Frequenz-Widget genau auf 87.5 MHz aus.",
        "answer": 87.5,
        "puzzle_piece": None,
        "hint": "Stellt den Schieberegler exakt auf 87.5 MHz."
    },
    21: {
        "person": "Person C",
        "title": "Tag 21: Rentiere anspannen",
        "type": "text",
        "image": None,
        "story": "Berechne die Aufstellung der Rentiere.",
        "question": "Wie viele unterschiedliche Anordnungen gibt es für 7 Rentiere hinter Rudolph? (Fakultät von 7 = 7!)",
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
        "question": "Geladen: (3 × 150 kg) + (4 × 110 kg) = 890 kg. Wie viel kg fehlen bis zu den geforderten 1000 kg?",
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
        "question": "Rechne: (Tag 3: 500) + (Tag 18: 83)",
        "answer": "583",
        "puzzle_piece": None,
        "hint": "500 + 83 = 583."
    },
    24: {
        "person": "Alle 3 gemeinsam",
        "title": "Tag 24: HEILIGABEND – Der Master-Code!",
        "type": "text",
        "image": "https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=600&q=80",
        "story": "Ihr steht im Hauptkontrollraum! Auf den Monitoren blinkt die Aufforderung zur Eingabe des Master-Codes.",
        "question": "Fügt zusammen: Code Tag 3 (500) + Code Tag 12 (NORD12) + Code Tag 23 (583)",
        "answer": "500NORD12583",
        "puzzle_piece": "🏆 MEISTER-TITEL: RETTER VON WEIHNACHTEN!",
        "hint": "Schreibe die drei Teilstücke genau so hintereinander: 500NORD12583"
    }
}

# ==============================================================================
# 3. SESSION STATE
# ==============================================================================
if "solved_doors" not in st.session_state:
    st.session_state.solved_doors = []

if "active_day" not in st.session_state:
    st.session_state.active_day = 1

if "mirror_state" not in st.session_state:
    st.session_state.mirror_state = ["\\", "/", "\\"]

# ==============================================================================
# 4. KOPFZEILE & FORTSCHRITT
# ==============================================================================
st.title("🎄 Nordpol-Expedition 2026")
st.caption("Das mathematisch-logische Advents-Abenteuer")

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
    
    # Optische Markierung für Labyrinth-Tage (5-11)
    if 5 <= i <= 11:
        prefix = "🌀 "
    else:
        prefix = ""
        
    if i in st.session_state.solved_doors:
        label = f"🎁 {prefix}Tag {i}"
    else:
        label = f"{prefix}Tag {i}"
        
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

    # --- RÄTSEL-WIDGETS ---

    # A) WIDGET TAG 9: Interaktiver 2D-Lichtstrahl & Spiegelpfad
    if door["type"] == "mirror_puzzle":
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

        # Visuelle Feedback-Vorschau des Strahls
        if st.session_state.mirror_state == ["/", "\\", "/"]:
            st.success("🟢 Strahlenverlauf: Ost ➔ Nord ➔ Ost ➔ Nord (Ziel getroffen!)")
            if st.button("Lichtstrahl aktivieren 🔦", key=f"chk_{day}"):
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
        else:
            st.warning("🔴 Strahl wird noch an den Nebelwänden reflektiert.")

    # B) WIDGET TAG 13: Interaktive Zahnrad-Simulation
    elif door["type"] == "gear_puzzle":
        rot = st.slider("⚙️ Umdrehungen des 12er-Rads:", 1, 12, 1, key="rot_slider")
        st.write(f"Rad 1 (12 Zähne): **{rot}** Umdrehungen")
        st.write(f"Rad 2 (18 Zähne): **{rot * 12 / 18:.2f}** Umdrehungen")
        st.write(f"Rad 3 (24 Zähne): **{rot * 12 / 24:.2f}** Umdrehungen")
        
        if st.button("Zahnräder einrasten ⚙️", key=f"chk_{day}"):
            if rot == door["answer"]:
                st.success("🎉 Alle Zahnräder stehen synchron auf Startposition!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Die Zähne stehen nicht auf der Markierung.")

    # C) WIDGET TAG 15: Interaktive Balkenwaage & Mischstation
    elif door["type"] == "scale_puzzle":
        st.write("⚖️ **Mischungs-Waage (Gesamtgewicht muss exakt 50 kg sein):**")
        w_hafer = st.slider("🌾 Hafer (kg)", 0, 50, 20, key="w_h")
        w_staub = st.slider("✨ Sternenstaub (kg)", 0, 50, 5, key="w_s")
        w_aepfel = st.slider("🍎 Äpfel (kg)", 0, 50, 10, key="w_a")
        
        total = w_hafer + w_staub + w_aepfel
        st.metric(label="Gesamtgewicht", value=f"{total} kg / 50 kg")
        
        if st.button("Futter-Mischung wiegen ⚖️", key=f"chk_{day}"):
            if w_hafer == 25 and w_staub == 10 and w_aepfel == 15:
                st.success("🎉 Perfektes Mischungsverhältnis! Die Rentiere sind begeistert.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Das Mischungsverhältnis oder Gesamtgewicht stimmt noch nicht.")

    # D) Zahlen-Sliders (Tag 1)
    elif door["type"] == "lock_sliders":
        c1, c2, c3, c4 = st.columns(4)
        v1 = c1.number_input("Stelle 1", 0, 9, 0, key=f"n1_{day}")
        v2 = c2.number_input("Stelle 2", 0, 9, 0, key=f"n2_{day}")
        v3 = c3.number_input("Stelle 3", 0, 9, 0, key=f"n3_{day}")
        v4 = c4.number_input("Stelle 4", 0, 9, 0, key=f"n4_{day}")
        
        if st.button("Schloss prüfen 🗝️", key=f"chk_{day}"):
            if [int(v1), int(v2), int(v3), int(v4)] == door["answer"]:
                st.success("🎉 Das Schloss springt auf!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Das Schloss bleibt blockiert.")

    # E) Binär-Kippschalter (Tag 16)
    elif door["type"] == "binary_switches":
        b1, b2, b3, b4, b5 = st.columns(5)
        s1 = b1.checkbox("Schalter 1 (Wert 16)", key="cb1")
        s2 = b2.checkbox("Schalter 2 (Wert 8)", key="cb2")
        s3 = b3.checkbox("Schalter 3 (Wert 4)", key="cb3")
        s4 = b4.checkbox("Schalter 4 (Wert 2)", key="cb4")
        s5 = b5.checkbox("Schalter 5 (Wert 1)", key="cb5")
        
        if st.button("Schaltkreis aktivieren ⚡", key=f"chk_{day}"):
            if [s1, s2, s3, s4, s5] == door["answer"]:
                st.success("🎉 Schaltung korrekt!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsche Schaltkombination.")

    # F) Interaktives Frequenz-Widget (Tag 20)
    elif door["type"] == "frequency_tuner":
        freq = st.slider("📻 Polarlichter-Empfänger (MHz):", 80.0, 100.0, 92.0, step=0.5, key="freq_slider")
        if st.button("Signal-Frequenz feststellen 📡", key=f"chk_{day}"):
            if abs(freq - door["answer"]) < 0.1:
                st.success("🎉 Glasklarer Empfang!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Nur Rauschen zu hören.")

    # G) Standard-Text-Eingabe
    else:
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
                st.error("❌ Das ist leider nicht korrekt.")

    with st.expander("💡 Hinweis anzeigen"):
        st.write(door["hint"])

# ------------------------------------------------------------------------------
# LABYRINTH-PUZZLE-SAMMLUNG (RECHTE SEITENLEISTE)
# ------------------------------------------------------------------------------
with puzzle_col:
    st.subheader("🌀 Labyrinth-Puzzleteile")
    st.caption("Sammlertasche für das Haupttor (Tag 12):")
    
    # Filtere alle gelösten Labyrinth-Puzzleteile
    lab_pieces = [d for d in st.session_state.solved_doors if DOORS[d]["puzzle_piece"]]
    
    if not lab_pieces:
        st.write("*Noch keine Puzzleteile im Nebel-Labyrinth gefunden.*")
    else:
        for d in sorted(lab_pieces):
            st.markdown(f"<div class='puzzle-card'><b>Tag {d}:</b><br>{DOORS[d]['puzzle_piece']}</div>", unsafe_allow_html=True)
            
    st.write("---")
    st.metric("Gefundene Labyrinth-Teile", f"{len(lab_pieces)} / 6")
