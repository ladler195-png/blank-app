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

# --- DATENBANK: ALLE TÜRICHEN VON 1 BIS 21 ---
DOORS = {
    # --- AKT 1: ZUHAUSE & AUFTAKT (1-4) ---
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
        "question": "Entschlüssele das Codewort mithilfe des antiken Hinweises:\n\nDeine Lösung:",
        "answer": "NORD",
        "puzzle_piece": None,
        "hint": "Der Lorbeerkranz verweist auf Julius Cäsar und eine klassische Verschiebung im Alphabet."
    },
    3: {
        "title": "Tag 3: Das Rentier-Expertenrätsel",
        "type": "reindeer_quiz",
        "story": "Nachdem das Codewort ausgesprochen ist, hört man Glockenklingeln. Vor dem Fenster steht ein Schlitten mit 8 Rentieren. Sie nehmen euch nur mit, wenn ihr ihr strenges Expertenwissen beweist.",
        "question": "Beantwortet die 5 anspruchsvollen Fragen über Rentiere nacheinander.",
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

    # --- AKT 2: DER FLUG DURCH DIE POLARNACHT (5-12) ---
    5: {
        "title": "Tag 5: Das Nebel-Tor",
        "type": "text",
        "story": "Der Schlitten durchbricht die Wolkendecke, steuert aber direkt auf eine massive, undurchdringliche Nebelwand aus blauem Eis zu. Das Barrieren-Schloss verlangt meteorologisches Fachwissen.",
        "question": "Wie nennt man den kritischen physikalischen Punkt in der Meteorologie, bei dem die Luft vollständig mit Wasserdampf gesättigt ist und Nebel entsteht? (Ein Wort, 8 Buchstaben)",
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
        "story": "Plötzliche Sturmböen drängen den Schlitten ab. Ihr müsst den optimalen, schnellsten Höhenkorridor (Jetstream) anhand von Expeditions-Protokollen berechnen.",
        "question": "Welcher Weg ist der schnellste (Gesamtzeit in Minuten als Wort eingeben)?\n- Weg Alpha: 7 Min Grundzeit * 3 - 4 Minuten\n- Weg Beta: 21 km bei 14 km/h + 2 Minuten Kletterzeit\n- Weg Gamma: Die Hälfte einer 30-km-Strecke bei 10 km/h + 1 Min Check",
        "answer": "ALPHA",
        "puzzle_piece": "🧩 Fragment 3: **N**",
        "hint": "Alpha = 17 Min, Beta = 92 Min, Gamma = 91 Min."
    },
    8: {
        "title": "Tag 8: Das verzerrte Funksignal",
        "type": "text",
        "story": "Mitten im Sturm empfängt das Funkgerät eine stark verrauschte Notfall-Nachricht aus der Weihnachtswerkstatt am Nordpol.",
        "question": "Entschlüssele den verrauschten Code (Rückwärts gelesen): 'RETTER'",
        "answer": "RETTER",
        "puzzle_piece": "🧩 Fragment 4: **T**",
        "hint": "Lies das Wort von rechts nach links."
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
        "story": "Der Nordpol kommt in Sicht! Eine finale magische Eistür versperrt den Landeplatz und verlangt das aus den Fragmenten gebildete Lösungswort.",
        "question": "Setze die gesammelten Fragmente zu dem 7-stelligen Ziel-Codewort zusammen:",
        "answer": "STERNEN",
        "puzzle_piece": "🏆 ZUGANG ZUR WERKSTATT FREIGESCHALTET",
        "hint": "Anordnung der gesammelten Hinweise am Himmel."
    },

    # --- AKT 3: DIE WIRTSCHAFT & WERKSTATT AM NORDPOL (13-21) ---
    13: {
        "title": "Tag 13: Das Notstrom-Aggregat",
        "type": "text",
        "story": "Ihr betretet die dunkle Haupthalle der Werkstatt. Um Licht zu machen, müsst ihr das alte Notstromaggregat über eine binäre Schaltung hochfahren.",
        "question": "Wandle die Binärzahl '1101' in das dezimale Zahlensystem um:",
        "answer": "13",
        "puzzle_piece": None,
        "hint": "8 + 4 + 0 + 1"
    },
    14: {
        "title": "Tag 14: Das Terminal der Chef-Elfe",
        "type": "text",
        "story": "Das Licht flackert an, aber der Hauptcomputer verlangt das Benutzerpasswort der Chef-Elfe, verschlüsselt als Kernbegriff.",
        "question": "Welches entscheidende Fest bildet das Herzstück des gesamten Nordpols? (Gesucht: 9 Buchstaben)",
        "answer": "WEIHNACHT",
        "puzzle_piece": None,
        "hint": "Der Name des Feiertags."
    },
    15: {
        "title": "Tag 15: Die Wunschlisten-Matrix",
        "type": "text",
        "story": "In der Sortierhalle läuft ein Fließband Amok, weil die Wunschlisten nach dem Prinzip einer mathematischen Reihe verrutscht sind.",
        "question": "Führe die Fibonacci-Reihe logisch fort: 1, 1, 2, 3, 5, 8, 13, ? (Gib die nächste Zahl ein)",
        "answer": "21",
        "puzzle_piece": None,
        "hint": "Addiere immer die beiden vorherigen Zahlen zusammen (8 + 13)."
    },
    16: {
        "title": "Tag 16: Der Fließband-Takt",
        "type": "text",
        "story": "Das Band stoppt vor einer Barriere. Die Steuerung verlangt das Lösen einer linearen Gleichung.",
        "question": "Löse das System: 2x + 4 = 12. Welchen Wert hat x?",
        "answer": "4",
        "puzzle_piece": None,
        "hint": "Subtrahiere 4 von 12 und teile durch 2."
    },
    17: {
        "title": "Tag 17: Die Geschenk-Waage",
        "type": "text",
        "story": "In der Verpackungsstation blockiert eine Sicherheitswaage den Weg. Es müssen Gewichte exakt verglichen werden.",
        "question": "Du hast 9 Päckchen, von denen eines schwerer ist. Wie viele Wägungen auf einer Balkenwaage brauchst du im Worst-Case mindestens?",
        "answer": "2",
        "puzzle_piece": None,
        "hint": "Teile in Dreiergruppen auf (3-3-3)."
    },
    18: {
        "title": "Tag 18: Der Elfen-Schichtplan",
        "type": "text",
        "story": "Vor der Spielzeug-Manufaktur hängt ein Logikgitter. Wer arbeitet in welcher Abteilung?",
        "question": "Elfe A arbeitet schneller als Elfe B. Elfe C arbeitet langsamer als Elfe B. Wer ist am schnellsten? (Gib den Buchstaben ein: A, B oder C):",
        "answer": "A",
        "puzzle_piece": None,
        "hint": "Der erste im Vergleich."
    },
    19: {
        "title": "Tag 19: Der Tresor des Weihnachtsmanns",
        "type": "text",
        "story": "Ihr erreicht das Büro des Weihnachtsmanns. An der Wand hängt ein schwerer Stahltresor für die Master-Schablone.",
        "question": "In welchem Jahr erreichte die historische Amundsen-Expedition als erste den Südpol? (Vierstellige Jahreszahl)",
        "answer": "1911",
        "puzzle_piece": None,
        "hint": "Es war im Dezember des Jahres 191... (1)."
    },
    20: {
        "title": "Tag 20: Der magische Polar-Kristall",
        "type": "text",
        "story": "Im Tresor findet ihr den rohen Polar-Kristall. Um ihn aufzuladen, muss ein Laserstrahl durch ein geometrisches System gelenkt werden.",
        "question": "Wie viel Grad beträgt die Winkelsumme in einem klassischen Dreieck?",
        "answer": "180",
        "puzzle_piece": None,
        "hint": "Zweimal ein rechter Winkel."
    },
    21: {
        "title": "Tag 21: Das Erwachen der Werkstatt",
        "type": "text",
        "story": "Der Kristall glüht in hellem Licht und wird in den Hauptkern eingesetzt. Die Maschinen erwachen ratternd zum Leben!",
        "question": "Gib das finale Lösungswort ein, das den Wendepunkt der Mission markiert:",
        "answer": "WENDEPUNKT",
        "puzzle_piece": "🌟 WERKSTATT VOLL EINSATZBEREIT",
        "hint": "Das entscheidende Wort für den Wendepunkt."
    }
}

