import streamlit as st

# --- SEITEN-KONFIGURATION ---
st.set_page_config(
    page_title="Weihnachtlicher Rätsel-Adventskalender für Profis",
    page_icon="🎄",
    layout="centered"
)

# --- SESSION STATE INITIALISIERUNG ---
if "solved_doors" not in st.session_state:
    st.session_state.solved_doors = []

if "quiz_step" not in st.session_state:
    st.session_state.quiz_step = 1

if "current_view" not in st.session_state:
    st.session_state.current_view = "overview"

# --- DATENBANK: ALLE 21 TÜRCHEN (ANSPRUCHSVOLL & INTERAKTIV) ---
DOORS = {
    1: {
        "title": "Tag 1: Die mysteriöse Holzbox",
        "type": "text",
        "story": "Es klingelt an der Haustür. Ihr öffnet, aber niemand steht davor. Stattdessen liegt ein schweres, eisiges Päckchen vor der Tür vom Absender 'Nordpol'. Im Wohnzimmer geöffnet, kommt eine Holzbox mit einem Zahlenschloss zum Vorschein.",
        "question": "Löse das Rätsel des Gedichts:\n\n> *Vier kleine Ziffern im winterlichen Schnee.*\n> *Zähle die Buchstaben, die ich dir steh.*\n> *Wie viele Ecken hat ein Stern plus die Anzahl der Rentiere fern*\n> *minus die Ziffer, die an Weihnachten lacht, hat das Schloss für euch aufgemacht.*\n\nGib den vierstelligen Zahlencode ein:",
        "answer": "5924",
        "puzzle_piece": None,
        "hint": "Stern-Ecken (5) + Rentiere (9) - Weihnachtstag (24)... achte auf die Ziffernkombination."
    },
    2: {
        "title": "Tag 2: Das vergilbte Pergament",
        "type": "text",
        "story": "Das Schloss springt auf und im Inneren liegt ein altes Pergament mit der kryptischen Cäsar-Verschlüsselung 'S I V X'.",
        "question": "Entschlüssele das Codewort mithilfe der klassischen Alphabet-Verschiebung (-3):",
        "answer": "NORD",
        "puzzle_piece": None,
        "hint": "Jeder Buchstabe im Alphabet wird um 3 Positionen zurückverschoben (S -> P -> O -> N...)."
    },
    3: {
        "title": "Tag 3: Das Rentier-Expertenrätsel",
        "type": "reindeer_quiz",
        "story": "Glockenklingeln! Vor dem Fenster wartet der Rentierschlitten. Die Tiere prüfen euch mit knallhartem biologischen und historischen Expertenwissen.",
        "question": "Beantwortet die 5 Fachfragen über Rentiere nacheinander.",
        "answer": "QUIZ_SOLVED",
        "puzzle_piece": None,
        "hint": "Biologisches Fachwissen über Augenanatomie, Geweihbiologie und historische Dokumente ist gefragt."
    },
    4: {
        "title": "Tag 4: Das Navigationssystem",
        "type": "text",
        "story": "Ihr sitzt im Schlitten. Das Bordsystem verlangt die exakten Kurskoordinaten aus dem Handbuch, formatiert untereinander.",
        "question": "Berechne die Koordinaten:\n\n- Breitengrad: Exakt 90 Grad Nord minus die Anzahl der Rentiere.\n- Längengrad: Die magische Quersumme von 2026 multipliziert mit 10.\n\nGib beide Werte als 5-stelligen Gesamtwert ein (Breitengrad + Längengrad):",
        "answer": "81100",
        "puzzle_piece": "Koordinaten-Init",
        "hint": "90 - 9 = 81; Quersumme von 2026 (2+0+2+6 = 10) * 10 = 100 -> 81100"
    },
    5: {
        "title": "Tag 5: Das Nebel-Tor",
        "type": "text",
        "story": "Der Schlitten steuert auf eine undurchdringliche Nebelwand aus blauem Eis zu. Nur meteorologisches Fachwissen öffnet die Barriere.",
        "question": "Wie nennt man den kritischen physikalischen Punkt in der Meteorologie, bei dem die Luft bei konstantem Druck vollständig mit Wasserdampf gesättigt ist? (8 Buchstaben)",
        "answer": "TAUPUNKT",
        "puzzle_piece": "🧩 Fragment 1: **E**",
        "hint": "Die Temperatur, bei der die relative Luftfeuchtigkeit 100% erreicht."
    },
    6: {
        "title": "Tag 6: Das magische Sudoku",
        "type": "sudoku_puzzle",
        "story": "Hinter dem Nebel glimmt eine eingefrorene Eistafel mit einem 4x4-Sudoku auf.",
        "question": "Löse das Raster auf der Eistafel.",
        "answer": "SOLVED",
        "puzzle_piece": "🧩 Fragment 2: **R**",
        "hint": "Jede Zeile, Spalte und jedes 2x2-Feld muss die Zahlen 1 bis 4 enthalten."
    },
    7: {
        "title": "Tag 7: Der Jetstream-Kurs",
        "type": "text",
        "story": "Plötzliche Sturmböen erfordern die mathematische Berechnung des schnellsten Höhenkorridors.",
        "question": "Welcher Weg ist der absolut schnellste (Gesamtzeit in Minuten als Wort eingeben)?\n- Weg Alpha: 7 Min Grundzeit * 3 - 4 Minuten\n- Weg Beta: 21 km Strecke bei 14 km/h Schnitt + 2 Minuten Kletterzeit\n- Weg Gamma: Die Hälfte einer 30-km-Strecke bei 10 km/h Schnitt + 1 Min Check",
        "answer": "ALPHA",
        "puzzle_piece": "🧩 Fragment 3: **N**",
        "hint": "Alpha = 17 Min, Beta = 92 Min, Gamma = 91 Min."
    },
    8: {
        "title": "Tag 8: Das verzerrte Funksignal (Morse-Decoder)",
        "type": "morse_puzzle",
        "story": "Mitten im Sturm empfängt das Funkgerät eine stark verrauschte Notfall-Nachricht aus der Weihnachtswerkstatt im Morse-Code.",
        "question": "Entschlüssele den Morse-Code: `.-. . - - . .-.`",
        "answer": "RETTER",
        "puzzle_piece": "🧩 Fragment 4: **T**",
        "hint": "A=.-, E=., R=.-., T=-. Lies den Code Spalte für Spalte von links nach rechts."
    },
    9: {
        "title": "Tag 9: Die Aurora-Spektralanalyse",
        "type": "text",
        "story": "Das Energieschild des Schlittens sinkt im Polarlicht. Ihr müsst die Haupt-Wellenlänge im optischen Spektrum einstellen.",
        "question": "Welche additive Grundfarbe liegt im sichtbaren Lichtspektrum bei einer Wellenlänge von ca. 700 Nanometern vor?",
        "answer": "ROT",
        "puzzle_piece": "🧩 Fragment 5: **E**",
        "hint": "Es ist die langwelligste Farbe des sichtbaren Spektrums."
    },
    10: {
        "title": "Tag 10: Das Polar-Wetter-Labyrinth",
        "type": "text",
        "story": "Das Auge des Sturms verlangt die exakte Vektor-Berechnung des Fluchtkurses.",
        "question": "Wenn ein Vektor exakt 3 Einheiten nach Norden und 4 Einheiten nach Osten zeigt, wie lang ist der direkte Weg (Luftlinie nach Pythagoras)? Gib die ganze Zahl ein.",
        "answer": "5",
        "puzzle_piece": "🧩 Fragment 6: **N**",
        "hint": "Satz des Pythagoras: 3² + 4² = c²"
    },
    11: {
        "title": "Tag 11: Der Energie-Kern",
        "type": "text",
        "story": "Der magische Antrieb verlangt eine kombinatorische Formel zur Energiebündelung.",
        "question": "Berechne die mathematische Fakultät von 5 (Notiert als 5!):",
        "answer": "120",
        "puzzle_piece": "🧩 Fragment 7: **S**",
        "hint": "Multipliziere fortlaufend: 1 * 2 * 3 * 4 * 5."
    },
    12: {
        "title": "Tag 12: Das Tor zum Polarkreis",
        "type": "text",
        "story": "Der Nordpol ist erreicht. Eine magische Eistür verlangt das aus den 7 gesammelten Fragmenten gebildete Codewort.",
        "question": "Setze die Fragmente (E-R-N-T-E-N-S oder analog angeordnet als Lösungswort) zusammen:",
        "answer": "STERNEN",
        "puzzle_piece": "🏆 ZUGANG ZUR WERKSTATT FREIGESCHALTET",
        "hint": "Ordne die Buchstaben zu einem hellen Himmelsphänomen an."
    },
    13: {
        "title": "Tag 13: Das Notstrom-Aggregat",
        "type": "binary_slider",
        "story": "Ihr betretet die dunkle Haupthalle. Schalte die Binär-Bits korrekt, um das Aggregat auf den dezimalen Wert **13** zu takten.",
        "question": "Bringe die Schalter in die richtige Position.",
        "answer": "13",
        "puzzle_piece": None,
        "hint": "Binärsumme: 8 + 4 + 0 + 1."
    },
    14: {
        "title": "Tag 14: Das Terminal der Chef-Elfe",
        "type": "text",
        "story": "Das Hauptterminal verlangt ein kryptografisches Master-Passwort, basierend auf dem Kernfest.",
        "question": "Welches entscheidende Fest bildet das Herzstück des gesamten Nordpols? (9 Buchstaben)",
        "answer": "WEIHNACHT",
        "puzzle_piece": None,
        "hint": "Der Name des Feiertags."
    },
    15: {
        "title": "Tag 15: Die Wunschlisten-Matrix",
        "type": "text",
        "story": "In der Sortierhalle läuft ein Fließband Amok, weil die Wunschlisten nach einer mathematischen Rekursionsformel verrutscht sind.",
        "question": "Führe die berühmte Fibonacci-Reihe logisch fort: 1, 1, 2, 3, 5, 8, 13, ?",
        "answer": "21",
        "puzzle_piece": None,
        "hint": "Die Summe der beiden vorherigen Zahlen (8 + 13)."
    },
    16: {
        "title": "Tag 16: Der Fließband-Takt",
        "type": "text",
        "story": "Eine automatische Sicherheitssperre verlangt die Lösung einer linearen Gleichung höheren Grades.",
        "question": "Löse die Gleichung nach x auf: 3x - 7 = 20. Welchen Wert hat x?",
        "answer": "9",
        "puzzle_piece": None,
        "hint": "Addiere 7 zu 20 und teile das Ergebnis durch 3."
    },
    17: {
        "title": "Tag 17: Das Fluss-Logikrätsel (Eisbär, Robbe & Fisch)",
        "type": "river_puzzle",
        "story": "An der eisigen Schlucht blockiert eine alte mechanische Brücke den Weg. Du musst einen Eisbären, eine Robbe und einen gefrorenen Fisch im Boot sicher über den eisigen Fluss bringen – allerdings darf der Eisbär die Robbe und die Robbe den Fisch nicht unbeaufsichtigt zurücklassen!",
        "question": "Wer darf als Erster in der ersten Überfahrt im Boot transportiert werden?",
        "answer": "ROBBE",
        "puzzle_piece": None,
        "hint": "Der natürliche Feind in der Mitte muss zuerst rübergebracht werden."
    },
    18: {
        "title": "Tag 18: Der Elfen-Schichtplan (Logik-Gitter)",
        "type": "elf_puzzle",
        "story": "Vor der Manufaktur hängt ein komplexes Logikgitter für die Schichtzuweisung.",
        "question": "Elfe A arbeitet schneller als Elfe B. Elfe C arbeitet langsamer als Elfe B. Wer ist am schnellsten?",
        "answer": "A",
        "puzzle_piece": None,
        "hint": "Der absolute Spitzenreiter im Geschwindigkeitsvergleich."
    },
    19: {
        "title": "Tag 19: Der Tresor des Weihnachtsmanns",
        "type": "text",
        "story": "Im Büro des Weihnachtsmanns hängt ein schwerer Stahltresor für die Master-Schablone.",
        "question": "In welchem historischen Jahr erreichte die Amundsen-Expedition als erste den Südpol? (Vierstellige Jahreszahl)",
        "answer": "1911",
        "puzzle_piece": None,
        "hint": "Es war im Dezember des Jahres 191..."
    },
    20: {
        "title": "Tag 20: Der magische Polar-Kristall",
        "type": "text",
        "story": "Um den rohen Polar-Kristall im Tresor aufzuladen, muss die Winkelsumme geometrisch bestimmt werden.",
        "question": "Wie viel Grad beträgt die klassische euklidische Innwinkelsumme in einem Dreieck?",
        "answer": "180",
        "puzzle_piece": None,
        "hint": "Genau die Hälfte eines Vollkreises bzw. zwei rechte Winkel."
    },
    21: {
        "title": "Tag 21: Das Erwachen der Werkstatt",
        "type": "text",
        "story": "Der Kristall glüht in hellem Licht. Die Maschinen erwachen ratternd zum Leben!",
        "question": "Gib das finale Lösungswort ein, das den ultimativen Wendepunkt der Mission markiert:",
        "answer": "WENDEPUNKT",
        "puzzle_piece": "🌟 WERKSTATT VOLL EINSATZBEREIT",
        "hint": "Das zentrale Wort für den Wendepunkt."
    }
}

