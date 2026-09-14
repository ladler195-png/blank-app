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
        "story": "Es klingelt an der Haustür. Ihr öffnet, aber niemand ist da – stattdessen liegt auf der Fußmatte eine schwere, eisige Holzbox mit dem Absender „Nordpol“. Auf dem Deckel prangt ein massives Zahlenschloss und ein eingravierter Reimgedicht-Hinweis.",
        "question": "Knacke das 4-stellige Zahlenschloss mithilfe des Reims auf der Box:\n\n> *„Vier kleine Ziffern im winterlichen Schnee,\n> hör gut zu, was ich dir steh:\n> Nimm die Ecken eines weisen Weihnachtssterns,\n> plus die treuen Rentiere des Nordpols fern.\n> Multipliziere das Ganze mit zwei,\n> dann ist die erste Hürde vorbei.“*\n\n**Eingabe:** Tippe das Ergebnis als vierstellige Zahl ein (z.B. 1234).",
        "answer": [0, 0, 2, 6],
        "puzzle_piece": None,
        "hint": "Zähle die Zacken eines klassischen Weihnachtssterns und überlege, wie viele Rentiere vor dem Schlitten stehen. Verdopple diese Summe."
    },
    2: {
        "person": "Person B",
        "title": "Tag 2: Das vergilbte Pergament",
        "type": "text",
        "image": None,
        "story": "Das Schloss der Holzbox springt auf! Ihr öffnet den Deckel und findet im Inneren ein altes, steif gefrorenes Pergament mit der verschlüsselten Nachricht: *„SIVX“*. Am Rand ist fein ein Lorbeerkranz eingraviert.",
        "question": "Entschlüssele das Codewort.\n\n**Eingabe:** Welches Wort steht entschlüsselt auf dem Pergament?",
        "answer": "NORD",
        "puzzle_piece": None,
        "hint": "Betrachte jeden Buchstaben des Codes und wandere im Alphabet vier Positionen nach links (Richtung A)."
    },
    3: {
        "person": "Person C",
        "title": "Tag 3: Das Rentier-Experten-Rätsel",
        "type": "text",
        "image": None,
        "story": "Ihr sprecht das magische Wort „NORD“ laut aus. Ein feines Glockenklingeln ertönt, und draußen im Schnee steht ein prachtvoller Elfen-Schlitten! Ihr klettert hinein, doch das Armaturenbrett verlangt einen Zündcode basierend auf einem echten, faszinierenden Rentier-Geheimnis.",
        "question": "Um das Cockpit zu starten, musst du ein echtes Biologie-Geheimnis der Rentiere lüften:\n*Wusstest du, dass Rentiere im Winter ihre Augenfarbe von goldbraun auf ein eisiges Blau umstellen, um im dunklen Polarlicht besser zu sehen?* \n\nSuche nach der Anzahl der Buchstaben dieses englischen Farbworts für Blau und multipliziere diese Zahl mit der Anzahl der Rentier-Geschlechter, die im Winter ein Geweih tragen (beide Geschlechter = ?).\n\n**Eingabe:** Tippe das Ergebnis als zweistellige Zahl ein (z.B. 42).",
        "answer": "8",
        "puzzle_piece": None,
        "hint": "Wie heißt 'Blau' auf Englisch und wie viele Buchstaben hat dieses Wort? Multipliziere das mit der Anzahl der Geschlechter, die im Winter ein Geweih tragen (männlich und weiblich)."
    },
    4: {
        "person": "Person A",
        "title": "Tag 4: Das Navigationssystem & die Koordinaten",
        "type": "text",
        "image": None,
        "story": "Der Schlitten brummt startklar! Ihr nehmt Platz, aber das Navigationssystem zeigt eine Fehlermeldung: „Kurs unbekannt. Bitte Zielkoordinaten eingeben.“",
        "question": "Berechne den 5-stelligen Kurs-Code aus Breit- und Längengrad:\n- Breitengrad: Nimm die fixen 90 Grad des Nordpols minus 10.\n- Längengrad: Nimm die Quersumme des aktuellen Jahres mal 10.\n\n**Eingabe:** Schreibe beide Zahlen ohne Leerzeichen direkt zusammen (z.B. 12345).",
        "answer": "80100",
        "puzzle_piece": None,
        "hint": "Rechne den Breitengrad (90 - 10) und den Längengrad (Quersumme von 2026 mal 10) getrennt aus und setze sie nahtlos aneinander."
    },
    # --- START NEBEL-LABYRINTH (Tage 5 - 11 sammeln 6 Puzzleteile) ---
    5: {
        "person": "Person B",
        "title": "Tag 5: Das Nebel-Tor & Fragment 1",
        "type": "text",
        "story": "Der Schlitten stoppt vor einer massiven, nebelverhangenen Wand aus blauem Eis. Das ist der Eingang zum Labyrinth. Auf einem alten Steinsockel liegt eine lederne Tasche für magische Fragmente.",
        "question": "Um das erste Siegel des Nebeltors zu brechen, beantworte: Welcher Zustand nimmt Wasser an, wenn es bei klarem Frost zu eisigen Kristallen gefriert?\n\n**Eingabe:** Tippe das Wort als Lösung ein (FEST / EIS / GEFROREN). *Tipp: Nimm den Begriff 'EIS'*.",
        "answer": "EIS",
        "puzzle_piece": "🧩 Fragment 1: Rahmenteil Oben-Links",
        "hint": "Es ist ein kurzes, dreibuchstabiges Wort für gefrorenes Wasser."
    },
    6: {
        "person": "Person C",
        "title": "Tag 6: Der eiserne Sudoku-Monolith",
        "type": "text",
        "story": "Ihr tretet tiefer in den Nebel und findet einen riesigen, gefrorenen Monolithen mit einer Logik-Zahlenmatrix.",
        "question": "In einem magischen 3x3-Gitter mit den Zahlen 1 bis 9 hat jede Reihe und Spalte die Summe 15.\nWelche Zahl befindet sich exakt im **Zentrum (Mitte)** des Quadrats?\n\n**Eingabe:** Tippe die einstellige Zahl ein.",
        "answer": "5",
        "puzzle_piece": "🧩 Fragment 2: Rahmenteil Oben-Mitte",
        "hint": "In einem magischen Quadrat steht die mittlere Zahl immer genau im Zentrum der Reihe von 1 bis 9."
    },
    7: {
        "person": "Person A",
        "title": "Tag 7: Die tückische Eisspalte",
        "type": "text",
        "story": "Der Pfad spaltet sich vor einer tiefen Schlucht. Ein Logik-Hinweis verrät, welcher Pfad stabil ist.",
        "question": "Drei Elfen wollen über die Schlucht. Elf A war schneller als Elf B, aber langsamer als Elf C.\nWer ist als Erster (und damit an der Spitze) über die Schlucht gegangen?\n\n**Eingabe:** Schreibe den Buchstaben des schnellsten Elfen (A, B oder C).",
        "answer": "C",
        "puzzle_piece": "🧩 Fragment 3: Rahmenteil Oben-Rechts",
        "hint": "Überlege, wer am längsten beziehungsweise als Erster gestartet ist, wenn A langsamer als C war."
    },
    8: {
        "person": "Person B",
        "title": "Tag 8: Das interaktive Morse-Echo",
        "type": "morse",
        "story": "Ein lautes Echosignal hallt durch die Nebelwände. Das Funkgerät knackt. Sendet das universelle Notsignal per Morse-Code, um den Nebel zu lichten!",
        "question": "Klicke die Morse-Zeichen in der korrekten Reihenfolge für **SOS** (... --- ...).\n(Kurz = ., Lang = -)\nDrücke danach auf Prüfen.",
        "answer": "...---...",
        "puzzle_piece": "🧩 Fragment 4: Rahmenteil Mitte-Links",
        "hint": "SOS besteht aus drei kurzen, drei langen und drei kurzen Signalen."
    },
    9: {
        "person": "Person C",
        "title": "Tag 9: Der Lichtstrahl-Spiegelpfad",
        "type": "text",
        "story": "Ein Laserstrahl bricht durch den Nebel. Ihr müsst den Spiegel-Code eingeben, um den Sensor zu treffen.",
        "question": "Der Spiegel steht auf Position Nord-Ost ('NO'). Welcher Buchstabe codiert diese Ausrichtung im Steuerungssystem?\n\n**Eingabe:** Tippe den 2-stelligen Großbuchstaben-Code ein.",
        "answer": "NO",
        "puzzle_piece": "🧩 Fragment 5: Zentrum-Teil",
        "hint": "Die Abkürzung für Nord-Ost."
    },
    10: {
        "person": "Person A",
        "title": "Tag 10: Der Fluss-Übergang",
        "type": "text",
        "story": "Ihr steht vor einem unterirdischen, eiskalten Gletscherfluss. Ein kleiner Yeti verlangt das klassische Transport-Logikrätsel.",
        "question": "Du hast einen Wolf, eine Ziege und einen Kohlkopf am Fluss. Du kannst nur eines davon im Boot mitnehmen. Wer darf niemals unbeaufsichtigt allein gelassen werden? (Wer frisst wen?)\n\n**Eingabe:** Antworte mit dem Tier, das die Ziege frisst.",
        "answer": "WOLF",
        "puzzle_piece": "🧩 Fragment 6: Rahmenteil Unten-Links",
        "hint": "Der Wolf frisst die Ziege, wenn du nicht aufpasst."
    },
    11: {
        "person": "Person B",
        "title": "Tag 11: Die finale Gletscher-Schlucht",
        "type": "text",
        "story": "Das letzte Hindernis vor dem Ausgang des Labyrinths. Eine versiegelte Steintür verlangt die Summe aller bisher gesammelten Fragmente.",
        "question": "Wie viele magische Fragmente müsst ihr insgesamt gesammelt haben, um das große Puzzle zu vervollständigen?\n\n**Eingabe:** Tippe die Zahl ein.",
        "answer": "6",
        "puzzle_piece": "🧩 Fragment 7: Rahmenteil Unten-Mitte",
        "hint": "Zähle die Fragmente von Tag 5 bis Tag 10 zusammen."
    },
    12: {
        "person": "Person C",
        "title": "Tag 12: Das Haupttor der Werkstatt",
        "type": "text",
        "story": "Ihr habt alle Teile beisammen! Das große Puzzlesichtfenster am Haupttor setzt sich zusammen. Löse das finale Lösungswort, um die Werkstatt zu öffnen.",
        "question": "Setze das Master-Wort aus dem allerersten Hinweis (Tag 2: NORD) und dem Ausgang zusammen.\n\n**Eingabe:** Tippe das finale Codewort ein (z.B. WORT12).",
        "answer": "NORD12",
        "puzzle_piece": "🏆 GEWONNEN: Die Werkstatt ist geöffnet!",
        "hint": "Verbinde das Wort aus Tag 2 nahtlos mit der Zahl 12."
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

# Sidebar für die Übersicht & Puzzleteile-Sammlung
st.sidebar.header("🧭 Abenteuer-Fortschritt")
st.sidebar.write(Gefundene Fragmente: {len(st.session_state.puzzle_pieces)} / 7)
for piece in st.session_state.puzzle_pieces:
    st.sidebar.success(piece)

# Hauptbereich: Anzeige der Tage
for day_num, door in DOORS.items():
    is_unlocked = day_num in st.session_state.unlocked_days
    
    with st.expander(f"{door['title']} ({door['person']})", expanded=(day_num == max(st.session_state.unlocked_days))):
        if not is_unlocked:
            st.warning("🔒 Dieser Tag ist noch gesperrt. Löse erst die vorherigen Aufgaben!")
            continue
            
        st.write(door["story"])
        st.markdown("---")
        st.write(door["question"])
        
        # Eingabe je nach Rätsel-Typ
        user_input = None
        if door["type"] == "lock_sliders":
            col1, col2, col3, col4 = st.columns(4)
            d1 = col1.number_input("Ziffer 1", 0, 9, 0, key=f"d1_{day_num}")
            d2 = col2.number_input("Ziffer 2", 0, 9, 0, key=f"d2_{day_num}")
            d3 = col3.number_input("Ziffer 3", 0, 9, 0, key=f"d3_{day_num}")
            d4 = col4.number_input("Ziffer 4", 0, 9, 0, key=f"d4_{day_num}")
            user_input = [d1, d2, d3, d4]
            
        elif door["type"] == "morse":
            morse_input = st.text_input("Morse-Eingabe (nutze . und -):", key=f"morse_{day_num}")
            user_input = morse_input.strip()
            
        else:
            user_input = st.text_input("Deine Antwort:", key=f"text_{day_num}").strip()
            
        # Prüfen-Button
        if st.button("Antwort prüfen", key=f"btn_{day_num}"):
            is_correct = False
            if door["type"] == "lock_sliders":
                if user_input == door["answer"]:
                    is_correct = True
            else:
                if str(user_input).upper() == str(door["answer"]).upper():
                    is_correct = True
                    
            if is_correct:
                st.success("Richtig gelöst! 🎉")
                # Puzzleteil hinzufügen falls vorhanden
                if door["puzzle_piece"] and door["puzzle_piece"] not in st.session_state.puzzle_pieces:
                    st.session_state.puzzle_pieces.append(door["puzzle_piece"])
                
                # Nächsten Tag freischalten
                next_day = day_num + 1
                if next_day not in st.session_state.unlocked_days and next_day <= len(DOORS):
                    st.session_state.unlocked_days.append(next_day)
                    st.rerun()
            else:
                st.error("Das war leider falsch. Probiere es noch einmal oder nutze den Hinweis!")
                
        # Hinweis-Expander (Verrät niemals die Lösung direkt)
        with st.expander("💡 Einen Hinweis anzeigen"):
            st.info(door["hint"])
