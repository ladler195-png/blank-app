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

# --- DETAIL-ANSICHT EINES TÜRICHENS ---
else:
    day = st.session_state.current_view
    door = DOORS[day]

    if st.button("⬅️ Zurück zur Türchen-Übersicht"):
        st.session_state.current_view = "overview"
        st.rerun()

    st.markdown("---")
    st.header(door["title"])
    st.info(door["story"])
    st.markdown("---")

    if day in st.session_state.solved_doors:
        st.success("✅ Dieses Türchen wurde bereits erfolgreich gelöst!")
        if door["puzzle_piece"]:
            st.markdown(f"**Gesammeltes Element:** {door['puzzle_piece']}")
        if st.button("🔄 Dieses Türchen zum Testen zurücksetzen"):
            st.session_state.solved_doors.remove(day)
            st.rerun()
    else:
        st.subheader("❓ Aufgabe:")
        st.write(door["question"])

        # 1. RENTIER-QUIZ (Tag 3)
        if door["type"] == "reindeer_quiz":
            st.write(f"**Experten-Frage {st.session_state.quiz_step} von 5**")
            step = st.session_state.quiz_step
            if step == 1:
                q1 = st.text_input("F1: Welche Farbe nimmt das Tapetum lucidum im Rentierauge im Winter an?", key="rq1")
                if st.button("Antwort 1 senden"):
                    if "BLAU" in q1.upper():
                        st.session_state.quiz_step = 2
                        st.rerun()
                    else:
                        st.error("❌ Falsch. Denk an das Spektrum der Polarlichter.")
            elif step == 2:
                q2 = st.selectbox("F2: Welches Geschlecht behält im Winter sein Geweih?", ["Bitte wählen...", "Männchen", "Weibchen / Kühe", "Beide"], key="rq2")
                if st.button("Antwort 2 senden"):
                    if "Weibchen" in q2:
                        st.session_state.quiz_step = 3
                        st.rerun()
                    else:
                        st.error("❌ Falsch.")
            elif step == 3:
                q3 = st.text_input("F3: Wie lautet der wissenschaftliche Artname auf Latein?", key="rq3")
                if st.button("Antwort 3 senden"):
                    if "TARANDUS" in q3.upper():
                        st.session_state.quiz_step = 4
                        st.rerun()
                    else:
                        st.error("❌ Falsch.")
            elif step == 4:
                q4 = st.number_input("F4: In welchem Jahr erschien das klassische Rentier-Gedicht erstmals?", min_value=1800, max_value=1900, value=1800, key="rq4")
                if st.button("Antwort 4 senden"):
                    if q4 == 1823:
                        st.session_state.quiz_step = 5
                        st.rerun()
                    else:
                        st.error("❌ Falsch.")
            elif step == 5:
                q5 = st.slider("F5: Wie viele Rentiere zogen den Schlitten im Original ohne Rudolph?", 1, 12, 4, key="rq5")
                if st.button("Finale Antwort senden"):
                    if q5 == 8:
                        st.success("🎉 Rentiere überzeugt! Das Rätsel ist geschafft.")
                        st.session_state.solved_doors.append(day)
                        st.session_state.quiz_step = 1
                        st.rerun()
                    else:
                        st.error("❌ Falsch.")

        # 2. SUDOKU (Tag 6)
        elif door["type"] == "sudoku_puzzle":
            st.markdown("""
            | Raster | Spalte 1 | Spalte 2 | Spalte 3 | Spalte 4 |
            | :---: | :---: | :---: | :---: | :---: |
            | **Z1** | **1**    | *[ ? ]*  | 3        | 4        |
            | **Z2** | 3        | 4        | *[ ? ]*  | 2        |
            | **Z3** | *[ ? ]*  | 2        | 1        | 3        |
            | **Z4** | 4        | 1        | 2        | *[ ? ]*  |
            """)
            c1, c2, c3, c4 = st.columns(4)
            v1 = c1.text_input("Feld 1 (Z1S2)", max_chars=1)
            v2 = c2.text_input("Feld 2 (Z2S3)", max_chars=1)
            v3 = c3.text_input("Feld 3 (Z3S1)", max_chars=1)
            v4 = c4.text_input("Feld 4 (Z4S4)", max_chars=1)

            if st.button("Sudoku überprüfen"):
                if v1.strip() == "2" and v2.strip() == "1" and v3.strip() == "4" and v4.strip() == "3":
                    st.success("✨ Sudoku korrekt gelöst!")
                    if door["puzzle_piece"]:
                        st.info(f"**Erhaltenes Element:** {door['puzzle_piece']}")
                    st.session_state.solved_doors.append(day)
                    st.rerun()
                else:
                    st.error("❌ Fehler im Raster.")

        # 3. MORSE-DECODER (Tag 8)
        elif door["type"] == "morse_puzzle":
            st.markdown("""
            > **Morse-Alphabet:** A = `.-` | E = `.` | R = `.-.` | T = `-`
            """)
            morse_input = st.text_input("Tippe das entschlüsselte Wort:", key=f"morse_{day}")
            if st.button("Morsecode abschicken 📡"):
                if morse_input.strip().upper() == "RETTER":
                    st.success("🎉 Signal erfolgreich decodiert!")
                    if door["puzzle_piece"]:
                        st.info(f"**Erhaltenes Element:** {door['puzzle_piece']}")
                    st.session_state.solved_doors.append(day)
                    st.rerun()
                else:
                    st.error("❌ Das Signal stimmt nicht.")

        # 4. BINÄR-SCHALTER (Tag 13)
        elif door["type"] == "binary_slider":
            st.markdown("Stelle die Bits ein:")
            b3 = st.checkbox("Bit 8er-Stelle")
            b2 = st.checkbox("Bit 4er-Stelle")
            b1 = st.checkbox("Bit 2er-Stelle")
            b0 = st.checkbox("Bit 1er-Stelle")
            
            calculated_val = (8 if b3 else 0) + (4 if b2 else 0) + (2 if b1 else 0) + (1 if b0 else 0)
            st.write(f"Aktueller Wert: **{calculated_val}** (Gesucht: 13)")

            if st.button("Aggregat starten ⚡"):
                if calculated_val == 13:
                    st.success("🎉 Perfekt! Aggregat läuft.")
                    st.session_state.solved_doors.append(day)
                    st.rerun()
                else:
                    st.error(f"❌ Der Wert ist {calculated_val}, benötigt werden 13.")

        # 5. FLUSS-LOGIKRÄTSEL (Tag 17)
        elif door["type"] == "river_puzzle":
            r_choice = st.selectbox("Wen nimmst du zuerst mit?", ["Bitte wählen...", "Eisbär", "Robbe", "Fisch"])
            if st.button("Überfahrt starten"):
                if r_choice == "Robbe":
                    st.success("🎉 Richtig! Die Robbe wird zuerst rübergebracht, da Eisbär und Fisch sich zwar nicht fressen, aber der Eisbär die Robbe gefährdet (bzw. klassisches Prinzip).")
                    st.session_state.solved_doors.append(day)
                    st.rerun()
                else:
                    st.error("❌ Falsch. Überlege, wer wen fressen würde, wenn man ihn allein lässt.")

        # 6. ELFEN-LOGIK (Tag 18)
        elif door["type"] == "elf_puzzle":
            elf_choice = st.radio("Wähle die schnellste Elfe:", ["Elfe A", "Elfe B", "Elfe C"])
            if st.button("Schichtplan bestätigen"):
                if elf_choice == "Elfe A":
                    st.success("🎉 Logikgitter gelöst!")
                    st.session_state.solved_doors.append(day)
                    st.rerun()
                else:
                    st.error("❌ Falsch.")

        # STANDARD-TEXT-EINGABE
        else:
            user_input = st.text_input("Deine Lösung:", key=f"input_{day}")
            if st.button("Antwort einreichen 🚀", key=f"btn_{day}"):
                if user_input.strip().upper() == door["answer"].upper():
                    st.success("🎉 Richtig!")
                    if door["puzzle_piece"]:
                        st.info(f"**Erhaltenes Element:** {door['puzzle_piece']}")
                    st.session_state.solved_doors.append(day)
                    st.rerun()
                else:
                    st.error("❌ Leider falsch.")

        with st.expander("💡 Einen Hinweis anzeigen"):
            st.write(door["hint"])
