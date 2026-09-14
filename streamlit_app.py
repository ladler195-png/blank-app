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
    /* Haupthintergrund: Sehr dunkles Tannengrün */
    .stApp {
        background-color: #0b1b10;
        color: #e2e8f0;
        font-family: 'Georgia', serif;
    }
    
    /* Warmgoldene Überschriften */
    h1, h2, h3 {
        color: #d69e2e !important;
        font-family: 'Georgia', serif;
        font-weight: normal;
        letter-spacing: 1px;
    }

    /* Subtile, edle Buttons */
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

    /* Infoboxen & Karten */
    .stAlert {
        border-radius: 8px;
        background-color: rgba(20, 46, 29, 0.7);
        border: 1px solid #2d5a3a;
    }
    
    .puzzle-card {
        border: 1px dashed #d69e2e;
        padding: 12px;
        border-radius: 8px;
        background-color: rgba(214, 158, 46, 0.08);
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Dezent rieselnde Schneeflocken
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
# 2. RÄTSEL- DATENBANK
# ==============================================================================
DOORS = {
    1: {
        "person": "Person A",
        "title": "Tag 1: Die verschlossene Kiste",
        "type": "lock_sliders",
        "image": "https://images.unsplash.com/photo-1543257580-7269da773bf5?w=600&q=80",
        "story": "Eine Holzschatulle liegt im Schnee. Auf dem Deckel ist eine Zahlenreihe eingraviert.",
        "question": "Löse die Reihe: 3, 7, 15, 31, __. Stelle das 4-stellige Zahlenschloss (z.B. 0-0-6-3) passend ein.",
        "answer": [0, 0, 6, 3],
        "puzzle_piece": "🧩 Puzzleteil 1: 'KOORDINATE NORD: 78°'",
        "hint": "Zahlenabstände verdoppeln sich (+4, +8, +16, +32). Die gesuchte Zahl ist 63."
    },
    2: {
        "person": "Person B",
        "title": "Tag 2: Das vergilbte Pergament",
        "type": "text",
        "image": "https://images.unsplash.com/photo-1516962215378-7fa2e137ae93?w=600&q=80",
        "story": "In der Kiste liegt eine alte Elfen-Chiffre.",
        "question": "Entschlüssele das Codewort (Cäsar-Chiffre, 4 Stellen zurück im Alphabet): 'SIVX'",
        "answer": "NORD",
        "puzzle_piece": "🧩 Puzzleteil 2: 'SYMBOL: 🧭 KOMPASS'",
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
        "question": "Addiere alle Primzahlen zwischen 10 und 25 (11, 13, 17, 19, 23).",
        "answer": "83",
        "puzzle_piece": "🧩 Puzzleteil 4: 'KURS: 83° OST'",
        "hint": "11 + 13 + 17 + 19 + 23 = 83"
    },
    5: {
        "person": "Person B",
        "title": "Tag 5: Die Nebelwand",
        "type": "text",
        "image": None,
        "story": "Vor euch baut sich das undurchdringliche Nebel-Labyrinth auf.",
        "question": "Kombiniere Tag 2 (NORD) + Tag 4 (83) ohne Leerzeichen.",
        "answer": "NORD83",
        "puzzle_piece": "🧩 Puzzleteil 5: 'GATE-KEY: NORD83'",
        "hint": "NORD + 83"
    },
    6: {
        "person": "Person C",
        "title": "Tag 6: Nikolaus-Schrein",
        "type": "text",
        "image": None,
        "story": "Ein steinerner Schrein versperrt den Pfad.",
        "question": "Welche Zahl steht in der Mitte (Feld X) eines magischen 3x3-Quadrats (Zahlen 1-9)?",
        "answer": "5",
        "puzzle_piece": "🧩 Puzzleteil 6: 'SIGIL: 5-STERNE'",
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
        "puzzle_piece": "🧩 Puzzleteil 7: 'PFAD: RECHTS-38'",
        "hint": "+3, +5, +7, +9, +11..."
    },
    8: {
        "person": "Person B",
        "title": "Tag 8: Das Gletscher-Echo",
        "type": "text",
        "image": None,
        "story": "Ein verzerrendes Echosignal hallt aus den Höhlen.",
        "question": "Wie lautet das Notsignal bei Schiffen/Expeditionen?",
        "answer": "SOS",
        "puzzle_piece": "🧩 Puzzleteil 8: 'SIGNAL: S.O.S'",
        "hint": "Drei Buchstaben: S-O-S"
    },
    9: {
        "person": "Person C",
        "title": "Tag 9: Die Spiegel-Grotte",
        "type": "text",
        "image": None,
        "story": "Lenke den Lichtstrahl ab.",
        "question": "Strahl startet OST. Spiegel-Reihenfolge: Links, Rechts, Links. Wohin zeigt der Strahl am Ende?",
        "answer": "NORD",
        "puzzle_piece": "🧩 Puzzleteil 9: 'SPIEGEL: NORD'",
        "hint": "Ost -> Links(Nord) -> Rechts(Ost) -> Links(Nord)."
    },
    10: {
        "person": "Person A",
        "title": "Tag 10: Der gefrorene Kompass",
        "type": "text",
        "image": None,
        "story": "Justiere die Kompassnadel.",
        "question": "Berechne den Rest der Division (Modulo): 2713 Modulo 360",
        "answer": "193",
        "puzzle_piece": "🧩 Puzzleteil 10: 'GRAD: 193°'",
        "hint": "2713 mod 360 = 193."
    },
    11: {
        "person": "Person B",
        "title": "Tag 11: Die Eisbrücke",
        "type": "text",
        "image": None,
        "story": "Tritt nur auf sichere Steine.",
        "question": "Summe aller Primfaktoren von 42 (42 = 2 × 3 × 7)?",
        "answer": "12",
        "puzzle_piece": "🧩 Puzzleteil 11: 'BRÜCKEN-CODE: 12'",
        "hint": "2 + 3 + 7 = 12."
    },
    12: {
        "person": "Person C",
        "title": "Tag 12: Der Werkstatteingang",
        "type": "text",
        "image": None,
        "story": "Das Tor zur Werkstatt steht vor euch.",
        "question": "Kombination: Tag 9 (NORD) + Tag 11 (12).",
        "answer": "NORD12",
        "puzzle_piece": "🧩 Puzzleteil 12: 'HAUPTTOR: OFFEN'",
        "hint": "NORD12"
    },
    13: {
        "person": "Person A",
        "title": "Tag 13: Der Maschinensaal",
        "type": "text",
        "image": None,
        "story": "Die Zahnräder klemmen.",
        "question": "Drei Zahnräder mit 12, 18 und 24 Zähnen. Wie viele Umdrehungen macht Rad 1 (12 Zähne), bis alle wieder in der Startposition sind?",
        "answer": "6",
        "puzzle_piece": "🧩 Puzzleteil 13: 'ZAHNRAD-RATIO: 6'",
        "hint": "kgV(12,18,24) = 72. 72 / 12 = 6 Umdrehungen."
    },
    14: {
        "person": "Person B",
        "title": "Tag 14: Chaos in der Packstation",
        "type": "text",
        "image": None,
        "story": "Sortiere die Durcheinander geworfenen Buchstaben.",
        "question": "Entferne alle Buchstaben von 'MAGIE' aus 'ELFENMAGIE'. Welcher Name bleibt übrig?",
        "answer": "ELFEN",
        "puzzle_piece": "🧩 Puzzleteil 14: 'SCHLÜSSEL: ELFEN'",
        "hint": "E-L-F-E-N-M-A-G-I-E minus M-A-G-I-E = ELFEN."
    },
    15: {
        "person": "Person C",
        "title": "Tag 15: Das Rentier-Kraftfutter",
        "type": "text",
        "image": None,
        "story": "Mische das Futter im richtigen Verhältnis.",
        "question": "Verhältnis 5:2:3 (Hafer : Sternenstaub : Äpfel). Bei 50 kg Gesamtmenge: Wie viel kg Sternenstaub werden benötigt?",
        "answer": "10",
        "puzzle_piece": "🧩 Puzzleteil 15: 'STERNENSTAUB: 10KG'",
        "hint": "50kg / 10 Teile = 5kg pro Teil. Sternenstaub = 2 Teile = 10kg."
    },
    16: {
        "person": "Person A",
        "title": "Tag 16: Schalttafel für Notstrom",
        "type": "binary_switches",
        "image": None,
        "story": "Die Hauptenergie muss freigeschaltet werden. Stellt die Binärzahl 25 ein.",
        "question": "Aktiviert die richtigen Schalter für den Gesamtwert 25 (16 + 8 + 1).",
        "answer": [True, True, False, False, True],
        "puzzle_piece": "🧩 Puzzleteil 16: 'ENERGIE: 25-KW'",
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
        "puzzle_piece": "🧩 Puzzleteil 17: 'MEDIAN-WERT: 23'",
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
        "puzzle_piece": "🧩 Puzzleteil 18: 'SICHERHEIT: 83'",
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
        "puzzle_piece": "🧩 Puzzleteil 19: 'DISTANZ: 300-KM'",
        "hint": "3 Kanten abfliegen: 100 + 100 + 100 = 300 km."
    },
    20: {
        "person": "Person B",
        "title": "Tag 20: Polarlichter-Frequenz",
        "type": "frequency_tuner",
        "image": None,
        "story": "Der Funkempfänger ist verstellt! Ihr müsst die exakte Resonanzfrequenz der Polarlichter finden.",
        "question": "Richtet das Frequenz-Widget genau auf 87.5 MHz aus, um das Signal aufzunehmen.",
        "answer": 87.5,
        "puzzle_piece": "🧩 Puzzleteil 20: 'RESONANZ: 87.5-MHZ'",
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
        "puzzle_piece": "🧩 Puzzleteil 21: 'FORMATION: 5040'",
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
        "puzzle_piece": "🧩 Puzzleteil 22: 'ZUSATZGEWICHT: 110-KG'",
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
        "puzzle_piece": "🧩 Puzzleteil 23: 'START-CODE: 583'",
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
    st.write(f"**Gesammelte Geschenke/Teile:** {len(st.session_state.solved_doors)} / 24")

st.divider()

# ==============================================================================
# 5. TÜRCHEN-GRID (MIT GESCHENK-ICON 🎁)
# ==============================================================================
cols = st.columns(6)
for i in range(1, 25):
    col = cols[(i - 1) % 6]
    if i in st.session_state.solved_doors:
        label = f"🎁 Tag {i}"
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
    
    if door["image"]:
        st.image(door["image"], use_column_width=True)
        
    st.info(f"📖 {door['story']}")
    st.markdown(f"**Aufgabe:** {door['question']}")

    # --- EINGABE-LOGIKEN (FEHLERFREI ABGESICHERT) ---

    # 1. Zahlen-Sliders (Tag 1)
    if door["type"] == "lock_sliders":
        st.write("⚙️ **Stelle die Rädchen an der Schatulle ein:**")
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

    # 2. Binär-Kippschalter (Tag 16)
    elif door["type"] == "binary_switches":
        st.write("⚡ **Schaltafel (Setzt die Binärschalter):**")
        b1, b2, b3, b4, b5 = st.columns(5)
        s1 = b1.checkbox("Schalter 1 (Wert 16)", key="cb1")
        s2 = b2.checkbox("Schalter 2 (Wert 8)", key="cb2")
        s3 = b3.checkbox("Schalter 3 (Wert 4)", key="cb3")
        s4 = b4.checkbox("Schalter 4 (Wert 2)", key="cb4")
        s5 = b5.checkbox("Schalter 5 (Wert 1)", key="cb5")
        
        if st.button("Schaltkreis aktivieren ⚡", key=f"chk_{day}"):
            if [s1, s2, s3, s4, s5] == door["answer"]:
                st.success("🎉 Schaltung korrekt! Der Notstrom läuft.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsche Summe/Schaltkombination.")

    # 3. Interaktives Frequenz-Widget (Tag 20 neu)
    elif door["type"] == "frequency_tuner":
        freq = st.slider("📻 Polarlichter-Empfänger (MHz):", 80.0, 100.0, 92.0, step=0.5, key="freq_slider")
        if st.button("Signal-Frequenz feststellen 📡", key=f"chk_{day}"):
            if abs(freq - door["answer"]) < 0.1:
                st.success("🎉 Das Knistern verschwindet! Glasklarer Empfang!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Nur leichtes Rauschen zu hören. Drehe weiter!")

    # 4. Standard Text-Antworten (Abgesichert für Tag 24)
    else:
        ans = st.text_input("Deine Lösung:", key=f"input_{day}")
        if st.button("Prüfen 🔍", key=f"chk_{day}"):
            # Entferne Leerzeichen & vergleiche case-insensitive
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
# PUZZLETEIL-SAMMLUNG (RECHTE SEITENLEISTE)
# ------------------------------------------------------------------------------
with puzzle_col:
    st.subheader("🧩 Eure Geschenke & Teile")
    st.caption("Freigeschaltete Hinweise für Tag 24:")
    
    if not st.session_state.solved_doors:
        st.write("*Noch keine Geschenke freigeschaltet. Löst euer erstes Rätsel!*")
    else:
        for d in sorted(st.session_state.solved_doors):
            st.markdown(f"<div class='puzzle-card'><b>Tag {d}:</b><br>{DOORS[d]['puzzle_piece']}</div>", unsafe_allow_html=True)