# --- HAUPTUI & DESIGN ---
st.title("🎄 Weihnachtlicher Rätsel-Adventskalender")
st.markdown("### Mission: Weihnachten retten 🎅✨")
st.markdown("---")

# Sidebar für die Navigation & visuelle Darstellung der gelösten Türchen
st.sidebar.markdown("### 🚪 Türchen-Übersicht")
day = st.sidebar.selectbox("Wähle ein Türchen:", list(DOORS.keys()))

# Visuelle Statusanzeige in der Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Fortschritt:** {len(st.session_state.solved_doors)} von {len(DOORS)} gelöst")
st.sidebar.progress(len(st.session_state.solved_doors) / len(DOORS))

door = DOORS[day]

# Hauptbereich
st.header(door["title"])
st.info(door["story"])
st.markdown("---")

# Überprüfen, ob das Türchen bereits gelöst wurde
if day in st.session_state.solved_doors:
    st.success("✅ Dieses Türchen wurde bereits erfolgreich gelöst!")
    if door["puzzle_piece"]:
        st.markdown(f"**Gesammeltes Element:** {door['puzzle_piece']}")
else:
    st.subheader("❓ Aufgabe:")
    st.write(door["question"])

    # 1. SPEZIAL-QUIZ FÜR TAG 3 (RENTIER-EXPERTE)
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
                    st.error("❌ Falsch. Denk an das Spektrum der Polarlichter.")
        elif step == 2:
            q2 = st.text_input("F2: Welches Geschlecht behält im Winter sein Geweih?", key="rq2")
            if st.button("Antwort 2 senden"):
                if any(w in q2.upper() for w in ["KUH", "WEIBLICH", "MÜTTER", "WEIBCHEN"]):
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
            q4 = st.text_input("F4: In welchem Jahr erschien das klassische Rentier-Gedicht erstmals?", key="rq4")
            if st.button("Antwort 4 senden"):
                if "1823" in q4:
                    st.session_state.quiz_step = 5
                    st.rerun()
                else:
                    st.error("❌ Falsch.")
        elif step == 5:
            q5 = st.text_input("F5: Wie viele Rentiere zogen den Schlitten im Original ohne Rudolph?", key="rq5")
            if st.button("Finale Antwort senden"):
                if "8" in q5 or "ACHT" in q5.upper():
                    st.success("🎉 Rentiere überzeugt! Das Rätsel ist geschafft.")
                    st.session_state.solved_doors.append(day)
                    st.session_state.quiz_step = 1
                    st.rerun()
                else:
                    st.error("❌ Falsch.")

    # 2. SPEZIAL-SUDOKU FÜR TAG 6
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
                st.success("✨ Sudoku korrekt gelöst! Fragment erhalten.")
                if door["puzzle_piece"]:
                    st.info(f"**Erhaltenes Element:** {door['puzzle_piece']}")
                st.session_state.solved_doors.append(day)
                st.rerun()
            else:
                st.error("❌ Fehler im Raster. Prüfe Zeilen und Spalten!")

    # 3. STANDARD-TEXT-EINGABE FÜR ALLE ANDEREN TAGE
    else:
        user_input = st.text_input("Deine Lösung:", key=f"input_{day}")
        if st.button("Antwort einreichen 🚀", key=f"btn_{day}"):
            if user_input.strip().upper() == door["answer"].upper():
                st.success("🎉 Richtig! Das Rätsel ist gelöst.")
                if door["puzzle_piece"]:
                    st.info(f"**Erhaltenes Element:** {door['puzzle_piece']}")
                st.session_state.solved_doors.append(day)
                st.rerun()
            else:
                st.error("❌ Das ist leider nicht korrekt. Probiere es noch einmal!")

    # Hinweis-Expander
    with st.expander("💡 Einen Hinweis anzeigen"):
        st.write(door["hint"])
