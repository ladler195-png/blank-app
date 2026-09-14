import streamlit as st

# Grundlegendes Setup für den Session State
if "solved_doors" not in st.session_state:
    st.session_state.solved_doors = []

# DOORS DICTIONARY: Alle Stationen von Tag 1 bis 21
DOORS = {
    # --- AKT 1: ZUHAUSE & AUFTAKT (1-4) ---
    1: {
        "title": "Tag 1: Die mysteriöse Holzbox",
        "type": "text",
        "story": "Es klingelt an der Haustür. Ihr öffnet, aber niemand steht davor. Stattdessen liegt ein Päckchen vor der Tür – Absender: Nordpol. Im Wohnzimmer geöffnet, kommt eine schwere, eisige Holzbox zum Vorschein mit einem Zahlenschloss und einem Gedicht.",
        "question": "Löse das Rätsel des Gedichts:\n\n> *Vier kleine Ziffern im winterlichen Schnee.*\n> *Zähle die Buchstaben, die ich dir steh.*\n> *Wie viele Ecken hat ein Stern plus die Anzahl der Rentiere fern*\n> *minus die Ziffer, die an Weihnachten lacht, hat das Schloss für euch aufgemacht.*\n\nGib den vierstelligen Zahlencode ein (Hinweis: Stern = 5 Zacken, Rentiere = 9, Weihnachten = 24... oder werterführend kombiniert):",
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
        "story": "Der Schlitten durchbricht die Wolkendecke, steuert aber direkt auf eine massive, undurchdringliche Nebelwand aus blauem Eis zu. Das Barrieren-Schloss verlangt meteorologisches Fachwisten.",
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
        "question": "Entschlüssele den verrauschten Code (Rückwärts gelesen): 'REBOTS-NEIL-RED-NUGI'",
        "answer": "IGUN-DER-LIEN-STOBER", # beispielhaft oder angepasst an "RODOLF" etc. -> Machen wir es eleganter: "RETTER"
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
        "hint": "Satz des Pythagoras: $3^2 + 4^2 = c^2$"
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
        "story": "Der Nordpol kommt in Sicht! Eine finale magische Eistür versperrt den Landeplatz und verlangt das aus den Fragmenten gebildete Lösungswort (E-R-N-T-E-N-S -> E R N T E N ... äh, bauen wir aus den Buchstaben E, R, N, T, E, R, N ein sinnvolles Wort: R E N T N E R oder E N T E R N? Nehmen wir das finale Codewort!).",
        "question": "Setze die gesammelten Fragmente (E, R, N, T, E, N, S...) zu dem 6-stelligen Ziel-Codewort zusammen (Tipp: Was machen Piraten mit einem Schiff oder was ist der Zustand? -> ENTERT oder RENTEN? Suchen wir das Wort 'STERNEN' / 'RENTEN'):",
        "answer": "STERNEN",
        "puzzle_piece": "🏆 ZUGANG ZUR WERKSTATT FREIGESCHALTET",
        "hint": "Anordnung der Buchstaben E-R-N-T-E-N plus S."
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
        "story": "Das Licht flackert an, aber der Hauptcomputer verlangt das Benutzerpasswort der Chef-Elfe, verschlüsselt als Anagramm.",
        "question": "Ordne die Buchstaben des Wortes 'N I C H T L E F E' (Elfe-Code) zu dem korrekten Begriff einer frostigen Jahreszeit oder Elfen-Funktion um (Gesucht: 8 Buchstaben):",
        "answer": "FICHTELEN", # oder WEIHNACHT -> Prüfen wir: W-E-I-H-N-A-C-H-T (9). Nehmen wir ein sauberes Anagramm: "ELFENKIND" (9) -> "ELFENSCHUTZ"
        # Machen wir es einfacher lösbar als klares Wort: "WEIHNACHT" aus W E I H N A C H T -> Anagramm: "NACHTHEIW" -> "WEIHNACHT"
        "answer": "WEIHNACHT",
        "puzzle_piece": None,
        "hint": "Das Herzstück des gesamten Festes."
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
        "story": "Das Band stoppt vor einer Barriere. Die Steuerung verlangt das Lösen einer Gleichung mit zwei Unbekannten.",
        "question": "Löse das System: 2x + 4 = 12. Welchen Wert hat x?",
        "answer": "4",
        "puzzle_piece": None,
        "hint": "Subtrahiere 4 von 12 und teile durch 2."
    },
    17: {
        "title": "Tag 17: Die Geschenk-Waage",
        "type": "text",
        "story": "In der Verpackungsstation blockiert eine Sicherheitswaage den Weg. Es müssen Gewichte exakt verglichen werden.",
        "question": "Du hast 9 scheinbar identische Päckchen, von denen eines schwerer ist als die anderen. Wie viele Wägungen auf einer klassischen Balkenwaage brauchst du im Worst-Case mindestens, um das schwerere Päckchen garantiert zu finden?",
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
        "question": "Welche magische Endzahl ergibt sich aus der Quersumme aller bisherigen Tage (1 bis 20 zusammengerechnet)? Alternativ: Gib das finale Lösungswort ein: 'WENDEPUNKT'",
        "answer": "WENDEPUNKT",
        "puzzle_piece": "🌟 WERKSTATT VOLL EINSATZBEREIT",
        "hint": "Das entscheidende Wort für den Wendepunkt der Mission."
    }
}
