from flask import Flask, render_template, request
import random
import time
import json
import sqlite3

app = Flask(__name__)

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

# -------- AGENT LOGIC (UNCHANGED) --------

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

# -------- ROUTES --------

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    decision = None

    if request.method == "POST":
        time.sleep(1)
        waste_level, waste_type, location_priority, weather_condition = sense_environment()
        decision = infer_action(
            waste_level, waste_type, location_priority, weather_condition
        )
        log_to_db(
            waste_level, waste_type, location_priority, weather_condition, decision
        )

        data = {
            "waste_level": waste_level,
            "waste_type": waste_type,
            "location_priority": location_priority,
            "weather_condition": weather_condition
        }

    return render_template("index.html", data=data, decision=decision)

@app.route("/logs")
def logs():
    c.execute("""
        SELECT waste_level, waste_type, location_priority,
               weather_condition, decision, timestamp
        FROM waste_log ORDER BY timestamp DESC
    """)
    rows = c.fetchall()
    return render_template("logs.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)
