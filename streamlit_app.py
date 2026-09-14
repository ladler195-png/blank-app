import streamlit as st
import datetime

# 1. SEITEN-KONFIGURATION
st.set_page_config(
    page_title="Adventskalender: Das Rätsel der Zeit",
    page_icon="⏰",
    layout="centered"
)

# 2. DATENBANK DER RÄTSEL (Beispiel für die ersten Tage)
DOORS = {
    1: {
        "person": "Person A",
        "title": "Tag 1: Die alte Werkstatt",
        "story": "Ihr betretet die alte Werkstatt. Auf dem Tisch liegt eine verschlossene Schatulle.",
        "question": "In welchem Jahr wurde die Weltzeit auf der Meridian-Konferenz in Washington festgelegt?",
        "answer": "1884",
        "hint": "Tipp: Suche nach dem Jahr der Internationalen Meridian-Konferenz."
    },
    2: {
        "person": "Person B",
        "title": "Tag 2: Das verschlüsselte Notizbuch",
        "story": "In der Schatulle liegt ein Notizbuch. Ein Wort ist mit Cäsar-Chiffre (+3) verschlüsselt: 'WHLW'.",
        "question": "Wie lautet das entschlüsselte Wort?",
        "answer": "ZEIT",
        "hint": "Tipp: Rücke jeden Buchstaben im Alphabet um 3 Stellen zurück."
    },
    3: {
        "person": "Person C",
        "title": "Tag 3: Der alte Tresor",
        "story": "Das Wort schaltet eine Geheimtür frei. Dahinter steht ein Tresor mit Drehrad.",
        "question": "Rechne aus: (Anzahl Tage im Advent * 30) + 22",
        "answer": "742",
        "hint": "Tipp: 24 * 30 + 22"
    }
}

# 3. SPIECHERSTAND (Session State initialisieren)
if "solved_doors" not in st.session_state:
    st.session_state.solved_doors = []

# 4. OBERFLÄCHE (HEADER)
st.title("⏰ Das Rätsel der verschollenen Zeit")
st.subheader("Ein Adventskalender für die Familie")

# Status-Übersicht für die 3 Personen
col_a, col_b, col_c = st.columns(3)
with col_a:
    solved_a = sum(1 for d in st.session_state.solved_doors if DOORS.get(d, {}).get("person") == "Person A")
    st.metric("Person A", f"{solved_a} / 8 Rätsel")
with col_b:
    solved_b = sum(1 for d in st.session_state.solved_doors if DOORS.get(d, {}).get("person") == "Person B")
    st.metric("Person B", f"{solved_b} / 8 Rätsel")
with col_c:
    solved_c = sum(1 for d in st.session_state.solved_doors if DOORS.get(d, {}).get("person") == "Person C")
    st.metric("Person C", f"{solved_c} / 8 Rätsel")

st.divider()

# 5. RÄTSEL-SELEKTOR (Türchen auswählen)
st.write("### 📅 Wähle dein Türchen")

# 24 Türchen in einem Raster anzeigen (6 Spalten pro Zeile)
cols = st.columns(6)
selected_day = None

for i in range(1, 25):
    col = cols[(i - 1) % 6]
    person = DOORS.get(i, {}).get("person", "Alle")
    
    # Status-Symbol bestimmen
    if i in st.session_state.solved_doors:
        label = f"✅ {i}"
    else:
        label = f"🔒 {i}"
        
    if col.button(label, key=f"door_btn_{i}"):
        st.session_state.active_day = i

# 6. RÄTSEL-DIALGO (Wenn ein Türchen geklickt wurde)
if "active_day" in st.session_state:
    day = st.session_state.active_day
    
    if day in DOORS:
        puzzle = DOORS[day]
        st.markdown(f"---")
        st.markdown(f"### 🚪 {puzzle['title']} ({puzzle['person']})")
        st.info(puzzle["story"])
        
        if day in st.session_state.solved_doors:
            st.success(f"🎉 Dieses Rätsel wurde bereits gelöst! Die Lösung war: **{puzzle['answer']}**")
        else:
            # Eingabefeld für die Lösung
            user_input = st.text_input("Deine Lösung eingeben:", key=f"input_{day}")
            
            col_submit, col_hint = st.columns([1, 1])
            with col_submit:
                if st.button("Lösung prüfen", type="primary"):
                    if user_input.strip().upper() == puzzle["answer"].upper():
                        st.session_state.solved_doors.append(day)
                        st.balloons()
                        st.success("Richtig gelöst! Hervorragend gemacht.")
                        st.rerun()
                    else:
                        st.error("Leider falsch. Versuche es noch einmal!")
            
            with col_hint:
                if st.button("Hinweis anzeigen"):
                    st.warning(puzzle["hint"])
    else:
        st.write(f"### 🚪 Tag {day}")
        st.write("Für diesen Tag ist noch kein Rätsel eingetragen.")
