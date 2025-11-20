♻️ Intelligent Waste Management Agent
A Knowledge-Based AI System for Smart Waste Collection Decisions

The Intelligent Waste Management Agent is a Knowledge-Based System (KBS) that automatically perceives waste bin conditions, applies logical rules stored in a JSON knowledge base, and decides optimal waste collection actions.
It also logs all sensed data and AI decisions into a database for monitoring and analysis.

This project demonstrates how an AI agent works using the classical cycle:

Perceive → Reason → Act → Learn

🌍 Problem Statement

Urban waste bins often overflow due to:

Lack of timely waste collection

No real-time monitoring

Inefficient routes

Weather-driven waste decay

Mismanagement of recyclable vs organic waste

This project solves these issues using AI reasoning, sensor simulation, and smart decision-making.

🚀 Features
🧠 1. Knowledge-Based Reasoning

All rules are stored in rules.json, making the system:

Explainable

Editable

Transparent

Easy to expand

👁️ 2. Environment Perception Simulation

Simulated IoT sensors generate:

Waste level

Waste type

Location priority

Weather condition

📊 3. Database Logging (MySQL or SQLite)

Every decision is saved for future insights:

Waste data

Weather

Priority

Final action

Timestamp

🖥️ 4. Clean Streamlit UI

One-click sensing

Instant reasoning

Action explanation

Table of historical logs

🧠 Knowledge Base (Rules)

These rules guide the agent’s decisions:

Rule 1: If waste_level > 85 and waste_type = Organic and weather_condition = Rainy → Urgent collection.
Rule 2: If waste_level > 85 → Collect immediately (bin almost full).
Rule 3: If 60 < waste_level ≤ 85 and location_priority = High → Schedule collection soon.
Rule 4: If 40 < waste_level ≤ 60 and waste_type = Recyclable → Optimize route for next recyclable trip.
Rule 5: If waste_level < 40 → No immediate action (monitor periodically).

🏗️ System Architecture
         ┌────────────────────┐
         │   JSON Knowledge   │
         │       Base         │
         └─────────┬──────────┘
                   │
                   ▼
       ┌───────────────────────────┐
       │  Intelligent Waste Agent  │
       ├───────────────────────────┤
       │ • Perceive (Sensors)      │
       │ • Reason (Rules)          │
       │ • Act (Decision)          │
       │ • Learn (Database Logs)   │
       └─────────┬─────────────────┘
                 │
                 ▼
     ┌─────────────────────┐
     │ Streamlit Interface │
     └─────────────────────┘
                 │
                 ▼
     ┌─────────────────────┐
     │   MySQL / SQLite    │
     │   Waste Logs Table  │
     └─────────────────────┘

🔄 Agent Decision-Making Flowchart
                 ┌────────────────────────┐
                 │ Sense Environment Data │
                 └───────────┬────────────┘
                             ▼
                ┌─────────────────────────┐
                │ Compare Data With Rules │
                └───────────┬─────────────┘
                            ▼
           ┌──────────────────────────────────┐
           │ Does Any Rule Match Conditions?  │
           └───────┬──────────────────────────┘
                   │ Yes
                   ▼
         ┌──────────────────────────┐
         │   Return Matched Action  │
         └──────────────────────────┘

                   │ No
                   ▼
         ┌──────────────────────────┐
         │ Default Routine Schedule │
         └──────────────────────────┘

🗄️ Database Schema (MySQL or SQLite)
TABLE waste_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    waste_level INT,
    waste_type VARCHAR(50),
    location_priority VARCHAR(20),
    weather_condition VARCHAR(20),
    decision VARCHAR(255),
    timestamp DATETIME
)

📸 Screenshots (Add yours here)
![UI Screenshot](link_here)
![Database Logs](link_here)

🛠️ Tech Stack
Frontend

Streamlit

Backend / Logic

Python

JSON Knowledge Base (Rules)

AI Rule-Matching Engine

Database

MySQL (Recommended)

SQLite (Alternative)

▶️ How to Run
1. Install dependencies
pip install streamlit mysql-connector-python

2. Run the app
streamlit run agent.py

3. Open the browser

Streamlit will open automatically or visit:

http://localhost:8501

📌 Future Improvements

Real IoT sensor integration

Bin overflow prediction using ML

Geolocation-based route optimization

Weather API integration for accuracy

Dashboard analytics with charts

💡 About This Project

This project demonstrates how Explainable AI + Smart City concepts can automate waste collection using:

Knowledge-based reasoning

Environmental perception

Decision automation

Logging and learning
