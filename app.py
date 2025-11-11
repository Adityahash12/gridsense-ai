import streamlit as st
import random
import json
import pandas as pd
from pathlib import Path
from streamlit.components.v1 import html

# ==============================
# 🧠 GRID SENSE AI — BACKEND CORE
# ==============================

def generate_random_signals(is_critical=False):
    """Generates synthetic signals representing sensor input."""
    if is_critical:
        temp = random.randint(90, 100)
        humidity = random.randint(80, 100)
        age_score = random.randint(70, 95)
        load = random.randint(90, 100)
    else:
        temp = random.randint(50, 85)
        humidity = random.randint(30, 75)
        age_score = random.randint(10, 65)
        load = random.randint(30, 85)

    return {
        "temperature": temp,
        "humidity": humidity,
        "component_age_score": age_score,
        "load_percentage": load,
        "fault_signal": random.choice([0, 0, 0, 1]) if is_critical else random.choice([0, 0, 0, 0, 0, 1]),
        "current_topology": random.choice(["Normal-A/B", "Rerouted-B/A"]),
        "renewable_input": random.randint(500, 1500),
        "weather_score": random.uniform(0.5, 0.95)
    }

def gridsense_reroute_logic(signals):
    """AI-driven predictive rerouting and sustainability decisions."""
    temp = signals["temperature"]
    humidity = signals["humidity"]
    age = signals["component_age_score"]
    load = signals["load_percentage"]

    stress_index = (temp * 0.4) + (humidity * 0.3) + (age * 0.3)
    CRITICAL_THRESHOLD = 80

    # Default values
    status_color = "🟢"
    fault_alert = "No existing physical fault detected (Fault Sensor: Nominal)."
    self_care_alert = "AI actively monitoring key stressors."
    reroute_message = "Line A carrying full load, Line B on standby."
    future_prediction = "Stable. No maintenance required."
    sustainability_suggestion = f"Routing {signals['renewable_input']} MW clean energy efficiently."

    if stress_index >= CRITICAL_THRESHOLD:
        status_color = "🔴"
        fault_alert = f"🚨 MICRO-FAILURE PREDICTED: Stress Index {stress_index:.1f}. Failure likely < 72 hours."
        self_care_alert = "⚡ REROUTE INITIATED: Calculating optimal power path."
        reroute_message = "✅ Stability maintained: Power rerouted to Line B, Line A isolated."
        future_prediction = f"Trend: CRITICAL. Rising stress; immediate isolation advised."
        sustainability_suggestion = f"Action: Rerouting prioritized {signals['renewable_input']} MW renewables."
    elif signals["fault_signal"] == 1:
        status_color = "🟠"
        fault_alert = "⚠️ REAL-TIME FAULT: Issue detected; AI mitigating damage."
        self_care_alert = "⚡ EMERGENCY REROUTE: Isolating fault sector."
        reroute_message = "🔄 Emergency reroute in progress. Grid recovering."
        future_prediction = "Trend: INSTABILITY. Further predictive monitoring ongoing."
        sustainability_suggestion = "Efficiency temporarily reduced; optimization underway."

    elif load > 80:
        future_prediction = f"Load high ({load}%). Balancing advised."
        sustainability_suggestion = "Shifting 10% load to Line B to avoid wastage."

    return status_color, fault_alert, self_care_alert, reroute_message, future_prediction, sustainability_suggestion, stress_index


# ==============================
# ⚙️ STREAMLIT APP CONFIG
# ==============================

st.set_page_config(page_title="GridSense AI — Predictive Grid Dashboard", layout="wide")

st.title("💡 GridSense: AI-Driven Smart Grid & Sustainability Prototype")
st.markdown("Real-time grid health monitoring, predictive rerouting, and renewable optimization.")

