from array import array
from base64 import b64decode
from functools import lru_cache
from html import escape
from io import BytesIO
from math import pi, sin
from sys import byteorder
import wave
import json
import random
import string
import re
import unicodedata
from datetime import date
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Der Nordpol-Fall", page_icon="🎄", layout="wide")

SAVE = Path(__file__).with_name("nordpol_spielstand.json")          # gemeinsamer Spielstand (auf dem Server)
TEST = st.query_params.get("test", "1") == "1"   # App-URL + ?test=1 -> alle Türchen offen
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
    if TEST:
        return
    try:
        SAVE.write_text(json.dumps(st.session_state.game, ensure_ascii=False))
    except Exception:
        pass


if "game" not in st.session_state:
    st.session_state.game = {"solved": [], "akte": {}} if TEST else load()
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


def txt(body, check, label="Eure Lösung"):
    def f(day):
        st.code(body, language=None)
        text_door(day, check, label)
    return f


def eq(*opts):
    normalized = {norm(option) for option in opts}
    return lambda a: norm(a) in normalized


def nums(*n):
    return lambda a: re.findall(r"\d+", a) == list(n)


def pad(k, fn):
    _, m, _ = st.columns(3)
    m.button("⬆️", key=k + "u", on_click=fn, args=(-1, 0), use_container_width=True)
    a, b, c = st.columns(3)
    a.button("⬅️", key=k + "l", on_click=fn, args=(0, -1), use_container_width=True)
    b.button("⬇️", key=k + "d", on_click=fn, args=(1, 0), use_container_width=True)
    c.button("➡️", key=k + "r", on_click=fn, args=(0, 1), use_container_width=True)


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


# Überarbeitete Fassung für Türchen 1–12
GRAVUR = ("Draußen ruht ein Irrlicht.", "Am Christbaum hängen Träume.",
          "Niemand erwartet ungewöhnlichen Nachtbesuch.", "Vielleicht ist es Rudolf.")
KISTENCODE = "3894"
PLAIN = ("Der Hauptschalter wurde von Hand umgelegt.\n"
         "Die Werkstatt braucht euch.\n"
         "Sprecht dreimal das Wort Laterne.")


def door1(day):
    st.markdown("> " + "  \n> ".join(GRAVUR))
    st.caption("Vier Zeilen, vier Ziffern.")
    text_door(day, eq(KISTENCODE), "Vierstelliger Code")



def door2(day):
    st.image(b64decode(LETTER_PNG), width=720)
    st.caption("Wie weit ihr gehen müsst, verrät euch der Absender.")
    with st.expander("Geheimtext zum Lesen und Kopieren"):
        st.code(vigenere(PLAIN.upper(), "H"), language=None)
    text_door(day, eq("LATERNE"), "Welches Wort sollt ihr dreimal aussprechen?")


def door3(day):
    questions = (
        ("Bei unserem Gespann haben die erwachsenen Bullen ihre Geweihe vor Dezember abgeworfen. "
         "Alle vier vor euch tragen noch eines. Was sind wir?", ("Erwachsene Bullen", "Kühe"), "Kühe"),
        ("Auf unserer Funkliste steht der Name, den man in Kanada für Rentiere verwendet. Welcher ist es?", ("Wapiti", "Karibu", "Elch"), "Karibu"),
        ("Wenn ihr uns im Dunkeln sucht, leuchten unsere Augen im Licht der Laterne. Im Sommer schimmert die Schicht hinter unserer Netzhaut goldfarben. "
         "Welche Farbe hat sie im Winter?", ("Grün", "Silber", "Blau"), "Blau"),
    )
    with st.form("f3"):
        picks = [st.radio(q, options, index=None, key=f"rentier{i}") for i, (q, options, _) in enumerate(questions)]
        if st.form_submit_button("Antworten prüfen"):
            if picks == [answer for _, _, answer in questions]:
                solve(day)
            st.error("Überprüft eure drei Antworten.")



MERAK, DUBHE = (2, 2), (3, 3)
POLAR = tuple(d + 2 * (d - m) for m, d in zip(MERAK, DUBHE))


def door4(day):
    stars = {MERAK: ("M", "Merak"), DUBHE: ("D", "Dubhe"),
             (5, 1): ("P", "Phecda"), (6, 2): ("G", "Megrez")}
    point = lambda x, y: (42 + x * 45, 292 - y * 40)
    lines = "".join(
        f'<path d="M{42+i*45} 52V292 M42 {292-i*40}H357"/>'
        for i in range(7)
    ) + '<path d="M357 52V292"/>'
    numbers = "".join(
        f'<text x="{point(i,0)[0]}" y="315" text-anchor="middle">{i}</text>'
        for i in range(8)
    ) + "".join(
        f'<text x="25" y="{point(0,i)[1]+4}" text-anchor="middle">{i}</text>'
        for i in range(1, 7)
    )
    points = "".join(
        f'<circle cx="{x}" cy="{y}" r="11" fill="#ffe09a"/>'
        f'<text x="{x}" y="{y+4}" text-anchor="middle" fill="#1c2430">{short}</text>'
        for (col, row), (short, _) in stars.items() for x, y in [point(col, row)]
    )
    st.markdown(
        '<svg viewBox="0 25 397 305" role="img" aria-label="Sternkarte mit Koordinatenraster" '
        'style="display:block;width:100%;max-width:440px;background:#16293d;border-radius:10px">'
        f'<g stroke="#57718b">{lines}</g><path d="M42 40V292H370" fill="none" stroke="#d6e7f6" stroke-width="2"/>'
        f'<g fill="#e6f2ff" font-size="14">{numbers}<text x="375" y="296">x</text><text x="36" y="40">y</text></g>'
        f'<g font-size="13" font-weight="bold">{points}</g></svg>',
        unsafe_allow_html=True,
    )
    st.caption(" · ".join(f"{short} = {name} ({x}|{y})" for (x, y), (short, name) in stars.items()))
    st.markdown("> Schaut, wie ihr auf dem Raster von **Merak (M)** nach **Dubhe (D)** kommt. "
                "Macht ab Dubhe **zweimal denselben Schritt**. Dort liegt der gesuchte Punkt.")
    with st.form("f4"):
        left, right = st.columns(2)
        x = left.number_input("Waagerecht (x)", min_value=0, max_value=7, value=0, step=1)
        y = right.number_input("Senkrecht (y)", min_value=0, max_value=6, value=0, step=1)
        if st.form_submit_button("Kurs bestätigen"):
            if (x, y) == POLAR:
                solve(day)
            st.error("Der Kurs stimmt noch nicht.")


MAZE = (
    "###########",
    "#S..#.....#",
    "#.#.#.###.#",
    "#.#...#...#",
    "#...###.#.#",
    "###.....#.#",
    "#...###.#.#",
    "#.#.....#E#",
    "###########",
)

DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))
CELL_COLORS = {"": "#536475", "▧": "#688b9e", "·": "#ddf2fc", "•": "#bddbe8",
               "⚑": "#a9e0ca", "🧭": "#f9d898", "🏮": "#f9d898", "🔧": "#f9d898", "✦": "#f9d898"}


def grid(rows, label):
    cells = "".join(
        f'<span style="background:{CELL_COLORS.get(cell, "#ddf2fc")};color:#172c3d;'
        f'display:grid;place-items:center;aspect-ratio:1">{escape(cell)}</span>'
        for row in rows for cell in row
    )
    st.markdown(f'<div role="img" aria-label="{escape(label)}" style="display:grid;'
                f'grid-template-columns:repeat({len(rows[0])},1fr);gap:3px;'
                f'max-width:{len(rows[0])*43}px;margin:12px 0">{cells}</div>',
                unsafe_allow_html=True)


def reset_fields(*keys):
    for key in keys:
        st.session_state.pop(key, None)


def _move(dr, dc):
    s = st.session_state
    r, c = s.maze_pos
    if MAZE[r + dr][c + dc] != "#":
        s.maze_pos = (r + dr, c + dc)
        s.maze_trail.add(s.maze_pos)


def door5(day):
    s = st.session_state
    r, c = s.setdefault("maze_pos", (1, 1))
    trail = s.setdefault("maze_trail", {(1, 1)})
    rows = []
    for i, row in enumerate(MAZE):
        cells = []
        for j, cell in enumerate(row):
            visible = abs(i - r) + abs(j - c) <= 1
            if (i, j) == (r, c) and cell not in "SE":
                symbol = "🧭"
            elif cell in "SE":
                symbol = {"S": "⚑", "E": "🏮"}[cell]
            elif (i, j) in trail:
                symbol = "•"
            else:
                symbol = ("▧" if cell == "#" else "·") if visible else ""
            cells.append(symbol)
        rows.append(cells)
    grid(rows, f"Nebellabyrinth, Figur in Zeile {r + 1}, Spalte {c + 1}")
    st.caption("⚑ Eingang oben links · 🏮 Weglaterne unten rechts · 🧭 Ihr · • Fußspuren · ▧ Eiswand")
    if MAZE[r][c] == "S":
        st.write("Ihr steht am Eingang. Nutzt die Pfeile, um jeweils ein Feld weiterzugehen.")
    elif MAZE[r][c] == "E":
        st.write("Ihr steht an der Weglaterne.")
    pad("maze", _move)
    st.button("Zum Eingang zurück", key="maze_reset", on_click=reset_fields, args=("maze_pos", "maze_trail"))
    if MAZE[r][c] == "E" and st.button("Weglaterne anzünden", type="primary"):
        solve(day)


# Das Werkzeug liegt an einer echten Halteposition.
ICE = (
    "#########", "#S.#..###", "#.......#", "#.......#", "#....#..#",
    "#.#.#..##", "##.#..###", "#.##.E..#", "#########",
)


def slide_position(pos, dr, dc):
    r, c = pos
    while ICE[r + dr][c + dc] != "#":
        r, c = r + dr, c + dc
    return r, c


def _slide(dr, dc):
    s = st.session_state
    destination = slide_position(s.ice_pos, dr, dc)
    if destination != s.ice_pos:
        s.ice_pos = destination
        s.ice_moves += 1


def door6(day):
    s = st.session_state
    pos = s.setdefault("ice_pos", (1, 1))
    moves = s.setdefault("ice_moves", 0)
    symbols = {"#": "▧", ".": "·", "S": "·", "E": "🔧"}
    grid([["🧭" if (i, j) == pos else symbols[ch] for j, ch in enumerate(row)]
          for i, row in enumerate(ICE)], "Eishang mit Werkzeug")
    st.caption(f"Ihr rutscht geradeaus bis zum nächsten Hindernis. Züge: {moves}. Hebt das Werkzeug erst auf, wenn ihr auf seinem Feld anhaltet.")
    if ICE[pos[0]][pos[1]] == "E":
        if st.button("Werkzeug aufheben", type="primary"):
            solve(day)
    else:
        pad("ice", _slide)
    st.button("Zum Start zurück", key="ice_reset", on_click=reset_fields, args=("ice_pos", "ice_moves"))


PEOPLE = ("Holly", "Gustav", "Mira", "Noel")


def bridge_move(far, lantern_far, party):
    party = set(party)
    if not 1 <= len(party) <= 2:
        raise ValueError("Wählt eine oder zwei Personen.")
    if any((person in far) != lantern_far for person in party):
        raise ValueError("Alle müssen am selben Ufer wie die Laterne stehen.")
    if "Holly" in party and len(party) == 1:
        raise ValueError("Holly braucht wegen ihrer Höhenangst Begleitung.")
    if "Gustav" in party and len(party) != 1:
        raise ValueError("Gustav muss mit seinem sperrigen Gepäck allein gehen.")
    return far ^ party, not lantern_far


def door8(day):
    s = st.session_state
    far, lantern_far, history = s.setdefault("bridge", (set(), False, []))
    left, right = st.columns(2)
    left.markdown("**Startufer**" + (" 🏮" if not lantern_far else ""))
    right.markdown("**Zielufer**" + (" 🏮" if lantern_far else ""))
    left.write(", ".join(p for p in PEOPLE if p not in far) or "—")
    right.write(", ".join(p for p in PEOPLE if p in far) or "—")
    st.caption("Höchstens zwei pro Gang. Holly braucht Begleitung. Gustav geht allein. Die Laterne kommt immer mit.")
    if history:
        st.write(f"Überquerungen: **{len(history)} / 7**")
        st.caption(" · ".join(history))
    available = [p for p in PEOPLE if (p in far) == lantern_far]
    if len(history) < 7:
        party = st.multiselect("Wer geht mit der Laterne?", available, key=f"bridge_party_{len(history)}")
        if st.button("Über die Brücke", type="primary"):
            try:
                new_far, new_side = bridge_move(far, lantern_far, party)
            except ValueError as error:
                st.error(str(error))
            else:
                s.bridge = (new_far, new_side, history + [" + ".join(party) + (" ←" if lantern_far else " →")])
                if len(new_far) == len(PEOPLE):
                    solve(day)
                st.rerun()
    else:
        st.warning("Sieben Gänge sind verbraucht. Probiert eine andere Reihenfolge.")
    st.button("Brücke zurücksetzen", on_click=reset_fields, args=("bridge",))


MORSE_WORDS = tuple(tuple(MORSE[ch] for ch in word) for word in ("TOR", "IM", "EIS"))


@lru_cache
def morse_audio(words):
    rate = 16000
    samples = array("h")
    unit = 1440
    for wi, word in enumerate(words):
        if wi:
            samples.extend([0] * (7 * unit))
        for li, letter in enumerate(word):
            if li:
                samples.extend([0] * (3 * unit))
            for si, symbol in enumerate(letter):
                if si:
                    samples.extend([0] * unit)
                length = unit * (3 if symbol == "-" else 1)
                samples.extend(int(11000 * min(1, n/80, (length-n)/80) * sin(2*pi*640*n/rate))
                               for n in range(length))
    result = BytesIO()
    if byteorder != "little":
        samples.byteswap()
    with wave.open(result, "wb") as stream:
        stream.setparams((1, 2, rate, 0, "NONE", "not compressed"))
        stream.writeframes(samples.tobytes())
    return result.getvalue()


def morse_card():
    for start in range(0, 26, 7):
        st.code("   ".join(f"{letter}  {MORSE[letter]}" for letter in string.ascii_uppercase[start:start+7]), language=None)


