from array import array
from functools import lru_cache
from html import escape
from io import BytesIO
from math import exp, pi, sin
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
    # Geheimtext als HTML-Text, damit er exakt, skalierbar und kopierbar bleibt.
    leaves = "".join(
        f'<ellipse cx="0" cy="-29" rx="3" ry="7" transform="rotate({angle})"/>'
        for angle in range(32, 335, 24)
    )
    wreath = (f'<svg width="65" height="65" viewBox="-36 -36 72 72" role="img" '
              f'aria-label="Blasser Lorbeerkranz"><g fill="#88733d" opacity=".62">{leaves}</g></svg>')
    st.markdown(
        '<div style="background:linear-gradient(135deg,#f5e9c9,#e3c88f);color:#382a18;'
        'padding:1rem 1.5rem 1.5rem;border:3px double #ab884f;border-radius:6px">'
        f'<div style="text-align:right">{wreath}</div>'
        f'<div style="font:600 1.05rem monospace;white-space:pre-wrap;overflow-wrap:anywhere">{cipher}</div>'
        '<p style="margin:1rem 0 0;font-style:italic">Wie weit ihr gehen müsst, verrät euch der Absender.</p>'
        '</div>', unsafe_allow_html=True)
    text_door(day, eq("LATERNE"), "Welches Wort sollt ihr dreimal aussprechen?")


def door3(day):
    questions = (
        ("Bei unserem Gespann haben die erwachsenen Bullen ihre Geweihe vor Dezember abgeworfen. "
         "Alle vier vor euch tragen noch eines. Was sind wir?", ("Erwachsene Bullen", "Kühe"), "Kühe"),
        ("Unter welchem Namen kennt man Rentiere in Kanada?", ("Wapiti", "Karibu", "Elch"), "Karibu"),
        ("Im Sommer schimmert die reflektierende Schicht hinter unserer Netzhaut goldfarben. "
         "Welche Farbe hat sie im Winter?", ("Grün", "Silber", "Blau"), "Blau"),
    )
    with st.form("f3"):
        picks = [st.radio(q, options, index=None, key=f"rentier{i}") for i, (q, options, _) in enumerate(questions)]
        if st.form_submit_button("Antworten prüfen"):
            if picks == [answer for _, _, answer in questions]:
                solve(day)
            st.error("Überprüft eure drei Antworten.")


def door4(day):
    st.markdown("**Sternkarte** · Merak (2|3) · Dubhe (4|7) · Phecda (6|4) · Megrez (8|6)")
    st.markdown("> Zieht eine Linie von Merak durch Dubhe. Geht ab Dubhe in derselben Richtung weiter. "
                "Die Strecke von Merak bis Dubhe passt noch fünfmal zwischen Dubhe und den Polarstern.")
    with st.form("f4"):
        left, right = st.columns(2)
        x = left.number_input("Waagerecht (x)", value=0, step=1)
        y = right.number_input("Senkrecht (y)", value=0, step=1)
        if st.form_submit_button("Kurs bestätigen"):
            if (x, y) == (14, 27):
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
               "🧭": "#f9d898", "🏮": "#f9d898", "🔧": "#f9d898", "✦": "#f9d898"}


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
            symbol = {"#": "▧", "E": "🏮"}.get(cell, "·")
            cells.append("🧭" if (i, j) == (r, c) else "•" if (i, j) in trail else symbol if visible else "")
        rows.append(cells)
    grid(rows, f"Nebellabyrinth, Figur in Zeile {r + 1}, Spalte {c + 1}")
    st.caption("🧭 Ihr · • Eure Fußspuren · ▧ Eiswand · Dunkle Felder liegen im Nebel.")
    pad("maze", _move)
    st.button("Zum Eingang zurück", key="maze_reset", on_click=reset_fields, args=("maze_pos", "maze_trail"))
    if MAZE[r][c] == "E" and st.button("Weglaterne anzünden", type="primary"):
        solve(day)


# Das Werkzeug liegt an einer echten Halteposition.
ICE = ("#######", "#S..#.#", "#.#...#", "#..#..#", "#.#..##", "#..#E.#", "#######")


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
    st.caption(f"Ihr rutscht geradeaus bis zum nächsten Hindernis. Züge: {moves}")
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
def audio_signal(kind, words=()):
    rate = 16000
    samples = array("h")
    if kind == "bells":
        for gain in (.18, .31, .52, .78, 1.0):
            for n in range(int(rate * .48)):
                t = n / rate
                wave_value = (sin(2*pi*1163*t) + .44*sin(2*pi*1729*t) + .24*sin(2*pi*2477*t))
                samples.append(int(12000 * gain * exp(-t*10) * min(t*500, 1) * wave_value))
    else:
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
    st.audio(audio_signal("morse", words), format="audio/wav")
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
    placed = st.session_state.setdefault("plates", {})
    filled = {cell: PLATE_SYMBOLS[name] for name, cells in placed.items() for cell in cells}
    grid([[filled.get((r, c), "·" if (r, c) in GAP else "▧") for c in range(4)]
          for r in range(3)], "Lücke für die drei Eisplatten")
    st.caption("Setzt die Platten in die hellen Felder. Der Anker ist die obere linke Ecke des Rechtecks um die Platte.")
    plate = st.selectbox("Eisplatte", tuple(PLATES))
    turns = st.select_slider("Drehung", options=(0, 90, 180, 270), format_func=lambda x: f"{x}°")
    shape = rotate_plate(PLATES[plate], turns // 90)
    grid([[PLATE_SYMBOLS[plate] if (r, c) in shape else "" for c in range(3)]
          for r in range(3)], "Vorschau der ausgewählten Eisplatte")
    anchor = st.selectbox("Ankerfeld (Zeile, Spalte)", [(r, c) for r in range(3) for c in range(4)],
                          format_func=lambda rc: f"{rc[0]+1}, {rc[1]+1}")
    left, right = st.columns(2)
    if left.button("Platte einsetzen", type="primary"):
        footprint = {(anchor[0] + r, anchor[1] + c) for r, c in shape}
        occupied = {cell for name, cells in placed.items() if name != plate for cell in cells}
        if footprint <= GAP and footprint.isdisjoint(occupied):
            placed[plate] = footprint
            st.rerun()
        st.error("Die Platte ragt über die Lücke hinaus oder überlappt eine andere.")
    if right.button("Platte herausnehmen", disabled=plate not in placed):
        placed.pop(plate)
        st.rerun()
    if set(filled) == GAP and st.button("Schlucht überqueren"):
        solve(day)
    st.button("Alle Platten herausnehmen", on_click=reset_fields, args=("plates",))


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


def map_piece(day, turns):
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
            f'style="display:block;width:100%;max-width:108px;background:#f3dfb2;border:1px solid #866e45">'
            f'{lines}{marks}<text x="78" y="87" fill="#6e5433" font-size="12">{day-4}</text></svg>')