# --- Sidebar Controls (Admin Only) ---
with st.sidebar:
    st.header("📡 Data Control (Admin Only)")

    if "signals" not in st.session_state:
        st.session_state.signals = generate_random_signals()

    if st.checkbox("Enable Admin Controls"):
        st.button("🔄 Random Normal Signals", on_click=lambda: st.session_state.update(signals=generate_random_signals(False)))
        st.button("💥 Random CRITICAL Signals", on_click=lambda: st.session_state.update(signals=generate_random_signals(True)))

        st.subheader("Core Failure Predictors")
        st.session_state.signals["temperature"] = st.slider("Temperature (°C)", 50, 100, st.session_state.signals["temperature"])
        st.session_state.signals["humidity"] = st.slider("Humidity (%)", 30, 100, st.session_state.signals["humidity"])
        st.session_state.signals["component_age_score"] = st.slider("Component Age", 0, 100, st.session_state.signals["component_age_score"])
        st.session_state.signals["load_percentage"] = st.slider("Load (%)", 0, 100, st.session_state.signals["load_percentage"])
        st.session_state.signals["fault_signal"] = st.selectbox("Fault Detected", [0, 1], index=st.session_state.signals["fault_signal"])
        st.session_state.signals["renewable_input"] = st.slider("Renewable Input (MW)", 0, 2000, st.session_state.signals["renewable_input"])
        st.session_state.signals["weather_score"] = st.slider("Weather Severity", 0.0, 1.0, st.session_state.signals["weather_score"], 0.05)

# --- Process the AI Logic ---
status_c, fault_t, self_care_t, reroute_s, future_p, sustainability_s, stress_i = gridsense_reroute_logic(st.session_state.signals)

# ==============================
# 📊 OUTPUT SECTION
# ==============================

st.header(f"🧠 AI Prediction & Grid Status — {status_c}")
st.metric("Combined Stress Index", f"{stress_i:.1f}", delta="> 80 triggers reroute", delta_color="inverse")
st.error(fault_t)
st.warning(self_care_t)
st.success(reroute_s)
st.info(future_p)
st.success(sustainability_s)
st.markdown("---")

# ==============================
# 🧾 SAVE JSON OUTPUT (For Website)
# ==============================

output_data = {
    "status": status_c,
    "system_health": "HEALTHY" if status_c == "🟢" else "ALERT",
    "stress_index": round(stress_i, 1),
    "fault_alert": fault_t,
    "self_care_action": self_care_t,
    "reroute_status": reroute_s,
    "future_prediction": future_p,
    "sustainability_focus": sustainability_s,
    "timestamp": str(pd.Timestamp.now())
}

# Save JSON for website access
json_path = Path("latest_output.json")
with open(json_path, "w") as f:
    json.dump(output_data, f, indent=4)

# Admin Download Option
st.download_button(
    label="⬇️ Download AI Output (Admin Only)",
    data=json.dumps(output_data, indent=4),
    file_name="latest_output.json",
    mime="application/json"
)

# ==============================
# 🌍 PUBLIC JSON ACCESS
# ==============================
html("""
<script>
    // Expose the JSON file publicly for frontend fetch
    fetch('latest_output.json')
      .then(response => response.json())
      .then(data => console.log('JSON ready for frontend:', data))
      .catch(err => console.error(err));
</script>
""", height=0)

# ==============================
# 🔍 DEBUG VIEW (Admin)
# ==============================
st.subheader("🔍 Live Model Output (Debug View)")
st.json(output_data)

st.caption("GridSense © 2025 | AI-driven predictive fault detection, rerouting & renewable optimization.")
# --- Optional: Auto-push latest_output.json to GitHub (so frontend sees live updates) ---

import base64
import requests

# === GitHub Repo Info ===
GITHUB_REPO = "Adityahash12/gridsense-ai"
FILE_PATH = "latest_output.json"
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")  # Secure token stored in Streamlit Secrets

if GITHUB_TOKEN:
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}

        # Get current file SHA
        r = requests.get(url, headers=headers)
        sha = r.json().get("sha", None)

        # Encode new JSON file
        content = base64.b64encode(json.dumps(output_data, indent=4).encode()).decode()

        data = {
            "message": "Auto-update AI output JSON",
            "content": content,
            "branch": "main",
        }
        if sha:
            data["sha"] = sha

        # Push update to GitHub
        r = requests.put(url, headers=headers, data=json.dumps(data))
        if r.status_code in [200, 201]:
            st.success("✅ Live AI data synced to GitHub successfully.")
        else:
            st.warning(f"⚠️ GitHub sync failed: {r.status_code}")
    except Exception as e:
        st.warning(f"GitHub push error: {e}")
else:
    st.info("ℹ️ GitHub auto-sync disabled (no token found).")

