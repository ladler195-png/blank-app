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
    cipher = vigenere(PLAIN.upper(), "H")
    leaves = "".join(
        f'<ellipse cx="0" cy="-22" rx="3.5" ry="6" transform="rotate({angle})"/>'
        for angle in range(37, 330, 22)
    )
    wreath = (
        '<svg width="52" height="52" viewBox="-30 -30 60 60" role="img" '
        'aria-label="Lorbeerkranz"><circle r="22" fill="none" stroke="#695737" opacity=".35"/>'
        f'<g fill="#695737" opacity=".72">{leaves}</g></svg>'
    )
    paragraphs = "".join(f'<div style="margin-bottom:.65rem">{line}</div>' for line in cipher.splitlines())
    st.markdown(
        '<div style="max-width:680px;background:#fff2d0;color:#21190e;padding:clamp(14px,4vw,34px);'
        'border:3px double #a5824b;border-radius:6px;margin:.6rem 0 1rem">'
        f'<div style="display:flex;justify-content:flex-end;margin-bottom:.25rem">{wreath}</div>'
        '<div aria-label="Geheimtext" style="font:600 clamp(16px,3vw,21px)/1.6 monospace;'
        f'letter-spacing:.06em;overflow-wrap:anywhere">{paragraphs}</div>'
        '<div style="border-top:1px solid #ac925f;padding-top:.65rem;font:italic 16px/1.5 Georgia,serif">'
        'Wie weit ihr gehen müsst, verrät euch der Absender.</div></div>',
        unsafe_allow_html=True,
    )
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

# Vorhandener Entwurf für den Werkstatt-Akt. Die Testoberfläche endet bei Türchen 12.
WORKSHOP_DOORS = {
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
}

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
    st.info("Testmodus · Alle zwölf Türchen sind direkt anwählbar. Der Fortschritt gilt für diese Sitzung.")
    if st.sidebar.button("Testspiel neu starten"):
        st.session_state.clear()
        st.rerun()

if "active" not in st.session_state:
    nxt = [d for d in DOORS if d not in game["solved"] and is_open(d)]
    st.session_state.active = nxt[0] if nxt else 1

for start in (1, 7):
    cols = st.columns(6)
    for i, d in enumerate(range(start, start + 6)):
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
    st.caption("Akt 1 · Der Ruf" if day <= 4 else "Akt 2 · Die Reise zur Werkstatt")
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
        if day == 2:
            st.markdown(PLAIN.replace("\n", "  \n"))
            st.audio(b64decode(BELLS_MP3), format="audio/mp3", autoplay=fresh)
    else:
        door["render"](day)
        hints(day, door["hints"])