def map_matches(placed):
    return set(placed) == set(MAP_FRAME) and all(
        piece_layout(*placed[slot])[0] == edges for slot, edges in MAP_FRAME.items()
    )


def door12(day):
    pieces = [n for n in range(5, 12) if n in game["solved"]]
    if TEST and len(pieces) < 7 and st.checkbox("Fehlende Kartenstücke zum Testen leihen"):
        pieces = list(range(5, 12))
    if len(pieces) < 7:
        st.info(f"Ihr habt {len(pieces)} von 7 Kartenstücken. Die übrigen findet ihr in Türchen 5 bis 11.")
    if not pieces:
        return
    placed = st.session_state.setdefault("map_placed", {})
    placed = {slot: item for slot, item in placed.items() if item[0] in pieces}
    for r in range(2):
        columns = st.columns(4)
        for c, column in enumerate(columns):
            slot = (r, c)
            if slot in MAP_FRAME:
                column.caption(f"Feld {MAP_ORDER.index(slot) + 1}")
                column.markdown(map_piece(*placed[slot]) if slot in placed else
                                '<div style="max-width:108px;aspect-ratio:1;border:2px dashed #a4c5cd"></div>',
                                unsafe_allow_html=True)
    if map_matches(placed):
        st.success("Die Karte passt. Folgt der Linie von der Fahne bis zur Eiswand.")
        columns = st.columns(3)
        for col, mark in zip(columns, ("Mond", "Stern", "Tanne")):
            if col.button(mark, key=f"wall_{mark}"):
                if mark == "Stern":
                    solve(day)
                st.error("An dieser Stelle bleibt die Eiswand geschlossen.")
    piece = st.selectbox("Kartenstück", pieces, format_func=lambda n: f"Stück {n-4} · Türchen {n}")
    turns = st.select_slider("Kartenstück drehen", (0, 90, 180, 270), format_func=lambda n: f"{n}°")
    st.markdown(map_piece(piece, turns // 90), unsafe_allow_html=True)
    slot = st.selectbox("Feld im Rahmen", MAP_ORDER, format_func=lambda p: f"Feld {MAP_ORDER.index(p)+1}")
    left, right = st.columns(2)
    if left.button("Kartenstück einsetzen", type="primary"):
        st.session_state.map_placed = {p: item for p, item in placed.items() if item[0] != piece}
        st.session_state.map_placed[slot] = (piece, turns // 90)
        st.rerun()
    if right.button("Feld leeren", disabled=slot not in placed):
        placed.pop(slot)
        st.session_state.map_placed = placed
        st.rerun()
    if len(placed) == 7 and not map_matches(placed):
        st.info("Prüft die Nahtsymbole und die Ausrichtung der Stücke.")


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
         "Ihr geht hinaus. Hinter den Rentieren wartet ein Schlitten. „Bevor ihr einsteigt, wollen wir wissen, "
         "wie gut ihr euch mit Rentieren auskennt.“",
         door3, "Die Rentiere am Schlitten sind Kühe. In Kanada heißen Rentiere Karibus.",
         "„Na gut“, sagt das Rentier. „Steigt ein.“ Ihr klettert auf die Sitzbank. Unter der dicken Wolldecke wird euch wieder warm.",
         "Alle vier Rentiere vor euch tragen im Dezember ein Geweih.",
         "Elch und Wapiti sind andere Tiere.",
         "Die gesuchte Farbe erinnert an einen klaren Winterhimmel."),
    4: D("Türchen 4 · Der Kurs zum Nordpol",
         "„Gebt uns einen Kurs, dann können wir los.“ Am Bordcomputer blinkt ein Koordinatenfeld. Daneben steckt eine Sternkarte.",
         door4, "Der Kurs zum Polarstern ist bestätigt.",
         "Die Kufen gleiten über den Schnee und heben ab. Unter euch werden die beleuchteten Fenster immer kleiner.",
         "Vergleicht die Koordinaten von Merak und Dubhe.",
         "Ein Schritt sind zwei Felder nach rechts und vier nach oben. Wiederholt ihn ab Dubhe fünfmal.",
         "Startet bei (4|7). Addiert waagerecht 10 und senkrecht 20."),
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
         "Plant rückwärts. Überlegt, aus welcher Richtung ihr auf dem Werkzeugfeld zum Stehen kommt."),
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
            snd = Path(__file__).with_name("glocken.mp3")
            st.audio(str(snd) if snd.is_file() else audio_signal("bells"),
                     format="audio/mp3" if snd.is_file() else "audio/wav", autoplay=fresh)
    else:
        door["render"](day)
        hints(day, door["hints"])
