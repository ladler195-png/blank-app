import streamlit as st
import time

# --- SEITEN-KONFIGURATION ---
st.set_page_config(
    page_title="Weihnachtlicher Rätsel-Adventskalender für Profis",
    page_icon="🎄",
    layout="wide"
)

# --- DESIGN & FARBZELLEN (Dunkelrot, Dunkelgrün & Gold) ---
st.markdown("""
<style>
    /* Gesamter Hintergrund in edlem Dunkelrot */
    .stApp {
        background-color: #4a0e17;
        color: #f4f6f5;
    }
    
    /* Überschriften in Gold */
    h1, h2, h3, h4, h5, h6 {
        color: #ffd700 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Advents-Türchen / Buttons: Dunkelgrün mit goldenem Rand */
    .stButton>button {
        background-color: #1e5631 !important;
        color: #ffd700 !important;
        border: 2px solid #ffd700 !important;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2e7d43 !important;
        color: #ffffff !important;
        border-color: #ffffff !important;
    }
    
    /* Puzzleteile / Karten */
    .puzzle-card {
        background-color: #143d26;
        border: 1px solid #ffd700;
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 8px;
        color: #ffffff;
    }
    
    /* Zeitstrahl-Container */
    .timeline-container {
        display: flex;
        overflow-x: auto;
        gap: 15px;
        padding: 15px 0;
        scrollbar-color: #ffd700 #143d26;
    }
    
    /* Morse-Terminal Bildschirm */
    .morse-screen {
        background-color: #143d26;
        border: 2px solid #ffd700;
        color: #00ff66;
        padding: 15px;
        font-family: monospace;
        font-size: 1.2rem;
        border-radius: 6px;
        text-align: center;
        margin-bottom: 15px;
    }

    /* NEU: Story-Boxen (früher blau, jetzt im dunkelgrünen Look mit Gold) */
    div.stAlert {
        background-color: #143d26 !important; /* Dunkelgrün */
        color: #ffffff !important;           /* Weißer Text */
        border: 1px solid #ffd700 !important; /* Goldener Rand */
    }
    div.stAlert svg {
        fill: #ffd700 !important; /* Info-Symbol in Gold */
    }
    
    /* Eingabefelder und kleine Texte */
    .stTextInput input {
        background-color: #380a11 !important;
        color: #ffffff !important;
        border: 1px solid #ffd700 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALISIERUNG ---
if "solved_doors" not in st.session_state:
    st.session_state.solved_doors = []

if "active_day" not in st.session_state:
    st.session_state.active_day = 1

if "morse_buffer" not in st.session_state:
    st.session_state.morse_buffer = ""

if "river" not in st.session_state:
    st.session_state.river = {"boat": "left", "wolf": "left", "goat": "left", "cabbage": "left"}

if "mirror_state" not in st.session_state:
    st.session_state.mirror_state = ["\\", "/", "\\"]

if "package_sort_step" not in st.session_state:
    st.session_state.package_sort_step = 0
# --- DATENBANK: ALLE TÜRCHEN (1 bis 24) ---
DOORS = {
    1: {
        "title": "Tag 1: Die mysteriöse Holzbox",
        "person": "Detektiv Kringle",
        "type": "text",
        "story": "Es klingelt an der Haustür. Ihr öffnet, aber niemand steht davor. Stattdessen liegt ein schweres, eisiges Päckchen vor der Tür vom Absender 'Nordpol'. Im Wohnzimmer geöffnet, kommt eine Holzbox mit einem Zahlenschloss zum Vorschein.",
        "question": "Löse das Rätsel des Gedichts:\n\n> *Vier kleine Ziffern im winterlichen Schnee.*\n> *Zähle die Buchstaben, die ich dir steh.*\n> *Wie viele Ecken hat ein Stern plus die Anzahl der Rentiere fern*\n> *minus die Ziffer, die an Weihnachten lacht, hat das Schloss für euch aufgemacht.*\n\nGib den vierstelligen Zahlencode ein:",
        "answer": "5924",
        "puzzle_piece": None,
        "hint": "Stern-Ecken (5) + Rentiere (9) - Weihnachtstag (24)... achte auf die Ziffernkombination."
    },
    2: {
        "title": "Tag 2: Das vergilbte Pergament",
        "person": "Archivar Frost",
        "type": "text",
        "story": "Das Schloss springt auf und im Inneren liegt ein altes Pergament mit der kryptischen Cäsar-Verschlüsselung 'S I V X'.",
        "question": "Entschlüssele das Codewort mithilfe der klassischen Alphabet-Verschiebung (-3):",
        "answer": "NORD",
        "puzzle_piece": None,
        "hint": "Jeder Buchstabe im Alphabet wird um 3 Positionen zurückverschoben (S -> P -> O -> N...)."
    },
    3: {
        "title": "Tag 3: Das Rentier-Expertenrätsel",
        "person": "Leit-Rentier Rudolf",
        "type": "text",
        "story": "Glockenklingeln! Vor dem Fenster wartet der Rentierschlitten. Die Tiere prüfen euch mit knallhartem biologischen und historischen Expertenwissen.",
        "question": "Welches Rentier-Leitmerkmal besitzen sowohl Männchen als auch Weibchen (im Gegensatz zu fast allen anderen Hirscharten)? Antworte mit einem Wort:",
        "answer": "GEWEIH",
        "puzzle_piece": None,
        "hint": "Es ist der prächtige Kopfschmuck, den Rentiere tragen."
    },
    4: {
        "title": "Tag 4: Das Navigationssystem",
        "person": "Pilot Blitz",
        "type": "text",
        "story": "Ihr sitzt im Schlitten. Das Bordsystem verlangt die exakten Kurskoordinaten aus dem Handbuch, formatiert untereinander.",
        "question": "Berechne die Koordinaten:\n\n- Breitengrad: Exakt 90 Grad Nord minus die Anzahl der Rentiere.\n- Längengrad: Die magische Quersumme von 2026 multipliziert mit 10.\n\nGib beide Werte als 5-stelligen Gesamtwert ein (Breitengrad + Längengrad):",
        "answer": "81100",
        "puzzle_piece": "Koordinaten-Init",
        "hint": "90 - 9 = 81; Quersumme von 2026 (2+0+2+6 = 10) * 10 = 100 -> 81100"
    },
    5: {
        "title": "Tag 5: Das Nebel-Tor",
        "person": "Wetter-Elfe Blizzard",
        "type": "text",
        "story": "Der Schlitten steuert auf eine undurchdringliche Nebelwand aus blauem Eis zu. Nur meteorologisches Fachwissen öffnet die Barriere.",
        "question": "Wie nennt man den kritischen physikalischen Punkt in der Meteorologie, bei dem die Luft bei konstantem Druck vollständig mit Wasserdampf gesättigt ist? (8 Buchstaben)",
        "answer": "TAUPUNKT",
        "puzzle_piece": "🧩 Fragment 1: **E**",
        "hint": "Die Temperatur, bei der die relative Luftfeuchtigkeit 100% erreicht."
    },
    6: {
        "title": "Tag 6: Das magische Sudoku",
        "person": "Mathematiker Zahlix",
        "type": "sudoku_puzzle",
        "story": "Hinter dem Nebel glimmt eine eingefrorene Eistafel mit einer mathematischen Zeilensummen-Aufgabe auf.",
        "question": "In einer unvollständigen Sudoku-Zeile stehen die Zahlen 8, [?], 6. Die Zeilensumme muss 15 ergeben.",
        "answer": "1",
        "puzzle_piece": "🧩 Fragment 2: **R**",
        "hint": "8 + x + 6 = 15. Welchen Wert hat x?"
    },
    7: {
        "title": "Tag 7: Der Jetstream-Kurs",
        "person": "Lotse Strato",
        "type": "logic_grid",
        "story": "Plötzliche Sturmböen erfordern die logische Zuordnung des schnellsten Höhenkorridors anhand von Logikgitter-Hinweisen.",
        "question": "Welcher Weg wurde als sicherster Korridor ermittelt? (Gib den Namen als Lösung ein, z.B. EISHÖHLE)",
        "answer": "EISHÖHLE",
        "puzzle_piece": "🧩 Fragment 3: **N**",
        "hint": "Suche nach dem geheimnisvollen Eishöhlen-Weg."
    },
    8: {
        "title": "Tag 8: Das verzerrte Funksignal",
        "person": "Funker Morse",
        "type": "morse_terminal",
        "story": "Mitten im Sturm empfängt das Funkgerät eine stark verrauschte Notfall-Nachricht aus der Weihnachtswerkstatt. Übertrage das universelle Notsignal.",
        "question": "Benutze das interaktive Terminal, um das SOS-Signal (...---...) zu senden.",
        "answer": "...---...",
        "puzzle_piece": "🧩 Fragment 4: **T**",
        "hint": "Dreimal kurz, dreimal lang, dreimal kurz."
    },
    9: {
        "title": "Tag 9: Das Laser-Spiegel-Rätsel",
        "person": "Ingenieur Lumina",
        "type": "mirror_puzzle",
        "story": "Das Energieschild des Schlittens sinkt im Polarlicht. Ihr müsst den Laserstrahl über die optischen Spiegel korrekt ausrichten.",
        "question": "Bringe alle drei Spiegel in die richtige Ausrichtung: Spiegel A (/), Spiegel B (\\), Spiegel C (/).",
        "answer": ["/", "\\", "/"],
        "puzzle_piece": "🧩 Fragment 5: **E**",
        "hint": "Schalte die Spiegel durch Klicken so, dass das grüne Kontrolllicht aufleuchtet."
    },
    10: {
        "title": "Tag 10: Die Fluss-Transport-Steuerung",
        "person": "Fährmann Brutus",
        "type": "river_crossing",
        "story": "Der Weg ist durch einen eisigen Fluss versperrt. Transportiere den Wolf, die Ziege und den Kohlkopf sicher auf die andere Seite, ohne dass Fress-Regeln verletzt werden.",
        "question": "Bringe alle Akteure über den Fluss.",
        "answer": "SOLVED",
        "puzzle_piece": "🧩 Fragment 6: **N**",
        "hint": "Achte darauf, dass der Wolf die Ziege und die Ziege den Kohl nicht allein lässt."
    },
    11: {
        "title": "Tag 11: Der Energie-Kern",
        "person": "Physik-Elfe Quanta",
        "type": "text",
        "story": "Der magische Antrieb verlangt eine kombinatorische Formel zur Energiebündelung.",
        "question": "Berechne die mathematische Fakultät von 5 (Notiert als 5!):",
        "answer": "120",
        "puzzle_piece": "🧩 Fragment 7: **S**",
        "hint": "Multipliziere fortlaufend: 1 * 2 * 3 * 4 * 5."
    },
    12: {
        "title": "Tag 12: Das Tor zum Polarkreis",
        "person": "Torwächter Boreas",
        "type": "text",
        "story": "Der Nordpol ist erreicht. Eine magische Eistür verlangt das aus den gesammelten Fragmenten gebildete Codewort.",
        "question": "Setze die gesammelten Buchstaben zu einem hellen Himmelsphänomen zusammen:",
        "answer": "STERNEN",
        "puzzle_piece": "🏆 ZUGANG ZUR WERKSTATT FREIGESCHALTET",
        "hint": "Ordne die Fragmente E-R-N-T-E-N-S zu."
    },
    13: {
        "title": "Tag 13: Die Ventil-Steuerung",
        "person": "Mechaniker Schraub",
        "type": "gear_puzzle",
        "story": "Ihr betretet die Maschinenhalle. Die Ventile müssen perfekt eingestellt werden, damit die Fließbänder anlaufen.",
        "question": "Justiere Ventil A und Ventil B so, dass der Zieldruck von exakt 72 Bar erreicht wird.",
        "answer": 72,
        "puzzle_piece": None,
        "hint": "Multipliziere den Wert von Ventil A mit Ventil B, bis 72 herauskommt."
    },
    14: {
        "title": "Tag 14: Paket-Sortier-Station",
        "person": "Roboter R-04",
        "type": "package_sort",
        "story": "In der Sortierhalle läuft ein Fließband Amok. Lenke die Pakete in die korrekten Rutschen.",
        "question": "Sortiere alle ankommenden Pakete fehlerfrei ein.",
        "answer": "SORTED",
        "puzzle_piece": None,
        "hint": "Befolge die Anweisungen auf dem Bildschirm für Standard- und Express-Pakete."
    },
    15: {
        "title": "Tag 15: Die Wunschlisten-Matrix",
        "person": "Chef-Elfe Holly",
        "type": "text",
        "story": "Die Wunschlisten sind nach einer mathematischen Rekursionsformel verrutscht.",
        "question": "Führe die Fibonacci-Reihe logisch fort: 1, 1, 2, 3, 5, 8, 13, ?",
        "answer": "21",
        "puzzle_piece": None,
        "hint": "Die Summe der beiden vorherigen Zahlen (8 + 13)."
    },
    16: {
        "title": "Tag 16: Das binäre Notstrom-Aggregat",
        "person": "Techniker Volt",
        "type": "binary_switches",
        "story": "Aktiviere die digitalen Schaltkreise für die Hauptbeleuchtung der Werkstatt.",
        "question": "Schalte die Binär-Bits so, dass der dezimale Wert 25 dargestellt wird.",
        "answer": [True, 1, 0, 0, 1],
        "puzzle_piece": None,
        "hint": "Dezimal 25 = 16 + 8 + 1 (Schalter 1, 2 und 5 aktivieren)."
    },
    17: {
        "title": "Tag 17: Frequenz-Tuner",
        "person": "Kommunikations-Elfe Antenne",
        "type": "frequency_tuner",
        "story": "Stelle den Funkempfänger auf die exakte Notruf-Frequenz ein.",
        "question": "Finde die richtige Frequenz im Bereich von 80 bis 100 MHz.",
        "answer": 92.5,
        "puzzle_piece": None,
        "hint": "Der Wert liegt genau zwischen 92.0 und 93.0 MHz."
    },
    18: {
        "title": "Tag 18: Futter-Mischwaage",
        "person": "Stallmeister Futter",
        "type": "scale_puzzle",
        "story": "Mische das magische Futter für die Rentiere in exakten Gewichtsverhältnissen an.",
        "question": "Stelle Hafer (25kg), Sternenstaub (10kg) und Äpfel (15kg) an den Schiebereglern ein.",
        "answer": "BALANCED",
        "puzzle_piece": None,
        "hint": "Justiere die Gewichte exakt nach den Vorgaben."
    },
    19: {
        "title": "Tag 19: Der Tresor des Weihnachtsmanns",
        "person": "Weihnachtsmann Claus",
        "type": "lock_sliders",
        "story": "Im Büro des Weihnachtsmanns hängt ein schwerer Stahltresor mit einem Ziffern-Zahlenschloss.",
        "question": "Gib den 4-stelligen Zifferncode [1, 9, 1, 1] ein.",
        "answer": [1, 9, 1, 1],
        "puzzle_piece": None,
        "hint": "Nutze das Entdeckungsjahr des Südpols als Code."
    },
    20: {
        "title": "Tag 20: Der magische Polar-Kristall",
        "person": "Kristall-Hüterin Aurora",
        "type": "frequency_tuner",
        "story": "Stelle den Resonanzwert des rohen Polar-Kristalls auf den korrekten Grad ein.",
        "question": "Wie viel Grad beträgt die klassische Winkelsumme im Dreieck?",
        "answer": 180.0,
        "puzzle_piece": None,
        "hint": "Genau die Hälfte eines Vollkreises."
    },
    21: {
        "title": "Tag 21: Das Erwachen der Werkstatt",
        "person": "Alle Elfen",
        "type": "text",
        "story": "Der Kristall glüht in hellem Licht. Die Maschinen erwachen ratternd zum Leben!",
        "question": "Gib das finale Lösungswort ein, das den ultimativen Wendepunkt der Mission markiert:",
        "answer": "WENDEPUNKT",
        "puzzle_piece": "🌟 WERKSTATT VOLL EINSATZBEREIT",
        "hint": "Das zentrale Wort für den Wendepunkt."
    },
    22: {
        "title": "Tag 22: Der magische Polar-Kompass",
        "person": "Navigatorin Polarstern",
        "type": "text",
        "story": "Der Schlitten nähert sich dem Ziel, aber der Nordstern wird von dichten Wolken verdeckt. Nur der magische Kompass zeigt den Weg, wenn man die Himmelsrichtungen richtig deutet.",
        "question": "Welche Himmelsrichtung liegt exakt im 90-Grad-Winkel rechts von Norden? (Antworte auf Deutsch, Großbuchstaben):",
        "answer": "OSTEN",
        "puzzle_piece": None,
        "hint": "Denke an den Spruch: 'Norden, ...'"
    },
    23: {
        "title": "Tag 23: Das letzte Rätsel des Weihnachtsmanns",
        "person": "Der Weihnachtsmann",
        "type": "text",
        "story": "Vor der allerletzten Tür steht der Weihnachtsmann persönlich. Er lächelt und stellt dir eine klassische Denksportaufgabe für die allerletzte Vorbereitungsnacht.",
        "question": "Ich habe Städte, aber keine Häuser. Ich habe Wälder, aber keine Bäume. Ich habe Wasser, aber keine Fische. Was bin ich?",
        "answer": "KARTE",
        "puzzle_piece": None,
        "hint": "Man schaut hinein, wenn man den Weg sucht (Land-... oder Welt-...)."
    },
    24: {
        "title": "Tag 24: HEILIGABEND – Das große Weihnachts-Finale! 🎄",
        "person": "Alle Elfen & Rentiere",
        "type": "special_finale",
        "story": "Alle Türchen sind geöffnet! Die Geschenke sind verpackt, die Rentiere gesattelt und der Sternenhimmel brennt in den schönsten Farben. Die Mission ist geschafft: Weihnachten ist gerettet!",
        "question": "Klicke unten auf den Start-Button, um den Startschuss für die Bescherung zu geben!",
        "answer": "GESCHAFFT",
        "puzzle_piece": "🌟 FROHE WEIHNACHTEN!",
        "hint": "Genieße den Moment – du hast es geschafft!"
    }
}

# --- HEADER & TITEL ---
st.title("🎄 Weihnachtlicher Rätsel-Adventskalender")
st.markdown("### Mission: Weihnachten retten (Profi-Edition) 🎅✨")
st.write("Wähle ein Türchen in der interaktiven Zeitleiste aus, um die anspruchsvollen Aufgaben zu lösen.")

# --- ZEITLEISTE (TIMELINE) ALS NAVIGATION (1 bis 24) ---
st.markdown("#### ⏳ Advents-Zeitstrahl (Türchen 1 bis 24)")
timeline_cols = st.columns(24)

for d_num in range(1, 25):
    is_solved = d_num in st.session_state.solved_doors
    is_active = st.session_state.active_day == d_num
    
    label = f"✓ {d_num}" if is_solved else f"{d_num}"
    
    with timeline_cols[d_num - 1]:
        if st.button(label, key=f"time_{d_num}", use_container_width=True):
            st.session_state.active_day = d_num
            st.rerun()

st.markdown("---")

# ==============================================================================
# RÄTSEL-FLÄCHE & DYNAMISCHES LAYOUT
# ==============================================================================
show_sidebar = 5 <= st.session_state.active_day <= 12
if show_sidebar:
    main_col, puzzle_col = st.columns([2, 1])
else:
    main_col = st.container()

with main_col:
    day = st.session_state.active_day
    door = DOORS[day]

    st.subheader(f"{door['title']}")
    st.caption(f"Verantwortlich: **{door['person']}**")
    
    st.info(f"📖 {door['story']}")
    st.markdown(f"**Aufgabe:** {door['question']}")

    # --- SONDER-WIDGETS ---
    
    # TAG 6: SUDOKU
    if door["type"] == "sudoku_puzzle":
        s_input = st.text_input("Fehlende Zahl oben in der Mitte eintragen:", key="s_in")
        if st.button("Sudoku bestätigen 🔢", key=f"chk_{day}"):
            if s_input.strip() == "1":
                st.success("🎉 Richtig! Die Zahl 1 vervollständigt die Zeilensumme 15.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsch. Überprüfe die Zeilensumme 8 + ? + 6 = 15.")

    # TAG 7: LOGIKGITTER
    elif door["type"] == "logic_grid":
        ans_lg = st.text_input("Deine Lösung (Weg):", key="lg_input")
        if st.button("Logikgitter auswerten 🗺️", key=f"chk_{day}"):
            if ans_lg.strip().upper() in ["EISHÖHLEN-WEG", "EISHOHLEN-WEG", "EISHÖHLE"]:
                st.success("🎉 Richtig gelöst!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Die Zuordnung stimmt noch nicht.")

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

    # TAG 10: TRANSPORT-RÄTSEL
    elif door["type"] == "river_crossing":
        st.write("🐺🐐🥬 **Fluss-Transport-Steuerung:**")
        r = st.session_state.river
        
        st.write(f"📍 **Linkes Ufer:** {[k for k, v in r.items() if v == 'left' and k != 'boat']}")
        st.write(f"🛶 **Boot Position:** Ufer {r['boat'].upper()}")
        st.write(f"📍 **Rechtes Ufer:** {[k for k, v in r.items() if v == 'right' and k != 'boat']}")
        
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            item_to_move = st.selectbox("Passagier mitnehmen:", ["Niemand (leer fahren)", "wolf", "goat", "cabbage"], key="river_item")
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

    # TAG 9: SPIEGEL-RÄTSEL
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

    # TAG 13: GETRIEBE-RÄTSEL
    elif door["type"] == "gear_puzzle":
        v_a = st.slider("Ventil A (Hauptfaktor)", 1, 12, 4, key="v_a_slider")
        v_b = st.slider("Ventil B (Multiplikator)", 1, 12, 4, key="v_b_slider")
        current_pressure = v_a * v_b
        st.metric("Aktueller Systemdruck", f"{current_pressure} Bar", delta=f"{current_pressure - 72} Bar Abweichung")
        
        if st.button("Ventile einrasten ⚙️", key=f"chk_{day}"):
            if current_pressure == 72:
                st.success("🎉 Perfekt! Der Systemdruck stabilisiert sich bei exakt 72 Bar.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error(f"❌ Druck inkorrekt ({current_pressure} Bar). Benötigt werden exakt 72 Bar!")

    # TAG 14: PAKET-SORTIER-MINISPIEL
    elif door["type"] == "package_sort":
        steps = [
            {"paket": "🎁 Riesen-Teddybär", "correct": "Standard-Rutsche"},
            {"paket": "⚡ Magischer Sternenstaub", "correct": "Express-Rutsche"},
            {"paket": "🧸 Holz-Eisenbahn", "correct": "Standard-Rutsche"}
        ]
        current_s = st.session_state.package_sort_step
        
        if current_s < len(steps):
            st.markdown(f"**Aktuelles Paket:** `{steps[current_s]['paket']}`")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                if st.button("📥 In Standard-Rutsche", key=f"sort_std_{current_s}"):
                    if steps[current_s]["correct"] == "Standard-Rutsche":
                        st.session_state.package_sort_step += 1
                        st.success("Richtig einsortiert!")
                        st.rerun()
                    else:
                        st.error("Falsche Rutsche!")
            with col_p2:
                if st.button("🚀 In Express-Rutsche", key=f"sort_exp_{current_s}"):
                    if steps[current_s]["correct"] == "Express-Rutsche":
                        st.session_state.package_sort_step += 1
                        st.success("Richtig einsortiert!")
                        st.rerun()
                    else:
                        st.error("Falsche Rutsche!")
        else:
            st.success("🎉 Alle Pakete erfolgreich sortiert!")
            if day not in st.session_state.solved_doors:
                st.session_state.solved_doors.append(day)
                st.rerun()

    # TAG 16: BINÄR-SCHALTER
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
                st.error("❌ Falsche Schaltung für Dezimalzahl 25.")

    # TAG 17 & 20: FREQUENZ / WAGE
    elif door["type"] == "frequency_tuner":
        freq = st.slider("📻 Empfänger (MHz):", 80.0, 100.0, 92.0, step=0.5, key="freq_slider")
        if st.button("Signal-Frequenz feststellen 📡", key=f"chk_{day}"):
            if abs(freq - door["answer"]) < 0.1:
                st.success("🎉 Glasklarer Empfang!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Nur Rauschen im Äther.")

    elif door["type"] == "scale_puzzle":
        w_hafer = st.slider("🌾 Hafer (kg)", 0, 50, 20, key="w_h")
        w_staub = st.slider("✨ Sternenstaub (kg)", 0, 50, 5, key="w_s")
        w_aepfel = st.slider("🍎 Äpfel (kg)", 0, 50, 10, key="w_a")
        if st.button("Futter-Mischung wiegen ⚖️", key=f"chk_{day}"):
            if w_hafer == 25 and w_staub == 10 and w_aepfel == 15:
                st.success("🎉 Perfektes Futter-Verhältnis!")
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

    # TAG 24: SPEZIAL-FINALE
    elif door["type"] == "special_finale":
        st.markdown("## 🎁✨ DER HEILIGABEND IST DA! ✨🎁")
        st.balloons()
        
        if st.button("🚀 Schlitten starten & Geschenke verteilen!", key="final_start_btn"):
            progress = st.progress(0)
            status = st.empty()
            
            for i in range(100):
                time.sleep(0.015)
                progress.progress(i + 1)
                status.text(f"Schlitten-Antrieb auf Höchstleistung... {i + 1}%")
            
            status.text("🎅 Ho Ho Ho! Der Schlitten ist abgehoben! Frohe Weihnachten!")
            st.success("🎉 MISSION ERFOLGREICH BEENDET! Du hast den ultimativen Adventskalender gemeistert.")
            
            st.markdown("""
            ---
            ### 📜 Urkunde des Chef-Elfen
            > **Hiermit wird feierlich bestätigt:**
            > Du hast alle 24 Stationen dieses kniffligen Profi-Kalenders gelöst.
            > Du bist offiziell **Ehren-Elf des Nordpols** und Retter des Weihnachtsfests!
            > 
            > *Vielen Dank fürs Miträtseln und fröhliche, besinnliche Feiertage!* 🎄✨
            """)
            
            if 24 not in st.session_state.solved_doors:
                st.session_state.solved_doors.append(24)
                st.rerun()

    # STANDARD-TEXT RÄTSEL
    else:
        if door["type"] not in ["sudoku_puzzle", "logic_grid", "morse_terminal", "river_crossing", "mirror_puzzle", "gear_puzzle", "package_sort", "binary_switches", "frequency_tuner", "scale_puzzle", "lock_sliders", "special_finale"]:
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
# SEITENLEISTE (FRAGMENT-SAMMLUNG FÜR TAG 5 BIS 12)
# ==============================================================================
if show_sidebar:
    with puzzle_col:
        st.subheader("🌀 Puzzleteil-Fragmente")
        st.caption("Sammle hier die Buchstaben (Tag 5 bis 12):")
        
        lab_pieces = [d for d in st.session_state.solved_doors if 5 <= d <= 12 and DOORS[d]["puzzle_piece"]]
        
        if not lab_pieces:
            st.write("*Noch keine Fragmente gesammelt.*")
        else:
            for d in sorted(lab_pieces):
                st.markdown(f"<div class='puzzle-card'><b>Tag {d}:</b><br>{DOORS[d]['puzzle_piece']}</div>", unsafe_allow_html=True)
                
        st.write("---")
        st.metric("Gefundene Fragmente", f"{len(lab_pieces)} / 8")
