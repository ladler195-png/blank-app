import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. SEITEN-KONFIGURATION & DUNKELGRÜNES DESIGN (CSS)
# ==============================================================================
st.set_page_config(
    page_title="Weihnachtlicher Rätsel-Adventskalender",
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
# 2. RÄTSEL-DATENBANK (AKT 1 BIS 4 - VOLLSTÄNDIG ÜBERARBEITET)
# ==============================================================================
DOORS = {
    # AKT 1: ZUHAUSE & AUFTAKT (1-4)
    # AKT 1: ZUHAUSE & AUFTAKT (1-4)
    1: {
        "title": "Tag 1: Die mysteriöse Holzbox",
        "type": "text",
        "story": "Es klingelt an der Haustür. Ihr öffnet, aber niemand steht davor. Stattdessen seht ihr vor eurer Tür ein Päckchen liegen und auf dem Absender steht Nordpol. Ihr nehmt das Päckchen mit nach rein und öffnet es im Wohnzimmer. Und zum Vorschein kommt eine schwere eisige Holzbox. Ihr guckt euch die Holzbox von jeder Seite an und findet an der einen Seite ein Gedicht und da drunter ein Zahlenschloss.",
        "question": "Löse das Rätsel des Gedichts und finde den vierstelligen Zahlencode heraus:\n\n> *Vier kleine Ziffern im winterlichen Schnee.*\n> *Zähle die Buchstaben, die ich dir steh.*\n> *Wie viele Ecken hat ein Stern plus die Anzahl der Rentiere fern*\n> *minus die Ziffer, die an Weihnachten lacht, hat das Schloss für euch aufgemacht.*\n\nGib den vierstelligen Zahlencode ein:",
        "answer": "0026",  # Hier kannst du den Code anpassen, falls er durch das neue Gedicht ein anderer ist!
        "puzzle_piece": None,
        "hint": "Achte auf die Hinweise im Gedicht (Sterne, Rentiere und das Datum von Weihnachten)."
    },
    2: {
        "title": "Tag 2: Das vergilbte Pergament",
        "type": "text",
        "story": "Das Schloss springt auf und im Inneren liegt ein Pergament. Auf diesem Pergament steht die Nachricht 'S I V X'. Unten ist ein Lorbeerkranz eingraviert.",
        "question": "Entschlüssele das Codewort. Der Lorbeerkranz bringt euch in die richtige Richtung.\n\nDeine Lösung:",
        "answer": "NORD",
        "puzzle_piece": None,
        "hint": "Benutzt den Caesar-Code."
    },
    3: {
        "title": "Tag 3: Das Rentier-Expertenrätsel",
        "type": "reindeer_quiz",
        "story": "Nachdem ihr das Zauberwort laut gesagt habt, hört ihr vom Weiten ein immer lauter werdendes Glockenklingeln. Ihr schaut aus dem Fenster und ihr könnt euren Augen kaum glauben, denn vor eurem Fenster steht ein Rentierschlitten mit acht Rentieren. Ihr geht nach draußen zu den Rentieren und die sagen, dass ihr das Codewort, das geheime Wort, gesagt habt, um jetzt mitzukommen. Aber damit ihr wirklich, damit wir euch dahin bringen, müsst ihr folgende Fragen über uns beantworten können. Das sagen die Rentiere.",
        "question": "Beantwortet die fünf anspruchsvollen Fragen über Rentiere nacheinander, um die Rentiere zu überzeugen.",
        "answer": "QUIZ_SOLVED",
        "puzzle_piece": None,
        "hint": "Hier ist biologisches und mythologisches Fachwissen über Rentiere gefragt (Augenfarbe im Winter, Geweihbiologie bei Kühen, wissenschaftlicher Name etc.)."
    },
    4: {
        "title": "Tag 4: Das Navigationssystem & die Koordinaten",
        "type": "text",
        "story": "Nachdem ihr euch mit den Rentieren bekannt gemacht habt, steigt ihr nun in den Schlitten ein und wollt gerade den Motor starten. Da fällt euch auf, dass das Navigationssystem exakte Kurskoordinaten braucht und ihr diese erst berechnen müsst. Zum Glück gibt es auch dafür ein Rätsel im Handbuch.",
        "question": "Berechne die Kurskoordinaten für das Navigationssystem:\nDer Breitengrad startet bei exakt 90 Grad Nord. Für den zweiten Schritt ziehen wir die Anzahl der Rentiere ab. Für den Längengrad nehmen wir die magische Quersumme von 2026 mal 10. Gib am Ende den kombinierten fünfstelligen Code aus den beiden Werten ein.",
        "answer": "81100",  # 90 - 9 = 81 (Breitengrad), Quersumme(2026) = 10 * 10 = 100 (Längengrad) -> 81100
        "puzzle_piece": None,
        "hint": "Rechne Schritt für Schritt: 90 - 9 für den Breitengrad und (2 + 0 + 2 + 6) * 10 für den Längengrad."
    },
    
    # AKT 2: DAS LABYRINTH (5-12)
    # AKT 2: DAS LABYRINTH (5-12)
    5: {
        "title": "Tag 5: Das Nebel-Tor & Fragment 1",
        "type": "text",
        "story": "Ihr fliegt los und der Schlitten schneidet durch die eiskalte Nacht. Plötzlich stoppt der Schlitten vor einer massiven, undurchdringlichen Nebelwand aus blauem Eis. Das magische Barrieren-Schloss verlangt meteorologisches Fachwissen über dieses Phänomen, um sich zu lichten.",
        "question": "Löse das Rätsel des Nebel-Tors:\n\n> *'Ich bin unsichtbar, wenn du mich atmest, doch zeige mich in klaren Frostnächten als dicker Dunst, wenn die Lufttemperatur den entscheidenden Punkt erreicht.'*\n\nWie nennt man diesen kritischen Punkt in der Meteorologie, bei dem die Luft vollständig mit Wasserdampf gesättigt ist und der Nebel entsteht? (Ein Wort, 8 Buchstaben)",
        "answer": "TAUPUNKT",
        "puzzle_piece": "🧩 Fragment 1: **E**",
        "hint": "Es beschreibt die Temperatur, bei der die relative Luftfeuchtigkeit 100 % erreicht."
    },
    6: {
        "title": "Tag 6: Das magische Sudoku (Fragment 2)",
        "type": "sudoku_puzzle",
        "story": "Nachdem sich die Nebelwand dank eures Wissens aufgelöst hat, tretet ihr durch das Tor in eine geheimnisvolle, schimmernde Eishöhle. Vor euch schwebt eine monolithische Steintafel, in die ein unvollendetes, magisches Zahlenraster aus purem Frost eingraviert ist. Die Runen flüstern: Nur wenn das magische Sudoku im perfekten Einklang gelöst wird, gibt die Tafel das nächste Fragment frei.",
        "question": "Löst das magische 4x4-Sudoku (oder ein klassisches 9x9-Sudoku, je nach Ausführung) auf der Steintafel. Tragt die fehlenden Zahlen in die markierten Felder ein.",
        "answer": "SOLVED", # Wird über die Logik unten geprüft
        "puzzle_piece": "🧩 Fragment 2: **R**",
        "hint": "In jeder Zeile, jeder Spalte und in jedem 2x2-Unterquadrat (bei 4x4) dürfen die Zahlen von 1 bis 4 nur einmal vorkommen."
    },
    7: {
        "title": "Tag 7: Die tückische Eisspalte",
        "type": "canyon_puzzle",
        "story": "Nach dem Verlassen der Eishöhle steht ihr plötzlich vor einer gewaltigen, tiefen Eisspalte, die euren Weg versperrt. Eine wackelige Hängebrücke führt hinüber, aber an der Felswand seht ihr einen alten Orientierungsplan und daneben blutige bzw. verkohlte Notizen von gescheiterten Vorgängern, die den falschen Pfad gewählt haben. Ihr müsst anhand der Hinweise den wahren 'Schnitzelweg' (den sicheren Pfad) identifizieren.",
        "question": "Analysiert die drei Wege an Hand der Wand-Notizen und findet den richtigen Schnitzelweg heraus.\n\n* **Weg A (Der Kristallpfad):** In den Notizen steht: *'Das Glitzern täuscht, hier brach das Eis unter unseren Stiefeln ein.'*\n* **Weg B (Der Windschatten-Pfad):** In den Notizen steht: *'Die Brise weht stetig von Osten, die Holzplanken halten, aber eine Markierung fehlt gänzlich.'*\n* **Weg C (Der Moos-Markierten-Pfad):** In den Notizen steht: *'Alte grüne Pfeile und Brotkrumen-Spuren weisen sicher über den Abgrund. Hier kam vor uns schon jemand durch.'*\n\nWelcher Weg ist der sichere Schnitzelweg? (Wähle A, B oder C):",
        "answer": "C",
        "puzzle_piece": "🧩 Fragment 3: **N**",
        "hint": "Lies dir die Notizen der Vorgänger genau durch: Wer war erfolgreich und wer ist eingebrochen oder hat sich verirrt?"
    },
    8: {
        "title": "Tag 8: Das interaktive Morse-Terminal 📻",
        "type": "morse_terminal",
        "story": "Ein Funksignal hallt durch die Nebelwände. Nutze das Morse-Terminal, um das universelle Notsignal **SOS** abzusetzen!",
        "question": "Klicke die Tasten in der korrekten Reihenfolge: Drei mal Kurz (•), drei mal Lang (-), drei mal Kurz (•).",
        "answer": "...---...",
        "puzzle_piece": "🧩 Fragment 4: **E**",
        "hint": "SOS = 3x Punkt, 3x Strich, 3x Punkt."
    },
    9: {
        "title": "Tag 9: Der Lichtstrahl-Spiegelpfad",
        "type": "mirror_puzzle",
        "story": "Ein Laserstrahl bricht durch den Nebel. Der Strahl kommt von Süden und muss nach Osten abgelenkt werden.",
        "question": "Bringe die drei Spiegel in die richtige Kombination, damit der Strahl umgelenkt wird.",
        "answer": "NO",
        "puzzle_piece": "🧩 Fragment 5: **D**",
        "hint": "Ein schräger Spiegel '/' lenkt einen von unten kommenden Strahl nach rechts ab."
    },
    10: {
        "title": "Tag 10: Das interaktive Transporträtsel (Wolf, Ziege, Kohl) 🐺🐐🥬",
        "type": "river_crossing",
        "story": "Du stehst am Gletscherfluss mit Wolf, Ziege und Kohl. Du darfst im Boot immer nur einen Passagier mitnehmen.",
        "question": "Bringe alle sicher auf die andere Seite, ohne dass Fressfeinde unbeaufsichtigt gelassen werden!",
        "answer": "COMPLETED",
        "puzzle_piece": "🧩 Fragment 6: **I**",
        "hint": "Nimm zuerst die Ziege rüber, fahre allein zurück, nimm den Wolf rüber..."
    },
    11: {
        "title": "Tag 11: Das Krypto-Zahlenschloss",
        "type": "text",
        "story": "Das Schloss vor dem Ausgang verlangt die Lösung eines Kombinatorik-Rätsels.",
        "question": "Wie viele verschiedene Möglichkeiten gibt es, 3 verschiedene Geschenke unter den Elfen aufzuteilen? (Fakultät von 3 = 3!)\n\n**Eingabe:** Zahl eingeben.",
        "answer": "6",
        "puzzle_piece": "🧩 Fragment 7: **T**",
        "hint": "3 * 2 * 1 = 6."
    },
    12: {
        "title": "Tag 12: Das geheime Lösungswort & Notiz 🧩",
        "type": "text",
        "story": "Ihr habt alle Fragmente von Tag 5 bis 11 gesammelt. Auf jedem Fragment stand ein Buchstabe! Zudem gab es einen System-Override-Token für Notfälle im Speicher: `OVERRIDE99!`",
        "question": "Setzt die gesammelten Buchstaben von Tag 5 bis 11 in der richtigen Reihenfolge zu einem 7-stelligen Lösungswort zusammen und tippt es ein.",
        "answer": "EXPEDIT",
        "puzzle_piece": "🏆 GEWONNEN: Das Tor zur Werkstatt ist geöffnet!",
        "hint": "Die Buchstaben aus den Fragmenten (Tag 5 bis 11) ergeben hintereinander gelesen ein passendes Wort."
    },
    
    # AKT 3: DIE WERKSTATT-RETTUNG (13-21)
    13: {
        "title": "Tag 13: Das synchrone Tri-Ventil-Netzwerk ⚙️",
        "type": "gear_puzzle",
        "story": "Ihr betretet die riesige Hauptmaschinerie. Das Haupt-Dampfnetz ist auf drei voneinander abhängige Ventile aufgeteilt. Ein restriktives Druck-Gleichungssystem muss gelöst werden.",
        "question": "Löse das Gleichungssystem für die Ventile A, B und C:\n1. A + B + C = 42\n2. B = 2C\n3. A × C = 160",
        "answer": {"a": 10, "b": 20, "c": 16},
        "puzzle_piece": None,
        "hint": "Setze B = 2C in die erste Gleichung ein..."
    },
    14: {
        "title": "Tag 14: Das interaktive Logistik-Constraint-Gitter der Rutschen 📦",
        "type": "package_sort",
        "story": "Die Förderbänder rotieren im Hyper-Modus. Vier Spezial-Pakete (Alpha, Beta, Gamma, Delta) müssen interaktiv per Schieberegler auf vier Express-Rutschen (1 bis 4) verteilt werden, entsprechend strenger Werkstatt-Regeln.",
        "question": "Axiome:\n1. Paket Alpha liegt auf einer ungeraden Rutsche, aber nicht auf Rutsche 1.\n2. Rutsche von Beta ist doppelt so hoch wie Gamma.\n3. Delta liegt auf einer höheren Rutsche als Beta.\n4. Gamma liegt auf Rutsche 1.",
        "answer": {"alpha": 3, "beta": 2, "gamma": 1, "delta": 4},
        "puzzle_piece": None,
        "hint": "Gamma = 1 -> Beta = 2 -> Delta = 4 -> Alpha = 3."
    },
    15: {
        "title": "Tag 15: Die interaktive Wunschzettel-Maschine 📜",
        "type": "wish_machine",
        "story": "Hier werden alle Kinderwünsche verarbeitet. Das Haupt-Datenband hängt fest und erfordert das Berechnen und Eintippen des nächsten Reihen-Glieds.",
        "question": "Analysiere die Code-Reihe der Wunschzettel-Maschine: 4, 9, 19, 39, 79, ?\nErmittle das nächste logische Glied über das interaktive Steuerpult.",
        "answer": "159",
        "puzzle_piece": None,
        "hint": "Jedes Glied wird verdoppelt und 1 addiert."
    },
    16: {
        "title": "Tag 16: Das binäre Logikgitter des Notfallkellers ⚡",
        "type": "binary_switches",
        "story": "Der Stromkreis im Keller ist mit einer Sicherheits-Schaltlogik abgesichert. Der Not-Trafo muss mit einer präzisen binären Last hochfahren.",
        "question": "Berechne die Zielzahl: Addition aus dem Wunschzettel-Ergebnis an zweiter Stelle (9) und der Anzahl der verbleibenden Tage bis Heiligabend (9), mal 3 minus 6 = **48**. Aktiviere die passenden Relais.",
        "answer": [True, True, False, False, False, False],
        "puzzle_piece": None,
        "hint": "32 + 16 = 48."
    },
    17: {
        "title": "Tag 17: Die interaktive Signal-Frequenz 📻",
        "type": "frequency_tuner",
        "story": "Am alten Radio-Kontrolltisch blinkt eine Notwarnung. Die Polarlichter stören den Hauptkanal. Stelle die Frequenz über den interaktiven Regler ein.",
        "question": "Berechne den Frequenz-Wert ($((24 + (2 \\times 4)) \\times 3) - 7$) und stelle den Regler auf diesen exakten MHz-Wert ein.",
        "answer": 89.0,
        "puzzle_piece": None,
        "hint": "(24 + 8) * 3 - 7 = 96 - 7 = 89 MHz."
    },
    18: {
        "title": "Tag 18: Das interaktive Hangar-Zahlenwort-Rätsel 🔐",
        "type": "hangar_puzzle",
        "story": "Das elektronische Master-Schloss des Hangars verlangt ein klassisches Zahlenwort-Rätsel, gesteuert über digitale Ziffern-Wahlräder.",
        "question": "Rätsel:\n> *„Ich bin eine zweistellige Zahl. Meine Zehnerziffer entspricht der halben Leistung des Ventil-Werts A (Tag 13: 10), und meine Einerziffer entspricht der Anzahl der Buchstaben im Wort NORDPOL (7).“*\nStelle den Code am Schloss ein.",
        "answer": 57,
        "puzzle_piece": None,
        "hint": "Hälfte von 10 = 5. Buchstaben in NORDPOL = 7. Ergibt 57."
    },
    19: {
        "title": "Tag 19: Das Rentier-Aufstellungs-Raster (3 Reihen à 2 Plätze) 🦌",
        "type": "reindeer_puzzle",
        "story": "Das Raster ist in 3 Reihen mit jeweils 2 Plätzen unterteilt, und Comet sitzt fest auf Platz 1.",
        "question": "Wie viele mathematisch valide Aufstellungen der Rentiere auf den Plätzen 2 bis 6 erfüllen exakt die Bedingungen?",
        "answer": "12",
        "puzzle_piece": None,
        "hint": "Analysiere die fixen Blöcke und schließe verbotene Nachbarn aus."
    },
    20: {
        "title": "Tag 20: Die alchemistische Sternenstaub-Waage ⚖️",
        "type": "scale_puzzle",
        "story": "Mische das Spezialfutter auf der Balkenwaage für den langen Flug an.",
        "question": "Stelle die Regler für Hafer, Sternenstaub und Elfen-Essenz so ein, dass exakt 75 kg entstehen.\n\nStaub ist doppelt so schwer wie Hafer\nEssenz ist 15 kg leichter als Staub",
        "answer": {"hafer": 18, "staub": 36, "essenz": 21},
        "puzzle_piece": None,
        "hint": "x + 2x + (2x - 15) = 75 => x = 18."
    },
    21: {
        "title": "Tag 21: Der interaktive Routen-Algorithmus ✈️",
        "type": "route_planner",
        "story": "Jetzt geht es um die finale Flug-Effizienz! Der Navigationscomputer der Rentiere berechnet die optimale Route über die Zeitzonen. Nutze den interaktiven Routenplaner.",
        "question": "Ermittle die Differenz (Ersparnis) zwischen der teuersten Route (A->B->C = 270) und dem effizienten Express-Modus (A->C = 240).",
        "answer": 30,
        "puzzle_piece": None,
        "hint": "270 - 240 = 30."
    },
    
    # AKT 4: DAS HARDCORE-FINALE (22-24)
    22: {
        "title": "Tag 22: Das verdeckte Easter-Egg (System-Override) 🕵️‍♂️",
        "type": "text",
        "story": "Das Haupt-Terminal blockiert den Start mit einer Firewall. Der Code von Tag 12 wird verlangt.",
        "question": "Gib den bei Tag 12 gefundenen Override-Token ein.",
        "answer": "OVERRIDE99!",
        "puzzle_piece": None,
        "hint": "Erinnere dich an die Zusatz-Notiz im Speicher von Tag 12."
    },
    23: {
        "title": "Tag 23: Das mechanische Zahnrad-Gleichgewicht ⚙️",
        "type": "gear_ratio_puzzle",
        "story": "Die Hauptschotten verriegeln sich durch ein Vier-Zahnrad-System.",
        "question": "Stelle die Zahnrad-Übersetzung so ein, dass am Hauptausgang exakt 144 Umdrehungen pro Minute (RPM) ankommen (Eingabe = 36).",
        "answer": 4,
        "puzzle_piece": None,
        "hint": "144 / 36 = 4."
    },
    24: {
        "title": "Tag 24: HEILIGABEND – Die Turing-Zustandsmaschine 💻",
        "type": "text",
        "story": "Der Start-Countdown läuft! Die finale Start-KI läuft auf einer virtuellen Turing-Maschine.",
        "question": "Zustandsvektor: $q_0 = 10, q_1 = 11$, multipliziert mit dem Faktor 4. Wie lautet das Ergebnis?",
        "answer": "84",
        "puzzle_piece": "🏆 HARDCORE MEISTER-TITEL: SYSTEM OVERRIDE ERFOLGREICH!",
        "hint": "(10 + 11) * 4 = 84."
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
        "ziege": "left",
        "kohl": "left"
    }

# ==============================================================================
# 4. KOPFZEILE & FORTSCHRITT
# ==============================================================================
st.title("🎄 Weihnachtlicher Rätsel-Adventskalender")
st.caption("Das mathematisch-logische Advents-Abenteuer mit System-Override")

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
    
    if i <= 4:
        prefix = "📦 "
    elif 5 <= i <= 12:
        prefix = "🌀 "
    elif 13 <= i <= 21:
        prefix = "⚙️ "
    else:
        prefix = "🔥 "
        
    label = f"✅ {prefix}Tag {i}" if i in st.session_state.solved_doors else f"{prefix}Tag {i}"
        
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

    st.subheader(door['title'])
    st.info(f"📖 {door['story']}")
    st.markdown(f"**Aufgabe:** {door['question']}")

    # Standard-Text-Eingabe
    if door["type"] == "text":
        ans = st.text_input("Deine Lösung:", key=f"txt_{day}")
        if st.button("Antwort einreichen 🚀", key=f"chk_{day}"):
            if ans.strip().upper() == str(door["answer"]).upper():
                st.success("🎉 Richtig gelöst!")
                if door["puzzle_piece"]:
                    st.markdown(f"<div class='puzzle-card'>{door['puzzle_piece']}</div>", unsafe_allow_html=True)
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Das ist leider nicht korrekt.")
    # TAG 3: RENTIER-EXPERTEN-QUIZ (5 ANSPRUCHSVOLLE FRAGEN)
    elif door["type"] == "reindeer_quiz":
        st.write("🦌 **Das Rentier-Experten-Quiz (Frage für Frage):**")
        
        # Initialisiere den Quiz-Fortschritt im Session State, falls nicht vorhanden
        if "quiz_step" not in st.session_state:
            st.session_state.quiz_step = 1

        step = st.session_state.quiz_step
        st.write(f"**Fortschritt: Frage {step} von 5**")
        
        if step == 1:
            st.markdown("**Frage 1:** Welchen ungewöhnlichen biologischen Farbwechsel vollziehen die Augen von Rentieren im Polarsommer zu Polarninter (Umstellung von Gold zu Blau), um im Dunkeln besser zu sehen?")
            q1_ans = st.text_input("Deine Antwort (Frage 1):", key="q1_input")
            if st.button("Antwort 1 absenden 🚀", key="btn_q1"):
                if "BLAU" in q1_ans.strip().upper():
                    st.success("Richtig! Im Winter wechselt das Tapetum lucidum zu Blau.")
                    st.session_state.quiz_step = 2
                    st.rerun()
                else:
                    st.error("❌ Falsch. Denk an das Spektrum, das bei Nordlicht dominiert.")
                    
        elif step == 2:
            st.markdown("**Frage 2:** Im Gegensatz zu fast allen anderen Hirscharten tragen bei Rentieren *beide* Geschlechter ein Geweih. Welche biologische Besonderheit weisen schwangere Rentierkühe im Winter bezüglich ihres Geweihs auf (im Vergleich zu den Männchen)?")
            q2_ans = st.text_input("Deine Antwort (Frage 2):", key="q2_input")
            if st.button("Antwort 2 absenden 🚀", key="btn_q2"):
                # Mütter behalten ihr Geweih im Winter (Bullen werfen es früher ab)
                if any(w in q2_ans.strip().upper() for w in ["BEHALTEN", "TRAGEN", "SPÄTER", "WEIHNACHTEN"]):
                    st.success("Richtig! Kühe behalten ihr Geweih über den Winter, um Ressourcen zu verteidigen.")
                    st.session_state.quiz_step = 3
                    st.rerun()
                else:
                    st.error("❌ Falsch. Überlege, wer im Winter die Führung der Herde übernimmt.")
                    
        elif step == 3:
            st.markdown("**Frage 3:** Wie lautet der wissenschaftliche (biologische) Artname des Rentiers auf Latein?")
            q3_ans = st.text_input("Deine Antwort (Frage 3):", key="q3_input")
            if st.button("Antwort 3 absenden 🚀", key="btn_q3"):
                if "RANGIFER TARANDUS" in q3_ans.strip().upper() or "TARANDUS" in q3_ans.strip().upper():
                    st.success("Hervorragend! *Rangifer tarandus* ist korrekt.")
                    st.session_state.quiz_step = 4
                    st.rerun()
                else:
                    st.error("❌ Falsch. Gesucht ist der zoologische Doppelname.")
                    
        elif step == 4:
            st.markdown("**Frage 4:** In welchem Jahr wurden die berühmten fliegenden Rentiere des Weihnachtsmanns (angeführt von Rudolph) erstmals namentlich in dem klassischen Gedicht *'A Visit from St. Nicholas'* (Clement Clarke Moore) erwähnt?")
            q4_ans = st.text_input("Deine Antwort (Frage 4):", key="q4_input")
            if st.button("Antwort 4 absenden 🚀", key="btn_q4"):
                if "1823" in q4_ans.strip():
                    st.success("Punktlandung! Das Jahr 1823 ist absolut korrekt.")
                    st.session_state.quiz_step = 5
                    st.rerun()
                else:
                    st.error("❌ Falsch. Es stammt aus dem frühen 19. Jahrhundert (ca. 182x).")
                    
        elif step == 5:
            st.markdown("**Frage 5:** Wie viele Rentiere zogen laut dem ursprünglichen Originalgedicht von 1823 den Schlitten (ohne Rudolph, der erst später dazukam)?")
            q5_ans = st.text_input("Deine Antwort (Frage 5):", key="q5_input")
            if st.button("Finale Antwort absenden 🚀", key="btn_q5"):
                if "8" in q5_ans.strip() or "ACHT" in q5_ans.strip().upper():
                    st.success("🎉 Unglaublich! Ihr habt alle 5 Expertenfragen bravourös gemeistert. Die Rentiere neigen anerkennend ihre Köpfe und der Schlitten ist bereit!")
                    st.session_state.quiz_step = 1  # Reset für eventuelles Neustarten
                    if day not in st.session_state.solved_doors:
                        st.session_state.solved_doors.append(day)
                        st.rerun()
                else:
                    st.error("❌ Falsch. Zähle die ursprünglichen Rentiere ohne den rotnasigen Nachzügler.")
    # TAG 6: SUDOKU (INTERAKTIV)
    # TAG 6: DAS MAGISCHE SUDOKU
    elif door["type"] == "sudoku_puzzle":
        st.markdown("🧊 **Die Eistafel der Zahlenmagie:**")
        st.write("Hier ist das magische 4x4-Sudoku. Füllt die leer gelassenen Felder (?) so aus, dass die Regeln erfüllt sind:")
        
        # Visuelle Darstellung als hübsche Markdown-Tabelle / Raster
        st.markdown("""
        | Zeile | Spalte 1 | Spalte 2 | Spalte 3 | Spalte 4 |
        | :---: | :---: | :---: | :---: | :---: |
        | **1** | **1**    | *[ ? ]*  | 3        | 4        |
        | **2** | 3        | 4        | *[ ? ]*  | 2        |
        | **3** | *[ ? ]*  | 2        | 1        | 3        |
        | **4** | 4        | 1        | 2        | *[ ? ]*  |
        """)
        
        st.info("💡 **Vorgabe:** Gegeben ist dieses 4x4-Sudoku. Ihr müsst die 4 fehlenden Werte (von oben nach unten / von links nach rechts) eingeben.")
        
        # Eingabefelder für die 4 fehlenden Zahlen der Reihe nach
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            val1 = st.text_input("Feld 1 (Z1, S2)", max_chars=1, key="sudoku_1")
        with col2:
            val2 = st.text_input("Feld 2 (Z2, S3)", max_chars=1, key="sudoku_2")
        with col3:
            val3 = st.text_input("Feld 3 (Z3, S1)", max_chars=1, key="sudoku_3")
        with col4:
            val4 = st.text_input("Feld 4 (Z4, S4)", max_chars=1, key="sudoku_4")
            
        if st.button("Sudoku-Lösung überprüfen ❄️", key="btn_sudoku"):
            # Korrekte Lösung für dieses Beispiel-Sudoku: 
            # Z1S2=2, Z2S3=1, Z3S1=4, Z4S4=3
            if val1.strip() == "2" and val2.strip() == "1" and val3.strip() == "4" and val4.strip() == "3":
                st.success("✨ Richtig! Die Eistafel knackt auf und enthüllt das **2. magische Fragment (R)**!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Das magische Raster glimmt kurz rot auf. Die Zahlenkombination ist noch nicht stimmig. Prüfe noch einmal Zeilen, Spalten und Blöcke!")

    # TAG 7: DIE EISIGE SCHLUCHT (SCHNITZELWEG)
    elif door["type"] == "canyon_puzzle":
        st.markdown("🌉 **Die Auswahl des Schnitzelwegs vor der Schlucht:**")
        st.write("Schaut euch die Hinweise an der Felswand an und entscheidet, welchen Weg ihr wählt:")
        
        st.markdown("""
        - ❄️ **Weg A:** Der eisige Kristallpfad (Gefahr von Einbrüchen laut Notizen)
        - 💨 **Weg B:** Der Windschatten-Pfad (Stabiles Holz, aber keinerlei Markierungen)
        - 🌲 **Weg C:** Der Moos-Markierte-Pfad (Sichere alte Markierungen und Spuren der Vorgänger)
        """)
        
        canyon_choice = st.radio("Welchen Weg wählt ihr?", ["Bitte wählen...", "Weg A", "Weg B", "Weg C"], key="canyon_radio")
        
        if st.button("Weg wählen & Brücke überqueren 🌁", key="btn_canyon"):
            if canyon_choice == "Weg C":
                st.success("🎉 Genial! Ihr folgt den alten Markierungen des Schnitzelwegs und überquert die Schlucht sicher. Als Belohnung findet ihr am anderen Ende das **3. Fragment (N)**!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            elif canyon_choice == "Bitte wählen...":
                st.warning("⚠️ Bitte trefft eine Auswahl.")
            else:
                st.error("❌ Das war der falsche Weg! Das Eis knirscht bedrohlich oder ihr verliert die Spur. Versucht es noch einmal.")

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
                st.markdown(f"<div class='puzzle-card'>{door['puzzle_piece']}</div>", unsafe_allow_html=True)
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsches Signal.")

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
            st.success("🟢 Korrekt ausgerichtet!")
            st.markdown(f"<div class='puzzle-card'>{door['puzzle_piece']}</div>", unsafe_allow_html=True)
            if st.button("Aktivieren 🔦", key=f"chk_{day}"):
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()

    # TAG 10: TRANSPORT-RÄTSEL (WOLF, ZIEGE, KOHL)
    elif door["type"] == "river_crossing":
        st.write("🐺🐐🥬 **Fluss-Transport-Steuerung (Wolf, Ziege, Kohl):**")
        r = st.session_state.river
        st.write(f"📍 **Linkes Ufer:** {[k for k, v in r.items() if v == 'left' and k != 'boat']}")
        st.write(f"🛶 **Boot Position:** Ufer {r['boat'].upper()}")
        st.write(f"📍 **Rechtes Ufer:** {[k for k, v in r.items() if v == 'right' and k != 'boat']}")
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            item_to_move = st.selectbox("Passagier mitnehmen:", ["Niemand (leer fahren)", "wolf", "ziege", "kohl"], key="river_item")
        with col_act2:
            if st.button("Ufer wechseln 🛶", key="river_move"):
                target = "right" if r["boat"] == "left" else "left"
                r["boat"] = target
                if item_to_move != "Niemand (leer fahren)":
                    r[item_to_move] = target
                if r["wolf"] == r["ziege"] and r["boat"] != r["wolf"]:
                    st.error("💀 Der Wolf hat die Ziege gefressen! Zurückgesetzt.")
                    st.session_state.river = {"boat": "left", "wolf": "left", "ziege": "left", "kohl": "left"}
                elif r["ziege"] == r["kohl"] and r["boat"] != r["ziege"]:
                    st.error("💀 Die Ziege hat den Kohlkopf gefressen! Zurückgesetzt.")
                    st.session_state.river = {"boat": "left", "wolf": "left", "ziege": "left", "kohl": "left"}
                st.rerun()
        if st.button("Zurücksetzen 🔄", key="river_reset"):
            st.session_state.river = {"boat": "left", "wolf": "left", "ziege": "left", "kohl": "left"}
            st.rerun()
        if r["wolf"] == "right" and r["ziege"] == "right" and r["kohl"] == "right":
            st.success("🎉 Alle sicher drüben!")
            st.markdown(f"<div class='puzzle-card'>{door['puzzle_piece']}</div>", unsafe_allow_html=True)
            if day not in st.session_state.solved_doors:
                st.session_state.solved_doors.append(day)
                st.rerun()

    # TAG 13: TRI-VENTIL-GLEICHUNGSSYSTEM
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
                st.success("🎉 Hervorragend! Das Gleichungssystem ist perfekt gelöst.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Die Bedingungen des Gleichungssystems sind noch nicht erfüllt.")

    # TAG 14: INTERAKTIVES PAKET-LEITSYSTEM
    elif door["type"] == "package_sort":
        st.write("📦 **Interaktives Paket-Leitsystem (Rutschen 1-4 zuweisen):**")
        p_alpha = st.selectbox("Paket Alpha", [1, 2, 3, 4], index=0, key="pa")
        p_beta = st.selectbox("Paket Beta", [1, 2, 3, 4], index=1, key="pb")
        p_gamma = st.selectbox("Paket Gamma", [1, 2, 3, 4], index=0, key="pg")
        p_delta = st.selectbox("Paket Delta", [1, 2, 3, 4], index=3, key="pd")
        
        if st.button("Rutschen-Konfiguration prüfen 📦", key=f"chk_{day}"):
            if p_alpha == 3 and p_beta == 2 and p_gamma == 1 and p_delta == 4:
                st.success("🎉 Perfekt! Alle Axiome und Paket-Regeln wurden fehlerfrei erfüllt.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Die Rutschen-Belegung widerspricht den logischen Axiomen.")

    # TAG 15: WUNSCHZETTEL-MASCHINE (INTERAKTIV)
    elif door["type"] == "wish_machine":
        st.write("📜 **Interaktives Wunschzettel-Rechenmodul:**")
        w_input = st.number_input("Nächsten Wert in der Reihe ermitteln:", min_value=0, max_value=500, value=0, key="wish_num")
        if st.button("Wunschzettel-Reihe berechnen 📜", key=f"chk_{day}"):
            if w_input == 159:
                st.success("🎉 Richtig! Das Muster (Multiplikation mit 2 und Addition von 1) wurde erfolgreich berechnet.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falscher Wert.")

    # TAG 16: STARKSTROM-RELAY NETZWERK
    elif door["type"] == "binary_switches":
        st.write("⚡ **Notfall-Keller SPS-Schaltpult (Zielzahl: 48):**")
        b1, b2, b3, b4, b5, b6 = st.columns(6)
        s1 = b1.checkbox("32", key="cb1")
        s2 = b2.checkbox("16", key="cb2")
        s3 = b3.checkbox("8", key="cb3")
        s4 = b4.checkbox("4", key="cb4")
        s5 = b5.checkbox("2", key="cb5")
        s6 = b6.checkbox("1", key="cb6")
        
        curr_val = (32 if s1 else 0) + (16 if s2 else 0) + (8 if s3 else 0) + (4 if s4 else 0) + (2 if s5 else 0) + (1 if s6 else 0)
        st.metric("Aktueller Relais-Wert", f"{curr_val}", delta=f"Ziel: 48")
        
        if st.button("SPS-Schaltkreis zünden ⚡", key=f"chk_{day}"):
            if curr_val == 48:
                st.success("🎉 Relais-Konfiguration exakt bestätigt!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error(f"❌ Wert inkorrekt ({curr_val}). Benötigt: 48.")

    # TAG 17: FREQUENZ-REGLER
    elif door["type"] == "frequency_tuner":
        st.write("📻 **Interaktiver Radio-Notkanal Resonanz-Tuner:**")
        fa = st.slider("Frequenz-Regler (MHz)", 50.0, 150.0, 70.0, step=0.5, key="fa_slide")
        st.markdown(f"**Aktuell eingestellt:** `{fa} MHz`")
        
        if st.button("Frequenz synchronisieren 📡", key=f"chk_{day}"):
            if abs(fa - 89.0) < 0.1:
                st.success("🎉 Resonanzpunkt perfekt getroffen! Der Notkanal steht klar im Äther.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Das Signal ist noch verrauscht.")

    # TAG 18: HANGAR-SCHLOSS
    elif door["type"] == "hangar_puzzle":
        st.write("🔐 **Interaktives Hangar-Zahlenwahl-Schloss:**")
        hangar_code = st.slider("Wähle die zweistellige Kombination", 10, 99, 10, key="hangar_slider")
        st.markdown(f"**Aktuell gewählt:** `{hangar_code}`")
        if st.button("Schloss entriegeln 🔐", key=f"chk_{day}"):
            if hangar_code == 57:
                st.success("🎉 Korrekt! Das Hangar-Tor schwingt auf.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Das Schloss bleibt verschlossen.")

    # TAG 19: RENTIER-AUFSTELLUNGS-RASTER
    elif door["type"] == "reindeer_puzzle":
        st.write("🦌 **Rentier-Aufstellungs-Raster (3 Reihen à 2 Plätze):**")
        ans_count = st.text_input("Wie viele valide Kombinationsmöglichkeiten gibt es insgesamt?", key="reindeer_count_ans")
        
        if st.button("Aufstellung verifizieren 🦌", key=f"chk_{day}"):
            if ans_count.strip() == "12":
                st.success("🎉 Perfekt! 12 valide Permutationen exakt errechnet.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsche Anzahl an Kombinationen.")

    # TAG 20: ALCHEMISTISCHE WAAGE (Sauberes Layout ohne Klammern)
    elif door["type"] == "scale_puzzle":
        st.write("⚖️ **Sternenstaub-Waage (Einheitliches Mischsystem):**")
        st.markdown("Stelle die Regler so ein, dass exakt 75 kg erreicht werden:")
        w_hafer = st.slider("Hafer (kg)", 0, 50, 10, key="w_h")
        w_staub = st.slider("Sternenstaub (kg)", 0, 50, 10, key="w_s")
        w_essenz = st.slider("Elfen-Essenz (kg)", 0, 50, 10, key="w_e")
        
        total_weight = w_hafer + w_staub + w_essenz
        st.write(f"Gesamtgewicht: **{total_weight} kg** (Ziel: 75 kg)")
        
        if st.button("Waage ausbalancieren ⚖️", key=f"chk_{day}"):
            if w_hafer == 18 and w_staub == 36 and w_essenz == 21 and total_weight == 75:
                st.success("🎉 Die Waage ist perfekt im Gleichgewicht!")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Die Gewichte stimmen nicht mit den Alchemie-Regeln überein.")

    # TAG 21: ROUTEN-PLANER (INTERAKTIV)
    elif door["type"] == "route_planner":
        st.write("✈️ **Interaktiver Routen-Differenz-Rechner:**")
        r_val = st.number_input("Ersparnis-Wert eingeben:", min_value=0, max_value=500, value=0, key="route_num")
        if st.button("Routen-Effizienz bestätigen ✈️", key=f"chk_{day}"):
            if r_val == 30:
                st.success("🎉 Korrekt! Die optimale Flug-Effizienz ist berechnet.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falscher Wert.")

    # TAG 23: ZAHNRAD-ÜBERSETZUNG
    elif door["type"] == "gear_ratio_puzzle":
        st.write("⚙️ **Zahnrad-Übersetzung:**")
        factor = st.slider("Übersetzungsfaktor", 1, 10, 1, key="gear_slider")
        rpm_out = 36 * factor
        st.write(f"Eingabe: 36 RPM × Faktor {factor} = **{rpm_out} RPM** (Ziel: 144 RPM)")
        
        if st.button("Zahnräder einkuppeln ⚙️", key=f"chk_{day}"):
            if factor == 4:
                st.success("🎉 Perfekte Übersetzung! Die Schotten öffnen sich.")
                if day not in st.session_state.solved_doors:
                    st.session_state.solved_doors.append(day)
                    st.rerun()
            else:
                st.error("❌ Falsche Drehzahl.")

# Optionale Anzeige der Fragmente / Hinweise in der Seitenleiste (Tage 5-12)
if show_sidebar:
    with puzzle_col:
        st.markdown("### 🧩 Deine Fragmente")
        st.markdown("Sammle alle Hinweise aus den Toren 5 bis 12:")
        for d_num in range(5, 13):
            if d_num in st.session_state.solved_doors:
                st.success(f"{DOORS[d_num]['puzzle_piece']}")
            else:
                st.info(f"Tag {d_num}: *Noch gesperrt*")