# --- HAUPTSEITE / TÜRCHEN-ÜBERSICHT ---
if st.session_state.current_view == "overview":
    st.title("🎄 Weihnachtlicher Rätsel-Adventskalender")
    st.markdown("### Mission: Weihnachten retten (Profi-Edition) 🎅✨")
    st.write("Wähle ein Türchen aus, um die anspruchsvollen Rätsel direkt zu testen.")
    
    solved_count = len(st.session_state.solved_doors)
    total_count = len(DOORS)
    st.markdown(f"**Gesamtfortschritt:** {solved_count} von {total_count} Türchen gelöst")
    st.progress(solved_count / total_count)
    st.markdown("---")

    door_keys = list(DOORS.keys())
    for i in range(0, len(door_keys), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(door_keys):
                d_num = door_keys[i + j]
                is_solved = d_num in st.session_state.solved_doors
                
                with cols[j]:
                    button_label = f"✅ Tag {d_num}" if is_solved else f"🔓 Tag {d_num}"
                    if st.button(button_label, use_container_width=True):
                        st.session_state.current_view = d_num
                        st.rerun()

# ==============================================================================
# 6. RÄTSEL-FLÄCHE & DYNAMISCHES LAYOUT (Sidebar nur für Tag 5 bis 12)
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

    # TAG 10: TRANSPORT-RÄTSEL (Mit Wolf, Ziege, Kohl auf Deutsch)
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
        rot = st.slider("⚙️ Umdrehungen des 12er-Rads:", 1, 12, 1, key="rot_slider")
        if st.button("Zahnräder einrasten ⚙️", key=f"chk_{day}"):
            if rot == door["answer"]:
                st.success("🎉 Synchronisiert! Die Fließbänder laufen wieder an.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Noch nicht synchron. Prüfe das kgV.")

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
                st.success("🎉 Stromkreis aktiv! Das Licht flackert und brennt hell.")
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
                st.success("🎉 Glasklarer Empfang mit dem Kontrollturm!")
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

    # STANDARD-TEXT ODER SPEZIAL-TEXT FÜR AKT 3 & 4
    else:
        if door["type"] not in ["sudoku_puzzle", "logic_grid", "morse_terminal", "river_crossing", "mirror_puzzle", "gear_puzzle", "binary_switches", "frequency_tuner", "scale_puzzle", "lock_sliders"]:
            ans = st.text_input("Deine Lösung:", key=f"input_{day}")
            if st.button("Prüfen 🔍", key=f"chk_{day}"):
                user_clean = ans.strip().replace(" ", "").upper()
                target_clean = str(door["answer"]).strip().replace(" ", "").upper()
                if user_clean == target_clean:
                    st.success("🎉 Richtig gelöst!")
                    if day not in st.session_state.solved_doors:
                        st.session_state.solved_doors.append(day)
                        if day == 24:
                            st.balloons()
                        st.rerun()
                else:
                    st.error("❌ Leider nicht korrekt.")

    with st.expander("💡 Hinweis anzeigen"):
        st.write(door["hint"])

# ==============================================================================
# SEITENLEISTE (FRAGMENT-SAMMLUNG NUR FÜR TAG 5 BIS 12)
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
