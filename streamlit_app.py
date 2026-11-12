import json
import random
import string
import re
import unicodedata
from datetime import date
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Der Nordpol-Fall", page_icon="🎄", layout="wide")

SAVE = Path("spielstand.json")          # gemeinsamer Spielstand (auf dem Server)
TEST = st.query_params.get("test") == "1"   # App-URL + ?test=1 -> alle Türchen offen
YEAR = 2026

st.markdown("""
<style>
.stApp {background:#0b2d1d;color:#f4f6f5}
h1,h2,h3,h4 {color:#ffd700 !important}
.stButton>button, .stFormSubmitButton>button {background:#4a0e17 !important;color:#ffd700 !important;
  border:2px solid #ffd700 !important;border-radius:8px;font-weight:bold}
.stButton>button:disabled {opacity:.35}
div.stAlert {background:#4a0e17 !important;border:1px solid #ffd700 !important}
div.stAlert p, div.stAlert span, div.stAlert div {color:#fff8dc !important}
.stTextInput input {background:#2e080e !important;color:#fff !important;border:1px solid #ffd700 !important}
.stCode, pre {background:#1a0509 !important;color:#ffe9a8 !important}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------- Spielstand
def load():
    try:
        return json.loads(SAVE.read_text())
    except Exception:
        return {"solved": [], "akte": {}}


def save():
    try:
        SAVE.write_text(json.dumps(st.session_state.game, ensure_ascii=False))
    except Exception:
        pass


if "game" not in st.session_state:
    st.session_state.game = load()
game = st.session_state.game


def norm(s: str) -> str:
    s = s.upper().replace("Ä", "AE").replace("Ö", "OE").replace("Ü", "UE").replace("ß", "SS").replace("ẞ", "SS")
    s = unicodedata.normalize("NFKD", s)
    return re.sub(r"[^A-Z0-9]", "", s)


def vigenere(text: str, key: str, sign: int = 1) -> str:
    out, i = [], 0
    for ch in text:
        if "A" <= ch <= "Z":
            out.append(chr((ord(ch) - 65 + sign * (ord(key[i % len(key)]) - 65)) % 26 + 65))
            i += 1
        else:
            out.append(ch)
    return "".join(out)


def solve(day: int):
    if day not in game["solved"]:
        game["solved"].append(day)
        game["akte"][str(day)] = DOORS[day]["akte"]
        save()
        st.session_state.celebrate = True
    st.rerun()


def hints(day: int, texts: list):
    key = f"h{day}"
    n = st.session_state.setdefault(key, 0)
    for i, t in enumerate(texts[:n], 1):
        st.markdown(f"💡 **Hinweis {i}:** {t}")
    if n < len(texts) and st.button(f"Hinweis {n + 1} von {len(texts)} anzeigen", key=f"hb{day}"):
        st.session_state[key] += 1
        st.rerun()


def text_door(day: int, check, label="Eure Lösung"):
    with st.form(f"f{day}"):
        a = st.text_input(label)
        if st.form_submit_button("Prüfen 🔍"):
            if check(a):
                solve(day)
            else:
                st.error("Das passt noch nicht.")


# ---------------------------------------------------------------- Türchen
def door1(day):
    st.code(
        "Seitlich ins Holz geritzt:\n\n"
        "  Vier Wörter, jedes kürzer als zehn Buchstaben.\n\n"
        "  I.   Mein Licht ist keine Lampe, mein Rot kein Lack.\n"
        "       Ich führe an, obwohl ich erst später dazukam.\n"
        "  II.  Um mich herum ist überall Süden.\n"
        "  III. Ein Stern, den man essen kann. Zimt ist mein Geheimnis.\n"
        "  IV.  Kein Anfang, kein Ende, ich hänge an der Tür.\n"
        "       Im Dezember trage ich vier Lichter nacheinander.\n\n"
        "  Das Schloss ist ordentlich: Es liest die Wörter, wie sie im\n"
        "  Lexikon stehen, nicht wie sie hier stehen. Ziffer = Länge.",
        language=None)
    text_door(day, lambda a: norm(a) == "5769", "Vierstelliger Code")


PLAIN = "HELFT UNS! JEMAND SABOTIERT DIE WERKSTATT. SPRECHT DREIMAL DAS WORT LATERNE."


def door2(day):
    cipher = vigenere(PLAIN, "NORDPOL")
    st.markdown(
        "<div style='background:#e9d8a6;color:#3b2a14;padding:18px;border-radius:6px;text-align:center;"
        "font-family:Georgia,serif;border:3px double #8a6d3b'>"
        "<div style='font-size:2rem'>🌿 ⚜ 🌿</div>"
        f"<div style='font-family:monospace;font-size:1.25rem;letter-spacing:2px;white-space:pre-wrap;margin-top:8px'>{cipher}</div>"
        "</div>", unsafe_allow_html=True)
    st.write("")
    text_door(day, lambda a: norm(a) == "LATERNE", "Das Wort, das ihr sprechen sollt")


def door3(day):
    qs = [
        ("Es ist Weihnachten. Welche Rentiere tragen jetzt noch Geweih?",
         ["Alle, es fällt erst im Frühjahr ab", "Nur die Männchen",
          "Vor allem die Weibchen, die Bullen werfen nach der Brunft ab"], 2),
        ("Wie heißen wilde Rentiere in Nordamerika?", ["Wapiti", "Karibu", "Elch"], 1),
        ("Was passiert im Winter mit den Rentieraugen?",
         ["Sie werden rot", "Sie schließen sich zur Winterruhe",
          "Die Reflexionsschicht färbt sich von gold zu blau"], 2),
    ]
    with st.form("f3"):
        picks = [st.radio(q, o, index=None, key=f"q3_{i}") for i, (q, o, _) in enumerate(qs)]
        if st.form_submit_button("Antworten 🦌"):
            if all(p is not None and o.index(p) == c for p, (_, o, c) in zip(picks, qs)):
                solve(day)
            else:
                st.error("Die Rentiere schnauben: Mindestens eine Antwort stimmt nicht.")


def door4(day):
    st.code(
        "BORDCOMPUTER: Passwort akzeptiert. Kurs unbekannt.\n"
        "Navigation nur nach Sternen. Planquadrate (x|y):\n\n"
        "  Alkaid (22|7)  Mizar (18|9)  Alioth (14|8)\n"
        "  Megrez (10|7)  Phecda (8|3)\n"
        "  Dubhe  (4|7)   Merak  (2|3)\n\n"
        "Zielstern: der Polarstern. Er ist nicht in der Karte.\n"
        "Eingabe: Planquadrat des Zielsterns (x y)", language=None)
    text_door(day, lambda a: re.findall(r"\d+", a) == ["14", "27"], "Planquadrat")


MAZE = [
    "#########",
    "#S..#...#",
    "#.#.#.#.#",
    "#.#...#.#",
    "#.#####.#",
    "#...#...#",
    "###.#.###",
    "#...#..E#",
    "#########",
]


def _move(dr, dc):
    r, c = st.session_state.maze_pos
    if MAZE[r + dr][c + dc] != "#":
        st.session_state.maze_pos = (r + dr, c + dc)
        st.session_state.maze_trail.add((r + dr, c + dc))


def door5(day):
    if not st.session_state.get("fog_done"):
        st.code(
            "Der Kompass dreht durch und zeigt WESTEN.\n"
            "Blitz ruft Kommandos in den Nebel:\n\n"
            "  Rechts 90! Links 45! Rechts 180! Links 135! Rechts 45!\n\n"
            "(Rechts = im Uhrzeigersinn, Start = Westen)", language=None)
        with st.form("f5"):
            a = st.text_input("In welche Himmelsrichtung fliegt ihr danach?")
            if st.form_submit_button("Kurs halten 🧭"):
                if norm(a) in {"NORDOST", "NORDOSTEN", "NO"}:
                    st.session_state.fog_done = True
                    st.rerun()
                else:
                    st.error("Der Nebel wird dichter. Das war nicht der Kurs.")
        return
    st.markdown("*Der Nebel reißt auf. Ihr landet vor einem Labyrinth aus Eis, doch zwischen den Blöcken "
                "hängt noch Nebel, ihr seht nur ein Feld weit.*")
    pos = st.session_state.setdefault("maze_pos", (1, 1))
    trail = st.session_state.setdefault("maze_trail", {(1, 1)})
    r, c = pos
    rows = []
    for i, row in enumerate(MAZE):
        line = ""
        for j, ch in enumerate(row):
            if (i, j) == pos:
                line += "@ "
            elif abs(i - r) <= 1 and abs(j - c) <= 1:
                line += "▓▓" if ch == "#" else ("E " if ch == "E" else ". ")
            elif (i, j) in trail:
                line += "+ "
            else:
                line += "░░"
        rows.append(line)
    st.code("\n".join(rows), language=None)
    st.caption("@ ihr · + euer Weg · ░ Nebel. Ihr seht nur das direkte Umfeld.")
    _, m, _ = st.columns([1, 1, 1])
    m.button("⬆️", key="mu", on_click=_move, args=(-1, 0), use_container_width=True)
    a, b, c3 = st.columns(3)
    a.button("⬅️", key="ml", on_click=_move, args=(0, -1), use_container_width=True)
    b.button("⬇️", key="md", on_click=_move, args=(1, 0), use_container_width=True)
    c3.button("➡️", key="mr", on_click=_move, args=(0, 1), use_container_width=True)
    if st.button("Zurück zum Start", key="mreset"):
        st.session_state.maze_pos = (1, 1)
        st.session_state.maze_trail = {(1, 1)}
        st.rerun()
    nr, nc = st.session_state.maze_pos
    if MAZE[nr][nc] == "E":
        solve(day)


def txt(body, check, label="Eure Lösung"):
    def f(day):
        st.code(body, language=None)
        text_door(day, check, label)
    return f


def eq(*opts):
    return lambda a: norm(a) in opts


def nums(*n):
    return lambda a: re.findall(r"\d+", a) == list(n)


def pad(k, fn):
    _, m, _ = st.columns(3)
    m.button("⬆️", key=k + "u", on_click=fn, args=(-1, 0), use_container_width=True)
    a, b, c = st.columns(3)
    a.button("⬅️", key=k + "l", on_click=fn, args=(0, -1), use_container_width=True)
    b.button("⬇️", key=k + "d", on_click=fn, args=(1, 0), use_container_width=True)
    c.button("➡️", key=k + "r", on_click=fn, args=(0, 1), use_container_width=True)


# ---- 6: Eisrutsch
ICE = ['#######', '#S..#.#', '#.#...#', '#..#..#', '#.#..##', '#..#.E#', '#######']


def _slide(dr, dc):
    r, c = st.session_state.ice_pos
    while ICE[r + dr][c + dc] != "#":
        r, c = r + dr, c + dc
        if ICE[r][c] == "E":
            break
    st.session_state.ice_pos = (r, c)
    st.session_state.ice_moves += 1


def door6(day):
    pos = st.session_state.setdefault("ice_pos", (1, 1))
    st.session_state.setdefault("ice_moves", 0)
    sym = {"#": "▓", ".": "·", "S": "S", "E": "E"}
    st.code("\n".join("".join("@" if (i, j) == pos else sym[ch] for j, ch in enumerate(row))
                      for i, row in enumerate(ICE)), language=None)
    st.caption(f"Ihr rutscht, bis ihr gegen ein ▓ stoßt (oder E erreicht). Züge: {st.session_state.ice_moves}")
    pad("ice", _slide)
    if st.button("Zurück zum Start", key="ice_reset"):
        st.session_state.ice_pos, st.session_state.ice_moves = (1, 1), 0
        st.rerun()
    if ICE[pos[0]][pos[1]] == "E":
        solve(day)


# ---- 7: Nim
def _nim(k):
    s = st.session_state
    s.nim -= k
    if s.nim == 0:
        s.nim_state = "win"
        return
    g = s.nim % 4 or random.randint(1, min(3, s.nim))
    s.nim -= g
    s.nim_log = f"Der Frostgeist nimmt {g}."
    if s.nim == 0:
        s.nim_state = "lose"


def door7(day):
    s = st.session_state
    s.setdefault("nim", 21)
    s.setdefault("nim_state", "play")
    s.setdefault("nim_log", "")
    if s.nim_state == "win":
        solve(day)
    st.markdown(f"### {s.nim} Eiszapfen übrig")
    st.write("🧊" * s.nim)
    if s.nim_state == "lose":
        st.error("Der Frostgeist hat den letzten Eiszapfen genommen. Er lacht und baut sie neu auf.")
        if st.button("Neu beginnen", key="nim_new"):
            s.nim, s.nim_state, s.nim_log = 21, "play", ""
            st.rerun()
        return
    st.caption(s.nim_log or "Ihr beginnt.")
    cols = st.columns(3)
    for k in (1, 2, 3):
        cols[k - 1].button(f"{k} nehmen", key=f"nim{k}", on_click=_nim, args=(k,),
                           disabled=k > s.nim, use_container_width=True)


# ---- 9: Morse
MORSE = dict(zip(string.ascii_uppercase, ".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..".split()))


def door9(day):
    msg = "GENERATOR AUS KOMMT SCHNELL"
    st.code("  /  ".join(" ".join(MORSE[ch] for ch in w) for w in msg.split()), language=None)
    text_door(day, eq("GENERATOR"), "Welches Gerät ist ausgefallen?")


# ---- 10: Spiegel
MIRR = ["..\\.\\.", "\\/.\\..", "././.\\", ".\\../.", "\\/....", "..\\..\\"]


def _trace():
    r, c, d = 2, 0, (0, 1)
    while 0 <= r < 6 and 0 <= c < 6:
        m = MIRR[r][c]
        if m == "/":
            d = (-d[1], -d[0])
        elif m == "\\":
            d = (d[1], d[0])
        r, c = r + d[0], c + d[1]
    side = "OBEN" if r < 0 else "UNTEN" if r > 5 else "LINKS" if c < 0 else "RECHTS"
    return side + str((c if side in ("OBEN", "UNTEN") else r) + 1)


def door10(day):
    lines = ["    1 2 3 4 5 6"]
    for i, row in enumerate(MIRR):
        lines.append(("▶ " if i == 2 else "  ") + f"{i + 1} " + " ".join(row))
    st.code("\n".join(lines), language=None)
    st.caption("Der Laser tritt bei ▶ (Zeile 3) von links ein. Spiegel: / und \\")
    text_door(day, lambda a: norm(a) == _trace(),
              "Kante und Nummer, wo er austritt (z. B. LINKS 5)")


# ---- 13: Generator (Lights Out)
def _lo(i):
    b = st.session_state.lo
    r, c = divmod(i, 3)
    for dr, dc in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
        if 0 <= r + dr < 3 and 0 <= c + dc < 3:
            b[(r + dr) * 3 + c + dc] ^= 1


def door13(day):
    if "lo" not in st.session_state:
        st.session_state.lo = [1] * 9
        for i in (0, 5, 7):
            _lo(i)
    b = st.session_state.lo
    for r in range(3):
        cols = st.columns(3)
        for c in range(3):
            cols[c].button("💡" if b[r * 3 + c] else "⚫", key=f"lo{r}{c}", on_click=_lo,
                           args=(r * 3 + c,), use_container_width=True)
    st.caption("Jeder Schalter dreht sich selbst und seine Nachbarn (oben, unten, links, rechts) um. Ziel: alle 9 leuchten.")
    if all(b):
        solve(day)


# ---- 24: Finale
FIN = "DANKE FUER EURE HILFE. FUSSEL WOLLTE NUR EINMAL MITFLIEGEN. HEUTE NACHT SITZT ER AUF PLATZ 59. FROHE WEIHNACHTEN"


PLAN = ["BBBMMM", "BBPMMM", "KKPPGG", "KKPSGG", "KSSSSG", "KKSSSG"]
ROOMS = {"B": ("Büro", "#e8c9c9"), "M": ("Masch.", "#c9d6e8"), "P": ("Pack.", "#efe6c4"),
         "K": ("Backstube", "#f2d4b0"), "G": ("Generator", "#d9c9ea"), "S": ("Stall", "#c9e8d1")}
SOLUTION = {"Holly": "1B", "Schraub": "2E", "Volt": "3C", "Fussel": "4F", "Zimta": "5A", "Gustav": "6D"}


def plan_html():
    th = "color:#ffd700;padding:4px 10px"
    h = "<table style='border-collapse:collapse;margin:8px auto'><tr><td></td>"
    h += "".join(f"<th style='{th}'>{c}</th>" for c in "ABCDEF") + "</tr>"
    for r, row in enumerate(PLAN):
        h += f"<tr><th style='{th}'>{r + 1}</th>"
        for k in row:
            name, col = ROOMS[k]
            h += (f"<td style='background:{col};color:#444;border:1px solid #0b2d1d;width:78px;height:40px;"
                  f"text-align:center;font-size:.7rem'>{name}</td>")
        h += "</tr>"
    return h + "</table>"


def door24(day):
    s = st.session_state
    if not s.get("fin"):
        st.markdown("**Murdoku:** Setzt die sechs Elfen mit Hilfe der Akte auf den Grundriss der Werkstatt. "
                    "In jeder Zeile und jeder Spalte steht genau ein Elf. Wer allein im Generatorraum stand, war der Täter.")
        st.markdown(plan_html(), unsafe_allow_html=True)
        cells = ["–"] + [f"{r}{c}" for r in range(1, 7) for c in "ABCDEF"]
        with st.form("f24a"):
            cols = st.columns(3)
            pick = {n: cols[i % 3].selectbox(n, cells, key=f"mu_{n}") for i, n in enumerate(SOLUTION)}
            who = st.selectbox("Wer war allein im Generatorraum?", ["–"] + list(SOLUTION), key="mu_who")
            if st.form_submit_button("Anklagen ⚖️"):
                if not all(pick[n] == SOLUTION[n] for n in SOLUTION):
                    st.error("Mindestens ein Elf steht an der falschen Stelle. Prüft die Aussagen und die Raumfarben.")
                elif who != "Fussel":
                    st.error("Die Plätze stimmen. Aber wer stand allein im Generatorraum?")
                else:
                    s.fin = True
                    st.rerun()
        return
    st.markdown("Der Täter steht vor euch und senkt den Kopf. Da reicht der Weihnachtsmann euch einen Zettel: "
                "*Ich habe meine Botschaft mit dem Namen des Täters verschlüsselt.*")
    st.code(vigenere(FIN, "FUSSEL"), language=None)
    text_door(day, eq("WEIHNACHTEN"), "Das letzte Wort der Nachricht")


def D(title, story, render, akte, after, *hints):
    return dict(title=title, story=story, render=render, akte=akte, after=after, hints=list(hints))


DUTY = ("Dienstplan 22:47: Holly, Schraub, Volt, Zimta, Fussel und Gustav standen auf dem Grundriss der Werkstatt "
        "(6 Zeilen, Spalten A bis F, Räume farbig). In jeder Zeile und in jeder Spalte stand genau ein Elf.")

DOORS = {
    1: dict(title="Türchen 1: Die Kiste vom Nordpol",
            story="Es klingelt an der Haustür. Ihr öffnet, aber niemand steht davor. Stattdessen liegt ein schweres, "
                  "eisiges Päckchen vor der Tür mit dem Absender Nordpol. Im Wohnzimmer öffnet ihr es, und eine "
                  "Holzbox mit Zahlenschloss kommt zum Vorschein. Ihr untersucht die Box: Seitlich ist eine Gravur eingeritzt.",
            render=door1, akte="Absender der Kiste: NORDPOL. Kistencode: 5769.",
            after="Das Schloss klackt. Die Kiste springt auf, Kälte strömt heraus. Obenauf liegt ein Brief.",
            hints=["Jede Zeile ergibt ein Wort. Die Ziffer ist seine Länge.",
                   "Rudolf, Nordpol, Zimtstern, Kranz. Und nun in alphabetische Reihenfolge bringen."]),
    2: dict(title="Türchen 2: Der Brief",
            story="Die Kiste springt auf, und darin liegt ein Brief. Aber ihr könnt ihn nicht lesen, denn er ist verschlüsselt.",
            render=door2, sound="glocken.mp3", akte="Hilferuf des Weihnachtsmanns: Jemand sabotiert die Werkstatt. Passwort für die Rentiere: LATERNE.",
            after="Ihr sprecht dreimal LATERNE. Zuerst passiert nichts. Dann hört ihr von weit her Glocken, die immer näher kommen. "
                  "Ihr schaut aus dem Fenster: Rentiere! Und sie reden mit euch.",
            hints=["Der Lorbeerkranz erinnert an einen römischen Feldherrn, der für eine Geheimschrift bekannt ist.",
                   "Die Verschiebung bleibt nicht gleich, sie wechselt nach einem Schlüsselwort (Vigenère).",
                   "Das Schlüsselwort steht auf dem Paket: der Absender. Es wird immer wiederholt."]),
    3: dict(title="Türchen 3: Die Rentier-Prüfung",
            story="Vor dem Fenster landet der Schlitten. Die Rentiere sprechen erst mit euch, wenn ihr bewiesen habt, "
                  "dass ihr euch wirklich mit ihnen auskennt.",
            render=door3, akte="Die Zugtiere sind Kühe (Weibchen). Nur sie haben zu Weihnachten noch Geweih.",
            after="Die Rentiere nicken. \"Ihr wisst Bescheid. Steigt ein, uns bleibt wenig Zeit!\" Ihr klettert in den Schlitten.",
            hints=["Denkt an den Jahreszyklus: Brunft im Herbst, Kälber im Frühjahr.",
                   "Karibu klingt nach Kanada."]),
    4: dict(title="Türchen 4: Kurs Nordpol",
            story="Ihr sitzt im Schlitten und wollt losfahren. Doch der Bordcomputer verlangt einen Kurs, und eine Karte "
                  "gibt es nicht, nur die Sterne.",
            render=door4, akte="Kurs bestätigt: Polarstern bei Planquadrat (14|27).",
            after="Der Schlitten ruckt an und hebt ab. Unter euch werden die Lichter der Stadt kleiner.",
            hints=["Im Großen Wagen gibt es zwei Zeigersterne an der Kastenseite, die den Weg weisen.",
                   "Merak und Dubhe. Man verlängert ihre Verbindung hinter Dubhe um das Fünffache ihres Abstands.",
                   "Dubhe + 5 × (Dubhe − Merak), für x und y getrennt gerechnet."]),
    5: dict(title="Türchen 5: Nebel und Eislabyrinth",
            story="Ihr fliegt los und kommt in einen dichten Nebel. Ohne Sicht seid ihr auf Kompass und Kommandos angewiesen.",
            render=door5, akte="Eissplitter 1 von 7 (Wert 4).",
            after="Im Zentrum liegt ein funkelnder Eissplitter. Auf ihm steht eine Zahl und ein Symbol. Das Tor zur "
                  "Werkstatt hat sieben Schlösser, dies ist erst der erste Splitter.",
            hints=["Jedes Kommando dreht um die genannte Gradzahl, 360° sind eine volle Runde.",
                   "Im Labyrinth bleibt eure Spur (+) sichtbar. Der linke Weg nach unten ist eine Sackgasse.",
                   "Geht oben herum und dann rechts außen nach unten."]),
}


DOORS.update({
    6: D("Türchen 6: Der Eisrutsch",
         "Ein Schneesturm zwingt euch zur Landung auf einem zugefrorenen Hang. Der Boden ist spiegelglatt: Wer losrutscht, hält erst an der nächsten Wand. Ihr müsst zum Zeichen E.",
         door6, "Eissplitter 2 von 7 (Wert 6).", "Bei E liegt ein Splitter. Der Sturm legt sich, ihr hebt wieder ab.",
         "Plant rückwärts: Von wo aus rutscht man über E?", "Sieben Züge reichen."),
    7: D("Türchen 7: Der Frostgeist",
         "Auf einem zugefrorenen See sitzt ein Frostgeist vor 21 Eiszapfen. Ihr nehmt abwechselnd 1 bis 3. Wer den letzten nimmt, gewinnt den Splitter.",
         door7, "Eissplitter 3 von 7 (Wert 1).", "Der Frostgeist murrt und schiebt euch den Splitter hin.",
         "Es gibt eine Strategie, mit der ihr als Erster immer gewinnt.", "Hinterlasst nach jedem eurer Züge eine Zahl, die durch 4 teilbar ist."),
    8: D("Türchen 8: Die Hängebrücke",
         "Eine morsche Hängebrücke über eine Schlucht. Es gibt nur eine Laterne, und sie wird zum Gehen gebraucht.",
         txt("Nur zwei Elfen dürfen gleichzeitig über die Brücke, die Laterne muss immer mit.\n"
             "Zeiten pro Elf: 1, 4, 5 und 8 Minuten. Zwei zusammen gehen im Tempo des Langsameren.\n\n"
             "Wie viele Minuten brauchen alle vier mindestens?", nums("19"), "Minuten"),
         "Eissplitter 4 von 7 (Wert 7).", "Alle sind drüben, die Brücke schaukelt, der vierte Splitter glitzert im Schnee.",
         "Vergleicht: Der Schnellste begleitet alle, oder die zwei Langsamsten gehen zusammen."),
    9: D("Türchen 9: Der Funkspruch",
         "Mitten im Flug knackt das Funkgerät. Aus der Werkstatt kommt eine Nachricht in Morsezeichen.",
         door9, "Funkspruch aus der Werkstatt: Der Generator ist ausgefallen. Eissplitter 5 von 7 (Wert 3).",
         "Es ist ein Notruf. Im Funkgerät klemmt ein Splitter, den ihr herausnehmt.",
         "Kurz = Punkt, lang = Strich. ' / ' trennt die Wörter."),
    10: D("Türchen 10: Der Polarlicht-Laser",
          "Das Polarlicht lädt den Schlitten auf. Doch der Laserstrahl muss durch ein Spiegelfeld, und ihr müsst vorhersagen, wo er austritt.",
          door10, "Eissplitter 6 von 7 (Wert 5).", "Der Strahl trifft den Schlitten, und im Lack entsteht ein Splitter aus Licht.",
          "Läuft der Strahl nach rechts, lenkt / ihn nach oben und \\ nach unten.", "Verfolgt ihn Feld für Feld. Er knickt neun Mal ab."),
    11: D("Türchen 11: Die Eiswächter",
          "Hinter einem Gletscher stehen drei Tore, und vor jedem ein Eiswächter. Hinter einem liegt der letzte Splitter.",
          txt("Nur einer der drei Wächter sagt die Wahrheit:\n\n"
              "  Wächter 1: Der Splitter liegt hinter Tor 1.\n"
              "  Wächter 2: Der Splitter liegt nicht hinter Tor 2.\n"
              "  Wächter 3: Der Splitter liegt nicht hinter Tor 1.\n\n"
              "Hinter welchem Tor liegt er?", nums("2"), "Tor Nummer"),
          "Eissplitter 7 von 7 (Wert 2).", "Ihr habt alle sieben Splitter. Vor euch erhebt sich ein gewaltiges Eistor.",
          "Prüft jedes Tor: Wie viele Wächter hätten dann recht?"),
    12: D("Türchen 12: Das Tor zum Nordpol",
          "Das Tor hat sieben Mulden. Eine Stimme flüstert: Setzt die Splitter vom kleinsten Wert zum größten ein.",
          txt("Die Splitter stehen in der Akte (Wert und Nummer).\n"
              "Gebt die Splitternummern (1 bis 7) in der Reihenfolge ein, in der ihr sie einsetzt.",
              lambda a: re.sub(r"\D", "", a) == "3751624", "Sieben Ziffern"),
          "Das Tor zur Werkstatt ist offen.", "Das Tor schwingt auf. Dahinter: Chaos, Dunkelheit, und ein Wimmern.",
          "Jeder Splitter hat eine Nummer und einen Wert. Sortiert nach dem Wert."),
    13: D("Türchen 13: Der Generator (Volt)",
          "Volt, der Elektriker, sitzt verzweifelt vor dem Notstrom-Schaltfeld. \"Um 22:47 fiel der Strom aus! Helft mir, die Lampen anzubekommen, dann sage ich euch, wo ich war.\"",
          door13, "Volt: Ich war weder im Büro noch in der Maschinenhalle. Ich stand in Spalte C.",
          "Alle Lampen brennen. Volt jubelt und erzählt euch, wo er war.",
          "Die Reihenfolge ist egal, und jedes Feld braucht höchstens einen Druck."),
    14: D("Türchen 14: Die Paketsortierung (Fussel)",
          "In der Packhalle sind alle Pakete vertauscht. Der kleine Fussel flitzt aufgeregt herum. \"Bringt die Pakete in Ordnung, dann erzähle ich euch, was ich weiß.\"",
          txt("Lieferschein-Regeln: Express-Pakete (*) zuerst, danach alle anderen. Innerhalb jeder Gruppe:\n"
              "nach Zielland alphabetisch, bei gleichem Land das leichtere zuerst.\n\n"
              "  A: Spanien, 3 kg      B*: Italien, 5 kg      C: Spanien, 1 kg\n"
              "  D*: Finnland, 2 kg    E: Italien, 2 kg\n\nIn welcher Reihenfolge laufen sie? (Buchstaben)",
              eq("DBECA"), "Reihenfolge"),
          "Fussel: Ich war weder im Büro noch in der Maschinenhalle. Ich stand oberhalb von Zimta.", "Fussel strahlt. Er wirkt dabei ein wenig verlegen."),
    15: D("Türchen 15: Die Zahnräder (Schraub)",
          "Mechaniker Schraub starrt auf ein Getriebe, das ruckelt. \"Wenn ihr mir sagt, wie sich Rad D dreht, weiß ich, welches Teil getauscht wurde.\"",
          txt("A (12 Zähne) greift in B (36 Zähne). C (10 Zähne) sitzt auf derselben Achse wie B und greift in D (25 Zähne).\n"
              "A dreht sich 15 Mal im Uhrzeigersinn.\n\nWie oft und in welche Richtung dreht sich D? (z. B. 3 links)",
              eq("2RECHTS", "2UHRZEIGERSINN", "2IMUHRZEIGERSINN"), "Umdrehungen und Richtung"),
          "Schraub: Ich war weder im Generatorraum noch in der Packhalle. Ich stand in Spalte E, und Volts Zeile liegt direkt neben meiner.", "Das Getriebe läuft rund. Schraub notiert etwas in seinem Heft.",
          "Wenn zwei Zahnräder ineinandergreifen, drehen sie in entgegengesetzte Richtungen."),
    16: D("Türchen 16: Die Paketstapel (Holly)",
          "Chef-Elfe Holly stapelt Pakete auf dem Förderband um. \"Berechnet mir die Zeit, dann nehme ich mir Zeit für euch.\"",
          txt("Sechs Pakete (unterschiedlich groß) liegen als Turm auf Platz 1. Sie sollen auf Platz 3, mit Platz 2 als Zwischenablage.\n"
              "Nie darf ein größeres auf ein kleineres. Ein Zug dauert 2 Sekunden.\n\nWie viele Sekunden mindestens?",
              nums("126"), "Sekunden"),
          "Holly: Ich war weder im Generatorraum noch im Stall. Ich stand in Spalte B.", "Holly nickt zufrieden und wirft einen Blick auf die Uhr.",
          "Mit n Paketen braucht man 2^n − 1 Züge."),
    17: D("Türchen 17: Die Karotten (Gustav)",
          "Im Stall sind die Rentiere unruhig, jemand hat das Futter vertauscht. Stallmeister Gustav braucht genau 5 Liter Karottensaft.",
          txt("Gustav hat einen 7-Liter- und einen 4-Liter-Krug, beide leer, ohne Markierungen.\n"
              "Ein Zug = einen Krug füllen, einen leeren oder von einem in den anderen gießen.\n\n"
              "Wie viele Züge braucht er mindestens, bis in einem Krug genau 5 Liter sind?", nums("8"), "Züge"),
          "Gustav: Ich war im Stall bei den Rentieren.", "Die Rentiere trinken zufrieden. Gustav klopft euch auf die Schulter.",
          "Probiert: Den 7er füllen, in den 4er gießen, den 4er leeren ..."),
    18: D("Türchen 18: Die Plätzchendosen (Zimta)",
          "Bäckerin Zimta ist verzweifelt: Eine ihrer 12 Plätzchendosen wurde ausgetauscht und wiegt anders (leichter oder schwerer, unbekannt).",
          txt("Ihr habt eine Balkenwaage ohne Gewichte.\n\nWie viele Wägungen genügen mindestens, um die falsche Dose sicher zu finden?",
              nums("3"), "Wägungen"),
          "Zimta: Ich war in der Backstube, in Zeile 5. Volt stand zwei Zeilen unter Holly.", "Zimta drückt euch eine warme Tüte Plätzchen in die Hand."),
    19: D("Türchen 19: Der Tresor",
          "Im Büro des Weihnachtsmanns steht ein Tresor. Holly ist weg, aber auf dem Tresor klebt ein Zettel mit früheren Versuchen.",
          txt("Vierstelliger Code, jede Ziffer höchstens einmal. ⚫ = richtige Ziffer, richtiger Platz. ⚪ = richtige Ziffer, falscher Platz.\n\n"
              "  6370: ⚫0 ⚪1\n  5431: ⚫0 ⚪2\n  4017: ⚫3 ⚪0\n  5179: ⚫0 ⚪2\n  2073: ⚫0 ⚪1\n\nDer Code?",
              nums("4817"), "Code"),
          DUTY, "Der Tresor springt auf. Darin liegt der Dienstplan der Unglücksnacht."),
    20: D("Türchen 20: Der Wunschzettel",
          "Im Tresor liegt ein Zettel, ungewöhnlich verschlüsselt. Er ist der einzige Wunschzettel ohne Absender.",
          lambda day: (st.code("".join(chr(155 - ord(c)) if "A" <= c <= "Z" else c for c in
                                       "EIN ELF WUENSCHT SICH NUR EINES: EINMAL MITFLIEGEN."), language=None),
                       text_door(day, eq("MITFLIEGEN"), "Was wünscht sich der Elf?")),
          "Wunschzettel eines Elfen (ohne Namen): Einmal mitfliegen.", "Ihr schweigt kurz. Das ist kein Wunsch eines Saboteurs, sondern eines Einsamen.",
          "Das Alphabet rückwärts: A wird Z, B wird Y."),
    21: D("Türchen 21: Der Hauptschalter",
          "[Platzhalter: hier kommt ein Rätsel nur für eure Familie hin.] Bis dahin: Der Hauptschalter steht in einem Raum, dessen Name durcheinandergeraten ist.",
          txt("Aus den Buchstaben M U R R A T O R E G A N E lässt sich der Raum bilden, in dem der Hauptschalter steht.", eq("GENERATORRAUM"), "Der Raum"),
          "Der Hauptschalter liegt im Generatorraum. Nur wer dort war, konnte ihn umlegen. Der Täter war dort allein.", "Ihr wisst jetzt, wo es geschah. Fehlt noch, wer."),
    22: D("Türchen 22: Die Zeitleiste",
          "Der Weihnachtsmann hat die Nacht rekonstruiert. Fünf Ereignisse sind durcheinandergeraten.",
          txt("A Stromausfall   B Pakete vertauscht   C Futter vertauscht   D Funkgerät ausgefallen   E Plätzchen verschwunden\n\n"
              "  - Die Pakete wurden als Erstes vertauscht.\n  - Die Plätzchen verschwanden vor dem Stromausfall.\n"
              "  - Das Futter wurde direkt nach dem Stromausfall vertauscht.\n  - Das Funkgerät fiel zuletzt aus.\n\nReihenfolge (Buchstaben)?",
              eq("BEACD"), "Reihenfolge"),
          "Reihenfolge der Nacht: Pakete, Plätzchen, Strom (22:47), Futter, Funk.", "Alles ergibt jetzt ein Bild."),
    23: D("Türchen 23: Der freie Sitz",
          "Der Schlitten ist beladen und startklar. Aber auf der Sitzbank ist ein Platz leer, und niemand weiß, für wen.",
          txt("Die Nummer des freien Sitzes ist die kleinste Zahl, die bei Division durch 3 den Rest 2, durch 4 den Rest 3 und durch 5 den Rest 4 lässt.",
              nums("59"), "Sitznummer"),
          "Im Schlitten ist Sitz 59 noch frei.", "Der Weihnachtsmann blickt nachdenklich auf den leeren Platz. Morgen ist Heiligabend."),
    24: D("Türchen 24: Heiligabend",
          "Der Schlitten steht startklar, doch eine Frage bleibt offen: Wer hat die Werkstatt sabotiert? Setzt die sechs Elfen mithilfe der Akte auf den Grundriss.",
          door24, "Fall gelöst.",
          "🎄 Der Schlitten hebt ab. Ihr seid offiziell Ehren-Elfen des Nordpols und habt Weihnachten gerettet. Frohe Weihnachten!",
          "Beginnt mit den Elfen, deren Raum feststeht (Gustav, Zimta). Jede Zeile und jede Spalte hat genau einen Elf.", "Spalten- und Zeilenangaben legen den Rest fest. Wer bleibt für den Generatorraum übrig?"),
})


# ---------------------------------------------------------------- Seite
def is_open(d: int) -> bool:
    return TEST or date.today() >= date(YEAR, 12, d)


st.title("🎄 Der Nordpol-Fall")
st.caption("Jemand sabotiert die Weihnachtswerkstatt. Nur ihr könnt sie noch retten.")

if TEST:
    st.warning("Testmodus: alle Türchen sind geöffnet.")

if "active" not in st.session_state:
    nxt = [d for d in DOORS if d not in game["solved"] and is_open(d)]
    st.session_state.active = nxt[0] if nxt else 1

for start in (1, 13):
    cols = st.columns(12)
    for i, d in enumerate(range(start, start + 12)):
        label = f"✓{d}" if d in game["solved"] else (str(d) if is_open(d) else f"🔒{d}")
        if cols[i].button(label, key=f"nav{d}", disabled=not is_open(d), use_container_width=True):
            st.session_state.active = d
            st.rerun()

with st.sidebar:
    st.subheader("🗂️ Die Akte")
    if not game["akte"]:
        st.write("*Noch leer.*")
    for d in sorted(game["akte"], key=int):
        st.markdown(f"**Türchen {d}:** {game['akte'][d]}")

st.markdown("---")
day = st.session_state.active
if day not in DOORS:
    st.subheader(f"Türchen {day}")
    st.info("Dieses Türchen wird noch gebaut.")
else:
    door = DOORS[day]
    st.subheader(door["title"])
    st.info(door["story"])
    fresh = st.session_state.pop("celebrate", False)
    if fresh:
        st.snow()
        if day == 24:
            st.balloons()
    if day in game["solved"]:
        st.success(f"Gelöst! Neuer Eintrag in der Akte: {door['akte']}")
        if door.get("after"):
            st.markdown(f"*{door['after']}*")
        snd = Path(__file__).parent / door["sound"] if door.get("sound") else None
        if snd and snd.exists():
            st.audio(str(snd), autoplay=fresh)
    else:
        door["render"](day)
        hints(day, door["hints"])
