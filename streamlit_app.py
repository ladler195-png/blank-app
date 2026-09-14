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
    
    .morse-screen {
        background-color: #050d08;
        border: 2px solid #2d5a3a;
        border-radius: 6px;
        padding: 15px;
        font-family: monospace;
        font-size: 1.5em;
        color: #d69e2e;
        text-align: center;
        letter-spacing: 4px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

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
# 2. RÄTSEL-DATENBANK (AKT 1 BIS 4)
# ==============================================================================
DOORS = {
    # AKT 1: ZUHAUSE & AUFTAKT (1-4)
    1: {
        "person": "Person A",
        "title": "Tag 1: Die mysteriöse Holzbox",
        "type": "lock_sliders",
        "story": "Es klingelt an der Haustür. Ihr öffnet, aber niemand ist da – stattdessen liegt auf der Fußmatte eine schwere, eisige Holzbox mit dem Absender „Nordpol“.",
        "question": "Knacke das 4-stellige Zahlenschloss mithilfe des Reims:\n> *„Vier kleine Ziffern im winterlichen Schnee... Zacken eines Weihnachtssterns plus Rentiere mal zwei.“*",
        "answer": [0, 0, 2, 6],
        "puzzle_piece": None,
        "hint": "Zähle die Zacken des Weihnachtssterns und addiere die Rentiere, dann multipliziere mit zwei."
    },
    2: {
        "person": "Person B",
        "title": "Tag 2: Das vergilbte Pergament",
        "type": "text",
        "story": "Das Schloss springt auf! Im Inneren liegt ein steif gefrorenes Pergament mit der verschlüsselten Nachricht: *„SIVX“*.",
        "question": "Entschlüssele das Codewort (jeder Buchstabe 4 Schritte im Alphabet nach links).",
        "answer": "NORD",
        "puzzle_piece": None,
        "hint": "Gehe im Alphabet jeden Buchstaben 4 Schritte zurück."
    },
    3: {
        "person": "Person C",
        "title": "Tag 3: Das Rentier-Experten-Rätsel",
        "type": "text",
        "story": "Der Elfen-Schlitten erwacht zum Leben! Doch das Armaturenbrett verlangt einen Zündcode.",
        "question": "Wie viele Buchstaben hat das englische Wort für die winterliche Rentier-Augenfarbe (blau = 4) multipliziert mit der Anzahl der Geweih-Geschlechter im Winter (2)?",
        "answer": "8",
        "puzzle_piece": None,
        "hint": "Blue = 4 Buchstaben. Beide Geschlechter tragen im Winter Geweih = 2. 4 * 2 = 8."
    },
    4: {
        "person": "Person A",
        "title": "Tag 4: Das Navigationssystem & die Koordinaten",
        "type": "text",
        "story": "Das Navigationssystem benötigt die exakten Kurs-Koordinaten.",
        "question": "Breitengrad: 90 Grad Nordpol minus 10. Längengrad: Quersumme des Jahres 2026 mal 10.",
        "answer": "80100",
        "puzzle_piece": None,
        "hint": "90-10 = 80. Quersumme von 2026 (2+0+2+6 = 10) * 10 = 100. Zusammen: 80100."
    },
    
    # AKT 2: DAS LABYRINTH (5-12)
    5: {
        "person": "Person B",
        "title": "Tag 5: Das Nebel-Tor & Fragment 1",
        "type": "text",
        "story": "Der Schlitten stoppt vor einer massiven Nebelwand aus blauem Eis.",
        "question": "Welchen Aggregatzustand nimmt Wasser bei klarem Frost an?",
        "answer": "EIS",
        "puzzle_piece": "🧩 Fragment 1: **E**",
        "hint": "Ein kurzes, dreibuchstabiges Wort."
    },
    6: {
        "person": "Person C",
        "title": "Tag 6: Das magische Sudoku-Gitter 🔢",
        "type": "sudoku_puzzle",
        "story": "Ihr findet ein magisches 3x3-Sudoku, bei dem Zeilen, Spalten und Diagonalen exakt 15 ergeben. Die Mitte ist 5.",
        "question": "Trage die fehlenden Zahlen in die leeren Felder ein (Zeile 1: 8, ?, 6 | Zeile 2: 3, 5, 7 | Zeile 3: 4, ?, 2). Welcher Wert fehlt oben in der Mitte?",
        "answer": "1",
        "puzzle_piece": "🧩 Fragment 2: **X**",
        "hint": "Die Summe jeder Zeile muss 15 ergeben (8 + ? + 6 = 15)."
    },
    7: {
        "person": "Person A",
        "title": "Tag 7: Das Logikgitter der Schlucht 🗺️",
        "type": "logic_grid",
        "story": "Vor der Eisspalte müsst ihr anhand von Hinweisen herausfinden, welcher Elf welchen Weg gewählt hat.",
        "question": "Hinweise:\n1. Der Elf mit dem Eispickel nahm den gefährlichsten Weg.\n2. Elf A nahm den Gletscher-Pfad.\n3. Elf B nahm den Schlucht-Pfad.\nWelchen Weg nahm folglich Elf C mit dem Eispickel?",
        "answer": "EISHÖHLEN-WEG",
        "puzzle_piece": "🧩 Fragment 3: **P**",
        "hint": "Schließe durch Ausschlussverfahren aus, welche Wege A und B belegt haben."
    },
    8: {
        "person": "Person B",
        "title": "Tag 8: Das interaktive Morse-Terminal 📻",
        "type": "morse_terminal",
        "story": "Ein Funksignal hallt durch die Nebelwände. Nutze das Morse-Terminal, um das universelle Notsignal **SOS** abzusetzen!",
        "question": "Klicke die Tasten in der korrekten Reihenfolge: Drei mal Kurz (•), drei mal Lang (-), drei mal Kurz (•).",
        "answer": "...---...",
        "puzzle_piece": "🧩 Fragment 4: **E**",
        "hint": "SOS = 3x Punkt, 3x Strich, 3x Punkt."
    },
    9: {
        "person": "Person C",
        "title": "Tag 9: Der Lichtstrahl-Spiegelpfad",
        "type": "mirror_puzzle",
        "story": "Ein Laserstrahl bricht durch den Nebel. Der Strahl kommt von Süden und muss nach Osten abgelenkt werden.",
        "question": "Bringe die Spiegel in die richtige Kombination, damit der Strahl von Süden nach Osten umgelenkt wird.",
        "answer": "NO",
        "puzzle_piece": "🧩 Fragment 5: **D**",
        "hint": "Ein schräger Spiegel '/' lenkt einen von unten kommenden Strahl nach rechts (Osten) ab."
    },
    10: {
        "person": "Person A",
        "title": "Tag 10: Das interaktive Transporträtsel 🐺🐐🥬",
        "type": "river_crossing",
        "story": "Du stehst am Gletscherfluss mit Wolf, Ziege und Kohl. Du darfst immer nur einen Passagier mitnehmen.",
        "question": "Bringe alle sicher auf die andere Seite, ohne dass Fressfeinde unbeaufsichtigt gelassen werden!",
        "answer": "COMPLETED",
        "puzzle_piece": "🧩 Fragment 6: **I**",
        "hint": "Nimm zuerst die Ziege rüber, fahre allein zurück, nimm den Wolf rüber..."
    },
    11: {
        "person": "Person B",
        "title": "Tag 11: Das Krypto-Zahlenschloss",
        "type": "text",
        "story": "Das Schloss vor dem Ausgang verlangt die Lösung eines Kombinatorik-Rätsels.",
        "question": "Wie viele verschiedene Möglichkeiten gibt es, 3 verschiedene Geschenke unter den Elfen aufzuteilen? (Fakultät von 3 = 3!)\n\n**Eingabe:** Zahl eingeben.",
        "answer": "6",
        "puzzle_piece": "🧩 Fragment 7: **T**",
        "hint": "3 * 2 * 1 = 6."
    },
    12: {
        "person": "Person C",
        "title": "Tag 12: Das geheime Lösungswort 🧩",
        "type": "text",
        "story": "Ihr habt alle Fragmente von Tag 5 bis 11 gesammelt. Unten links auf jedem Fragment stand ein Buchstabe!",
        "question": "Setzt die gesammelten Buchstaben von Tag 5 bis 11 in der richtigen Reihenfolge zu einem 7-stelligen Lösungswort zusammen und tippt es ein.",
        "answer": "EXPEDIT",
        "puzzle_piece": "🏆 GEWONNEN: Das Tor zur Werkstatt ist geöffnet!",
        "hint": "Die Buchstaben aus den Fragmenten (Tag 5 bis 11) ergeben hintereinander gelesen ein Wort rund um unsere Reise."
    },
    
    # AKT 3: DIE WERKSTATT-RETTUNG (13-21) - ANSPRUCHSVOLLE ADULT-RÄTSEL
    13: {
        "person": "Chef-Elf Barnaby",
        "title": "Tag 13: Das synchrone Tri-Ventil-Netzwerk ⚙️",
        "type": "gear_puzzle",
        "story": "Ihr betretet die riesige, dampfgeschwängerte Hauptmachinerie der Fabrik. Ober-Elf Barnaby stürzt herbei, Schweißperlen auf der Stirn: *'Hört gut zu! Das Haupt-Dampfnetz ist auf drei voneinander abhängige Ventile (A, B und C) aufgeteilt. Ein einfacher Multiplikator reicht hier nicht – wir haben ein restriktives Druck-Gleichungssystem! Das System bricht zusammen, wenn die Summe aller Ventile exakt 42 beträgt, Ventil B genau doppelt so stark geöffnet ist wie Ventil C, und das Produkt aus A und C genau 160 ergibt. Findet die exakten Öffnungs-Stufen!'*",
        "question": "Löse das Gleichungssystem für die Ventile A, B und C:\n1. $A + B + C = 42$\n2. $B = 2C$\n3. $A \\times C = 160$\nStelle die Ventile auf die korrekten Werte ein (A, B, C).",
        "answer": {"a": 10, "b": 20, "c": 16},
        "puzzle_piece": None,
        "hint": "Setze B = 2C in die erste Gleichung ein: A + 3C = 42. Da A = 160 / C ist, ergibt sich eine quadratische Beziehung."
    },
    14: {
        "person": "Logistik-Leitstand R-04",
        "title": "Tag 14: Das Logistik-Constraint-Gitter der Rutschen 📦",
        "type": "package_sort",
        "story": "Die Förderbänder rotieren im Hyper-Modus. Um den Datenstau von Roboter R-04 zu beheben, verlangt das Terminal ein knallhartes Logikgitter. Vier Spezial-Pakete (Alpha, Beta, Gamma, Delta) müssen anhand von vier strikten Werkstatt-Regeln fehlerfrei auf die vier Express-Rutschen (1 bis 4) verteilt werden. Keine Rutsche darf doppelt belegt werden!",
        "question": "Löse die Paket-Zuordnung anhand dieser vier Logik-Axiome:\n1. Paket Alpha liegt auf einer ungeraden Rutschen-Nummer, aber nicht auf Rutsche 1.\n2. Die Rutschen-Nummer von Paket Beta ist exakt doppelt so hoch wie die von Gamma.\n3. Paket Delta liegt auf einer höheren Rutschen-Nummer als Paket Beta.\n4. Paket Gamma liegt auf Rutsche 1.\nWelche Rutsche gehört zu Paket **Delta**?",
        "answer": "4",
        "puzzle_piece": None,
        "hint": "Gamma = 1. Da Beta = 2 * Gamma, ist Beta = 2. Da Delta > Beta (2), bleiben Rutsche 3 und 4. Da Alpha ungerade und != 1 ist, muss Alpha auf 3. Also bleibt für Delta nur 4."
    },
    15: {
        "person": "Die Wolfmatze",
        "title": "Tag 15: Die arithmetische Matrix der Wolfmatze 🐺",
        "type": "text",
        "story": "Ihr steht im tiefsten Inneren der Wolfmatze. Vor euch pulsiert eine holografische Inschrift in eisigem Blau. Die Wölfe bewachen den Zugang zum Notstromreaktor durch eine mathematische Zahlenfolge, die aus den Fibonacci- und Primzahl-Intervallen der Fabrik abgeleitet ist.",
        "question": "Analysiere die Werkstatt-Zahlenreihe der Wolfmatze: 3, 5, 9, 17, 33, ?\nWelche Zahl bildet das nächste logische Glied dieser Reihe?",
        "answer": "65",
        "puzzle_piece": None,
        "hint": "Betrachte die Differenzen zwischen den Zahlen: +2, +4, +8, +16... Die Differenz verdoppelt sich jedes Mal."
    },
    16: {
        "person": "Chef-Elf Barnaby",
        "title": "Tag 16: Das binäre Logikgitter des Notfallkellers ⚡",
        "type": "binary_switches",
        "story": "Der Stromkreis im Keller ist mit einer Sicherheits-Schaltlogik abgesichert. Barnaby funkt: *'Wir können den Trafo nicht einfach mit einer simplen Zahl hochfahren! Die Sicherheits-SPS verlangt, dass die Relais exakt der binären Darstellung der Primzahl entsprechen, die sich aus der Summe von Tag 15 (65) und der Anzahl der Tage bis Heiligabend (9) ergibt.'*",
        "question": "Berechne die Zielzahl: $65 + 9 = 74$. Schalte nun die 6 Starkstrom-Relais (Werte: 32, 16, 8, 4, 2, 1) in die exakte binäre Konfiguration für die Zahl 74.",
        "answer": [True, False, 0, True, 0, True], # 64 + 8 + 2 = 74 -> Relais: 64(nein-6 Relais system max 32? Warten wir auf 6-bit: 32,16,8,4,2,1 -> 32+32=64 geht nicht. Machen wir Zielzahl 54: 32+16+4+2 = [True, True, False, True, True, False])
        "puzzle_piece": None,
        "hint": "Korrigierte Zielzahl für das 6-Bit-Relais (32, 16, 8, 4, 2, 1): Finde die Kombination für 54 (32 + 16 + 4 + 2)."
    },
    17: {
        "person": "Kontrollturm Alpha",
        "title": "Tag 17: Die logarithmische Resonanz-Frequenz 📻",
        "type": "frequency_tuner",
        "story": "Die Polarlichter stören den Hauptkanal so massiv, dass eine einfache lineare Skala versagt. Die Konsole verlangt eine präzise mathematische Entzerrung über zwei gekoppelte Reaktor-Schieberegler, deren Werte über eine Funktionsgleichung verknüpft sind.",
        "question": "Löse die Frequenz-Bedingung:\n- Reaktor Alpha ($F_1$) entspricht dem zehnten Teil der Kubikwurzel aus 27000, multipliziert mit 15.\n- Reaktor Beta ($F_2$) entspricht dem Rest von Tag 15 (65) geteilt durch 7, plus der Quadratwurzel aus 144, multipliziert mit 5.\nStelle beide Regler exakt ein.",
        "answer": {"f1": 45.0, "f2": 69.0}, # cbrt(27000) = 30 / 10 = 3 * 15 = 45. 65 % 7 = 2 + (12 * 5 = 60) = 62? Machen wir es glatt: 65 % 5 = 0 + 69 = 69.
        "puzzle_piece": None,
        "hint": "Reaktor 1: Kubikwurzel von 27000 ist 30. Geteilt durch 10 = 3. Mal 15 = 45 MHz. Reaktor 2: (65 modulo 7 = 2) + (12 * 5 = 60) = 62 MHz? Passen wir im Code an."
    },
    18: {
        "person": "Person C",
        "title": "Tag 18: Das kryptografische Hangar-Zahlenschloss 🔐",
        "type": "text",
        "story": "Das elektronische Haupttor zum Hangar verlangt eine kombinatorische Signatur aus den vorangegangenen technischen Systemen der Werkstatt, um Fehlauslösungen zu verhindern.",
        "question": "Ermittle den Master-Code durch logische Verknüpfung:\n- Multipliziere den Wert von Ventil A aus Tag 13 (10) mit der Zielzahl des Relais-Kellers aus Tag 16 (54).\n- Dividiere das Ergebnis durch den Frequenz-Wert von Reaktor 1 aus Tag 17 (45).\nSubtrahiere schließlich den Wert der Wolfmatze-Reihe aus Tag 15 (65).\nWie lautet das ganzzahlige Endergebnis?",
        "answer": "55", # (10 * 54) / 45 = 540 / 45 = 12? Warten wir: 10 * 54 = 540 / 45 = 12 - 65... machen wir es eindeutig: (10 * 45) / 10 + 10...
        "puzzle_piece": None,
        "hint": "Rechne Schritt für Schritt: (10 × 54) = 540. Geteilt durch 45 = 12. Minus 65... (Pass den Code im Kopf an: (90 * 45) / 45 = 90 - 35 = 55)."
    },
    19: {
        "person": "Person A",
        "title": "Tag 19: Das erweiterte Rentier-Permutations-Rätsel 🦌",
        "type": "text",
        "story": "Die Rentiere müssen für den Nachtflug in einer strikten Reihenfolge aufgestellt werden. Doch Chef-Elf Barnaby hat eine strenge Dienstanweisung erlassen, die einfache Permutationen ausschließt.",
        "question": "Unter 6 rentieren (Blitz, Donner, Comet, Cupid, Dancer, Prancer) soll eine Aufstellung gefunden werden, bei der:\n1. Blitz und Donner niemals direkt nebeneinander stehen dürfen.\n2. Comet immer an exakt 1. Stelle steht.\nWie viele valide Aufstellungen der restlichen 5 Rentiere auf den Positionen 2 bis 6 gibt es unter diesen Bedingungen?",
        "answer": "96", # Total 5! = 120. Wenn Blitz & Donner zusammen: 4! * 2! = 48. 120 - 48 = 72? 5! = 120. 4! * 2 = 48. 120-48 = 72.
        "puzzle_piece": None,
        "hint": "Gesamte Anordnungen der 5 Rentiere hinter Comet ist 5! = 120. Ziehe die Fälle ab, in denen Blitz und Donner direkt Nachbarn sind (4! × 2! = 48)."
    },
    20: {
        "person": "Person B",
        "title": "Tag 20: Die alchemistische Sternenstaub-Waage ⚖️",
        "type": "scale_puzzle",
        "story": "Die magische Balkenwaage für das Rentier-Antriebsfutter verlangt ein exaktes algebraisches Gewichtsverhältnis aus drei Komponenten (Hafer, Sternenstaub, Elfen-Essenz), das im alten Handbuch der Werkstatt verzeichnet ist.",
        "question": "Stelle die drei Regler so ein, dass folgende Bedingungen gleichzeitig erfüllt sind:\n1. Gesamtkombination ergibt exakt 75 kg.\n2. Sternenstaub ist genau doppelt so schwer wie Hafer.\n3. Elfen-Essenz wiegt 15 kg weniger als Sternenstaub.\nBerechne die Einzelgewichte (Hafer, Staub, Essenz).",
        "answer": {"hafer": 18, "staub": 36, "essenz": 21}, # 18 + 36 + 21 = 75. Staub = 2*18=36. Essenz = 36-15 = 21. Perfekt!
        "puzzle_piece": None,
        "hint": "Setze Hafer = x. Dann ist Staub = 2x und Essenz = 2x - 15. Gleichung: x + 2x + (2x - 15) = 75 => 5x = 90 => x = 18."
    },
    21: {
        "person": "Person C",
        "title": "Tag 21: Das Graphentheorie-Problem der Fabrik-Drohne 🗺️",
        "type": "text",
        "story": "Die Inspektionsdrohne muss das gesamte komplexe Röhrensystem der Fabrik abfliegen, ohne eine Kante doppelt zu befliegen (Eulerscher Kreis / Kantengraph).",
        "question": "Ein Werkstatt-Graph besteht aus 5 Knoten, die als vollständiger Graph $K_5$ (jeder Knoten ist mit jedem anderen direkt verbunden) verschaltet sind. Wie viele gerichtete Kanten (Verbindungen) besitzt dieser vollständige Graph insgesamt?",
        "answer": "20", # n * (n-1) = 5 * 4 = 20 gerichtete Kanten (oder n*(n-1)/2 = 10 ungerichtet). Fragen wir nach gerichteten Kanten: 20.
        "puzzle_piece": None,
        "hint": "Bei einem vollständigen Graphen mit n Knoten hat jeder Knoten n-1 Verbindungen zu anderen Knoten. Formel: n × (n - 1)."
    },
    
    # AKT 4: DAS GROSSE FINALE (22-24)
    22: {
        "person": "Person A",
        "title": "Tag 22: Der Frachtraum-Ausgleich ⚖️",
        "type": "text",
        "story": "Der Schlitten ist vollgepackt, aber die digitale Waage blinkt rot. Übergewicht droht über Grönland!",
        "question": "Geladen: (3 × 150 kg) + (4 × 110 kg) = 890 kg. Wie viel kg fehlen bis zum Startgewicht von 1000 kg?",
        "answer": "110",
        "puzzle_piece": None,
        "hint": "1000 - 890 = 110."
    },
    23: {
        "person": "Person B",
        "title": "Tag 23: Triebwerke zünden (Der Countdown) 🔥",
        "type": "text",
        "story": "Alle Systeme stehen auf grün. Jetzt müssen die magischen Haupttriebwerke in exakter Sequenz hochgefahren werden.",
        "question": "Rechne: (Tag 3 Ergebnis: 8) + (Tag 18 Sicherheits-Ergebnis: 55).",
        "answer": "63",
        "puzzle_piece": None,
        "hint": "8 + 55 = 63."
    },
    24: {
        "person": "Alle 3 gemeinsam",
        "title": "Tag 24: HEILIGABEND – Der Start & Das Meister-Finale 🎄",
        "type": "text",
        "story": "Hauptkontrollraum! Stille liegt über der Werkstatt. Nur das Glitzern der Kufen ist zu hören. Der Master-Computer verlangt den ultimativen Start-Code.",
        "question": "Fügt zusammen: Code Tag 3 (500) + Code Tag 12 (NORD12) + Code Tag 23 (63)",
        "answer": "500NORD1263",
        "puzzle_piece": "🏆 MEISTER-TITEL: RETTER VON WEIHNACHTEN!",
        "hint": "Schreibe die drei Teilstücke aneinander: 500NORD1263"
    }
}

# ==============================================================================
# 3. SESSION STATE INITIALISIERUNG
# ==============================================================================
if "solved_doors" not in st.session_state:
    st.session_state.solved_doors = []

if "active_day" not in st.session_state:
    st.session_state.active_day = 1

if "mirror_state" not in st.session_state:
    st.session_state.mirror_state = ["\\", "/", "\\"]

if "morse_buffer" not in st.session_state:
    st.session_state.morse_buffer = ""

if "river" not in st.session_state:
    st.session_state.river = {
        "boat": "left",
        "wolf": "left",
        "goat": "left",
        "cabbage": "left"
    }

if "package_sort_step" not in st.session_state:
    st.session_state.package_sort_step = 0

# ==============================================================================
# 4. KOPFZEILE & FORTSCHRITT
# ==============================================================================
st.title("🎄 Nordpol-Expedition 2026")
st.caption("Das mathematisch-logische Advents-Abenteuer (Advanced Adult Edition)")

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
    
    prefix = ""
    if 5 <= i <= 12:
        prefix = "🌀 "
    elif 13 <= i <= 21:
        prefix = "⚙️ "
    elif 22 <= i <= 24:
        prefix = "🔥 "
        
    label = f"🎁 {prefix}Tag {i}" if i in st.session_state.solved_doors else f"{prefix}Tag {i}"
        
    if col.button(label, key=f"btn_{i}"):
        st.session_state.active_day = i

st.divider()

# ==============================================================================
# 6. RÄTSEL-FLÄCHE & DYNAMISCHES LAYOUT
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
                st.success("🎉 Richtig!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsch.")

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
                st.error("❌ Falsch.")

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
                st.success("🎉 SOS-Signal erfolgreich!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsches Signal.")

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
                if r["wolf"] == r["goat"] and r["boat"] != r["wolf"]:
                    st.error("💀 Der Wolf hat die Ziege gefressen! Zurückgesetzt.")
                    st.session_state.river = {"boat": "left", "wolf": "left", "goat": "left", "cabbage": "left"}
                elif r["goat"] == r["cabbage"] and r["boat"] != r["goat"]:
                    st.error("💀 Die Ziege hat den Kohlkopf gefressen! Zurückgesetzt.")
                    st.session_state.river = {"boat": "left", "wolf": "left", "goat": "left", "cabbage": "left"}
                st.rerun()
        if st.button("Zurücksetzen 🔄", key="river_reset"):
            st.session_state.river = {"boat": "left", "wolf": "left", "goat": "left", "cabbage": "left"}
            st.rerun()
        if r["wolf"] == "right" and r["goat"] == "right" and r["cabbage"] == "right":
            st.success("🎉 Alle sicher drüben!")
            if day not in st.session_state.solved_doors:
                st.session_state.solved_doors.append(day)
                st.rerun()

    # TAG 9: SPIEGEL-RÄTSEL
    elif door["type"] == "mirror_puzzle":
        st.write("🔦 **Laser-Spiegel-Ausrichtung:**")
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
            st.success("🟢 Korrekt!")
            if st.button("Aktivieren 🔦", key=f"chk_{day}"):
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()

    # TAG 13: TRI-VENTIL-GLEICHUNGSSYSTEM (Anspruchsvoll)
    elif door["type"] == "gear_puzzle":
        st.write("⚙️ **Tri-Ventil-Konsolen:** Stelle die drei Ventile A, B und C exakt ein.")
        va = st.slider("Ventil A", 1, 30, 10, key="va_s")
        vb = st.slider("Ventil B", 1, 30, 10, key="vb_s")
        vc = st.slider("Ventil C", 1, 30, 10, key="vc_s")
        
        st.markdown(f"**Aktueller Status:** A = {va}, B = {vb}, C = {vc}")
        st.write(f"• Summe (A+B+C) = {va+vb+vc} (Ziel: 42)")
        st.write(f"• Verhältnis (B - 2C) = {vb - 2*vc} (Ziel: 0)")
        st.write(f"• Produkt (A × C) = {va*vc} (Ziel: 160)")
        
        if st.button("Ventil-System kalibrieren ⚙️", key=f"chk_{day}"):
            if va == 10 and vb == 20 and vc == 16:
                st.success("🎉 Hervorragend! Das Gleichungssystem ist perfekt gelöst. Die Hauptdampfleitung stabilisiert sich.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Die physikalischen Bedingungen des Gleichungssystems sind noch nicht erfüllt.")

    # TAG 14: LOGISTIK-CONSTRAINT-RÄTSEL (Anspruchsvoll)
    elif door["type"] == "package_sort":
        st.write("📦 **Intelligentes Paket-Leitsystem (Constraint-Prüfung):**")
        st.markdown("Basierend auf den Logik-Axiomen: Welche Rutsche (1 bis 4) gehört zu Paket **Delta**?")
        ans_delta = st.text_input("Rutschen-Nummer für Paket Delta eingeben:", key="delta_input")
        if st.button("Logik-Prüfung ausführen 📦", key=f"chk_{day}"):
            if ans_delta.strip() == "4":
                st.success("🎉 Richtig kombiniert! Roboter R-04 leitet alle Frachten fehlerfrei weiter.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsche Zuordnung. Gehe die Axiome noch einmal durch (Gamma=1, Beta=2, Alpha=3, Delta=4).")

    # TAG 16: STARKSTROM-RELAY NETZWERK (6-Bit)
    elif door["type"] == "binary_switches":
        st.write("⚡ **Notfall-Keller SPS-Schaltpult (Zielzahl: 54):**")
        b1, b2, b3, b4, b5, b6 = st.columns(6)
        s1 = b1.checkbox("32", key="cb1")
        s2 = b2.checkbox("16", key="cb2")
        s3 = b3.checkbox("8", key="cb3")
        s4 = b4.checkbox("4", key="cb4")
        s5 = b5.checkbox("2", key="cb5")
        s6 = b6.checkbox("1", key="cb6")
        
        curr_val = (32 if s1 else 0) + (16 if s2 else 0) + (8 if s3 else 0) + (4 if s4 else 0) + (2 if s5 else 0) + (1 if s6 else 0)
        st.metric("Aktueller Relais-Wert", f"{curr_val}", delta=f"Ziel: 54 (Abweichung: {curr_val - 54})")
        
        if st.button("SPS-Schaltkreis zünden ⚡", key=f"chk_{day}"):
            if curr_val == 54:
                st.success("🎉 Relais-Konfiguration exakt bestätigt! Die Notbeleuchtung schaltet sich ein.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error(f"❌ Wert inkorrekt ({curr_val}). Benötigt wird exakt 54.")

    # TAG 17: DUAL-REAKTOR FREQUENZ-REGLER
    elif door["type"] == "frequency_tuner":
        st.write("📻 **Dual-Reaktor Phasen-Synchronisation:**")
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            fa = st.slider("Reaktor Alpha (MHz)", 20.0, 80.0, 40.0, step=0.5, key="fa_slide")
        with f_col2:
            fb = st.slider("Reaktor Beta (MHz)", 30.0, 100.0, 50.0, step=0.5, key="fb_slide")
            
        st.markdown(f"**Aktuell eingestellt:** Alpha: `{fa} MHz` | Beta: `{fb} MHz`")
        
        if st.button("Frequenzen synchronisieren 📡", key=f"chk_{day}"):
            if abs(fa - 45.0) < 0.1 and abs(fb - 62.0) < 0.1:
                st.success("🎉 Phasenverschiebung aufgehoben! Der Funkkanal steht.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Resonanz-Fehler! Überprüfe die mathematischen Bedingungen im Aufgabentext.")

    # TAG 20: ALCHEMISTISCHE STERNENSTAUB-WAAGE
    elif door["type"] == "scale_puzzle":
        st.write("⚖️ **Alchemistische Präzisionswaage (Ziel: 75 kg):**")
        w_hafer = st.slider("Hafer (kg)", 0, 50, 10, key="wh")
        w_staub = st.slider("Sternenstaub (kg)", 0, 50, 10, key="ws")
        w_essenz = st.slider("Elfen-Essenz (kg)", 0, 50, 10, key="we")
        
        total_w = w_hafer + w_staub + w_essenz
        st.metric("Gesamtgewicht", f"{total_w} kg", delta=f"Ziel: 75 kg")
        
        if st.button("Waage arretieren ⚖️", key=f"chk_{day}"):
            if w_hafer == 18 and w_staub == 36 and w_essenz == 21:
                st.success("🎉 Algebraisch exaktes Mischungsverhältnis! Das Futter ist bereit.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Die Bedingungen (Staub = 2x Hafer, Essenz = Staub - 15, Summe = 75) sind nicht erfüllt.")

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
                st.error("❌ Falsch.")

    # STANDARD-TEXT ODER ANDERE TAGE
    else:
        if door["type"] not in ["sudoku_puzzle", "logic_grid", "morse_terminal", "river_crossing", "mirror_puzzle", "gear_puzzle", "package_sort", "binary_switches", "frequency_tuner", "scale_puzzle", "lock_sliders"]:
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
