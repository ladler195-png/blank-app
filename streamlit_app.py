import streamlit as st

# ==============================================================================
# 1. SEITEN-EINSTELLUNGEN & DESIGN
# ==============================================================================
st.set_page_config(
    page_title="Expedition Nordpol: Der Adventskalender",
    page_icon="🎄",
    layout="centered"
)

# Custom CSS für weihnachtliches Aussehen
st.markdown("""
    <style>
    .main {
        background-color: #0b1d3a;
        color: #f1f5f9;
    }
    .stButton>button {
        background-color: #d97706;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. RÄTSEL-DATENBANK (TAGE 1 BIS 5)
# ==============================================================================
DOORS = {
    1: {
        "person": "Person A",
        "title": "Tag 1: Das geheimnisvolle Päckchen",
        "story": "Vor der Haustür liegt ein verschneites, unadressiertes Päckchen. Darin befindet sich eine alte Holzschatulle, die mit einem 4-stelligen Zahlenschloss gesichert ist. Auf dem Deckel ist eine geheimnisvolle Rune eingraviert.",
        "question": "Welcher 4-stellige Code öffnet das Schloss? Löse die Zahlenreihe: 3, 7, 15, 31, __",
        "answer": "63",
        "hint": "Die Differenz zwischen den Zahlen verdoppelt sich in jedem Schritt (+4, +8, +16, +32)."
    },
    2: {
        "person": "Person B",
        "title": "Tag 2: Der Hilferuf der Elfen",
        "story": "Die Schatulle springt auf! Darin liegt ein alt aussehendes Pergament. Die Schrift ist in einer Elfen-Chiffre verfasst.",
        "question": "Entschlüssele den Notsender-Code (Cäsar-Chiffre, 4 Stellen zurück im Alphabet): 'SIVX'",
        "answer": "NORD",
        "hint": "Ziehe von jedem Buchstaben 4 Stellen im Alphabet ab (S -> N, I -> O, V -> R, X -> D)."
    },
    3: {
        "person": "Person C",
        "title": "Tag 3: Der Elfen-Schlitten",
        "story": "Ein leises Glockenläuten ertönt draußen. Ein magischer, führerloser Elfen-Schlitten ist auf der Straße gelandet! Um die Startkonsole zu aktivieren, müsst ihr die Energiefrequenz kalibrieren.",
        "question": "Berechne die Startfrequenz: (Anzahl Rentiere: 8) × (Schatullencode von Tag 1: 63) - 4",
        "answer": "500",
        "hint": "Rechne: 8 * 63 - 4"
    },
    4: {
        "person": "Person A",
        "title": "Tag 4: Die Flugkarte zum Nordpol",
        "story": "Der Schlitten hebt geräuschlos ab und steigt in den Nachthimmel. Im Cockpit klappt eine magische Sternenkarte auf, um den Kurs einzustellen.",
        "question": "Welcher Kurs führt durch den Polarhimmel? Berechne die Summe aller Primzahlen zwischen 10 und 25.",
        "answer": "60",
        "hint": "Die Primzahlen in diesem Bereich sind 11, 13, 17, 19. Addiere diese vier Zahlen."
    },
    5: {
        "person": "Person B",
        "title": "Tag 5: Die Landung im Eisnebel",
        "story": "Der Schlitten sinkt herab. Vor euch liegt nicht die Werkstatt, sondern eine undurchdringliche, eisige Nebelwand – das Tor zum Nebel-Labyrinth. Ein magisches Siegel verlangt das Losungswort.",
        "question": "Setze das Losungswort zusammen: Das Lösungswort von Tag 2 + das Ergebnis von Tag 4 (z. B. HALO10).",
        "answer": "NORD60",
        "hint": "Kombiniere den Begriff von Tag 2 (NORD) direkt mit der Zahl von Tag 4 (60)."
    }
}
    # ------------------ AKT II: DAS NEBEL-LABYRINTH ------------------
    6: {
        "person": "Person C",
        "title": "Tag 6: Nikolaus im Eisnebel (Spezial)",
        "story": "Im dichten Nebel findet ihr eine goldene Nikolaus-Statuette im Schnee. Auf dem Sockel befindet sich ein 3x3 Zahlen-Raster. Nur wenn die Zeilen- und Spaltensummen magisch überall 15 ergeben, leuchtet der Nikolaus-Kompass auf!",
        "question": "Welche Zahl gehört in die Mitte (Feld X) des magischen 3x3-Quadrats (Zahlen 1-9)?",
        "answer": "5",
        "hint": "In jedem magischen 3x3-Quadrat mit den Zahlen 1 bis 9 liegt die Zahl 5 immer genau in der Mitte."
    },
    7: {
        "person": "Person A",
        "title": "Tag 7: Die Weggabelung der Eiszapfen",
        "story": "Das Labyrinth teilt sich in vier Pfade (N, O, S, W). Ein Wegweiser zeigt kryptische Zahlen an: 'N=12, O=24, S=36'. Die Eiszapfen am Weg W folgen einer mathematischen Gesetzmäßigkeit.",
        "question": "Welche Zahl hat der Weg W, wenn die Folge 3, 6, 11, 18, 27, __ lautet?",
        "answer": "38",
        "hint": "Schau dir die Abstände an: +3, +5, +7, +9... Wie viel musst du zu 27 addieren?"
    },
    8: {
        "person": "Person B",
        "title": "Tag 8: Das Echo im Gletscher",
        "story": "Ihr hört ein lautes Dröhnen. Das Nebelhorn der Elfen schallt durch die Spalten. Es wirft ein Echo zurück, das sich in seiner Frequenz verdoppelt.",
        "question": "Ein Ton von 440 Hz wird 3-mal im Echo gedoppelt. Wie hoch ist die Endfrequenz in Hz?",
        "answer": "3520",
        "hint": "Rechne: 440 * 2 * 2 * 2 (oder 440 * 8)."
    },
    9: {
        "person": "Person C",
        "title": "Tag 9: Die Eisspiegel-Grotte",
        "story": "Eine Sackgasse! Um die Nebeltür aufzubrennen, muss der Lichtstrahl einer Laterne über Spiegel umgelenkt werden. Jeder Spiegel dreht den Lichtstrahl um 90 Grad.",
        "question": "Der Strahl startet nach Osten. Er trifft nacheinander auf 3 Spiegel: Links, Rechts, Links. In welche Himmelsrichtung schlägt der Strahl am Ende ein? (NORD, OST, SUED oder WEST)",
        "answer": "NORD",
        "hint": "Start: Ost -> Links abbiegen = Nord -> Rechts abbiegen = Ost -> Links abbiegen = Nord."
    },
    10: {
        "person": "Person A",
        "title": "Tag 10: Der gefrorene Kompass",
        "story": "Ihr findet einen Kompass im Schnee. Die Nadel ist durch Eis blockiert. Auf dem Gehäuse stehen 4 Zahlen, die zusammen den korrekten Grad-Winkel (0-360°) ergeben.",
        "question": "Welcher Winkel führt aus dem Nebel? Löse: (Höhe des Watzmanns: 2713) Modulo 360",
        "answer": "193",
        "hint": "Teile 2713 durch 360. Der Rest dieser Division (2713 - 7 * 360) ist das Ergebnis."
    },
    11: {
        "person": "Person B",
        "title": "Tag 11: Die brüchige Eisbrücke",
        "story": "Vor euch liegt eine tief schimmernde Gletscherspalte. Die Steinbrücke ist nur passierbar, wenn ihr die Trittsteine nach der Logik der Primfaktoren wählt.",
        "question": "Wie lautet die Summe aller Primfaktoren der Zahl 42? (42 = 2 × 3 × 7)",
        "answer": "12",
        "hint": "Addiere die drei Primzahlen 2, 3 und 7."
    },
    12: {
        "person": "Person C",
        "title": "Tag 12: Der Durchbruch am Nordpol",
        "story": "Der Nebel lichtet sich schlagartig! Vor euch erstrahlen die Lichter der Nordpol-Werkstatt. Um das große Holztor zu öffnen, müsst ihr den Code aus den Hinweisen des Labyrinths eingeben.",
        "question": "Setzt das Tor-Passwort zusammen: Wort von Tag 9 + Ergebnis von Tag 11 (z. B. WEST15).",
        "answer": "NORD12",
        "hint": "Kombiniere die Himmelsrichtung von Tag 9 (NORD) direkt mit der Zahl von Tag 11 (12)."
    }
}
# ==============================================================================
# 3. SPEICHERSTAND (SESSION STATE)
# ==============================================================================
if "solved_doors" not in st.session_state:
    st.session_state.solved_doors = []

# ==============================================================================
# 4. KOPFBEREICH & STATUS
# ==============================================================================
st.title("🎄 Expedition Nordpol")
st.caption("Ein Adventskalender für die Familie")

col_a, col_b, col_c = st.columns(3)
with col_a:
    solved_a = sum(1 for d in st.session_state.solved_doors if DOORS.get(d, {}).get("person") == "Person A")
    st.metric("Person A", f"{solved_a} / 8 Gelöst")
with col_b:
    solved_b = sum(1 for d in st.session_state.solved_doors if DOORS.get(d, {}).get("person") == "Person B")
    st.metric("Person B", f"{solved_b} / 8 Gelöst")
with col_c:
    solved_c = sum(1 for d in st.session_state.solved_doors if DOORS.get(d, {}).get("person") == "Person C")
    st.metric("Person C", f"{solved_c} / 8 Gelöst")

st.divider()

# ==============================================================================
# 5. TÜRCHEN-GRID
# ==============================================================================
st.write("### 📅 Wähle dein Türchen")

# 6 Spalten pro Zeile anzeigen
cols = st.columns(6)
for i in range(1, 13):
    col = cols[(i - 1) % 6]
    
    if i in st.session_state.solved_doors:
        label = f"✅ Tag {i}"
    else:
        label = f"🔒 Tag {i}"
        
    if col.button(label, key=f"door_btn_{i}"):
        st.session_state.active_day = i

# ==============================================================================
# 6. RÄTSEL-DIALOG
# ==============================================================================
if "active_day" in st.session_state:
    day = st.session_state.active_day
    
    if day in DOORS:
        puzzle = DOORS[day]
        st.markdown("---")
        st.markdown(f"### 🚪 {puzzle['title']} ({puzzle['person']})")
        st.info(puzzle["story"])
        st.write(f"**Rätsel:** {puzzle['question']}")
        
        if day in st.session_state.solved_doors:
            st.success(f"🎉 Richtig gelöst! Die richtige Antwort war: **{puzzle['answer']}**")
        else:
            user_input = st.text_input("Deine Lösung:", key=f"input_{day}")
            
            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("Lösung prüfen", type="primary"):
                    if user_input.strip().upper() == puzzle["answer"].upper():
                        st.session_state.solved_doors.append(day)
                        st.balloons()
                        st.success("Richtig! Der Weg öffnet sich.")
                        st.rerun()
                    else:
                        st.error("Falsch. Versucht es noch einmal!")
            with c2:
                if st.button("Hinweis anzeigen"):
                    st.warning(puzzle["hint"])