def door9(day):
    st.markdown("**Empfangsstation · Werkstatt**")
    segment = st.radio("Abschnitt", ("Ganzer Funkspruch", "Wort 1", "Wort 2", "Wort 3"), horizontal=True)
    words = MORSE_WORDS if segment == "Ganzer Funkspruch" else (MORSE_WORDS[int(segment[-1]) - 1],)
    st.audio(morse_audio(words), format="audio/wav")
    with st.expander("Signale lesen"):
        st.code("   /   ".join("  ".join(word) for word in words), language=None)
    if 8 in game["solved"] or TEST:
        with st.expander("Morsekarte aus dem Notfunkkasten"):
            if 8 not in game["solved"]:
                st.caption("Vorschau im Testmodus. Im Spiel findet ihr die Karte in Türchen 8.")
            morse_card()
    else:
        st.caption("Die Morsekarte liegt im Notfunkkasten an der Brücke.")
    text_door(day, eq("TOR IM EIS"), "Welche drei Wörter funkt die Werkstatt?")


MIRRORS = {(2, 1): "/", (1, 1): "/", (1, 3): "/", (2, 3): "/", (2, 4): "/", (4, 2): "\\"}
LIGHT_EXIT = (5, 4)


def trace_light(mirrors):
    r, c, dr, dc = 2, 0, 0, 1
    states, path = set(), set()
    while 0 <= r < 5 and 0 <= c < 5:
        state = (r, c, dr, dc)
        if state in states:
            return path, None
        states.add(state)
        path.add((r, c))
        if mirrors.get((r, c)) == "/":
            dr, dc = -dc, -dr
        elif mirrors.get((r, c)) == "\\":
            dr, dc = dc, dr
        r, c = r + dr, c + dc
    return path, (r, c)


def door10(day):
    mirrors = st.session_state.setdefault("mirrors", MIRRORS.copy())
    path, exit_pos = trace_light(mirrors)
    st.caption("Der Strahl tritt links in Zeile 3 ein. Lenkt ihn zur Markierung unter Spalte 5.")
    for r in range(5):
        cols = st.columns([1, 1, 1, 1, 1, 2])
        for c in range(5):
            p = (r, c)
            lit = "✦ " if p in path else ""
            if p in mirrors:
                if cols[c].button(lit + mirrors[p], key=f"mirror{r}{c}",
                                  help=f"Spiegel in Zeile {r + 1}, Spalte {c + 1} drehen"):
                    mirrors[p] = "\\" if mirrors[p] == "/" else "/"
                    st.rerun()
            else:
                cols[c].markdown("✦" if lit else "·")
    st.markdown("**Ziel** · unter Spalte 5")
    if exit_pos == LIGHT_EXIT:
        if st.button("Den markierten Durchgang nehmen", type="primary"):
            solve(day)
    st.button("Spiegel zurücksetzen", on_click=reset_fields, args=("mirrors",))


PLATES = {
    "Blau · L-Form": ((0, 0), (1, 0), (1, 1)),
    "Grün · gerade": ((0, 0), (0, 1), (0, 2)),
    "Gelb · Winkel": ((0, 0), (0, 1), (1, 1)),
}
PLATE_SYMBOLS = dict(zip(PLATES, ("🟦", "🟩", "🟨")))
GAP = {(r, c) for r in range(3) for c in range(4)} - {(0, 0), (1, 1), (2, 3)}


def rotate_plate(shape, turns):
    for _ in range(turns):
        shape = tuple((c, -r) for r, c in shape)
    top, left = min(r for r, _ in shape), min(c for _, c in shape)
    return {(r - top, c - left) for r, c in shape}



def door11(day):
    state = st.session_state
    placed = state.setdefault("plates", {})
    rotations = state.setdefault("plate_rotations", {})
    st.markdown("**1. Platte auswählen und bei Bedarf drehen**")
    plate = st.radio("Eisplatte", tuple(PLATES), horizontal=True, label_visibility="collapsed")
    symbol = PLATE_SYMBOLS[plate]
    turns = rotations.get(plate, 0)
    shape = rotate_plate(PLATES[plate], turns)
    anchor = min(shape)
    preview = [["⊕" if (r, c) == anchor else symbol if (r, c) in shape else ""
                for c in range(max(c for _, c in shape) + 1)]
               for r in range(max(r for r, _ in shape) + 1)]
    grid(preview, f"Vorschau für {plate}, der Anker ist mit einem Plus markiert")
    left, right = st.columns(2)
    if left.button("↻ 90° drehen", key="plate_turn"):
        rotations[plate] = (turns + 1) % 4
        st.rerun()
    if right.button("Platte herausnehmen", disabled=plate not in placed):
        placed.pop(plate)
        st.rerun()

    st.markdown("**2. Ein Feld in der Lücke anklicken**")
    st.caption("Das mit ⊕ markierte Kästchen der Platte landet auf dem Feld, das ihr anklickt.")
    filled = {cell: PLATE_SYMBOLS[name] for name, cells in placed.items() for cell in cells}
    occupied = {cell for name, cells in placed.items() if name != plate for cell in cells}
    for r in range(3):
        columns = st.columns(4)
        for c, column in enumerate(columns):
            cell = (r, c)
            label = filled.get(cell, "⬜" if cell in GAP else "🧊")
            if column.button(label, key=f"plate_cell_{r}_{c}", disabled=cell not in GAP or cell in occupied,
                             help=f"Zeile {r + 1}, Spalte {c + 1}", width="stretch"):
                footprint = {(r + i - anchor[0], c + j - anchor[1]) for i, j in shape}
                if footprint <= GAP and footprint.isdisjoint(occupied):
                    placed[plate] = footprint
                    st.rerun()
                st.warning("Die Platte passt hier in dieser Drehung nicht. Dreht sie oder wählt ein anderes Feld.")
    if set(filled) == GAP and st.button("Schlucht überqueren", type="primary"):
        solve(day)
    st.button("Alle Platten herausnehmen", on_click=reset_fields, args=("plates", "plate_rotations"))


# Norden, Osten, Süden, Westen. Nahtsymbole gehören paarweise zusammen.
MAP_FRAME = {
    (0, 0): ("", "●", "✚", "Start"),
    (0, 1): ("", "◆", "○", "●"),
    (0, 2): ("", "▲", "■", "◆"),
    (0, 3): ("", "Stern", "", "▲"),
    (1, 0): ("✚", "◇", "", ""),
    (1, 1): ("○", "△", "", "◇"),
    (1, 2): ("■", "", "", "△"),
}
# Der eingezeichnete Pfad ist von den Nahtsymbolen unabhängig.
MAP_ROUTE = {
    (0, 0): (3, 2), (1, 0): (0, 1), (1, 1): (3, 0), (0, 1): (2, 1),
    (0, 2): (3, 1), (0, 3): (3, 1), (1, 2): (),
}
MAP_ORDER = tuple(MAP_FRAME)
PIECE_SLOTS = (5, 2, 4, 0, 6, 3, 1)
PIECE_TURNS = (1, 3, 2, 1, 3, 2, 1)


def piece_layout(day, turns):
    index = day - 5
    slot = MAP_ORDER[PIECE_SLOTS[index]]
    rotation = (PIECE_TURNS[index] + turns) % 4
    edges = MAP_FRAME[slot]
    return tuple(edges[(side - rotation) % 4] for side in range(4)), tuple(
        (side + rotation) % 4 for side in MAP_ROUTE[slot])


def map_piece(day, turns, max_width=108):
    edges, roads = piece_layout(day, turns)
    label = {"Start": "⚑", "Stern": "★"}
    positions = ((50, 0), (100, 50), (50, 100), (0, 50))
    names = ("oben", "rechts", "unten", "links")
    description = ", ".join(f"{name}: {edge or 'Außenrand'}" for name, edge in zip(names, edges))
    lines = "".join(f'<path d="M50 50 L{x} {y}" stroke="#266472" stroke-width="8"/>'
                    for i, (x, y) in enumerate(positions) if i in roads)
    marks = "".join(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="central" '
                    f'fill="#273545" font-size="15">{label.get(edge, edge)}</text>'
                    for (x, y), edge in zip(((50, 12), (89, 50), (50, 88), (11, 50)), edges) if edge)
    return (f'<svg viewBox="0 0 100 100" role="img" aria-label="Stück {day-4}, {description}" '
            f'style="display:block;width:100%;max-width:{max_width}px;background:#f3dfb2;border:1px solid #866e45">'
            f'{lines}{marks}<text x="78" y="87" fill="#6e5433" font-size="12">{day-4}</text></svg>')


def map_matches(placed):
    return set(placed) == set(MAP_FRAME) and all(
        piece_layout(*placed[slot])[0] == edges for slot, edges in MAP_FRAME.items()
    )



def map_seams(placed):
    matches = conflicts = 0
    for (r, c), (piece, turns) in placed.items():
        edges, _ = piece_layout(piece, turns)
        for side, (dr, dc) in enumerate(DIRECTIONS):
            neighbour = (r + dr, c + dc)
            if neighbour not in MAP_FRAME:
                boundary = MAP_FRAME[(r, c)][side]
                conflicts += edges[side] != boundary
            elif side in (1, 2) and neighbour in placed:
                other_edges, _ = piece_layout(*placed[neighbour])
                correct = bool(edges[side]) and edges[side] == other_edges[(side + 2) % 4]
                matches += correct
                conflicts += not correct
    return matches, conflicts


def door12(day):
    state = st.session_state
    pieces = [n for n in range(5, 12) if n in game["solved"]]
    if TEST and len(pieces) < 7 and st.checkbox("Fehlende Kartenstücke zum Testen leihen"):
        pieces = list(range(5, 12))
    if len(pieces) < 7:
        st.info(f"Ihr habt {len(pieces)} von 7 Kartenstücken. Die übrigen findet ihr in Türchen 5 bis 11.")
    if not pieces:
        return

    placed = {slot: item for slot, item in state.setdefault("map_placed", {}).items() if item[0] in pieces}
    rotations = state.setdefault("map_rotations", {})
    positions = {n: pos for pos, (n, _) in placed.items()}
    st.markdown("**1. Kartenstück auswählen**")
    buttons = st.columns(len(pieces))
    if state.get("map_piece_selected") not in pieces:
        state.map_piece_selected = next((n for n in pieces if n not in positions), pieces[0])
    for col, n in zip(buttons, pieces):
        label = f"{'✓ ' if n in positions else ''}{n - 4}"
        col.button(label, key=f"select_piece_{n}", help=f"Kartenstück {n - 4}",
                   type="primary" if state.map_piece_selected == n else "secondary",
                   on_click=set_map_selection, args=(n,), width="stretch")

    piece = state.map_piece_selected
    slot = positions.get(piece)
    turns = rotations.get(piece, placed[slot][1] if slot is not None else 0)
    preview, actions = st.columns([1, 2])
    preview.markdown(map_piece(piece, turns), unsafe_allow_html=True)
    actions.write(f"**Stück {piece - 4}** · {turns * 90}°")
    if actions.button("↻ 90° drehen", key="map_turn"):
        rotations[piece] = (turns + 1) % 4
        if slot is not None:
            placed[slot] = (piece, rotations[piece])
            state.map_placed = placed
        st.rerun()
    if actions.button("Stück herausnehmen", disabled=slot is None):
        placed.pop(slot)
        state.map_placed = placed
        st.rerun()

    assembled = map_matches(placed)
    if not assembled:
        st.markdown("**2. Feld im Rahmen anklicken**")
        st.caption("Gleiche Symbole gehören aneinander. Die Fahne gehört an den linken Rand. "
                   "Wenn ein Feld schon besetzt ist, kommt das alte Stück zurück in die Auswahl.")
    if assembled:
        tiles = "".join(map_piece(*placed[pos], max_width=450) for pos in MAP_ORDER)
        st.markdown(
            '<div style="display:grid;grid-template-columns:repeat(4,1fr);max-width:450px">'
            f'{tiles}</div>', unsafe_allow_html=True,
        )
    with st.container(width=450):
        for r in range(2) if not assembled else ():
            columns = st.columns(4, gap=None)
            for c, column in enumerate(columns):
                pos = (r, c)
                if pos not in MAP_FRAME:
                    continue
                column.markdown(
                    map_piece(*placed[pos], max_width=450) if pos in placed else
                    '<div style="width:100%;aspect-ratio:1;border:1px dashed #a4c5cd"></div>',
                    unsafe_allow_html=True,
                )
                label = f"Feld {MAP_ORDER.index(pos) + 1}"
                if column.button(label, key=f"map_slot_{r}_{c}", width="stretch"):
                    placed = {p: item for p, item in placed.items() if item[0] != piece}
                    placed[pos] = (piece, turns)
                    state.map_placed = placed
                    used = {n for n, _ in placed.values()}
                    state.map_piece_selected = next((n for n in pieces if n not in used), piece)
                    st.rerun()
    matches, conflicts = map_seams(placed)
    st.write(f"**{len(placed)}/7** eingesetzt · **{matches}/8** passende Nähte")
    if conflicts:
        st.caption(f"{conflicts} Kanten passen noch nicht zusammen oder liegen am falschen Außenrand.")
    if assembled:
        st.success("Die Karte passt. Folgt der Linie von der Fahne bis zur Eiswand.")
        columns = st.columns(3)
        for col, mark in zip(columns, ("Mond", "Stern", "Tanne")):
            if col.button(mark, key=f"wall_{mark}"):
                if mark == "Stern":
                    solve(day)
                st.error("An dieser Stelle bleibt die Eiswand geschlossen.")
    if placed:
        st.button("Kartenrahmen leeren", on_click=reset_fields,
                  args=("map_placed", "map_rotations", "map_piece_selected"))


def set_map_selection(piece):
    st.session_state.map_piece_selected = piece


# ---- 13: Generator (Lights Out)

def door13(day):
    circuits = {"Flurlicht": 2, "Steuerung": 3, "Förderband": 3, "Aufzug": 4, "Backofen": 5}
    selected = st.session_state.setdefault("backup_circuits", set())
    st.write("Volts Notiz: „Wir brauchen Licht im Flur. Zum Prüfen muss das Förderband laufen. "
             "Das Band braucht seine Steuerung. Der Aufzug bleibt vorerst aus.“")
    for name, power in circuits.items():
        active = name in selected
        if st.button(f"{'●' if active else '○'} {name} · {power} Einheiten", key=f"power_{name}",
                     type="primary" if active else "secondary", width="stretch"):
            selected.symmetric_difference_update({name})
            st.rerun()
    used = sum(circuits[name] for name in selected)
    st.progress(min(used / 8, 1.0), text=f"{used} von 8 Einheiten belegt")
    if used > 8:
        st.warning("Zu viel für den Notstrom. Schaltet einen Stromkreis wieder aus.")
    if st.button("Notstrom starten", disabled=used > 8, type="primary"):
        if selected == {"Flurlicht", "Steuerung", "Förderband"}:
            solve(day)
        st.error("Mit dieser Auswahl fehlen noch Stromkreise für Volts Auftrag.")


