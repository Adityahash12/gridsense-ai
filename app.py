import streamlit as st
import random
import json

# --- State Management & Random Signal Generation ---

def generate_random_signals(is_critical=False):
    """Generates a set of random signals, optionally forcing a critical condition."""
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

if 'signals' not in st.session_state:
    st.session_state.signals = generate_random_signals()

def set_random_signals(critical=False):
    st.session_state.signals = generate_random_signals(critical)

# --- Core AI Logic ---

def gridsense_reroute_logic(signals):
    temp = signals["temperature"]
    humidity = signals["humidity"]
    age = signals["component_age_score"]
    load = signals["load_percentage"]
    stress_index = (temp * 0.4) + (humidity * 0.3) + (age * 0.3)
    CRITICAL_STRESS_THRESHOLD = 80

    fault_alert = "No existing physical fault detected (Fault Sensor: Nominal)."
    self_care_alert = "AI Prediction Model: Actively monitoring key stressors. Continuous refinement."
    reroute_message = "Current Flow: Line A is carrying 100% load. Line B is idle or supporting low load."
    future_prediction = "Trend: Stable. Stress Index is low. No immediate maintenance required."
    sustainability_suggestion = "Status: Optimal energy routing. Prioritizing renewable input efficiently."
    status_color = "🟢"

    if stress_index >= CRITICAL_STRESS_THRESHOLD:
        status_color = "🔴"
        fault_alert = f"🚨 MICRO-FAILURE PREDICTED: High stress index ({stress_index:.1f}). Failure likely in < 72 hours."
        self_care_alert = "⚡ DYNAMIC REROUTING INITIATED: Computing least-disruptive power route."
        reroute_message = "✅ GRID STABILITY MAINTAINED: Load transferred to Line B. Line A isolated for maintenance."
        future_prediction = f"Trend: CRITICAL. Stress index {stress_index:.1f} rising. Immediate risk if not isolated."
        sustainability_suggestion = f"Action: Rerouting prioritizes {signals['renewable_input']} MW from renewables."
    elif signals["fault_signal"] == 1:
        status_color = "🟠"
        fault_alert = "⚠️ IMMEDIATE FAULT ALERT: Physical issue detected. AI isolating fault sector."
        self_care_alert = "⚡ DAMAGE MITIGATION REROUTE: Emergency isolation activated."
        reroute_message = "🔄 EMERGENCY REROUTE: Power diverted; stability recovering."
        future_prediction = "Trend: INSTABILITY. Minor stress due to reroute. Further analysis required."
        sustainability_suggestion = "Action: Efficiency loss detected; AI optimizing future routing."
    else:
        if load > 80:
            future_prediction = f"Trend: RISING STRESS. Load {load}% expected to peak. Recommend proactive balancing."
            sustainability_suggestion = "Action: Shift 10% of load to Line B to prevent wastage."
        else:
            future_prediction = f"Trend: STABLE. Stress Index ({stress_index:.1f}) nominal. Stable next 24 hrs."
            sustainability_suggestion = f"Action: MAXIMIZE RENEWABLES — routing {signals['renewable_input']} MW clean."

    return status_color, fault_alert, self_care_alert, reroute_message, future_prediction, sustainability_suggestion, stress_index


# --- Streamlit Dashboard UI ---
st.set_page_config(page_title="GridSense: AI & Sustainability Prototype", layout="wide")
st.title("💡 GridSense: Predictive Energy Healing AI Prototype (v2)")

st.markdown("This prototype demonstrates **predictive fault avoidance** and **sustainability-focused rerouting**.")
st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    st.header("📡 Data Collection Layer")
    st.button("🔄 Random Normal Signals", on_click=set_random_signals, args=(False,))
    st.button("💥 Random CRITICAL Signals", on_click=set_random_signals, args=(True,))

    st.subheader("Core Failure Predictors")
    st.session_state.signals["temperature"] = st.slider("Temperature (°C)", 50, 100, st.session_state.signals["temperature"])
    st.session_state.signals["humidity"] = st.slider("Humidity (%)", 30, 100, st.session_state.signals["humidity"])
    st.session_state.signals["component_age_score"] = st.slider("Component Age/Health Score", 0, 100, st.session_state.signals["component_age_score"])
    st.session_state.signals["load_percentage"] = st.slider("Load (%)", 0, 100, st.session_state.signals["load_percentage"])
    st.session_state.signals["fault_signal"] = st.selectbox("Fault Detected", [0, 1], index=st.session_state.signals["fault_signal"], format_func=lambda x: "NO (0)" if x == 0 else "YES (1)")
    st.session_state.signals["renewable_input"] = st.slider("Renewable Input (MW)", 0, 2000, st.session_state.signals["renewable_input"])
    st.session_state.signals["weather_score"] = st.slider("Weather Severity", 0.0, 1.0, st.session_state.signals["weather_score"], 0.05, format="%.2f")

# --- AI Processing ---
status_c, fault_t, self_care_t, reroute_s, future_p, sustainability_s, stress_i = gridsense_reroute_logic(st.session_state.signals)

# --- Output Display ---
st.header(f"🧠 AI Prediction & Self-Healing Action — {status_c}")
st.metric("Combined Grid Stress Index", f"{stress_i:.1f}", delta="> 80 = Critical")
st.error(fault_t)
st.warning(self_care_t)
st.success(reroute_s)
st.info(future_p)
st.success(sustainability_s)

st.markdown("---")
st.caption("GridSense: AI-driven fault prediction, rerouting, and renewable optimization in real-time.")

# --- Save Output to JSON ---
output_data = {
    "status": status_c,
    "fault_alert": fault_t,
    "self_care": self_care_t,
    "reroute_message": reroute_s,
    "future_prediction": future_p,
    "sustainability": sustainability_s,
    "stress_index": stress_i
}

with open("model_output.json", "w") as f:
    json.dump(output_data, f, indent=4)
