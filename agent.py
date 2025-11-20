import streamlit as st
import random
import time
import json
import sqlite3

st.set_page_config(page_title="Intelligent Waste Management Agent", page_icon="♻️", layout="centered")

st.markdown("<h1 style='text-align:center;color:#27ae60;'>♻️ Intelligent Waste Management Agent</h1>", unsafe_allow_html=True)
st.write("This Knowledge-Based Agent perceives waste bin conditions, reasons using logical rules, and decides optimal waste collection actions.")

# Load rules from JSON
with open("rules.json", "r", encoding="utf-8") as file:
    rules = json.load(file)

# Initialize SQLite database
conn = sqlite3.connect("waste_data.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS waste_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    waste_level INTEGER,
    waste_type TEXT,
    location_priority TEXT,
    weather_condition TEXT,
    decision TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def infer_action(waste_level, waste_type, location_priority, weather_condition):
    for rule in rules:
        cond = rule["condition"]
        level = cond.get("waste_level", None)
        type_ = cond.get("waste_type", None)
        priority = cond.get("location_priority", None)
        weather = cond.get("weather_condition", None)
        match = True
        if level:
            if "-" in level:
                low, high = map(int, level.split("-"))
                if not (low < waste_level <= high):
                    match = False
            elif level.startswith(">"):
                if not (waste_level > int(level[1:])):
                    match = False
            elif level.startswith("<"):
                if not (waste_level < int(level[1:])):
                    match = False
        if type_ and type_ != waste_type:
            match = False
        if priority and priority != location_priority:
            match = False
        if weather and weather != weather_condition:
            match = False
        if match:
            return rule["action"]
    return "⚙️ Routine collection scheduling"

def sense_environment():
    waste_level = random.randint(10, 100)
    waste_type = random.choice(["Organic", "Plastic", "Recyclable", "E-waste"])
    location_priority = random.choice(["Low", "Medium", "High"])
    weather_condition = random.choice(["Sunny", "Rainy", "Cloudy"])
    return waste_level, waste_type, location_priority, weather_condition

def log_to_db(waste_level, waste_type, location_priority, weather_condition, decision):
    c.execute("""
        INSERT INTO waste_log (waste_level, waste_type, location_priority, weather_condition, decision)
        VALUES (?, ?, ?, ?, ?)
    """, (waste_level, waste_type, location_priority, weather_condition, decision))
    conn.commit()

if st.button("🌍 Sense Environment and Decide Action"):
    st.subheader("Perceiving Environment...")
    time.sleep(1)
    waste_level, waste_type, location_priority, weather_condition = sense_environment()

    st.metric("Waste Level (%)", waste_level)
    st.write(f"**Waste Type:** {waste_type}")
    st.write(f"**Location Priority:** {location_priority}")
    st.write(f"**Weather Condition:** {weather_condition}")

    st.subheader("Reasoning & Decision-Making...")
    time.sleep(1)
    decision = infer_action(waste_level, waste_type, location_priority, weather_condition)
    st.success(decision)

    log_to_db(waste_level, waste_type, location_priority, weather_condition, decision)

    st.subheader("Knowledge-Based Rules Applied:")
    st.code("""See rules.json for all applied rules""")

st.markdown("---")
st.markdown("<h4 style='text-align:center;color:#555;'>Agent Type: Knowledge-Based Intelligent Agent</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#999;'>Perceives → Reasons → Acts → Learns</p>", unsafe_allow_html=True)

# Display all logged data
st.subheader("📊 Logged Data")
c.execute("""
    SELECT waste_level, waste_type, location_priority, weather_condition, decision, timestamp 
    FROM waste_log ORDER BY timestamp DESC
""")
rows = c.fetchall()
if rows:
    st.table(rows)
else:
    st.write("No data logged yet.")
