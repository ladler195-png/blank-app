import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. SEITEN-KONFIGURATION & STYLING (CSS)
# ==============================================================================
st.set_page_config(
    page_title="Nordpol-Expedition 2026",
    page_icon="❄️",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #0b1d3a 0%, #1a365d 100%);
        color: #ffffff;
    }
    h1, h2, h3 {
        color: #f6ad55 !important;
        font-family: 'Georgia', serif;
        text-shadow: 2px 2px 4px #000000;
    }
    div.stButton > button {
        background-color: #2b6cb0;
        color: white;
        border-radius: 12px;
        border: 2px solid #ed8936;
        font-weight: bold;
        width: 100%;
        padding: 10px;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #c53030;
        color: white;
        border-color: #f6ad55;
        transform: scale(1.03);
    }
    .stAlert {
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Animierter Schneefall-Effekt
components.html("""
    <script src="https://unpkg.com/magic-snowflakes/dist/snowflakes.min.js"></script>
    <script>
        var snowflakes = new Snowflakes({
            color: '#ffffff',
            count: 25,
            minOpacity: 0.2,
            maxOpacity: 0.8
        });
    </script>
""", height=0)

# ==============================================================================
# 2. RÄTSEL-DATENBANK (TAGE 1 BIS 24)
# ==============================================================================
DOORS = {
    # AKT I
    1: {
        "person": "Person A",
        "title": "Tag 1: Das geheimnisvolle Päckchen",
        "type": "lock_sliders",
        "story": "Vor der Haustür liegt ein verschneites Päckchen mit einer Holzschatulle und einem 4-stelligen Zahlenschloss.",
        "question": "Stelle die 4 Zahlenräder ein. Welcher Code öffnet das Schloss? (Rätsel: 3, 7, 15, 31, __ -> Bilde einen 4-stelligen Code aus Auffüllen mit 0en)",
        "answer": [0, 0, 6, 3],
        "hint": "Die Differenz zwischen den Zahlen verdoppelt sich (+4, +8, +16, +32). Das Ergebnis ist 63. Stelle an den Reglern 0-0-6-3 ein."
    },
    2: {
        "person": "Person B",
        "title": "Tag 2: Der Hilferuf der Elfen",
        "type": "text",
        "story": "In der Schatulle liegt ein vergilbtes Pergament mit einer Elfen-Chiffre.",
        "question": "Entschlüssele den Notsender-Code (Cäsar-Chiffre, 4 Stellen zurück im Alphabet): 'SIVX'",
        "answer": "NORD",
        "hint": "Ziehe von jedem Buchstaben 4 Stellen im Alphabet ab (S -> N, I -> O, V -> R, X -> D)."
    },
    3: {
        "person": "Person C",
        "title": "Tag 3: Der Elfen-Schlitten",
        "type": "text",
        "story": "Ein führerloser Elfen-Schlitten wartet draußen! Um die Startkonsole zu aktivieren, müsst ihr die Energiefrequenz kalibrieren.",
        "question": "Berechne die Startfrequenz: (Anzahl Rentiere: 8) × (Lösung von Tag 1: 63) - 4",
        "answer": "500",
        "hint": "Rechne: 8 * 63 - 4"
    },
    4: {
        "person": "Person A",
        "title": "Tag 4: Die Flugkarte zum Nordpol",
        "type": "text",
        "story": "Im Cockpit klappt eine magische Sternenkarte auf, um den Kurs einzustellen.",
        "question": "Welcher Kurs führt durch den Polarhimmel? Berechne die Summe aller Primzahlen zwischen 10 und 25.",
        "answer": "60",
        "hint": "Die Primzahlen sind 11, 13, 17, 19. Addiere diese vier Zahlen."
    },
    5: {
        "person": "Person B",
        "title": "Tag 5: Die Landung im Eisnebel",
        "type": "text",
        "story": "Der Schlitten sinkt herab. Vor euch liegt die undurchdringliche Nebelwand – das Tor zum Nebel-Labyrinth.",
        "question": "Setze das Losungswort zusammen: Lösung von Tag 2 + Ergebnis von Tag 4 (z. B. HALO10).",
        "answer": "NORD60",
        "hint": "Kombiniere den Begriff von Tag 2 (NORD) direkt mit der Zahl von Tag 4 (60)."
    },

    # AKT II
    6: {
        "person": "Person C",
        "title": "Tag 6: Nikolaus im Eisnebel",
        "type": "text",
        "story": "Im dichten Nebel findet ihr eine goldene Nikolaus-Statuette im Schnee.",
        "question": "Welche Zahl gehört in die Mitte (Feld X) des magischen 3x3-Quadrats (Zahlen 1-9)?",
        "answer": "5",
        "hint": "In jedem magischen 3x3-Quadrat mit den Zahlen 1 bis 9 liegt die Zahl 5 immer genau in der Mitte."
    },
    7: {
        "person": "Person A",
        "title": "Tag 7: Die Weggabelung der Eiszapfen",
        "type": "text",
        "story": "Das Labyrinth teilt sich in vier Pfade. Die Eiszapfen am Weg W folgen einer mathematischen Gesetzmäßigkeit.",
        "question": "Welche Zahl hat der Weg W, wenn die Folge 3, 6, 11, 18, 27, __ lautet?",
        "answer": "38",
        "hint": "Schau dir die Abstände an: +3, +5, +7, +9... Wie viel musst du zu 27 addieren?"
    },
    8: {
        "person": "Person B",
        "title": "Tag 8: Das Echo im Gletscher",
        "type": "text",
        "story": "Das Nebelhorn der Elfen schallt durch die Spalten. Es wirft ein Echo zurück, das sich in seiner Frequenz verdoppelt.",
        "question": "Ein Ton von 440 Hz wird 3-mal im Echo gedoppelt. Wie hoch ist die Endfrequenz in Hz?",
        "answer": "3520",
        "hint": "Rechne: 440 * 2 * 2 * 2 (oder 440 * 8)."
    },
    9: {
        "person": "Person C",
        "title": "Tag 9: Die Eisspiegel-Grotte",
        "type": "text",
        "story": "Um die Nebeltür aufzubrennen, muss der Lichtstrahl einer Laterne über Spiegel umgelenkt werden.",
        "question": "Der Strahl startet nach Osten. Er trifft nacheinander auf 3 Spiegel: Links, Rechts, Links. In welche Himmelsrichtung schlägt der Strahl am Ende ein?",
        "answer": "NORD",
        "hint": "Start: Ost -> Links = Nord -> Rechts = Ost -> Links = Nord."
    },
    10: {
        "person": "Person A",
        "title": "Tag 10: Der gefrorene Kompass",
        "type": "text",
        "story": "Die Kompassnadel ist durch Eis blockiert.",
        "question": "Welcher Winkel führt aus dem Nebel? Löse: (Höhe des Watzmanns: 2713) Modulo 360",
        "answer": "193",
        "hint": "Teile 2713 durch 360. Der Rest dieser Division (2713 - 7 * 360) ist das Ergebnis."
    },
    11: {
        "person": "Person B",
        "title": "Tag 11: Die brüchige Eisbrücke",
        "type": "text",
        "story": "Die Steinbrücke ist nur passierbar, wenn ihr die Trittsteine nach der Logik der Primfaktoren wählt.",
        "question": "Wie lautet die Summe aller Primfaktoren der Zahl 42? (42 = 2 × 3 × 7)",
        "answer": "12",
        "hint": "Addiere die drei Primzahlen 2, 3 und 7."
    },
    12: {
        "person": "Person C",
        "title": "Tag 12: Der Durchbruch am Nordpol",
        "type": "text",
        "story": "Der Nebel lichtet sich! Vor euch erstrahlen die Lichter der Werkstatt.",
        "question": "Setzt das Tor-Passwort zusammen: Wort von Tag 9 + Ergebnis von Tag 11 (z. B. WEST15).",
        "answer": "NORD12",
        "hint": "Kombiniere die Himmelsrichtung von Tag 9 (NORD) direkt mit der Zahl von Tag 11 (12)."
    },

    # AKT III
    13: {
        "person": "Person A",
        "title": "Tag 13: Der vereiste Maschinensaal",
        "type": "text",
        "story": "Die Hauptgetriebe der Geschenkmaschine stecken fest. Drei Zahnräder mit 12, 18 und 24 Zähnen greifen ineinander.",
        "question": "Nach wie vielen Umdrehungen des ersten Rads (12 Zähne) stehen alle drei Räder wieder in ihrer Startposition?",
        "answer": "6",
        "hint": "Das kgV von 12, 18 und 24 ist 72. Teile 72 durch 12 Zähne."
    },
    14: {
        "person": "Person B",
        "title": "Tag 14: Das Durcheinander in der Packstation",
        "type": "text",
        "story": "Ein Kobold hat die Geschenkaufkleber vertauscht! Nur ein Anagramm enthüllt den echten Namen des Oberelfs.",
        "question": "Welches Wort ergibt sich aus den Buchstaben 'E-L-F-E-N-M-A-G-I-E', wenn man das Wort 'MAGIE' entfernt?",
        "answer": "ELFEN",
        "hint": "Streich die Buchstaben M-A-G-I-E aus dem Wort heraus."
    },
    15: {
        "person": "Person C",
        "title": "Tag 15: Das Rentier-Futter-Rezept",
        "type": "text",
        "story": "Rudolph und seine Freunde brauchen Stärkung! Das Kraftfutter besteht aus Hafer, Sternenstaub und Äpfeln im Verhältnis 5 : 2 : 3.",
        "question": "Ihr wollt insgesamt 50 kg Futter herstellen. Wie viele kg Sternenstaub benötigt ihr?",
        "answer": "10",
        "hint": "Gesamtteile: 5 + 2 + 3 = 10 Teile. 50 kg / 10 Teile = 5 kg pro Teil. Sternenstaub hat 2 Teile (2 * 5 kg)."
    },
    16: {
        "person": "Person A",
        "title": "Tag 16: Die Sternenstaub-Batterie",
        "type": "binary_switches",
        "story": "Die Energiegeneratoren der Werkstatt sind schwach. Ein Schieberegler-Panel verlangt die Aktivierung der Batterie für die Dezimalzahl 25.",
        "question": "Aktiviere die 5 Kippschalter so, dass der Binärcode der Dezimalzahl 25 entspricht (16 + 8 + 1).",
        "answer": [True, True, False, False, True],
        "hint": "Schalterwerte von links nach rechts: 16, 8, 4, 2, 1. Aktiviere 16, 8 und 1."
    },
    17: {
        "person": "Person B",
        "title": "Tag 17: Die Wunschzettel-Sortiermaschine",
        "type": "text",
        "story": "Millionen Briefe fliegen durch die Luft! Der Sortieralgorithmus fragt nach dem Median einer Datenreihe.",
        "question": "Wie lautet der Median der folgenden Werte: 12, 45, 7, 23, 89, 34, 19?",
        "answer": "23",
        "hint": "Sortiere die 7 Zahlen aufsteigend: 7, 12, 19, 23, 34, 45, 89. Nimm genau die vierte (mittlere) Zahl."
    },
    18: {
        "person": "Person C",
        "title": "Tag 18: Das Sicherheitssystem der Werkstatt",
        "type": "text",
        "story": "Die Schalttafel der Werkstatt verlangt den Werkstatt-Schlüsselcode.",
        "question": "Berechne den Werkstatt-Code: (Lösung Tag 13: 6) × (Lösung Tag 15: 10) + (Lösung Tag 17: 23)",
        "answer": "83",
        "hint": "Rechne: 6 * 10 + 23"
    },

    # AKT IV
    19: {
        "person": "Person A",
        "title": "Tag 19: Der Flugrouten-Optimierer",
        "type": "text",
        "story": "Der Weihnachtsmann muss 4 Städte anfliegen (A, B, C, D). Die Distanzen bilden ein Quadrat mit Seitenlänge 100 km.",
        "question": "Was ist die kürzeste Strecke (in km), um alle 4 Ecken eines 100x100km Quadrats einmal abzufliegen?",
        "answer": "300",
        "hint": "Du musst 3 Kanten des Quadrats entlangfliegen: 100 km + 100 km + 100 km."
    },
    20: {
        "person": "Person B",
        "title": "Tag 20: Der Polarlichter-Sender",
        "type": "audio_morse",
        "story": "Damit der Schlitten im Dunkeln navigieren kann, empfängt das Radio ein Morsesignal aus den Polarlichtern.",
        "question": "Höre dir das Tonsignal an und gib das internationale Notsignal in Großbuchstaben ein.",
        "answer": "SOS",
        "hint": "Drei kurze Töne, drei lange Töne, drei kurze Töne (S-O-S)."
    },
    21: {
        "person": "Person C",
        "title": "Tag 21: Die magische Rentiere-Aufstellung",
        "type": "text",
        "story": "Die 8 Rentiere müssen vor den Schlitten gespannt werden.",
        "question": "Wenn Rudolph immer ganz vorne stehen muss, wie viele Möglichkeiten gibt es dann noch für die restlichen 7 Rentiere? (7!)",
        "answer": "5040",
        "hint": "Berechne 7! = 7 × 6 × 5 × 4 × 3 × 2 × 1."
    },
    22: {
        "person": "Person A",
        "title": "Tag 22: Die Puffer-Reserve",
        "type": "cargo_slider",
        "story": "Der Schlitten belädt sich automatisch. Geladen sind bereits 3 Kisten zu je 150 kg und 4 Kisten zu je 110 kg. Das Zielgewicht ist exakt 1000 kg.",
        "question": "Stelle am Regler die noch fehlende Puffer-Reserve in kg ein.",
        "answer": 110,
        "hint": "Bisher geladen: (3*150) + (4*110) = 890 kg. Es fehlen noch 110 kg."
    },
    23: {
        "person": "Person B",
        "title": "Tag 23: Die finale Startbereitschaft",
        "type": "text",
        "story": "Alle Systeme stehen auf Grün! Nur noch der Freigabe-Schlüssel fehlt.",
        "question": "Addiere den Schlitten-Code von Tag 3 (500) und den Werkstatt-Code von Tag 18 (83).",
        "answer": "583",
        "hint": "Rechne: 500 + 83"
    },
    24: {
        "person": "Alle 3 gemeinsam",
        "title": "Tag 24: HEILIGABEND – Die Rettung von Weihnachten!",
        "type": "text",
        "story": "Ihr steht gemeinsam im Kontrollraum. Um Punkt 24:00 Uhr muss der Master-Code eingegeben werden!",
        "question": "Kombiniert den Schlitten-Code (Tag 3: 500) + Tor-Code (Tag 12: NORD12) + Freigabe-Code (Tag 23: 583) ohne Leerzeichen!",
        "answer": "500NORD12583",
        "hint": "Setze die drei Ergebnisse direkt hintereinander zusammen: 500 + NORD12 + 583"
    }
}

# ==============================================================================
# 3. SESSION STATE INITIALISIERUNG
# ==============================================================================
if "solved_doors" not in st.session_state:
    st.session_state.solved_doors = []

if "active_day" not in st.session_state:
    st.session_state.active_day = 1

# ==============================================================================
# 4. KOPFZEILE & FORTSCHRITT
# ==============================================================================
st.title("🎄 Expedition Nordpol: Das Escape-Adventskalender-Abenteuer")

progress = len(st.session_state.solved_doors) / 24
st.write(f"**Expeditions-Fortschritt:** {len(st.session_state.solved_doors)} von 24 Rätseln gelöst")
st.progress(progress)

st.divider()

# ==============================================================================
# 5. TÜRCHEN-GRID
# ==============================================================================
st.write("### 📅 Wähle dein Türchen")

cols = st.columns(6)
for i in range(1, 25):
    col = cols[(i - 1) % 6]
    if i in st.session_state.solved_doors:
        label = f"🎁 Tag {i}"
    elif i == 24:
        label = f"⭐ Tag {i}"
    else:
        label = f"🔒 Tag {i}"
        
    if col.button(label, key=f"door_btn_{i}"):
        st.session_state.active_day = i

st.divider()

# ==============================================================================
# 6. AKTIVES RÄTSEL RENDERN
# ==============================================================================
day = st.session_state.active_day
door = DOORS[day]

st.subheader(f"✨ {door['title']}")
st.caption(f"👤 Zuständig: **{door['person']}**")
st.info(f"📖 **Geschichte:** {door['story']}")
st.markdown(f"❓ **Aufgabe:** {door['question']}")

# ------------------------------------------------------------------------------
# RÄTSEL-TYP 1: Interaktive Drehräder (Tag 1)
# ------------------------------------------------------------------------------
if door["type"] == "lock_sliders":
    st.write("🔒 **Drehe die 4 Zahlenräder der Schatulle:**")
    c1, c2, c3, c4 = st.columns(4)
    v1 = c1.slider("Rad 1", 0, 9, 0, key="s1")
    v2 = c2.slider("Rad 2", 0, 9, 0, key="s2")
    v3 = c3.slider("Rad 3", 0, 9, 0, key="s3")
    v4 = c4.slider("Rad 4", 0, 9, 0, key="s4")
    
    current_code = [v1, v2, v3, v4]
    
    if st.button("Schloss öffnen 🔑"):
        if current_code == door["answer"]:
            st.success("🎉 *KLICK!* Das Schloss springt auf!")
            if day not in st.session_state.solved_doors:
                st.session_state.solved_doors.append(day)
                st.rerun()
        else:
            st.error("❌ Das Schloss bleibt verschlossen.")

# ------------------------------------------------------------------------------
# RÄTSEL-TYP 2: Binär-Kippschalter (Tag 16)
# ------------------------------------------------------------------------------
elif door["type"] == "binary_switches":
    st.write("⚡ **Batterie-Konsole (Schalter-Werte: 16 | 8 | 4 | 2 | 1):**")
    b_cols = st.columns(5)
    sw1 = b_cols[0].toggle("16", key="b1")
    sw2 = b_cols[1].toggle("8", key="b2")
    sw3 = b_cols[2].toggle("4", key="b3")
    sw4 = b_cols[3].toggle("2", key="b4")
    sw5 = b_cols[4].toggle("1", key="b5")
    
    current_val = (16 if sw1 else 0) + (8 if sw2 else 0) + (4 if sw3 else 0) + (2 if sw4 else 0) + (1 if sw5 else 0)
    st.metric("Aktuelle Batterieladung", f"{current_val} / 25")
    
    if st.button("Energie einspeisen ⚡"):
        if [sw1, sw2, sw3, sw4, sw5] == door["answer"]:
            st.success("🎉 Die Batterie ist geladen! Der Generator summst wieder.")
            if day not in st.session_state.solved_doors:
                st.session_state.solved_doors.append(day)
                st.rerun()
        else:
            st.error("❌ Überlastung oder zu wenig Energie! Überprüfe die Schalter.")

# ------------------------------------------------------------------------------
# RÄTSEL-TYP 3: Audio Morse-Signal (Tag 20)
# ------------------------------------------------------------------------------
elif door["type"] == "audio_morse":
    st.write("📻 **Empfange das Morsesignal:**")
    # Generiertes MP3-Morsesignal für "SOS"
    st.audio("https://upload.wikimedia.org/wikipedia/commons/1/1d/SOS_morse_code.ogg")
    
    ans = st.text_input("Deine Übersetzung:", key=f"input_{day}")
    if st.button("Signal senden 📡"):
        if ans.strip().upper() == door["answer"]:
            st.success("🎉 Signal korrekt entschlüsselt!")
            if day not in st.session_state.solved_doors:
                st.session_state.solved_doors.append(day)
                st.rerun()
        else:
            st.error("❌ Falsches Signal.")

# ------------------------------------------------------------------------------
# RÄTSEL-TYP 4: Frachtraum-Waage (Tag 22)
# ------------------------------------------------------------------------------
elif door["type"] == "cargo_slider":
    st.write("⚖️ **Frachtraum-Waage im Cockpit:**")
    val = st.slider("Puffer-Reserve in kg hinzufügen", 0, 300, 50, step=10, key="cargo_s")
    total = 890 + val
    st.metric("Gesamtgewicht im Schlitten", f"{total} kg / 1000 kg")
    
    if st.button("Gewicht bestätigen ⚖️"):
        if val == door["answer"]:
            st.success("🎉 Perfekte Ausbalancierung! Der Schlitten liegt optimal in der Luft.")
            if day not in st.session_state.solved_doors:
                st.session_state.solved_doors.append(day)
                st.rerun()
        else:
            st.error("❌ Falsches Gewicht! Der Schlitten wäre nicht ausbalanciert.")

# ------------------------------------------------------------------------------
# RÄTSEL-TYP 5: Standard Text-/Zahleneingabe
# ------------------------------------------------------------------------------
else:
    ans = st.text_input("Deine Antwort:", key=f"input_{day}")
    if st.button("Antwort prüfen 🚀"):
        if ans.strip().upper() == door["answer"].upper():
            st.success("🎉 Richtig! Das Türchen ist geöffnet.")
            if day not in st.session_state.solved_doors:
                st.session_state.solved_doors.append(day)
                st.rerun()
        else:
            st.error("❌ Leider falsch! Versuche es noch einmal.")

# Ausklappbarer Hinweis
with st.expander("💡 Brauchst du einen Hinweis?"):
    st.write(door["hint"])