def order_cards(day, cards, answer, action, heading):
    key = f"order_{day}"
    order = st.session_state.setdefault(key, [])
    for card, label in cards.items():
        if st.button(label, key=f"card_{day}_{card}", disabled=card in order, width="stretch"):
            order.append(card)
            st.rerun()
    st.markdown(f"**{heading}**")
    st.write(" → ".join(cards[card] for card in order) if order else "Noch leer.")
    left, middle, right = st.columns(3)
    if left.button(action, key=f"order_check_{day}", disabled=len(order) != len(cards), type="primary"):
        if tuple(order) == answer:
            solve(day)
        st.error("Die Reihenfolge stimmt noch nicht.")
    if middle.button("Letzte Karte zurück", key=f"order_undo_{day}", disabled=not order):
        order.pop()
        st.rerun()
    right.button("Alles zurücksetzen", key=f"order_reset_{day}", on_click=reset_fields, args=(key,))


def door14(day):
    packages = {
        "A": "📦 A · Spanien · 3 kg",
        "B": "📦 B · Italien · 5 kg · Express",
        "C": "📦 C · Spanien · 1 kg",
        "D": "📦 D · Finnland · 2 kg · Express",
        "E": "📦 E · Italien · 2 kg",
    }
    st.markdown("Klickt die Pakete in der Reihenfolge an, in der sie aufs Band sollen.")
    st.markdown("1. Express zuerst.\n2. Innerhalb jeder Gruppe nach Zielland von A bis Z.\n"
                "3. Beim gleichen Zielland kommt das leichtere Paket zuerst.")
    order_cards(day, packages, tuple("DBECA"), "Band starten", "Förderband")



LIFT_CARTS = {
    "A": ("Geschenkpapier", 0, 1),
    "B": ("Geschenke", 0, 2),
    "C": ("Breiter Wagen", 0, 2),
    "D": ("Leere Kisten", 1, 0),
}
FLOORS = ("Packhalle", "Materiallager", "Verladung")


def door15(day):
    state = st.session_state
    floor, locations, load = state.setdefault(
        "lift", (0, {cart: start for cart, (_, start, _) in LIFT_CARTS.items()}, set())
    )
    st.caption("Klickt einen Wagen auf der aktuellen Ebene an, um ihn einzuladen oder auszuladen. "
               "In die Kabine passen zwei normale Wagen. Der breite Wagen fährt allein.")
    for level, col in enumerate(st.columns(3)):
        col.markdown(f"**{level} · {FLOORS[level]}**")
        for cart, (name, _, destination) in LIFT_CARTS.items():
            if locations[cart] != level and not (cart in load and level == floor):
                continue
            aboard = cart in load
            if col.button(f"{'🛗' if aboard else '📦'} {name} → {destination}",
                          key=f"lift_cart_{cart}", disabled=floor != level,
                          help="Ausladen" if aboard else "Einladen", width="stretch"):
                if aboard:
                    load.remove(cart)
                    locations[cart] = floor
                    if all(locations[k] == dest for k, (_, _, dest) in LIFT_CARTS.items()) and not load:
                        solve(day)
                elif len(load) == 2 or ("C" in load or cart == "C") and load:
                    st.warning("Der Wagen passt mit dieser Ladung nicht in die Kabine.")
                    continue
                else:
                    load.add(cart)
                    locations[cart] = -1
                st.rerun()
        if col.button("🛗 Aufzug hier" if level == floor else "Hierher fahren",
                      key=f"lift_floor_{level}", disabled=level == floor, width="stretch"):
            state.lift = (level, locations, load)
            st.rerun()
    st.write(f"**Kabine auf Ebene {floor}** · " + (", ".join(LIFT_CARTS[k][0] for k in LIFT_CARTS if k in load) or "leer"))
    st.button("Aufzug zurücksetzen", on_click=reset_fields, args=("lift",))



def door16(day):
    state = st.session_state
    stacks = state.setdefault("stacks", [[4, 3, 2, 1], [], []])
    source = state.get("stack_source")
    st.caption("Klickt das oberste Paket und dann den Zielplatz an. Ein größeres Paket darf nie auf einem kleineren liegen.")
    for i, col in enumerate(st.columns(3)):
        stack = stacks[i]
        col.markdown(f"**Platz {i+1}**")
        boxes = "".join(
            f'<div style="background:#d8ac72;color:#392317;border:1px solid #684624;width:{32+size*16}%;'
            f'text-align:center;margin:2px auto">📦 {size}</div>' for size in reversed(stack)
        )
        col.markdown(f'<div style="height:115px;display:flex;flex-direction:column;justify-content:flex-end">'
                     f'{boxes}</div>', unsafe_allow_html=True)
        label = "Hier ablegen" if source is not None and source != i else (
            "Auswahl lösen" if source == i else f"Paket {stack[-1]} nehmen" if stack else "Platz frei"
        )
        if col.button(label, key=f"stack{i}", disabled=source is None and not stack,
                      type="primary" if i == source else "secondary", width="stretch"):
            if source is None:
                state.stack_source = i
            elif source == i:
                state.stack_source = None
            elif stack and stack[-1] < stacks[source][-1]:
                st.warning("Das größere Paket passt nicht auf das kleinere.")
                continue
            else:
                stack.append(stacks[source].pop())
                state.stack_source = None
                state.stack_moves = state.get("stack_moves", 0) + 1
                if stacks[2] == [4, 3, 2, 1]:
                    solve(day)
            st.rerun()
    st.caption(f"Züge: {state.get('stack_moves', 0)}")
    st.button("Stapel zurücksetzen", on_click=reset_fields, args=("stacks", "stack_source", "stack_moves"))


