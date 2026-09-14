import streamlit as st

# --- SEITEN-KONFIGURATION ---
st.set_page_config(
    page_title="Weihnachtlicher Rätsel-Adventskalender",
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

# --- DATENBANK: ALLE TÜRICHEN VON 1 BIS 21 ---
DOORS = {
    1: {
        "title": "Tag 1: Die mysteriöse Holzbox",
        "type": "text",
        "story": "Es klingelt an der Haustür. Ihr öffnet, aber niemand steht davor. Stattdessen liegt ein Päckchen vor der Tür – Absender: Nordpol. Im Wohnzimmer geöffnet, kommt eine schwere, eisige Holzbox zum Vorschein mit einem Zahlenschloss und einem Gedicht.",
        "question": "Löse das Rätsel des Gedichts:\n\n> *Vier kleine Ziffern im winterlichen Schnee.*\n> *Zähle die Buchstaben, die ich dir steh.*\n> *Wie viele Ecken hat ein Stern plus die Anzahl der Rentiere fern*\n> *minus die Ziffer, die an Weihnachten lacht, hat das Schloss für euch aufgemacht.*\n\nGib den vierstelligen Zahlencode ein:",
        "answer": "5924",
        "puzzle_piece": None,
        "hint": "Rechne: Stern-Ecken (5) + Rentiere (9) minus Weihnachtstag (24)... beachte die Ziffernkombination."
    },
    2: {
        "title": "Tag 2: Das vergilbte Pergament",
        "type": "text",
        "story": "Das Schloss springt auf und im Inneren liegt ein altes Pergament. Darauf steht die kryptische Nachricht 'S I V X'. Unten ist ein Lorbeerkranz eingraviert.",
        "question": "Entschlüssele das Codewort mithilfe des antiken Hinweises (Cäsar-Verschiebung):\n\nDeine Lösung:",
        "answer": "NORD",
        "puzzle_piece": None,
        "hint": "Der Lorbeerkranz verweist auf Julius Cäsar und eine klassische Verschiebung im Alphabet."
    },
    3: {
        "title": "Tag 3: Das Rentier-Expertenrätsel",
        "type": "reindeer_quiz",
        "story": "Nachdem das Codewort ausgesprochen ist, hört man Glockenklingeln. Vor dem Fenster steht ein Schlitten mit 8 Rentieren. Sie nehmen euch nur mit, wenn ihr ihr strenges Expertenwissen beweist.",
        "question": "Beantwortet die anspruchsvollen Fragen über Rentiere nacheinander.",
        "answer": "QUIZ_SOLVED",
        "puzzle_piece": None,
        "hint": "Biologisches Fachwissen über Augen, Geweih, Artnamen und Historie ist gefragt."
    },
    4: {
        "title": "Tag 4: Das Navigationssystem",
        "type": "text",
        "story": "Ihr sitzt im Schlitten und wollt starten, doch das Navigationssystem verlangt exakte Kurskoordinaten aus dem Handbuch.",
        "question": "Berechne die Kurskoordinaten:\nDer Breitengrad startet bei exakt 90 Grad Nord, minus der Anzahl der Rentiere. Für den Längengrad nehmen wir die magische Quersumme von 2026 mal 10. Gib den kombinierten 5-stelligen Wert ein.",
        "answer": "81100",
        "puzzle_piece": "Koordinaten-Init",
        "hint": "90 - 9 = Breitengrad; (2+0+2+6) * 10 = Längengrad."
    },
    5: {
        "title": "Tag 5: Das Nebel-Tor",
        "type": "text",
        "story": "Der Schlitten durchbricht die Wolkendecke, steuert aber direkt auf eine massive, undurchdringliche Nebelwand aus blauem Eis zu.",
        "question": "Wie nennt man den kritischen physikalischen Punkt in der Meteorologie, bei dem die Luft vollständig mit Wasserdampf gesättigt ist und Nebel entsteht?",
        "answer": "TAUPUNKT",
        "puzzle_piece": "🧩 Fragment 1: **E**",
        "hint": "Die Temperatur, bei der die relative Luftfeuchtigkeit 100% erreicht."
    },
    6: {
        "title": "Tag 6: Das magische Sudoku",
        "type": "sudoku_puzzle",
        "story": "Hinter dem Nebel glimmt die Steintafel des Bordsystems auf – eine eingefrorene Eistafel mit einem magischen Zahlenraster.",
        "question": "Löse das 4x4-Sudoku auf der Eistafel.",
        "answer": "SOLVED",
        "puzzle_piece": "🧩 Fragment 2: **R**",
        "hint": "Jede Zeile, Spalte und jedes 2x2-Feld enthält die Zahlen 1 bis 4."
    },
    7: {
        "title": "Tag 7: Der Jetstream-Kurs",
        "type": "text",
        "story": "Plötzliche Sturmböen drängen den Schlitten ab. Ihr müsst den optimalen, schnellsten Höhenkorridor (Jetstream) berechnen.",
        "question": "Welcher Weg ist der schnellste (Gesamtzeit in Minuten als Wort eingeben)?\n- Weg Alpha: 7 Min Grundzeit * 3 - 4 Minuten\n- Weg Beta: 21 km bei 14 km/h + 2 Minuten Kletterzeit\n- Weg Gamma: Die Hälfte einer 30-km-Strecke bei 10 km/h + 1 Min Check",
        "answer": "ALPHA",
        "puzzle_piece": "🧩 Fragment 3: **N**",
        "hint": "Alpha = 17 Min, Beta = 92 Min, Gamma = 91 Min."
    },
    8: {
        "title": "Tag 8: Das verzerrte Funksignal (Morse-Decoder)",
        "type": "morse_puzzle",
        "story": "Mitten im Sturm empfängt das Funkgerät eine stark verrauschte Notfall-Nachricht aus der Weihnachtswerkstatt. Nutze die Morse-Tabelle, um das Signal zu entschlüsseln!",
        "question": "Entschlüssele den Morse-Code: `.-. . - - . .-.`",
        "answer": "RETTER",
        "puzzle_piece": "🧩 Fragment 4: **T**",
        "hint": "A=.-, E=., R=.-., T=-. Lies den Code Spalte für Spalte."
    },
    9: {
        "title": "Tag 9: Die Aurora-Spektralanalyse",
        "type": "text",
        "story": "Das Energieschild des Schlittens sinkt durch die Polarlichter. Ihr müsst die Haupt-Wellenlänge im RGB-Spektrum exakt einstellen.",
        "question": "Welche additive Grundfarbe liegt bei einer reinen Wellenlänge von ca. 700 Nanometern im Lichtspektrum vor?",
        "answer": "ROT",
        "puzzle_piece": "🧩 Fragment 5: **E**",
        "hint": "Es ist die Farbe am langwelligen Ende des sichtbaren Spektrums."
    },
    10: {
        "title": "Tag 10: Das Polar-Wetter-Labyrinth",
        "type": "text",
        "story": "Ihr müsst das Auge des Sturms durchqueren. Ein magisches Vektor-Labyrinth auf dem Display versperrt den Kurs.",
        "question": "Wenn ein Vektor 3 Einheiten nach Norden und 4 nach Osten zeigt, wie lang ist der direkte Weg (Luftlinie nach Pythagoras)? Gib die ganze Zahl ein.",
        "answer": "5",
        "puzzle_piece": "🧩 Fragment 6: **N**",
        "hint": "Satz des Pythagoras: 3² + 4² = c²"
    },
    11: {
        "title": "Tag 11: Der Energie-Kern",
        "type": "text",
        "story": "Kurz vor dem Ziel glimmt der magische Antrieb des Schlittens rot. Er verlangt eine mathematische Formel zur Energiebündelung.",
        "question": "Berechne die Fakultät von 5 (5! = 1 * 2 * 3 * 4 * 5):",
        "answer": "120",
        "puzzle_piece": "🧩 Fragment 7: **S**",
        "hint": "Multipliziere die Zahlen von 1 bis 5 fortlaufend durch."
    },
    12: {
        "title": "Tag 12: Das Tor zum Polarkreis",
        "type": "text",
        "story": "Der Nordpol kommt in Sicht! Eine finale magische Eistür verlangt das aus den Fragmenten gebildete Lösungswort.",
        "question": "Setze die gesammelten Fragmente zu dem 7-stelligen Ziel-Codewort zusammen:",
        "answer": "STERNEN",
        "puzzle_piece": "🏆 ZUGANG ZUR WERKSTATT FREIGESCHALTET",
        "hint": "Anordnung der gesammelten Hinweise am Himmel."
    },
    13: {
        "title": "Tag 13: Das Notstrom-Aggregat",
        "type": "binary_slider",
        "story": "Ihr betretet die Haupthalle der Werkstatt. Schalte die Binär-Schalter passend ein, um das Aggregat auf den Wert **13** zu bringen.",
        "question": "Bringe die Schalter in die richtige Position für die Dezimalzahl 13.",
        "answer": "13",
        "puzzle_piece": None,
        "hint": "Binär: 8 + 4 + 0 + 1 (Schalter 8, 4 und 1 auf ON)."
    },
    14: {
        "title": "Tag 14: Das Terminal der Chef-Elfe",
        "type": "text",
        "story": "Das Licht flackert an, aber der Hauptcomputer verlangt das Benutzerpasswort der Chef-Elfe.",
        "question": "Welches entscheidende Fest bildet das Herzstück des gesamten Nordpols? (9 Buchstaben)",
        "answer": "WEIHNACHT",
        "puzzle_piece": None,
        "hint": "Der Name des Feiertags."
    },
    15: {
        "title": "Tag 15: Die Wunschlisten-Matrix",
        "type": "text",
        "story": "In der Sortierhalle läuft ein Fließband Amok, weil die Wunschlisten nach einer mathematischen Reihe verrutscht sind.",
        "question": "Führe die Fibonacci-Reihe logisch fort: 1, 1, 2, 3, 5, 8, 13, ?",
        "answer": "21",
        "puzzle_piece": None,
        "hint": "Addiere immer die beiden vorherigen Zahlen (8 + 13)."
    },
    16: {
        "title": "Tag 16: Der Fließband-Takt",
        "type": "text",
        "story": "Das Band stoppt vor einer Barriere. Die Steuerung verlangt das Lösen einer linearen Gleichung.",
        "question": "Löse die Gleichung: 2x + 4 = 12. Welchen Wert hat x?",
        "answer": "4",
        "puzzle_piece": None,
        "hint": "Subtrahiere 4 von 12 und teile durch 2."
    },
    17: {
        "title": "Tag 17: Die Geschenk-Waage",
        "type": "text",
        "story": "In der Verpackungsstation blockiert eine Sicherheitswaage den Weg. Es müssen Gewichte verglichen werden.",
        "question": "Du hast 9 Päckchen, von denen eines schwerer ist. Wie viele Wägungen auf einer Balkenwaage brauchst du im Worst-Case mindestens?",
        "answer": "2",
        "puzzle_piece": None,
        "hint": "Teile in Dreiergruppen auf (3-3-3)."
    },
    18: {
        "title": "Tag 18: Der Elfen-Schichtplan (Logik-Rätsel)",
        "type": "elf_puzzle",
        "story": "Vor der Spielzeug-Manufaktur hängt ein interaktives Logikgitter für den Schichtplan.",
        "question": "Ordne die Elfen nach Geschwindigkeit zu: Wer arbeitet am schnellsten?",
        "answer": "A",
        "puzzle_piece": None,
        "hint": "Elfe A arbeitet schneller als B, C arbeitet langsamer als B."
    },
    19: {
        "title": "Tag 19: Der Tresor des Weihnachtsmanns",
        "type": "text",
        "story": "Ihr erreicht das Büro des Weihnachtsmanns. An der Wand hängt ein schwerer Stahltresor.",
        "question": "In welchem Jahr erreichte die historische Amundsen-Expedition als erste den Südpol? (Vierstellige Jahreszahl)",
        "answer": "1911",
        "puzzle_piece": None,
        "hint": "Es war im Dezember des Jahres 191... (1)."
    },
    20: {
        "title": "Tag 20: Der magische Polar-Kristall",
        "type": "text",
        "story": "Im Tresor findet ihr den rohen Polar-Kristall. Um ihn aufzuladen, muss ein Laserstrahl gelenkt werden.",
        "question": "Wie viel Grad beträgt die Winkelsumme in einem klassischen Dreieck?",
        "answer": "180",
        "puzzle_piece": None,
        "hint": "Zweimal ein rechter Winkel."
    },
    21: {
        "title": "Tag 21: Das Erwachen der Werkstatt",
        "type": "text",
        "story": "Der Kristall glüht in hellem Licht und wird in den Hauptkern eingesetzt. Die Maschinen erwachen zum Leben!",
        "question": "Gib das finale Lösungswort ein, das den Wendepunkt der Mission markiert:",
        "answer": "WENDEPUNKT",
        "puzzle_piece": "🌟 WERKSTATT VOLL EINSATZBEREIT",
        "hint": "Das entscheidende Wort für den Wendepunkt."
    }
}

# --- HAUPTSEITE / TÜRCHEN-ÜBERSICHT ---
if st.session_state.current_view == "overview":
    st.title("🎄 Weihnachtlicher Rätsel-Adventskalender")
    st.markdown("### Mission: Weihnachten retten 🎅✨")
    st.write("Wähle ein Türchen aus, um die interaktiven Aufgaben zu testen.")
    
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
                q1 = st.text_input("F1: Welche Farbe nimmt das Tapetum lucidum im Rentierauge im Winter an (Gold zu...)?", key="rq1")
                if st.button("Antwort 1 senden"):
                    if "BLAU" in q1.upper():
                        st.session_state.quiz_step = 2
                        st.rerun()
                    else:
                        st.error("❌ Falsch. Denk an Polarlichter.")
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
                        st.error("❌ Falsch. Versuche es mit dem Slider.")

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

        # 3. MORSE-DECODER WIDGET (Tag 8)
        elif door["type"] == "morse_puzzle":
            st.markdown("""
            > **Morse-Alphabet Referenz:**
            > A = `.-` | E = `.` | R = `.-.` | T = `-`
            """)
            morse_input = st.text_input("Tippe das entschlüsselte Wort (Großbuchstaben):", key=f"morse_{day}")
            if st.button("Morsecode abschicken 📡"):
                if morse_input.strip().upper() == "RETTER":
                    st.success("🎉 Signal erfolgreich decodiert!")
                    if door["puzzle_piece"]:
                        st.info(f"**Erhaltenes Element:** {door['puzzle_piece']}")
                    st.session_state.solved_doors.append(day)
                    st.rerun()
                else:
                    st.error("❌ Das Signal stimmt noch nicht ganz.")

        # 4. BINÄR-SCHALTER WIDGET (Tag 13)
        elif door["type"] == "binary_slider":
            st.markdown("Stelle die Bits ein (Wert = $8 \\cdot b_3 + 4 \\cdot b_2 + 2 \\cdot b_1 + 1 \\cdot b_0$):")
            b3 = st.checkbox("Bit 8er-Stelle (Wert 8)")
            b2 = st.checkbox("Bit 4er-Stelle (Wert 4)")
            b1 = st.checkbox("Bit 2er-Stelle (Wert 2)")
            b0 = st.checkbox("Bit 1er-Stelle (Wert 1)")
            
            calculated_val = (8 if b3 else 0) + (4 if b2 else 0) + (2 if b1 else 0) + (1 if b0 else 0)
            st.write (Aktueller Wert: **{calculated_val}** (Gesucht: 13))

            if st.button("Aggregat starten ⚡"):
                if calculated_val == 13:
                    st.success("🎉 Perfekt! Aggregat läuft.")
                    st.session_state.solved_doors.append(day)
                    st.rerun()
                else:
                    st.error(f"❌ Der Wert ist derzeit {calculated_val}, benötigt werden 13.")

        # 5. ELFEN-LOGIK WIDGET (Tag 18)
        elif door["type"] == "elf_puzzle":
            elf_choice = st.radio("Wähle die schnellste Elfe:", ["Elfe A", "Elfe B", "Elfe C"])
            if st.button("Schichtplan bestätigen"):
                if elf_choice == "Elfe A":
                    st.success("🎉 Logikgitter gelöst!")
                    st.session_state.solved_doors.append(day)
                    st.rerun()
                else:
                    st.error("❌ Falsch. Überprüfe die Bedingungen.")

        # STANDARD-TEXT-EINGABE FÜR REST
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
