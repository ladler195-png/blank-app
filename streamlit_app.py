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

# Weihnachtliches Custom-CSS
st.markdown("""
    <style>
    /* Dunkelblauer Nacht-Hintergrund */
    .stApp {
        background: linear-gradient(180deg, #0b1d3a 0%, #1a365d 100%);
        color: #ffffff;
    }
    
    /* Überschriften im Weihnachts-Look */
    h1, h2, h3 {
        color: #f6ad55 !important;
        font-family: 'Georgia', serif;
        text-shadow: 2px 2px 4px #000000;
    }

    /* Styling der Türchen-Buttons */
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
    
    /* Hover-Effekt auf Buttons */
    div.stButton > button:hover {
        background-color: #c53030;
        color: white;
        border-color: #f6ad55;
        transform: scale(1.03);
    }

    /* Container für Rätsel-Karten */
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
    # AKT I: DER RUF AUS DEM ELFENREICH
    1: {
        "person": "Person A",
        "title": "Tag 1: Das geheimnisvolle Päckchen",
        "story": "Vor der Haustür liegt ein verschneites Päckchen mit einer Holzschatulle und einem 4-stelligen Zahlenschloss.",
        "question": "Welcher Code öffnet das Schloss? Löse die Zahlenreihe: 3, 7, 15, 31, __",
        "answer": "63",
        "hint": "Die Differenz zwischen den Zahlen verdoppelt sich in jedem Schritt (+4, +8, +16, +32)."
    },
    2: {
        "person": "Person B",
        "title": "Tag 2: Der Hilferuf der Elfen",
        "story": "In der Schatulle liegt ein alt aussehendes Pergament mit einer Elfen-Chiffre.",
        "question": "Entschlüssele den Notsender-Code (Cäsar-Chiffre, 4 Stellen zurück im Alphabet): 'SIVX'",
        "answer": "NORD",
        "hint": "Ziehe von jedem Buchstaben 4 Stellen im Alphabet ab (S -> N, I -> O, V -> R, X -> D)."
    },
    3: {
        "person": "Person C",
        "title": "Tag 3: Der Elfen-Schlitten",
        "story": "Ein führerloser Elfen-Schlitten wartet draußen! Um die Startkonsole zu aktivieren, müsst ihr die Energiefrequenz kalibrieren.",
        "question": "Berechne die Startfrequenz: (Anzahl Rentiere: 8) × (Schatullencode von Tag 1: 63) - 4",
        "answer": "500",
        "hint": "Rechne: 8 * 63 - 4"
    },
    4: {
        "person": "Person A",
        "title": "Tag 4: Die Flugkarte zum Nordpol",
        "story": "Im Cockpit klappt eine magische Sternenkarte auf, um den Kurs einzustellen.",
        "question": "Welcher Kurs führt durch den Polarhimmel? Berechne die Summe aller Primzahlen zwischen 10 und 25.",
        "answer": "60",
        "hint": "Die Primzahlen in diesem Bereich sind 11, 13, 17, 19. Addiere diese vier Zahlen."
    },
    5: {
        "person": "Person B",
        "title": "Tag 5: Die Landung im Eisnebel",
        "story": "Der Schlitten sinkt herab. Vor euch liegt die undurchdringliche Nebelwand – das Tor zum Nebel-Labyrinth.",
        "question": "Setze das Losungswort zusammen: Lösung von Tag 2 + Ergebnis von Tag 4 (z. B. HALO10).",
        "answer": "NORD60",
        "hint": "Kombiniere den Begriff von Tag 2 (NORD) direkt mit der Zahl von Tag 4 (60)."
    },

    # AKT II: DAS NEBEL-LABYRINTH
    6: {
        "person": "Person C",
        "title": "Tag 6: Nikolaus im Eisnebel",
        "story": "Im dichten Nebel findet ihr eine goldene Nikolaus-Statuette im Schnee.",
        "question": "Welche Zahl gehört in die Mitte (Feld X) des magischen 3x3-Quadrats (Zahlen 1-9)?",
        "answer": "5",
        "hint": "In jedem magischen 3x3-Quadrat mit den Zahlen 1 bis 9 liegt die Zahl 5 immer genau in der Mitte."
    },
    7: {
        "person": "Person A",
        "title": "Tag 7: Die Weggabelung der Eiszapfen",
        "story": "Das Labyrinth teilt sich in vier Pfade. Die Eiszapfen am Weg W folgen einer mathematischen Gesetzmäßigkeit.",
        "question": "Welche Zahl hat der Weg W, wenn die Folge 3, 6, 11, 18, 27, __ lautet?",
        "answer": "38",
        "hint": "Schau dir die Abstände an: +3, +5, +7, +9... Wie viel musst du zu 27 addieren?"
    },
    8: {
        "person": "Person B",
        "title": "Tag 8: Das Echo im Gletscher",
        "story": "Das Nebelhorn der Elfen schallt durch die Spalten. Es wirft ein Echo zurück, das sich in seiner Frequenz verdoppelt.",
        "question": "Ein Ton von 440 Hz wird 3-mal im Echo gedoppelt. Wie hoch ist die Endfrequenz in Hz?",
        "answer": "3520",
        "hint": "Rechne: 440 * 2 * 2 * 2 (oder 440 * 8)."
    },
    9: {
        "person": "Person C",
        "title": "Tag 9: Die Eisspiegel-Grotte",
        "story": "Um die Nebeltür aufzubrennen, muss der Lichtstrahl einer Laterne über Spiegel umgelenkt werden.",
        "question": "Der Strahl startet nach Osten. Er trifft nacheinander auf 3 Spiegel: Links, Rechts, Links. In welche Himmelsrichtung schlägt der Strahl am Ende ein?",
        "answer": "NORD",
        "hint": "Start: Ost -> Links = Nord -> Rechts = Ost -> Links = Nord."
    },
    10: {
        "person": "Person A",
        "title": "Tag 10: Der gefrorene Kompass",
        "story": "Die Kompassnadel ist durch Eis blockiert.",
        "question": "Welcher Winkel führt aus dem Nebel? Löse: (Höhe des Watzmanns: 2713) Modulo 360",
        "answer": "193",
        "hint": "Teile 2713 durch 360. Der Rest dieser Division (2713 - 7 * 360) ist das Ergebnis."
    },
    11: {
        "person": "Person B",
        "title": "Tag 11: Die brüchige Eisbrücke",
        "story": "Die Steinbrücke ist nur passierbar, wenn ihr die Trittsteine nach der Logik der Primfaktoren wählt.",
        "question": "Wie lautet die Summe aller Primfaktoren der Zahl 42? (42 = 2 × 3 × 7)",
        "answer": "12",
        "hint": "Addiere die drei Primzahlen 2, 3 und 7."
    },
    12: {
        "person": "Person C",
        "title": "Tag 12: Der Durchbruch am Nordpol",
        "story": "Der Nebel lichtet sich! Vor euch erstrahlen die Lichter der Werkstatt.",
        "question": "Setzt das Tor-Passwort zusammen: Wort von Tag 9 + Ergebnis von Tag 11 (z. B. WEST15).",
        "answer": "NORD12",
        "hint": "Kombiniere die Himmelsrichtung von Tag 9 (NORD) direkt mit der Zahl von Tag 11 (12)."
    },

    # AKT III: DIE RETTUNG DER WERKSTATT
    13: {
        "person": "Person A",
        "title": "Tag 13: Der vereiste Maschinensaal",
        "story": "Die Hauptgetriebe der Geschenkmaschine stecken fest. Drei Zahnräder mit 12, 18 und 24 Zähnen greifen ineinander.",
        "question": "Nach wie vielen Umdrehungen des ersten Rads (12 Zähne) stehen alle drei Räder wieder in ihrer Startposition?",
        "answer": "6",
        "hint": "Das kgV von 12, 18 und 24 ist 72. Teile 72 durch 12 Zähne."
    },
    14: {
        "person": "Person B",
        "title": "Tag 14: Das Durcheinander in der Packstation",
        "story": "Ein Kobold hat die Geschenkaufkleber vertauscht! Nur ein Anagramm enthüllt den echten Namen des Oberelfs.",
        "question": "Welches Wort ergibt sich aus den Buchstaben 'E-L-F-E-N-M-A-G-I-E', wenn man das Wort 'MAGIE' entfernt?",
        "answer": "ELFEN",
        "hint": "Streich die Buchstaben M-A-G-I-E aus dem Wort heraus."
    },
    15: {
        "person": "Person C",
        "title": "Tag 15: Das Rentier-Futter-Rezept",
        "story": "Rudolph und seine Freunde brauchen Stärkung! Das Kraftfutter besteht aus Hafer, Sternenstaub und Äpfeln im Verhältnis 5 : 2 : 3.",
        "question": "Ihr wollt insgesamt 50 kg Futter herstellen. Wie viele kg Sternenstaub benötigt ihr?",
        "answer": "10",
        "hint": "Gesamtteile: 5 + 2 + 3 = 10 Teile. 50 kg / 10 Teile = 5 kg pro Teil. Sternenstaub hat 2 Teile (2 * 5 kg)."
    },
    16: {
        "person": "Person A",
        "title": "Tag 16: Die Sternenstaub-Batterie",
        "story": "Die Energiegeneratoren der Werkstatt sind schwach. Ein Schieberegler verlangt die binäre Eingabe der Zahl 25.",
        "question": "Wandle die Dezimalzahl 25 in eine 5-stellige Binärzahl um (bestehend aus 0 und 1).",
        "answer": "11001",
        "hint": "25 = 16 + 8 + 0 + 0 + 1. Setze für vorhandene Werte eine 1, sonst eine 0."
    },
    17: {
        "person": "Person B",
        "title": "Tag 17: Die Wunschzettel-Sortiermaschine",
        "story": "Millionen Briefe fliegen durch die Luft! Der Sortieralgorithmus fragt nach dem Median einer Datenreihe.",
        "question": "Wie lautet der Median der folgenden Werte: 12, 45, 7, 23, 89, 34, 19?",
        "answer": "23",
        "hint": "Sortiere die 7 Zahlen aufsteigend: 7, 12, 19, 23, 34, 45, 89. Nimm genau die vierte (mittlere) Zahl."
    },
    18: {
        "person": "Person C",
        "title": "Tag 18: Das Sicherheitssystem der Werkstatt",
        "story": "Die Schalttafel der Werkstatt verlangt den Werkstatt-Schlüsselcode.",
        "question": "Berechne den Werkstatt-Code: (Lösung Tag 13: 6) × (Lösung Tag 15: 10) + (Lösung Tag 17: 23)",
        "answer": "83",
        "hint": "Rechne: 6 * 10 + 23"
    },

    # AKT IV: DAS FINALE
    19: {
        "person": "Person A",
        "title": "Tag 19: Der Flugrouten-Optimierer",
        "story": "Der Weihnachtsmann muss 4 Städte anfliegen (A, B, C, D). Die Distanzen bilden ein Quadrat mit Seitenlänge 100 km.",
        "question": "Was ist die kürzeste Strecke (in km), um alle 4 Ecken eines 100x100km Quadrats einmal abzufliegen?",
        "answer": "300",
        "hint": "Du musst 3 Kanten des Quadrats entlangfliegen: 100 km + 100 km + 100 km."
    },
    20: {
        "person": "Person B",
        "title": "Tag 20: Der Polarlichter-Sender",
        "story": "Damit der Schlitten im Dunkeln navigieren kann, müsst ihr die Frequenz der Polarlichter auf Morseschrift abstimmen.",
        "question": "Übersetze den Morsecode in Wortform: ••• / --- / •••",
        "answer": "SOS",
        "hint": "Drei kurze Töne stehen für S, drei lange für O."
    },
    21: {
        "person": "Person C",
        "title": "Tag 21: Die magische Rentiere-Aufstellung",
        "story": "Die 8 Rentiere müssen vor den Schlitten gespannt werden.",
        "question": "Wenn Rudolph immer ganz vorne stehen muss, wie viele Möglichkeiten gibt es dann noch für die restlichen 7 Rentiere? (7!)",
        "answer": "5040",
        "hint": "Berechne 7! = 7 × 6 × 5 × 4 × 3 × 2 × 1."
    },
    22: {
        "person": "Person A",
        "title": "Tag 22: Die Puffer-Reserve",
        "story": "Der Schlitten belädt sich automatisch. Ihr müsst ein Zielgewicht im Frachtraum einstellen.",
        "question": "Welches Gewicht (in kg) fehlt noch? Ziel = 1000 kg. Geladen: 3 Kisten zu je 150 kg und 4 Kisten zu je 110 kg.",
        "answer": "110",
        "hint": "3 * 150 = 450. 4 * 110 = 440. Summe bisher: 890 kg. Berechne 1000 - 890."
    },
    23: {
        "person": "Person B",
        "title": "Tag 23: Die finale Startbereitschaft",
        "story": "Alle Systeme stehen auf Grün! Nur noch der Freigabe-Schlüssel fehlt.",
        "question": "Addiere den Schlitten-Code von Tag 3 (500) und den Werkstatt-Code von Tag 18 (83).",
        "answer": "583",
        "hint": "Rechne: 500 + 83"
    },
    24: {
        "person": "Alle 3 gemeinsam",
        "title": "Tag 24: HEILIGABEND – Die Rettung von Weihnachten!",
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

# Fortschrittsbalken
progress = len(st.session_state.solved_doors) / 24
st.write(f"**Expeditions-Fortschritt:** {len(st.session_state.solved_doors)} von 24 Rätseln gelöst")
st.progress(progress)

st.divider()

# ==============================================================================
# 5. TÜRCHEN-GRID (24 TAGE)
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
# 6. AKTIVES RÄTSEL-INTEREST
# ==============================================================================
day = st.session_state.active_day
door_data = DOORS[day]

st.subheader(f"✨ {door_data['title']}")
st.caption(f"👤 Zuständig: **{door_data['person']}**")

# Geschichte & Rätsel anzeigen
st.info(f"📖 **Geschichte:** {door_data['story']}")
st.markdown(f"❓ **Aufgabe:** {door_data['question']}")

# Eingabefeld für die Antwort
user_input = st.text_input("Deine Antwort:", key=f"input_{day}")

col1, col2 = st.columns([1, 4])

with col1:
    if st.button("Antwort prüfen 🚀"):
        # Groß-/Kleinschreibung und Leerzeichen ignorieren
        if user_input.strip().upper() == door_data["answer"].upper():
            st.success("🎉 Richtig! Das Türchen ist geöffnet.")
            if day not in st.session_state.solved_doors:
                st.session_state.solved_doors.append(day)
                st.rerun()
        else:
            st.error("❌ Leider falsch! Versuche es noch einmal.")

# Hinweis-Button (ausklappbar)
with st.expander("💡 Brauchst du einen Hinweis?"):
    st.write(door_data["hint"])