def door17(day):
    recipe = (3, 2, 1)
    troughs = {"Kufe": 12, "Mohn": 18}
    st.write("**Gustavs Rezeptkarte** · 3 Teile Heu, 2 Teile Hafer, 1 Teil Karotten.")
    with st.form("feed"):
        mixtures = {}
        for name, total in troughs.items():
            st.markdown(f"**{name} · {total} Portionen**")
            mixtures[name] = tuple(
                col.number_input(ingredient, min_value=0, max_value=total, step=1, key=f"feed_{name}_{i}")
                for i, (col, ingredient) in enumerate(zip(st.columns(3), ("Heu", "Hafer", "Karotten")))
            )
        if st.form_submit_button("Futtertröge prüfen"):
            if all(mixtures[name] == tuple(total * part // sum(recipe) for part in recipe)
                   for name, total in troughs.items()):
                solve(day)
            for name, mixture in mixtures.items():
                total = troughs[name]
                if sum(mixture) != total:
                    st.warning(f"{name}: Im Trog sind {sum(mixture)} von {total} Portionen.")
                elif mixture != tuple(total * part // sum(recipe) for part in recipe):
                    st.warning(f"{name}: Die Gesamtmenge stimmt. Prüft noch die Mischung.")


def scale_html(left, right, result):
    angle = 10 if result == "Links leichter" else -10 if result == "Rechts leichter" else 0
    return (
        f'<svg viewBox="0 0 400 145" style="width:100%;max-width:370px" role="img" '
        f'aria-label="{result or "Waage bereit"}"><path d="M200 45L165 130H235Z" fill="#c39966"/>'
        f'<g transform="rotate({angle} 200 45)" stroke="#ffd68c" stroke-width="4" fill="none">'
        '<path d="M85 45H315M85 45L50 101H120Z M315 45L280 101H350Z"/>'
        f'<text x="85" y="125" stroke="none" fill="#fff5db" text-anchor="middle">{", ".join(map(str,left)) or "–"}</text>'
        f'<text x="315" y="125" stroke="none" fill="#fff5db" text-anchor="middle">{", ".join(map(str,right)) or "–"}</text>'
        '</g></svg>'
    )


def door18(day):
    state = st.session_state
    if "light_dose" not in state:
        state.light_dose = random.randint(1, 9)
    light = state.light_dose
    rounds = state.setdefault("weighings", [])
    numbers = tuple(range(1, 10))
    candidates = set(numbers)
    for i, (left, right, outcome) in enumerate(rounds, 1):
        with st.expander(f"Wägung {i} · {outcome}", expanded=True):
            st.markdown(scale_html(left, right, outcome), unsafe_allow_html=True)
        if outcome == "Links leichter":
            candidates.intersection_update(left)
        elif outcome == "Rechts leichter":
            candidates.intersection_update(right)
        else:
            candidates.difference_update(left + right)
    if len(rounds) < 2 and len(candidates) > 1:
        picks = state.setdefault("scale_picks", {})
        side = st.radio("Dose auf diese Schale setzen", ("Links", "Rechts"), horizontal=True)
        st.caption("Klickt eine Dose erneut für dieselbe Schale an, um sie herunterzunehmen.")
        for row in range(3):
            for col, number in zip(st.columns(3), numbers[row*3:row*3+3]):
                mark = {"Links": " · L", "Rechts": " · R"}.get(picks.get(number), "")
                if col.button(f"🥫 {number}{mark}", key=f"dose_{number}", width="stretch"):
                    if picks.get(number) == side:
                        picks.pop(number)
                    else:
                        picks[number] = side
                    st.rerun()
        left = sorted(n for n in picks if picks[n] == "Links")
        right = sorted(n for n in picks if picks[n] == "Rechts")
        st.markdown(scale_html(left, right, ""), unsafe_allow_html=True)
        if st.button("Wiegen", disabled=not left or len(left) != len(right)):
            result = "Links leichter" if light in left else "Rechts leichter" if light in right else "Gleich schwer"
            rounds.append((left, right, result))
            state.scale_picks = {}
            st.rerun()
    if len(rounds) == 2 and len(candidates) > 1:
        st.warning("Mehrere Dosen kommen noch infrage. Setzt die Waage zurück und probiert es erneut.")
    if len(candidates) == 1:
        with st.form("dose_guess"):
            suspect = st.selectbox("Welche Dose ist leichter?", numbers, index=None)
            if st.form_submit_button("Dose prüfen"):
                if suspect == light:
                    solve(day)
                st.warning("Schaut euch die Ergebnisse der Waage noch einmal an.")
    st.button("Waage zurücksetzen", on_click=reset_fields, args=("weighings", "scale_picks"))


def door19(day):
    code = st.session_state.setdefault("safe_code", [])
    st.caption("Vier verschiedene Ziffern. Die Rückmeldungen auf dem Zettel beziehen sich auf den geheimen Code.")
    panel, note = st.columns([1, 1.2])
    with panel:
        windows = "".join(
            f'<span style="display:inline-grid;place-items:center;width:21%;height:48px;border:2px solid #b58b54;'
            f'background:#211a17;color:#fff0b9;font-size:1.4rem">{code[i] if i < len(code) else "–"}</span>'
            for i in range(4)
        )
        st.markdown(f'<div style="display:flex;justify-content:space-between;background:#3d4449;padding:12px">{windows}</div>',
                    unsafe_allow_html=True)
        for digits in ("123", "456", "789", "0"):
            for col, digit in zip(st.columns(3), digits):
                if col.button(digit, key=f"safe_{digit}", disabled=len(code) == 4 or digit in code, width="stretch"):
                    code.append(digit)
                    st.rerun()
        undo, check = st.columns(2)
        if undo.button("⌫ Löschen", disabled=not code):
            code.pop()
            st.rerun()
        if check.button("Öffnen", disabled=len(code) != 4, type="primary"):
            if "".join(code) == "4817":
                solve(day)
            st.error("Der Tresor bleibt verschlossen.")
    with note:
        st.markdown(
            '<div style="background:#f5dfb2;color:#302317;padding:12px;border-radius:4px">'
            '<strong>Frühere Versuche</strong><table style="width:100%;margin-top:8px">'
            '<tr><th>Code</th><th>Richtige Stelle</th><th>Falsche Stelle</th></tr>'
            + "".join(f"<tr><td>{guess}</td><td>{right}</td><td>{wrong}</td></tr>"
                      for guess, right, wrong in (("6370",0,1),("5431",0,2),("4017",3,0),("5179",0,2),("2073",0,1)))
            + "</table></div>", unsafe_allow_html=True
        )


def door21(day):
    st.write("**Testauftrag von Fussel** · Prüft nur den Wagen, auf dem das Probepaket für Schneedorf liegt.")
    left, right = st.columns(2)
    left.markdown("**Wagenliste**  \n5 · Eisfeld  \n7 · Schneedorf  \n9 · Winterau")
    right.markdown("**Ausgangsplan**  \nKlappe A · Ost: Eisfeld, Sternbrück  \n"
                   "Klappe B · Nord: Schneedorf, Tannenwinkel  \nKlappe C · West: Winterau, Flockental")
    with st.form("sort_test"):
        mode = st.radio("Umfang", ("Ganze Anlage", "Einzelner Wagen"), horizontal=True, index=None)
        cart = st.radio("Wagen", (5, 7, 9), horizontal=True, index=None)
        route = st.radio("Route", ("Ost", "Nord", "West"), horizontal=True, index=None)
        exit_gate = st.radio("Ausgang", ("A", "B", "C"), horizontal=True, index=None)
        if st.form_submit_button("Probepaket losschicken"):
            if None in (mode, cart, route, exit_gate):
                st.warning("Stellt alle vier Regler ein.")
            elif mode != "Einzelner Wagen":
                st.warning("Die Anlage hält den Versuch an. Es ist wieder die ganze Halle ausgewählt.")
            elif (cart, route) != (7, "Nord"):
                st.warning("Das Probepaket erreicht den Prüfplatz, aber Wagen oder Route stimmen noch nicht.")
            elif exit_gate != "B":
                st.warning(f"Das Probepaket landet an Klappe {exit_gate}. Schneedorf gehört zu Klappe B.")
            else:
                solve(day)


DELIVERY_ROUTES = {
    "Nord": ("Schneedorf", "Tannenwinkel"),
    "Ost": ("Sternbrück", "Eisfeld"),
    "West": ("Flockental", "Winterau"),
}
DELIVERY_CARTS = {"7": "Schneedorf", "5": "Eisfeld", "9": "Winterau", "3": "Tannenwinkel"}


def door22(day):
    st.caption("Ordnet jedem Wagen die Route zu, die seinen Zielort anfährt.")
    for col, (route, stops) in zip(st.columns(3), DELIVERY_ROUTES.items()):
        col.markdown(f"**{route}**")
        col.markdown("🛷 Werkstatt" + "".join(f"  \n↓  \n📍 {stop}" for stop in stops))
    with st.form("route_loading"):
        assignments = {cart: st.selectbox(f"Wagen {cart} · {town}", tuple(DELIVERY_ROUTES), index=None)
                       for cart, town in DELIVERY_CARTS.items()}
        if st.form_submit_button("Verladung prüfen"):
            if all(route and DELIVERY_CARTS[cart] in DELIVERY_ROUTES[route] for cart, route in assignments.items()):
                solve(day)
            st.warning("Mindestens ein Wagen fehlt auf seiner Route oder ist falsch zugeordnet.")


def door23(day):
    state = st.session_state
    lineup = state.setdefault("reindeer_slots", [None] * 4)
    selected = state.get("reindeer_selected")
    st.markdown("- Mohn steht direkt vor Flocke.\n- Kufe steht vor Glut.\n"
                "- Flocke und Glut stehen beide nicht an zweiter Stelle.")
    st.caption("Wählt ein Rentier und klickt auf seinen Platz. Ein dort stehendes Rentier kommt zurück in die Auswahl.")
    for col, name in zip(st.columns(4), ("Mohn", "Glut", "Flocke", "Kufe")):
        if col.button(name, key=f"deer_{name}", type="primary" if selected == name else "secondary", width="stretch"):
            state.reindeer_selected = name
            st.rerun()
    st.write("**Vorn → direkt vor dem Schlitten 🛷**")
    for i, col in enumerate(st.columns(4)):
        if col.button(f"{i+1} · {lineup[i] or 'frei'}", key=f"harness_{i}",
                      disabled=selected is None, width="stretch"):
            if selected in lineup:
                lineup[lineup.index(selected)] = None
            lineup[i] = selected
            state.reindeer_selected = None
            st.rerun()
    if st.button("Gespann prüfen", disabled=None in lineup, type="primary"):
        if lineup == ["Kufe", "Mohn", "Flocke", "Glut"]:
            solve(day)
        st.warning("Die Reihenfolge passt noch nicht zu allen Hinweisen.")
    st.button("Gespann zurücksetzen", on_click=reset_fields, args=("reindeer_slots", "reindeer_selected"))


def door24(day):
    st.write("**Erster Halt: Schneedorf · Laternenweg 7**")
    for address in ("Tannenwinkel · Laternenweg 7", "Schneedorf · Glockenweg 7", "Schneedorf · Laternenweg 7"):
        if st.button(f"📦 {address}", key=f"first_delivery_{address}", width="stretch"):
            if address == "Schneedorf · Laternenweg 7":
                solve(day)
            st.warning("Vergleicht Ort, Straße und Hausnummer mit Hollys Liste.")


PLAN = ["BBBMMM", "BBPMMM", "KKPPGG", "KKPSGG", "KSSSSG", "KKSSSG"]
ROOMS = {"B": ("Büro", "#e8c9c9"), "M": ("Masch.", "#c9d6e8"), "P": ("Pack.", "#efe6c4"),
         "K": ("Backstube", "#f2d4b0"), "G": ("Generator", "#d9c9ea"), "S": ("Stall", "#c9e8d1")}
SOLUTION = {"Holly": "1B", "Schraub": "2E", "Volt": "3C", "Fussel": "4F", "Zimta": "5A", "Gustav": "6D"}


def plan_html(positions=None):
    occupants = {cell: name for name, cell in (positions or {}).items()}
    th = "color:#ffd700;padding:4px 10px"
    h = "<table style='border-collapse:collapse;margin:8px auto'><tr><td></td>"
    h += "".join(f"<th style='{th}'>{c}</th>" for c in "ABCDEF") + "</tr>"
    for r, row in enumerate(PLAN):
        h += f"<tr><th style='{th}'>{r + 1}</th>"
        for c, k in zip("ABCDEF", row):
            name, col = ROOMS[k]
            occupant = occupants.get(f"{r+1}{c}")
            if occupant:
                name += f"<br><strong>{occupant}</strong>"
            h += (f"<td style='background:{col};color:#444;border:1px solid #0b2d1d;width:78px;height:40px;"
                  f"text-align:center;font-size:.7rem'>{name}</td>")
        h += "</tr>"
    return h + "</table>"


def door20(day):
    state = st.session_state
    placements = state.setdefault("elf_positions", {})
    crosses = state.setdefault("elf_crosses", {})
    st.write("Um 22:47 stand genau ein Elf im Generatorraum. Setzt je einen Elf in jede Zeile und jede Spalte.")
    with st.expander("Aussagen und Protokoll lesen", expanded=True):
        for n in (13, 14, 15, 16, 17, 18, 19):
            if n in game["solved"]:
                st.write(game["akte"][str(n)])
            elif TEST:
                st.write(DOORS[n]["akte"])
        if TEST and any(n not in game["solved"] for n in range(13, 20)):
            st.caption("Im Direkt-Test stehen hier auch Hinweise aus übersprungenen Türchen.")
    elf = st.selectbox("Elf auswählen", tuple(SOLUTION))
    mode = st.radio("Was möchtet ihr markieren?", ("× Ausschließen", "✓ Platzieren"), horizontal=True)
    marks = crosses.setdefault(elf, set())
    taken = {cell: name for name, cell in placements.items() if name != elf}
    st.caption("Ein Kreuz gilt nur für den gewählten Elf. Erneut klicken entfernt es. "
               "Beim Platzieren sind Zeilen und Spalten mit einem anderen Elf gesperrt.")
    for row, rooms in enumerate(PLAN, 1):
        cols = st.columns(6, gap="small")
        for column, room, col in zip("ABCDEF", rooms, cols):
            cell = f"{row}{column}"
            selected = placements.get(elf) == cell
            blocked = any(other[0] == cell[0] or other[1] == cell[1] for other in taken)
            occupant = taken.get(cell)
            icon = f"✓ {elf}" if selected else f"× · {occupant}" if occupant and cell in marks else (
                occupant or ("×" if cell in marks else "·" if blocked else "")
            )
            name, color = ROOMS[room]
            col.markdown(
                f'<div style="background:{color};color:#222;text-align:center;padding:3px;font-size:.8rem">'
                f'{name}</div>', unsafe_allow_html=True,
            )
            if col.button(f"{column}{row} {icon}".strip(), key=f"murdoku_{cell}",
                          disabled=(mode == "✓ Platzieren" and blocked) or (mode == "× Ausschließen" and selected),
                          type="primary" if selected else "secondary", width="stretch"):
                if mode == "× Ausschließen":
                    marks.symmetric_difference_update({cell})
                elif selected:
                    placements.pop(elf)
                else:
                    placements[elf] = cell
                    marks.discard(cell)
                st.rerun()
    st.write(f"**{len(placements)}/6 Elfen platziert**")
    who = st.selectbox("Wer war im Generatorraum?", tuple(SOLUTION), index=None)
    if st.button("Fall lösen", type="primary", disabled=len(placements) != 6 or who is None):
        if placements != SOLUTION:
            st.error("Mindestens eine Position passt noch nicht zu den Aussagen.")
        elif who != "Fussel":
            st.error("Die Plätze stimmen. Schaut nach, wer im Generatorraum steht.")
        else:
            solve(day)
    st.button("Plan und Kreuze leeren", on_click=reset_fields, args=("elf_positions", "elf_crosses"))


def D(title, story, render, akte, after, *hints):
    return dict(title=title, story=story, render=render, akte=akte, after=after, hints=list(hints))


DUTY = ("Dienstplan 22:47: Holly, Schraub, Volt, Zimta, Fussel und Gustav standen auf dem Grundriss der Werkstatt "
        "(6 Zeilen, Spalten A bis F, Räume farbig). In jeder Zeile und in jeder Spalte stand genau ein Elf.")

DOORS = {}

DOORS.update({
    1: D("Türchen 1 · Die Kiste vom Nordpol",
         "Es klingelt. Vor der Tür steht ein eisiges Päckchen. Als Absender steht darauf: NORDPOL. "
         "Darin findet ihr eine Holzbox mit Zahlenschloss. Seitlich ist ein Gedicht ins Holz geritzt.",
         door1, "Absender des Päckchens: NORDPOL.",
         "Das Schloss klackt. Die Kiste springt auf. Obenauf liegt ein Brief.",
         "Zählt die Wörter in jeder Zeile. Was fällt euch auf?",
         "Lest die Anfangsbuchstaben der Wörter jeder Zeile von links nach rechts.",
         "Draußen ruht ein Irrlicht ergibt D–R–E–I. Die erste Ziffer ist 3."),
    2: D("Türchen 2 · Der verschlüsselte Brief",
         "Ihr öffnet den Brief und zieht einen gefalteten Zettel heraus. Die Buchstaben ergeben keinen Sinn. "
         "In der Ecke erkennt ihr einen blassen Lorbeerkranz.",
         door2, "Der Hauptschalter wurde von Hand umgelegt. Das Rufwort lautet LATERNE.",
         "„Laterne. Laterne. Laterne.“ Erst bleibt es still. Dann hört ihr draußen ein leises Läuten. "
         "Es kommt näher und verstummt vor dem Fenster. Draußen stehen vier Rentiere im Schnee. "
         "Eines hebt den Kopf. „Ihr habt gerufen?“",
         "Der Lorbeerkranz weist auf Caesar und seine Geheimschrift hin.",
         "Wer hat das Päckchen geschickt? Zählt die Buchstaben des Absenders.",
         "Geht für jeden Buchstaben sieben Stellen zurück. Vor A geht es bei Z weiter. KLY wird zu DER."),
    3: D("Türchen 3 · Die Rentierprüfung",
         "Ihr geht hinaus. „Das Rufwort hat euch zu uns geführt“, sagt eines der Rentiere. „Aber für den Flug müssen wir "
         "wissen, ob ihr euch mit unserem Gespann auskennt. Ihr sitzt vorn mit uns. Bei schlechter Sicht müssen wir uns "
         "auf kurze Zurufe verlassen können. Kennt ihr die Antworten auf unsere drei Fragen?“",
         door3, "Die Rentiere am Schlitten sind Kühe. In Kanada heißen Rentiere Karibus.",
         "„Na gut“, sagt das Rentier. „Steigt ein.“ Ihr klettert auf die Sitzbank. Unter der dicken Wolldecke wird euch wieder warm.",
         "Alle vier Rentiere vor euch tragen im Dezember ein Geweih.",
         "Elch und Wapiti sind andere Tiere.",
         "Die gesuchte Farbe erinnert an einen klaren Winterhimmel."),
    4: D("Türchen 4 · Der Kurs zum Nordpol",
         "„Gebt uns einen Kurs, dann können wir los.“ Am Bordcomputer blinkt ein Koordinatenfeld. Daneben steckt eine Sternkarte.",
         door4, "Der Kurs zum Polarstern ist bestätigt.",
         "Die Kufen gleiten über den Schnee und heben ab. Unter euch werden die beleuchteten Fenster immer kleiner.",
         "Zählt die Kästchen von Merak nach Dubhe. Die senkrechte Achse wird nach oben größer.",
         "Ein Schritt geht ein Feld nach rechts und ein Feld nach oben.",
         "Beginnt bei Dubhe auf (3|3) und macht von dort zwei solche Schritte."),
    5: D("Türchen 5 · Das Labyrinth im Nebel",
         "Dichter Nebel zwingt den Schlitten zur Landung. Vor euch ragen Eiswände aus dem Schnee. „Am anderen Ende steht "
         "eine Weglaterne“, sagt eines der Rentiere. „Zündet sie an, dann finden wir euch wieder.“",
         door5, "Wegkartenstück 1 von 7.",
         "Im Licht der Laterne entdeckt ihr ein Stück einer Wegkarte. Ihr steckt es ein. Kurz darauf hört ihr Schlittenglocken.",
         "Geht vom Eingang zuerst nach Osten.", "Geht an der ersten Eiswand nach Süden und sucht einen Gang nach Osten.",
         "Haltet euch am Ende am rechten Rand nach Süden."),
    6: D("Türchen 6 · Der Eishang",
         "Beim Abholen hat sich ein Werkzeug vom Schlitten gelöst. Es liegt unten auf dem spiegelglatten Eishang.",
         door6, "Wegkartenstück 2 von 7.", "Ihr hebt das Werkzeug auf. Darunter klebt ein Stück der Wegkarte.",
         "Plant rückwärts. Überlegt, aus welcher Richtung ihr auf dem Werkzeugfeld zum Stehen kommt.",
         "Von oben könnt ihr auf dem Werkzeugfeld anhalten. Sucht eine Position in derselben Spalte."),
    7: D("Türchen 7 · Der Frostgeist",
         "Ein Frostgeist kennt den sicheren Weg über den See. Er zeigt ihn euch, wenn ihr sein Eiszapfenspiel gewinnt. "
         "Abwechselnd nehmt ihr 1, 2 oder 3 Eiszapfen. Wer den letzten nimmt, gewinnt.",
         door7, "Wegkartenstück 3 von 7.", "Der Frostgeist schiebt euch ein Kartenstück zu und winkt euch auf den sicheren Weg.",
         "Es gibt einen ersten Zug, nach dem ihr jeden Gegenzug passend ergänzen könnt.",
         "Lasst dem Frostgeist nach jedem eurer Züge ein Vielfaches von vier."),
    8: D("Türchen 8 · Die Hängebrücke",
         "Holly, Gustav, Mira und Noel stehen vor einer schmalen Hängebrücke. Sie haben nur eine Laterne. Bringt alle in höchstens sieben Gängen hinüber.",
         door8, "Wegkartenstück 4 von 7 und eine Morsekarte.",
         "Drüben hängt ihr die Laterne an einen Haken. Daneben steht ein Kasten mit der Aufschrift NOTFUNK. Darin liegen ein Kartenstück und eine Morsekarte.",
         "Schickt zuerst Mira und Noel zusammen hinüber.", "Holt die Laterne zurück, damit Gustav allein hinübergehen kann."),
    9: D("Türchen 9 · Der Notruf der Werkstatt",
         "Am Notfunkkasten blinkt eine Lampe. Aus dem Lautsprecher kommen kurze und lange Töne. Nach einer Pause wiederholt sich der Spruch.",
         door9, "Wegkartenstück 5 von 7. Notruf der Werkstatt: TOR IM EIS.",
         "„Tor im Eis“, lest ihr vor. Unter dem Deckel der Empfangsstation klemmt ein weiteres Kartenstück.",
         "Ein kurzer Ton ist ein Punkt, ein langer ein Strich.", "Spielt die Wörter einzeln ab und vergleicht die Signale mit der Morsekarte."),
    10: D("Türchen 10 · Der verborgene Durchgang",
          "Vor euch liegen mehrere Spalten im Eis. Ein alter Lichtwegweiser kann den richtigen Durchgang markieren.",
          door10, "Wegkartenstück 6 von 7.", "Unter der beleuchteten Markierung findet ihr einen schmalen Durchgang. Daneben steckt ein Kartenstück.",
          "Dreht die Spiegel durch Anklicken. Der leuchtende Stern zeigt, welche Felder der Strahl erreicht.",
          "Versucht, den Strahl in der mittleren Zeile bis zum Spiegel ganz rechts zu lenken."),
    11: D("Türchen 11 · Die letzte Schlucht",
          "Ein Stück des Wegs ist weggebrochen. In einer Nische liegen drei Eisplatten. Damit könnt ihr die Lücke schließen.",
          door11, "Wegkartenstück 7 von 7.", "Ihr überquert die Schlucht. Auf der anderen Seite hängt ein Kartenstück an einem Wegpfosten.",
          "Die gerade Platte passt waagerecht über drei Felder oder senkrecht über drei Zeilen."),
    12: D("Türchen 12 · Das Werkstatttor",
          "Ihr steht vor einer Eiswand. Der Funkspruch hat euch verraten, dass hier das Tor liegt. Setzt eure Wegkarte zusammen und findet den Eingang.",
          door12, "Der Eingang zur Werkstatt ist geöffnet.",
          "Das Eis unter der Markierung schiebt sich beiseite. Ihr tretet über die Schwelle. In der Werkstatt ist es dunkel.",
          "Die Fahne markiert den linken Rand. Dreht die Kartenstücke, bis sich gleiche Nahtsymbole berühren.",
          "Die Linie führt von der Fahne zu einer Markierung an der Außenkante."),
})

DOORS.update({
    13: D("Türchen 13 · Die Notstromtafel",
          "Hinter dem Tor ist es dunkel. Volt winkt euch mit seiner Laterne zu einer kleinen Notstromtafel. "
          "Seit 22:47 steht die Werkstatt still. Jetzt braucht er Licht und Strom für den ersten Check am Förderband.",
          door13, "Volt · 22:47 · Ich stand in Spalte C, weder im Büro noch in der Maschinenhalle.",
          "Die Lampen im Flur springen an. Volt bittet euch, beim Aufräumen die Elfen zu fragen, wo sie beim Stromausfall waren.",
          "Die Notiz nennt drei Stromkreise. Zusammen brauchen sie genau acht Einheiten."),
    14: D("Türchen 14 · Das Förderband",
          "In der Packhalle warten fünf Pakete darauf, auf dem Prüfband von Hand sortiert zu werden. Fussel reicht euch die Sortierregeln.",
          door14,
          "Fussel: Ich war weder im Büro noch in der Maschinenhalle. Ich stand oberhalb von Zimta. Fund: Ein falsches Ziel-Etikett trägt den Zeitstempel 22:45.",
          "Das erste Band ist wieder frei. Unter einem Paket findet ihr ein falsches Ziel-Etikett von 22:45. Da war der Strom noch an.",
          "Nur zwei Pakete sind Express. Sortiert sie zuerst nach Land.",
          "Die beiden normalen Pakete nach Spanien kommen hinter das normale Paket nach Italien."),
    15: D("Türchen 15 · Der Lastenaufzug",
          "Schraub hat den Aufzug wieder betriebsbereit gemacht. Vier Wagen stehen zwischen Packhalle, Materiallager und Verladung fest. Bringt sie zu ihren Zielen.",
          door15,
          "Schraub: Ich stand in Spalte E, weder im Generatorraum noch in der Packhalle. Meine Zeile grenzte direkt an Volts Zeile.",
          "Der letzte Wagen rollt auf seine Ebene. Schraub erzählt euch, wo er um 22:47 stand.",
          "Ihr könnt auf einer Ebene Wagen ausladen und andere einladen, bevor ihr weiterfahrt."),
    16: D("Türchen 16 · Die Paketstapel",
          "Holly braucht Platz auf der Ladefläche. Setzt den Stapel mit vier Paketen von Platz 1 auf Platz 3 um.",
          door16,
          "Holly: Ich stand in Spalte B, weder im Generatorraum noch im Stall.",
          "Der Stapel steht am Ziel. Holly kann den nächsten Wagen hereinrollen und gibt euch ihre Aussage für die Akte.",
          "Räumt die drei kleineren Pakete zuerst auf Platz 2. Dann kann das größte direkt auf Platz 3."),
    17: D("Türchen 17 · Futter für die Rentiere",
          "Im Stall bereitet Gustav die Tröge für den Abflug vor. Kufe und Mohn brauchen unterschiedlich viel Futter, aber dieselbe Mischung.",
          door17, "Gustav: Ich war beim Stromausfall im Stall bei den Rentieren.",
          "Gustav stellt die fertigen Tröge hin. Während die Rentiere fressen, erzählt er euch, wo er beim Ausfall war.",
          "Eine vollständige Mischung besteht aus sechs Teilen. Überlegt, wie oft sie in jeden Trog passt."),
    18: D("Türchen 18 · Die Plätzchendosen",
          "Zimta hat neun gleich aussehende Dosen für die Reiseverpflegung. Eine ist leichter. Findet sie mit höchstens zwei Wägungen.",
          door18, "Zimta: Ich war in der Backstube in Zeile 5. Volt stand zwei Zeilen unter Holly.",
          "In der leichten Dose fehlen Plätzchen. Zimta tauscht sie aus und erzählt euch, wo sie um 22:47 stand.",
          "Teilt die Dosen in drei Gruppen mit je drei Dosen und wiegt zwei Gruppen gegeneinander.",
          "Bei Gleichstand liegt die leichte Dose in der dritten Gruppe. Wiegt anschließend zwei Dosen aus der verdächtigen Gruppe gegeneinander."),
    19: D("Türchen 19 · Der Tresor",
          "Im Büro klebt ein Zettel mit früheren Versuchen am Tresor. Dahinter liegen die Unterlagen zur letzten Schicht.",
          door19,
          DUTY + " Protokoll: 22:44 Teststart an der gesamten Anlage. 22:45 falsche Ziele. 22:47 Hauptschalter von Hand umgelegt. Er steht im Generatorraum, dort war nur ein Elf.",
          "Der Tresor springt auf. Im Protokoll steht: Erst begann der Testlauf an der gesamten Anlage, dann liefen die Pakete falsch. Zwei Minuten später ging der Strom aus.",
          "Bei 4017 sind drei Ziffern am richtigen Platz. Testet, welche ausgetauscht werden muss."),
    20: D("Türchen 20 · Wer war am Schalter?",
          "Legt die Aussagen neben den Werkstattplan. Wer stand um 22:47 im Generatorraum und legte den Hauptschalter um?",
          door20, "Fall gelöst: Fussel stoppte den fehlgeleiteten Sortierlauf am Hauptschalter.",
          "Fussel blickt auf den Plan. „Ich wollte nur Wagen sieben testen. Aus Versehen habe ich die ganze Anlage ausgewählt. "
          "Als die Pakete falsch liefen, habe ich den Hauptschalter umgelegt. Danach habe ich mich nicht getraut, es zu sagen.“ "
          "Holly schiebt ihm das Protokoll hin. „Dann zeig uns morgen, wie wir den Test richtig machen.“",
          "Beginnt bei Holly, Volt und Schraub. Ihre Spalten stehen fest.",
          "Zimta stand in Zeile 5 in der Backstube. Gustav war im Stall."),
    21: D("Türchen 21 · Der sichere Neustart",
          "Fussel steht wieder am Schaltpult. Dieses Mal soll erst ein einziges Probepaket durchlaufen, bevor die Anlage weiter sortiert.",
          door21, "Der Testlauf mit Wagen 7 und Klappe B war erfolgreich.",
          "Das Probepaket kommt an der richtigen Klappe an. Fussel gibt das Zeichen für die restlichen Wagen.",
          "Prüft zuerst den Umfang. Es geht um einen einzelnen Wagen."),
    22: D("Türchen 22 · Die Schlitten beladen",
          "Die Pakete sind wieder auf den richtigen Wagen. An der Verladung zeigt Holly euch, welche Orte auf welcher Route liegen.",
          door22, "Alle Paketwagen sind ihren Auslieferrouten zugeordnet.",
          "Die letzten Wagen werden verladen. Holly legt die Nordroute ganz oben auf die Abfahrtsliste.",
          "Die Nordroute fährt zwei Orte an. Ihr dürft ihr mehr als einen Wagen zuordnen."),
    23: D("Türchen 23 · Das Rentiergespann",
          "Die Geschenke sind verladen. Stellt Kufe, Mohn, Flocke und Glut an ihre Plätze vor dem Schlitten.",
          door23, "Das Rentiergespann ist abfahrbereit.",
          "Holly reicht Fussel die Liste für den ersten Halt. „Du kennst die Wagen inzwischen am besten. Hilfst du uns beim Verteilen?“",
          "Betrachtet Mohn und Flocke als festes Paar.",
          "Steht das Paar ganz hinten, müsste Glut an zweiter Stelle stehen."),
    24: D("Türchen 24 · Die erste Auslieferung",
          "Die Glocken läuten und der Schlitten hebt ab. Beim ersten Halt zieht Fussel drei Pakete nach vorn. Holly liest euch die Adresse vor. Welches nehmt ihr mit?",
          door24, "Das erste Geschenk ist ausgeliefert.",
          "Ihr reicht Fussel das Paket. Er trägt es mit Holly zur Tür, an der eine kleine Laterne brennt. "
          "Als sie wieder aufsteigen, liest er schon die nächste Adresse vor. Frohe Weihnachten! 🎄",
          "Auf der Nordroute gibt es zwei Orte. Achtet bei der Adresse auch auf die Straße."),
})

# Briefgrafik für Türchen 2
LETTER_PNG = (
    "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"
    "ERFRPVA0VbWvIyIiIiIionqgsAONiIiIiIjIGZgkhIiIiIiIyCE4DxoREREREZFDsAeNiIiIiIjIIZSgbtjXERERERERUT1QLJNB"
    "jkRERERERE6guN2afR0RERERERHVAwXsQCMiIiIiInIEzoNGRERERETkEMziSERERERE5BCcB42IiIiIiMghFMMw7euIiIiIiIio"
    "HiimyQoaERERERGREyiqymFoRERERERETqAoCitoRERERERETsDaGRERERERkUMonAaNiIiIiIjIGdiDRkRERERE5BCcB42IiIiI"
    "iMghlEBAt68jIiIiIiKieqAoHIVGRERERETkCIpLU+3riIiIiIiIqB5wDBoREREREZFDKGANjYiIiIiIyBEUwSFoREREREREjsB5"
    "0IiIiIiIiBxCCeiGfR0RERERERHVA8UyOQiNiIiIiIjICRS3W7OvIyIiIiIionrAaaqJiIiIiIgcgvOgEREREREROQTnQSMiIiIi"
    "InIIzoNGRERERETkEIphmvZ1REREREREVA8U3WAFjYiIiIiIyAkUVVHs64iIiIiIiKgeKJrKChoREREREZETsHZGRERERETkEJwH"
    "jYiIiIiIyCHYg0ZEREREROQQCqdBIyIiIiIicgYlENTt64iIiIiIiKgeKGAXGhERERERkSMoLlWzryMiIiIiIqJ6oAj2oBERERER"
    "ETkCszgSERERERE5BOdBIyIiIiIicggFrKERERERERE5gqIbhn0dERERERER1QPFNNmFRkRERERE5ASK2800+0RERERERE7ALI5E"
    "REREREQOoXAaNCIiIiIiImdgDxoREREREZFDcB40IiIiIiIih1BMw7SvIyIiIiIionqgGCYraERERERERE6gqAqHoRERERERETmB"
    "oqisoBERERERETmBAmYJISIiIiIicgRFcCI0IiIiIiIiR2B8IxERERERkUNwHjQiIiIiIiKHUAJB3b6OiIiIiIiI6oHCIWhERERE"
    "RETOoLhdmn0dERERERER1QOOQSMiIiIiInIIzoNGRERERETkEJwHjYiIiIiIyCE4DxoREREREZFDKEHdsK8jIiIiIiKieqCYJgeh"
    "EREREREROYHidqn2dURERERERFQPFMEsIURERERERI7AedCIiIiIiIgcglkciYiIiIiIHEJhgCMREREREZEzMIsjERERERGRQyhB"
    "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"
    "N3zk4Bz0zYkNx6xIXd3bE7E3/zDWbylv/EpN9uK80f0rvT+XZbd86x+3o1/PDtK2PTq3kvbb5ty9MQk2EG6cWrOpvHcgPTUJvbu3"
    "k7apa2s27pSOybD+3dCzcxtpG7vBvTtLx23nnoPYlFvz16QTzF28XmpUaJSWjN9cPxYpUb2ItS09NQnNa/hZE09aSpIUkfHx1Hlx"
    "hyjUpf0Hj1Tag+T1uCu9bmtSdEOpaVl47/M5JxTlVNvlFqp5ChpoDS2o63j1gxlS4XL86AE4d1TiPVfVMaxfV2m8x5FjJfh02gLM"
    "nLdaGijdo3NrnNq/ei00+w4WSmOsurRvgczGVad3HdCro9T7tGvvwTpvOavKmk07Iz0YihAxrVdpKV60bVmextueKGTn3oORELa+"
    "PdpLN6M1m3dJrcvRCUKSvR60bBY/FMgeJtAvpz08bhc6tM6WbqrHEy6w70AhXvtwhlRhv/XKs2o0tBHhbHG5u8sTMwghpLCqimQ3"
    "aYScqBCrEp8fe/aXJ2CpLW6XhsaNyhst8vYfwp+e+wRbduyDaR5f6Ic9e+Og3p0ghECvrm2l66I2whxTkr24avxw6WH/9Y9LsWjV"
    "FqnnCAAuO3dYhaG2NWlovy7S+NRdew4ed4GgqusW4fEtF58zWFr3ydc/Y9GqLVJyFJem4tJxQxPuQajre3tV7Pfnrh1aokUCWSjb"
    "tsySjkcZ+zV4qLAI622NTQjfz6Mb7rp1bFXt7Jc1zR7hMND2DIonJdmL/j3le9OW3F9espC8/YfwwjvTpEyj9940vtJEVTWhuMQn"
    "jY3s2aVNnZwnl507DCMHlzc87ck/jP9NX1Dj99rKpKUkITlqzOfK9bn4+yufI2//oTr9HvHccvmZUuTVqo078P38NdI21VGb5Raq"
    "HQ0ywvFQYRFe/2gmZi1cG1lX22EESV43rr3gNGmHfzNrGf717rTIshACV40fXu3Wsm22EL7MjLSEwliyGqdJ40Cqaj3KLziCS+98"
    "BqOvmVjh69yb/yaNG0nU6o07MXvROun1r3en4W8vfx65UY4/Y0BMK7rX40b71uXhMfZEIas3lveQ9OzaBoOi5hTZkrs3kpzBniCk"
    "TcvMCkPKosMEVFVBr66hePzMxmnSAPzqhguU+gJ45s0p2BOVcXLgKZ1wwVmDarzVrrjULxVgkzxuZKRXXQlQVQVtWpQnZgFQZQ/a"
    "yvW5OPfmv8WcK9GvS+98ptIxT2kpSRjaVy7kb9iWh1sfeRVnXvdn/N9DL+Pl97/F0jXbEur1sYc3NslIRYdwQahtyyy0iUo+Uxth"
    "jgAwuE9nDI1KOe/zB/H7p/4r9Rz16dE+buWmNjRtki7dDwqPluBQFaFkx3vdlrGPx8vbfwi/f+q/UnKUMSP6SAWVytTHvb0q9vtz"
    "86YZUm9idamqgtNsY/EWr9oSU6DcuG2PNK55WL+ucSt8daXUF4hJdpCdFf8ea2fPZryzivtqbT6rasOm3L34+yufS/eZms40eqiw"
    "CD8t2SBdq9/MWoZ7/vp2JJy+UVoybrh4VJ2cJ5qq4IaLT5fuOV//uDQmsqU2ZWc2Ql9boqS5S9bj2ntfwFnX/Rm3P/YG/vPZj9i4"
    "bU9MEqPa1igtGTdffkaN9TLWVrmFao8S3VLfUOzaexBf/1g+YLss21t1K0bV1TenvdRiZDe0bxcMjgqvOl6tm1ccphbN7dakQktR"
    "sa/eMmR9NHUeJj7/ifSa/O3CyE3xjmvPwd03nhu3kBV9g41OFGKvdOV0bo1uHVvC6wk9fPYXHMHufaECgz1BSOvmmdLg9DL2MIHO"
    "7ZpHKohul4bhUVmrfP5gwuP6LMvClzMXS3+7dfNM3H/LhGqNuzleqSnehMNq7VnmyvZhbbts3FD07xm/JzF3dz4+nTYf9//9XYz7"
    "vyfw1OtfVjoNgD28MXpuqEZpyegf1WOZX3AE23bGJp85UfFSzkc7nnFXJyLJ60azqAKzaZlVDkw/kesWFYzHi9YoLRmXjRtaZS9L"
    "mfq6t1dHovfnyvTs0kZq9V63Zbd07zYME0uiQpW8HpeUXMQJvB4XGid4z4nu5QCAg4eO1clcVHVl1oK1UrKK/j07YsIJJAWKZ9fe"
    "g/jbK5Ola3XSG19FnpHtW2fjlb/cim4d44f214Z2rZpKwz98/iDe+2JOnYxrRrii8qsrz5KyQZcxLQsbtubh3cmzcdsfX8f4W/6B"
    "1z6cUadzgPbNaY+zTysPPT/eXsbaKrdQ7VKiB6JT7dJUFVdNGB6pIERzaSqunDD8uFquciuYQ6i6EimQ1ZeX3/8Wk974Ku6Ewi2b"
    "NZZSqZeF0Rw5VoKtO0Kt1+mpSWjVrAlaZDeODEiPrsztLziCgqi/3a1Dy7gPR3uYQM8ubZCWUp71L7oCiHCmw0QeNqs37cRbn/4Q"
    "WVaEwK1XnFnj487KFBw+FpPa/XjVVctiSjjJw2kDK29VNi0L02Yvx62PvFphhjt7eKM91Co6pNSyLMxfvqnaD8VE2FPOR6vuuKsT"
    "JSCqHLdXXZVdt2VGDOweN90/TnBqAaeoqftzNHur9669Bdi2q7wRwd4A0a1jK7RpUR4KXh9KfH5pPsoTYZgmauFybNByd+fjnr+8"
    "jTmL1tXKvS4eIQTOG9Vf6kWvaCqi2tIsKwN/v//qKnvp/YEgPpo6D3dOfBP7w9MQ1DZNVXHFeadKvYxfzVyM1RVMDVOR2iq3UO1q"
    "8FkcAaCoxIdX/vvdcY+3qI4u7VvgvNED7KsxZkSfKgdLV8Qe/nG8FKFU2lKdmuzFfbdMiJnrJPr1yO0X11pBYPqcFbj7L/+JuTlm"
    "NU5Hdmb5oPmysXQ79xyMhIy0a9UUTTPTkZrsjYSyAcCSNdtgGCZ27y2I3JCEEOjYtjyTXzR7VjT72LA2LbLQLepGv37LbilkMZ79"
    "Bwsx6fWvpKx9N11+Ro2Gt9hlNk6rsXFNFfWOlIk3/479dd8tE+L2WNo1yUjF4/dcjvee/g2uHD+80grskWMleO4/X8dURO3hjV6P"
    "K6bV2D7f1LK122qldzleynmEv9NVE4ZXuW9rkgXruMfzVaai67ZMvPBv1MDUAqjje3tFaur+HM3e6m1ZlpTlbfvufKlSPKRP5zrr"
    "ia1IstdTYyn+VUVBZadFfT+rTtSytdvwxczFdVZRKpNfcAR/ev4TfPz1z3X2b2ekp+CmS0dL1/n7X86pNAKiprVukYmXHr8ZLz9+"
    "CyacObDSnt3c3fl49YMZddYw2b51Nq6ImqopqBt47/M5lQ5HsauNcgvVPqWi8Jpfsj492uMfD1wjhRat2rijTi46IQTOG91fKoym"
    "JntxaTXCeKqSaMhZIKBLv7eqMLfkJA+G9esaM9dJ9GvEwO5x07RX5Yn7rsKP/50ovb5/7zG8+Y/bpcxju/cV4PWPZko3m9RkL9pG"
    "FYL25heiuMSPTdv3RB4yXdq3QLLXAyGEdHPamXcARSU+aZB940YpUsrxMvYwgZQkDw4ePibF9C9atQXeqF7QohJfzPxO0XTDwPtf"
    "zJXGcfXv2REX1sK4s8pUJ7y12BbiUVXIVrz5d+yvYf26xoQxVUQIgdYtMvHrq8bgo+fvwbdv/wGv/PlWXDJ2aEwP9IZteViyWs5K"
    "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"
    "fupOPPnQtXXaIGRXH/sH4TFsD9x6vvQMn/rjUnw3V07oc6KinxmTfn9twpkna4uow4QhyUke/PaGc/Hlaw9WeGw7tmmG2685G5+9"
    "fF+938uQYMKQ2ii3tGjaGPffOiHSsHnmqafg7BG9I9tSzRLfTbKslV8B7UZORdMcObEAERERERER1Z0GOw8aERERERGR01Q8MIWI"
    "iIiIiIjqlFLfkxMSERERERFRCCtoREREREREDqFolcxNRERERERERHVHYZ59IiIiIiIiZ2D9jIiIiIiIyCGYxZGIiIiIiMghOA8a"
    "ERERERGRQyiWxSoaERERERGREyi6btjXERERERERUT1QBLOEEBEREREROQLnQSMiIiIiInIIZnEkIiIiIiJyCIUBjkRERERERM7A"
    "HjQiIiIiIiKH4DxoREREREREDqEEg7p9HREREREREdUDMeWJoLVhuoZ2I6eiac5S+/tEDVJB4THc8di/kV9wBADQp0d7/P3+q5Hk"
    "dds3xZxF6/D4C5/CDE/63rZlFp5++Ho0bZIOAPh52UY8+syHtk/JFCHQtWNLXDp2KEYM7A6P22XfpFrfqbrsf7si2ZmN0C+nA84a"
    "fgr65rSHplaeBfbDKT/h9Y9mRpafuO8qnNq/m7QNAFiWhZfe/xafTV8QWXfuqP6496bxUNWKI7Htf3/syL6475YJ0FQ1of0OAJmN"
    "0zBiYHdccd6paNG0sfReovslnop+a5mZ81bhiZcnS+uaZWXgxYk3Iatx6NypiP23/erKs3DVhBHSNnbH8xkA+Pcn3+O/X86V1h3v"
    "ubc3/zDuevxNHCosktZXta+qUtlvW7J6Kx568v3I9dmqWRM8++gNyM5sFNnebtP2Pbj7L/+Bzx8EALTMboxnHrkBzZtmxJwTieyL"
    "RD5T6gvg4ac/wMr1uVGfjK9lsyaYcMYAnH/mQCQneexvV8n+b2VnNsLLf74FmRlp9k0jTNPExm17MG3OCvy8bCMKDh+LvJed2QhD"
    "+nbBJecMQduWWajO9D31cU4kwn7MKqIIgfats3HFeafi9CE5ce/dVbGfb2ef1gcP33aRfTOJbhhYsS4X38xajiWrt+JYcSkQ/j4t"
    "shtj9LBemHDGgErPcyJyLsXj1uzriChBubvz8exbUyOFP0UI3HzZGZHKWaJMy8KGrXn460uf4VePvoYdeQfsmzhCfsERfDt3BR74"
    "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"
    "tl8yTVXRo3Nr/OHOS/D6E7+OmZrD63HjwV9dgLefuhMTzhwohaoqQqBjm2a4/Zqz8Z8n74ipSMXTukUmXnr8Zrz8+C0xfw/h+8KE"
    "Mwfi7afuxJMPXRtTGYjXUPFLOie8HjcG9e6Mv99/NSb9/lo0yZDDvdu1aoo3/3E7nrjvKgzq3VmaFy76s4/95tKYsYDx9OnRHu9M"
    "uhOTfn8dRg/thbSU8jBQRQi0atYE1144Eh+/8Ds8+KsL4s7BN3JwD1x9/ggoQsDjduGWK86UxpQSUf0SX/9dt9Z9o6LdyKlomiOP"
    "tSAiIiIiIqK6o5hm7bTIEhERERERUfUo9sxNREREREREVD/sc1MSERERERFRPak4VRARERERERHVKYUj0IiIiIiIiJxBicx2SERE"
    "RERERPVKMS3Tvo6IiIiIiIjqgWIYrKARERERERE5gaKqzBNCRERERETkBIqisIJGRERERETkBAqnQSMiIiIiInIGdp8RERERERE5"
    "BOdBIyIiIiIicgjOg0ZEREREROQQSlDX7euIiIiIiIioHihCME0IERERERGREyiaptrXERERERERUT0Q3z5lWaumAO1GTkXTnKX2"
    "94niKvUF8PDTH2Dl+lz7W1X61ZVn4YIxg/D7p/6L1Rt3AgDSU5PwwmM3oV2rpvbNsXXnPvz28f+gxOcHwp+/asII+2YAgElvfIVv"
    "Zi0DAHg9Ljz9++vx36/mYv7yTZFtKvs8ABiGiWffmhr5OwBwyxVn4uoJIyCEwIdTfsLrH82MvPfEfVfh1P7dIssnwr5fszMb4eU/"
    "34LMjDT7phGmaWLjtj2YNmcFfl62EQWHj0Xey85shCF9u+CSc4agbcssVKfH/FhxKR74x3vYuG2PtL6q/VeVgsJjuOOxfyO/4AgA"
    "oE+P9vj7/Vcjyeu2b4o5i9bh8Rc+hWmFBsu2bZmFv91/NV56b3qNHtOfl23Eo898GHmvqr9nZ/9NFWmWlYExI3rjwjGDpGOa6Ocr"
    "cvZpffDwbRcBcf5WZfu3THU+oxsGFq3cgi9mLMbqjTvh8weAUDgGWmQ3xpC+XXD+mQOrfb5V5zvEOy+efvh6NG2SDgDHdTwr+4z9"
    "uqyORP5txPn9FcnObIR+OR1w1vBT0DenPTQ1tpF1++58/Pbxt1BU4gMANMlIxYt/uhktshvbN5Ws3rgTv3vibRiGCQDo1rElrrng"
    "NEx87pPIvm7VrAmeffQGZGc2sn263Kbte3D3X/4Dnz8IAGiZ3RjPPHIDmjfNkLabOW8Vnnh5srSuWVYGXpx4E7Iah47l8bIsCzv3"
    "HMRn3y6MuS9mpKegd/d2OOe0Phjcp3PcfVjZ+VCR4/kMAPz7k+/x3y/nSusqO/+jJfo8siwLL73/LT6bviCy7txR/XHvTeOhqhUn"
    "9Lb//bEj++K+WyZAU9WY4xx9H6rI31/9HN/NXQmEn9HP//H/0LVDy8j79mstkWcg0S+RUo3nJ1GNSfZ60KV9i8jy0aJS7DtYKG1T"
    "Zvuu/EjlDABWbtiBQDB27GSJz49dew9GlptnZaB1i0xcfM4Q6UT/bPpC5O0/FFm2W7tlF2b8FHqAIFz4O/f0ftUqbNaV3XsLcOef"
    "3sQdf/o3pny/RCqEAEB+wRFM+X4JbnzwJTz05Ps4cOio9H5lcncfwJYd++yrsXDlFpT6QoXy2pS7Ox/PvjU1UjBUhMDNl52BVs2a"
    "nLTHdP/BQrz/xRxc+dvn8N3clbDCv+1ksSPvAG7+/St49JkPsXjVlkjlDABMy0Le/kOY/O1C3PjgS/jTc5/gUGGR9PmaUNF5UVY5"
    "+6XLLziCb+euwAP/eA83PPASlq/dHnMeNc/KQKd2zSPLhwqLsH5rnrRNPGs27YxUzgBg4CmdMLh3Zwzp2yWyLm//IUz9YWnMv1lG"
    "Nwx8OGVepNAOAJeOGxZTOTMME3OXbJDWIXyNbNq+1766Wnz+AJ56/Uvc+OBLce+LhUeLMWfROjz6zIe44YGXjqviXVOOFZdiyeqt"
    "9tXYuC1Pep6dKCEExo/uj0ZpyZF1M35aibVbdknbRcvbfwifTV8YWU5N9uLy806NW6EloppVcbMJUS3r0amVtLwlN7YyACCmYJG7"
    "+wCOFpVI6wDgyNESqZDetlVTpCZ70TenPUYOzomsLyg8hs+/WxS3gOEPBPHRlHkI6kZk3SVjh6Jxo1RpOyfYsDUPtz/2BjZsq7rg"
    "BQCLV2/FXRPfjFvpimfhys1SYa1MTRcc4iku8eFf707HkWPlx/nWK8/CaYN6AMBJf0x1w8CTr30h9QI63f6DhfjDsx9h557Ejv3c"
    "JevxxMuTpcaVE1XVedHQ7Nl/CPf+7R18Om2+dO4ned0Y0qeztO3iVVviXh9l/IEglq8rr6ioqoIhfbrA43bhygnD4YoaDvHV90uw"
    "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"
    "krVs7XZpnX2KA3urbqJqouBQNm5kvC3U5o2PZkrZOk8W8Xqt+vZoj/TU5ArDv04G+QVHKu29SktNwpjhvaV1J1Loddp5URP3u5q0"
    "YPlmqTJTUXh3emoS+uaUT7Nx8PBRbN+Vj1UbduBoUfm8aMMHlCfsqGn28MZEHU+Y47GiUhyL+l12iqJg5KAeUiWkxBeo9NyuKfaG"
    "sETVRLRCTfO4XVK0yt78wyjxVTyNiD8YlLJnpiYnoXGcBgUiApTEb3lEMt0w8PZns6TxXwNP6YQLzhpUrUKo26VJk6Lm5h3Ap9Pm"
    "R5btKfOjx6Hl5h3AR1PnRd6L7m1zIt0w8M+3puL5t7+JWxkqKfXjaNREspqqxIydsGf4mr9sI9ZuqbyXYtGqLVKBtm3LLGmS8HgV"
    "uETVVMFBU1XcdvUYKVNgUYkPT7w8WZqjierHhq15uOXhV/G/aQsqLSwneeUeyxMN+3PKeVFT97uasu9AIWb8tFJaN7x/t7jh3SJO"
    "6vz5yzZhcVRPTpOMVPSoxYm112/Nk8Ibq6M6YY7FJT5MfOFTTHzh00rHK7pdmjRJdbx7bW1YmkCDWkVqIlqhJmWkp0g9ttt35Vc6"
    "MfjuvQXS+MfMxqlxE5QQEbM40gmY/O1CTJ+zIrLcunkm7r9lQkwBLRE5nVvbVwHhNPL2NOTR49DsOrTOTijZQX2wLAv/m7YA0+es"
    "wPTZyzFj3iqpoGtZFn5YsEYqxMRrEW/bMgtnDDslshzUDTz56hfYYQthLLN20y48++ZU6d8aPbSX1HKZm3cAW6IenCMH52Dmu4/h"
    "x/9OjPt6+uHra2V8REo4lXr0Mdy9rwDvfzG3Tlq3Kb79BwvxxMuTcay4FK99OAPPv/1NzJhGhAvH02aX3xMQp8f3eDjhvKjJ+92J"
    "2rZzPx566n2p57ptyyyMGNhd2i5al/bN0SZq+pGpPy7F3MXrI8u9uratdPzYiTAME/OWloc3qqqCFx67Kea+Uvb69u0/YEhUwp9E"
    "wxx1w8CrH8zAsrXbsGztNtzz17fj3hcty8LsReuqvNfWtOISHxatKh/z1yQjFR/88+6Y31/2+uLVB6X5K2siWqEm2bNuFpX48OK7"
    "0+NWjItLfHjtw5lSiKM9S3BNWbhyMy66fRJGXzMRf33ps7jfh8jplNpvL6Jfol17D+KjKeU9VwiPc9iwbY800DneK94Ds1WzJnFj"
    "3ptnZcSM7UhLSUKntnJ4Xpmczq3rvDV79cadMb/R/tqRdwCrN+3Evz/5HginIn/ytS/w4JPvY+a8VZi9aB2eeXMK/v1x6P0yQ/p0"
    "iWkRF0LgyvGnonVU6uw9+Ydx44MvYeLzn0T+3jezluH+v7+Lux5/Uwoza986GxeOGRRZBoDFq7YiqJcXdAf26lhpqJN9TEtNFhy6"
    "d2qFB249X2rNnvrj0ip7bmrS1p37Y46h/bV+y4nPAXey+HLmEqnn6MuZi3HxHU/j2bem4of5azB70Tp8OWMx7nr8LSl5RmqyF70S"
    "HBNalfo8L2r6fpeIQ4VF+GnJBulvfTljMe7569u4+eFXsHNP+STxihC4+bIzKg0Xy0hPqbAhDLb5yGpa/qEjWLWhPLzRnlbezj7n"
    "YqJhjuu27Ma0OeXjE7fs2IcbH3wJ9//9XXwzaxlmL1qHmfNW4fEXPsVrH86QPhvvXlvT7A1hXdq3QGbjiqc0sGfgTCRaIdHnUU0Q"
    "QmDcqH5SIp9la7fh2vv+hfe+mBP59977Yg6uve9f0r3Bpak4Y1ivyHJFSkr9mL98U8xviH7NW7ohEtK698BhPP3GlEiP6/c/r8Z3"
    "P62y/VUi51OvO3vixP0bgYx2m5DStPzGQVSZ/QcLMeWHpdCjQjVy8w5g1sK1Vb6yMxvFJBJQVQXzl29CweHytNUAMOCUThgzvHdM"
    "pavU55dafxH+G6HU34m1AhcUHsP0OSsiv6F50wycdeop0sMmnjWbdmLpmvIHzZpNu2J+o/2VndkIo4b0RMHhImyKekDvyT+MuYvX"
    "Y9bCtVLoB8It4rdccSZS4mTXS032Iqdza8xeuE4az7Yj70Dk7/28bGPMnGnZmY0w8e7LpSxmxSU+vD15Fg6GJxZOTfbihktGVToB"
    "tsetYeP2PZGxFIGgjnatmiYUIlXqC+DrH5ehONwDE2+/t22ZBY/HJe3nVRt2oG9O+5gKe7TjPaa79hbgh/lrIsvbd+XHHEP7K2gY"
    "kTnBEvlNx+N4fs/xfJeqPtO9Y0ts2bkPefsPRT5jGCY2bd+DOYvWYdbCtViwYnNMGNr/XToaIwZ0j7l+46nqO6Aa54X9eA7o1THm"
    "nmNX2Wdq+n4Xj/33Hy0qwdwloWu57LVgxea4YZ23XXM2xp3er9L9LISAogjpN5ZpkpGKGy8eVe3ejJ+WbMDWneVJRs489RRpXssy"
    "i1dtxfSoitOoob0wcnDl6fyFAGbOWxXZ5yU+P0YN6Vlpj2V2ZiMked0xSTj25h/Gz8s2YtbCtZi7eH1MBaV/z4645fIzpApaZedD"
    "Rar6zDezlkuh5JecMxS9ulaeyt4wTOlvmpaFkYN7REKHj/d5FP297OdeSrIX543uj2Rv7LPHLjuzEYpKfFi3ubzByucPYvm67ZF/"
    "b/m67THJQW694iyMHtoz5hzQdQPf/7w6cp4HgjrmL9sU8xuiXz8v24gRA7sjs3Ea9uYfxlffL5au1UbpyVXO30jkNIq/gmQFRHUp"
    "Ndkr9QiV6dO9XcwNHAA6tMmOeXg0Tk9F86YVF97rm6aquPO6cxJK+56d2Qh/vOtSNG2Sbn8ronunVnjlz7eie9S8ZJUZdEonvDjx"
    "Zmm8H+K06nZq17zKRCvCNl8RajDMEeG/f8FZgzAwKo13UDcw6fWv4hZQqXalJHvx53uuSGjy3zI3XXZGjc8LxvNC1rJZEzz7yA24"
    "bNywhPZz1w4t4jZwVNWTcyLs4Y0AMKh3pyq/r33OxUTCHIUQuGzcMDz7yA0xqfQr0r9nRzx6x8V1Ht7o9bjQs0vFPZpl7MesJqMV"
    "aoIQAr+68qyYrJgVUYTAr68aU+P3hjJpqUlITZYbGhJ9RhI5CUMcyRGEEOjTvZ20TlUVtI9KqR8tO7MR2rSUK3RtW2YhLaV2H7In"
    "yutx48FfXYC3n7oTE84cKBWKFCHQsU0z3H7N2fjPk3fEVKTiad0iEy89fjNefvyWmL+H8H6acOZAvP3UnXjyoWvjVvjs4Y29urap"
    "tJW6TIfW2VJClpouOCR53bj/lglSxX33vgK8+N70CrNgUu3xuF24cvxwTHnjITxy+8Xo37NjTI9Ly2ZNcO2FI/HxC7/DdReOTLgy"
    "Vx0N/bzIzmyEc07ri0m/vw7vTLoT/Xp2SLig2zg9NW6loKLkIjXBHt7YJCNVmiqlIklet9S7lGiYoxAC/Xp2wHtP34UX/3Qzzjmt"
    "b8zYurSUJIwe2gsv/ulmTPr9tXWSWMreENauVVO0yG4sbRNP4/RUdIsax5lImGNd01QV14Wv++svPh2d2jaXrn1NVdGpbXP8+qox"
    "+OTFe3Hl+OG1cm8AgBZNG+P+WycgIxwBcuapp+DsEb3tmxE5nvhukmWt/ApoN3IqmuYstb9PREREREREdaR2RgQTERERERFRtXEe"
    "NCIiIiIiIodQwBoaERERERGRI0RPKUNERERERET1SInO3kZERERERET1RzFNxjgSERERERE5geKqpblPiIiIiIiIqHoUzlRNRERE"
    "RETkDJwHjYiIiIiIyCE4DxoREREREZFDcB40IiIiIiIih1AsizU0IiIiIiIiJ1B0g/OgEREREREROYGiKMwTQkRERERE5ASKygoa"
    "ERERERGRIyiC86ARERERERE5ArvPiIiIiIiIHILzoBERERERETkEe9CIiIiIiIgcQgkGdfs6IiIiIiIiqgfsQSMiIiIiInIIxeXS"
    "7OuIiIiIiIioHihglhAiIiIiIiJH4DxoREREREREDsExaERERERERA7BedCIiIiIiIgcQtF1w76OiIiIiIiI6oFimuxDIyIiIiIi"
    "cgLF5VLt64iIiIiIiKgeKIJpHImIiIiIiByBWRyJiIiIiIgcQmH/GRERERERkTOwB42IiIiIiMghFINZHImIiIiIiByB86ARERER"
    "ERE5hKKqjHIkIiIiIiJyAkVjBY2IiIiIiMgRFI5AIyIiIiIicgYFrKERERERERE5giI4ERoREREREZEjcAAaERERERGRQyj+oG5f"
    "R0RERERERPWAPWhEREREREQOoXhcmn0dERERERER1QP2oBERERERETkE50EjIiIiIiJyCM6DRkRERERE5BCcB42IiIiIiMghFN0w"
    "7euIiIiIiIioHigGK2hERERERESOoLg01b6OiIiIiIiI6oGiKByERkRERERE5AScB42IiIiIiMghOA8aERERERGRQ7AHjYiIiIiI"
    "yCEUy2IfGhERERERkRMoum7Y1xEREREREVE9UASzOBIRERERETmCoimcB42IiBo6NlYSEZEzKILPJCKiBssCYFmAaQGGpSAAL4Ii"
    "CVYDyiFlQSAgvAjAC8NSYFqhfcIR2kREVB8azhOYiKjBEJVWsMoqZEFDwKcrKDFcKDGT4EMKTDUZqrAgGlD1RADQBGCpyShFCkrM"
    "JJQYLvh0BUEztK8qY0FpQHuLiIhqG+dBIyL6RREwhAuGcNvfABCqbARMgaKghmLDA1NLg+ZNh1DdEIoClwoo0MN9aw2FBQU6NBUQ"
    "QoGiuqF502FqqSg2PCgOavAbosKKmi7cMIWbYZJERFQj2OxHRPRLIRRYqgdBkRy3gmVYQKmuoER3AaoHbq8XLpcLhqEjGAhAc7mg"
    "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"
    "ROT7FfXZIyIiIiIisg/agyYiIiIiIrITny4HRURERERERH6lWFt/fkxEREREREQ+g2imTWgiIiIiIiJ7oDL7IiIiIiIiO6EiISIi"
    "IiIiIjuhPmgiIiIiIiI7oT5oIiIiIiIiO6EURxERERERkZ1QFUcREREREZGdiLWrD5qIiIiIiMgexBTj82MiIiIiIiLyGcScFKCJ"
    "iIiIiIjsgaIzERERERGRnVAfNBERERERkZ3QCpqIiIiIiMhORLVBExERERER2Yfwkz+t/m/+PPPjP/4JP/qDv3j++KOt2vNDu7ZM"
    "WhwUEREREblVLzV+CX/2p9X/8lsCtG/eN/7J//LXzw/LE//Nf/X7/Cf/0fH54d346X/7Pz8/9EVa//Efcvwv//D54d34Z//yb/nn"
    "/+pvnx/+Iv0P//1/9vzQrmhM7IPGxH5oTOyDxsQ+1L/6G979T//r88NfJI2J/fjv/usf87s/Wohzzs8fk1/Tn/zRD3cdnJ3+/F8/"
    "P/TF2vMbDHAzbzB/8kc/fH5oVzQm9uH//rcnjYmduJUxoRvR/dj7mLhoTOzCLY2Jp2LQJrTfyH/8+wf+i/98v28y9a/+hss/vZ03"
    "mT37Z//yNt5g/uSPfrjrMXH683+tMbET/1xjYhduaUxM/+nvPT+0K7dyI/oSxkT9q795fviLtOfgjBsaE89po9Zv6E92/AaDZoB2"
    "45ZmgPb8oQvczI3oSxgTf/3vzs8Pf5E0JvZh/cd/yPSP9hug3cokHjsfE5rY3o9bGhPPqQ/ab+AlpDZqBmgfbiU423vKyq2kcbHz"
    "MaHUxv24lTEx/aPf2/WYuKVJvL2Pifp/3cZ900uYxLuVMfGLRBSh/b0otXE/NAO0Dy8hZUVjYh+U2rgPNzUmdnwjyo1N4mlM7MOe"
    "gzNuaEz8MrHbyyo/uRdKbdwHzQDtx54/dLmxNK69jwmlNu7DLY0JpTbug8bEPux9Eu+WxsQvE3tXgPbrUmrjfuz5RpQbmgHae8rK"
    "raRxsfMxodTG/biVMaHUxv3QmNiHlzCJdytj4leJ05SeH5NvsecZIKU27setzAApZWU/9j4mlNq4Dzc1JnZ8I8qNTeJpTOzDnoMz"
    "bmhMfJsYVGf/17L3GSClNu7DLc0A7flDlxtLWdn7mFBq4z7c0phQauM+aEzsw94n8W5pTHybqPDsu3sJM0BKbdyHWwnO9j5hcSsp"
    "K+x8TCi1cT9uZUwotXE/NCb24SVM4t3KmPgu1Aft17Dn4EypjftxKzNAe69kekspK3sfE3/9b29j5ewlTOLdzJjY8Y0oNzaJpzGx"
    "D3sOzrihMfFdqQ/ad7T3GSClNu7DLc0A7b6S6Y186GpM7Meeb0S5sTGh1MZ90JjYh71P4t3SmPiuoplCtG/zEmaAlNq4D7dyI/oS"
    "KpneCo2Jfdj7JN6tjIm9pzYq3Xc/bmVMaBLvZYq99+fH5Jk9B2dKbdyPW5kBUmrjfmhM7MNLmMS7mTGx4xtRVMl0N25pTOw5OOOG"
    "JvF+XTFGbUP7VfY+A6TUxn24pRkgpTbug8bEfuz5RpQbGxN7T21UJdN9uKUxsWe3Mon39xFTUoD2y7yEGSClNu7DrdyIKrVxPzQm"
    "9mHvk3i3MiaU2rgfGhP7oEm8ly2iLWi/1J6DM6U27setzAAptXE/NCb24SVM4t3MmNjxjShKbdyNWxoTew7OuKFJvL+vqD7Vv9je"
    "Z4CU2rgPtzQDpNTGfdCY2I8934hyY2NCqY37oDGxD5rEe/mU3/gLvIQZIKU27sOt3IgqtXE/NCb2Ye+TeLcyJpTauB8aE/ugSbwv"
    "g/qg/QJ7Ds7QDNBu3MoM0N5TG5Xuux+3MiZewiTerYyJtOOVM5TauBu3NCb2HJxxQ5N4v6nwZ39a/S//PPPjP/4JP/qDv3j+OABm"
    "8C/+j5d1Qn/8Dw/PD31ne14p4HpDegv2nLLCdWb0VmhM7IPGxD5oPOyHxsQ+aEzsh8bEx/6ff/950ot/90fr80Pfye/9hwtv7jLh"
    "J39a/d98S4AmIiIiIiIi3784T/n5MREREREREfkMtAdNRERERERkJ9QHTUREREREZCfUB01ERERERGQn1AdNRERERERkJ2Lt9vyY"
    "iIiIiIiIfAbRFKCJiIiIiIjsQpym9PyYiIiIiIiIfAb/P11Z9s4N4XSYAAAAAElFTkSuQmCC"
)


# Mitgelieferter Glockenton: freesound_community-copper-bells-85490.mp3
BELLS_MP3 = (
    "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"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqPvHPM2XO8yRA4xkD"
    "ow7Dow6DssDIYdh0WAsLAWmFg6FgFgMF5WC5WFpYC0wtC0wPDowPDswOGTysOzDsDjA4DysOzA4DjA4DysDjDsOjA8DysDjA8Dyw"
    "B/lYHFgDjA4DisDzA4D/8wtCwy/CwwsCwrVDzC0LP8sOcaqi9/+YvOcYvi8ViWBQXMMAxMSgXAgYFYLAUMECgMSxWC4FBcw6A4wP"
    "Dow7A/zA8DysDiwBxYA4//PkZLEvmdsEAHbX5AAAA0gAAAAAsAf5YA7/LAHGB4H+VgcVgcWAO//8wPA8rA/ysDywB5WB3//gY2Qv"
    "AwL4GF4L4RC+BjYC8Bw3GwBhfC+BhfC8DAvf8DC+F4GBewYF8DC8F+DAvQiA4DAeA4DAeA+BgPAcDAHhEBwGA8B4MAdBgDgiA8GA"
    "OAwHAOCIDwYA+EQHgwB8IgPCIDwMB4DgiA6Bk/J9/////+DAT4Ign4RBPgMKaBPgYKqgYJ+FNgYU2QGAYU0CfgYJ8CfBEE/BgJ+D"
    "AT4Ign//hEE//8DBPgT+TEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqjqlUK2wdVL5kslGMAuVjEx2DiwDiwOzGJlMLEsDGIx2DzB4PMdA7zBw6MHA4sA8x2Dysd+Y"
    "PBxg8d+YPBxg8HFYPMHjsrHZYBxWDiwDjCIRMABAsBEwAATAABVOqYsA4wcD//PkZGIlsdsGAHM2tAAAA0gAAAAAywDzSIOMHLw4"
    "kOzBwOKwd/lioFdRLAs/yxUDOgsQYTFAIxjshooYahCGZetQuegUWmTYLSoFpsFpv/wKsWmQKQLQKQLTZLTJsemymwWm/0Ci0ybC"
    "bP//gYXgv8IheA2gheBgX//hEL4MC9hEbIMC9g2Dww4Ng8AQC4Ng0GweGGBsHg2DQbBoYcGwYF1wYBYGwYDYNC6wXXBsGww8GwYF"
    "1gutCILf////BgLP+BiyFkBizFkBpRFkBiyFmBizl6BvuFn//wiLP/wMWYsqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqOoZs19USuomT"
    "ieIRAHH3zMgXMLmUsDswcOysHAULGFhh4gABgEAqkDgEqVqghAKBZaRAorGJaQCBcCBf0C02PLTpsFpy0qbKbH/5YB5jsHGDzIZk"
    "//PkZFQj/d0MAHK25gAAA0gAAAAAB3lgHlgHFgHFheG6R2YPBxg4HmDh2VpEweO2rCEImABcHABUgcIBAEBCAQ4BmAAA1Vq7VFTt"
    "Xar7VPauqRUocAlShwgVKqb2rqnauqZqv+IACqZqyp1Sf/+Bi0WQiLYGLRaDKiERaDBb+BiwWgYtFoRFgRFoGLTqERaBi0WhEWQi"
    "LQYLYRC4AwuC6wNg7C6wNgwAQLgDC8MMDYMBsGQwwYeDYMhhww3C62EQf///4RB3CIP/+ERZgwwEDFkx8GCy////hEL4MC+BheC9"
    "TEFNRTMuMTAwVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"
    "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVMvl4y+Xz"
    "bBeLBkMdmUweDy0wFGBhcLmAAD7VECkCy0xaZNktKHAJUjVVStWau1QQAFqrVGqhwgao1ZUpWEWrqnaqqRUypv8sA8rBxYBxWkPM"
    "HA/zFgsMWnU82dTFot8rFhnQ6GLRaVmQtMWkTZLS//PkZG8nRfsSAHK72gAAA0gAAAAAFpy0haQtImwWmTYQK9AtApNj0Ck2P9Nj"
    "wusDYN4XWhdaGH4Yf/+EQcEQfCIOBgPCIPgYOB8Ii0DOos8Ii3CItwMWiwDFosAzpBwMWiwGHUDFotAzqLQMWiwDFotBh0BsGA2D"
    "gBheDYPC6wXXhdcAQLhhoYaDYNBsGhhwuuDYPg2DuDYOwis//////+DC8Bl4vwMvF8GNj//wY2QYXuES+Z2dFg7MPOzDpE2U6Nlv"
    "Ss6Kzsw8OLAeWA4w4OMPDisO8rDisPKw8sB/lYcqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqozpBjFotMWiwDJQCBcwsFzB4OM"
    "HA4wcDiwFzC4XTZEAREAADgEWmLSFpQ4AFYBasqdAtNnwKFvLARMAAArCCpPVI1ZUntXar7Vv/zHQPLA//PkZE8jRd8QAHMVtgAA"
    "A0gAAAAA7K0h/+WBYYt8ZwdfFYt8sCwsZorFgY1AgGOcpTpyFpwcgy5RmymwmwmwgWgWWlQLLSoFldkC/QLLT+mx//5aVNgtMmyW"
    "m9ApAotMmymyWlQK/y0iBSbPps/6bBaVNgC2LSlpQYLAidQYLP/hEWgZ1zYGdRaDBZBgtgwWhEWhELhhgbBgXXhhwbBwNg4GwcDY"
    "OBsHBdfhdcLrBhwbBoYbDDg2DgbB3//////4ML8Il4GF7//gZfbAGXy94RL+DC8Bl5sgZeqgGXy8ES9VTEFNRTMuMTAwVVVVVVVV"
    "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"
    "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVTYqNMpI0rRhWjCtGlZTM0gQ"
    "wIBDEwFMTgQwKBSwBDAoEMTgUwKJ1GggLKcmBQJ5YApWBFOVOFOAgLKNqceWAWo2iso2o2ioo0o34VBSnP+WA15YKZWjP/ywQDIG"
    "9K1B/+WK8VqBNpIwuWzt//PkZGsm0gsQAHMVtAAAA0gAAAAAIxI4zmLkJGi5wRL///LGv/yvRY2V78rKWCFghYKVlLBCshlL5lKZ"
    "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"
    "oGHRABmGAawMJL6hACzAEgBgYIBgZB5OUEAZhgqYgCpKBgEzFdMsomVNzaComTBpkJ0PJQkAo8qeIAEMBCgvNapzqGUIGBgHakIw"
    "IBCTP3IfeYQStYLVGCA+YdWRxN+D0KGhSYNFxl80GEySYJUpz6nm4iGYdGgAWJ0a7nEiaY3EBdkuC/gXCjHRJOuKNZdl/WBN80l+"
    "Y9K6V/YaVWY8w1ls52s7ULizDXJZQYOAGFGpmQSp//PkZNY0Og8KAG+bsgAAA0gAAAAAkpksAYSEBgE5TY10yFgTFlNlhXpLuGTg"
    "RuHSf5SmMDACBzBwowkEQHRtdLdl1Sd2ZdElzLGk8RYjecKUT9mbqNxLqmJC5AJCqAbawFCsjTaZ6YUOgIxSOijtU+XZTHIfisSj"
    "TWmXTcpkCgTTnZehtl4o+xiBpS7NDYly0S5KzWDAgTMcIw4iMeRzRidNSFQ1njKZGzm9GarCl1ggCM3KjHXI4VUDht5VMYEn+TMu"
    "f63HWu0laGnajNnGWwzJJdf/5TYf5/pdTyZW5lt5TEFNRTMuMTAwVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"
    "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVTmfQ0l3M+UDPz0DWoCIzEAYWPkmH0gQHAQMB1wQyDQhHODg"
    "aITXhKlLXGnQE/7qzMAK6SpZYtaU8+7BCukBK6FYuZ6lT1JXBYCrha0NRIt8YMwJB2ol5VBFxhQGBiIFQApKgmAIoFCwhiDkxrFJ"
    "pZxgr4himOZGbKmKOBE8WimpNGUZiA0QnAikAOC2ZmClrQqgCgxYFPaB3+TRYgpc4M5ax5juYcZpMORa//PkZKousgzaAG9ZXoAA"
    "A0gAAAAA68ClytrurpCoS/3KAKRaMIRVuhfMc510VoA4ZKllICFRuBgJl0DDQQ+GGwC4C1sbst/XX2aWhqFwFrwlW5pRb4vapiZQ"
    "oJMIDSFwIETylSNq6FYrjpoDQYSgADBmUxlxVbnHfmtXsvs+7BVpOO6splDjLRawrpgLuMmYE77q1YAV0nLCIdEAKgiOTgzstfaG"
    "2WsBg6qqsztS1pUjwlUeXUgJXQta5K35fWGGnPrSw6wJ335uR9xU0lhy9KNzT4FiVPx9X0YMtF+ItMiVTEFNRTMuMTAwVVVVVVVV"
    "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"
    "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"
    "VVVVVVVkASQeAYdNhokUGhl+ZMaBvsPGzGuYQNxoceGGi6YnAgABaoIPnZdSw06LwxCVyifor9LTXLut63cr0UZoKecnpbGoBiEV"
    "pqs1X5ea1C2dJbFmzThj//PkZFUkHUg4rnO7wgAAA0gAAAAANIvgyHATnwRO33QzFbTDKjNKxY1VuTPGiOpwMFaibGnIafKOabt8"
    "aPzMZIxybVJ8b1h0a3IeY8oMZIg6YlFSaqC6btRyZAzAaSs6bAGMauhaaVByZ/lMZOG+YOFIUHIYnhICAFa5D8sktyfjUzY7lSyq"
    "Oyixa/mu7xiVSvSUdmvDC7kNgCEAUSMbGTckc2u6MpwynAPt4gZrkYWakUrSqQqKw80lwGWulG5BLpTBENAYCMBEDAQoxcVNuRzZ"
    "7oy3BH8U+/mEWyJixqReTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAw"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "TEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAA"
    "A0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAw"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "TEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAA"
    "A0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAw"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "TEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAA"
    "A0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAw"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "TEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAA"
    "A0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAw"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "TEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAA"
    "A0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAw"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "TEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAA"
    "A0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAw"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "TEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAA"
    "A0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAw"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "TEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAA"
    "A0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//PkZAAAAAGkAAAAAAAAA0gAAAAATEFNRTMuMTAw"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqTEFNRTMuMTAwqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
)


# ---------------------------------------------------------------- Seite
def is_open(d: int) -> bool:
    return TEST or (date.today() >= date(YEAR, 12, d) and (d == 1 or d - 1 in game["solved"]))


st.title("🎄 Der Nordpol-Fall")
st.caption("Jemand sabotiert die Weihnachtswerkstatt. Nur ihr könnt sie noch retten.")

if TEST:
    st.info("Testmodus · Alle 24 Türchen sind direkt anwählbar. Der Fortschritt gilt für diese Sitzung.")
    if st.sidebar.button("Testspiel neu starten"):
        st.session_state.clear()
        st.rerun()

if "active" not in st.session_state:
    nxt = [d for d in DOORS if d not in game["solved"] and is_open(d)]
    st.session_state.active = nxt[0] if nxt else 1

for start in range(1, max(DOORS) + 1, 6):
    cols = st.columns(6)
    for i, d in enumerate(range(start, min(start + 6, max(DOORS) + 1))):
        label = f"✓{d}" if d in game["solved"] else (str(d) if is_open(d) else f"🔒{d}")
        if cols[i].button(label, key=f"nav{d}", disabled=not is_open(d), use_container_width=True):
            st.session_state.active = d
            st.rerun()

with st.sidebar:
    st.subheader("🗂️ Die Akte")
    pieces = [n for n in range(5, 12) if n in game["solved"]]
    st.write(f"Wegkarte · {len(pieces)} / 7 Stücke")
    if pieces:
        with st.expander("Kartenstücke ansehen"):
            for n in pieces:
                st.markdown(map_piece(n, 0), unsafe_allow_html=True)
    if 8 in game["solved"]:
        with st.expander("Morsekarte ansehen"):
            morse_card()
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
    act = "Akt 1 · Der Ruf" if day <= 4 else "Akt 2 · Die Reise zur Werkstatt" if day <= 12 else "Akt 3 · Die Werkstatt"
    st.caption(act)
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
        if day == 19:
            st.markdown(plan_html(), unsafe_allow_html=True)
        if day == 2:
            st.markdown(PLAIN.replace("\n", "  \n"))
            st.audio(b64decode(BELLS_MP3), format="audio/mp3", autoplay=fresh)
    else:
        door["render"](day)
        hints(day, door["hints"])
