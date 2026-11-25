"""Renewable Energy Availability Prediction - demo dashboard.
Demo values are synthetic, not measured hardware data.
Run: streamlit run app.py
"""
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Renewable Energy Availability", page_icon="☀️", layout="wide")
st.title("☀️ Renewable Energy Availability Prediction")
st.caption("Hybrid Solar + Piezoelectric Energy Generation | ESP32 / IoT concept dashboard")
st.info("Demo mode: synthetic sample data. Replace with calibrated ESP32 sensor data for real monitoring and prediction.")

@st.cache_data
def make_demo_data(days=3, interval_minutes=15):
    rng = np.random.default_rng(12)
    n = days * 24 * 60 // interval_minutes
    times = pd.date_range(end=pd.Timestamp.now().floor("15min"), periods=n, freq=f"{interval_minutes}min")
    hour = times.hour + times.minute / 60
    daylight = np.maximum(0, np.sin(np.pi * (hour - 6) / 12))
    irradiance = np.clip(950 * daylight + rng.normal(0, 45, n), 0, 1000)
    pv_power = np.clip(30 * irradiance / 1000 * (0.88 + rng.normal(0, .04, n)), 0, 30)
    activity = rng.poisson(1.2, n)
    piezo_power = np.clip(activity * rng.uniform(.01, .06, n), 0, .5)
    pv_voltage = np.where(pv_power > .2, 17.8 + rng.normal(0, .5, n), 0)
    pv_current = np.divide(pv_power, pv_voltage, out=np.zeros(n), where=pv_voltage > 0)
    piezo_voltage = np.where(piezo_power > 0, rng.uniform(1.5, 8, n), 0)
    piezo_current = np.divide(piezo_power, piezo_voltage, out=np.zeros(n), where=piezo_voltage > 0)
    load_w = 3.5 + rng.normal(0, .25, n)
    batt_v = np.clip(12.1 + np.cumsum((pv_power + piezo_power - load_w) * interval_minutes / 60 / 90 * .015), 11.4, 13.0)
    soc = np.clip(58 + (batt_v - 12.1) * 20, 10, 100)
    return pd.DataFrame({"Timestamp": times, "Irradiance_Wm2": irradiance, "PV_V": pv_voltage,
        "PV_A": pv_current, "PV_W": pv_power, "Piezo_V": piezo_voltage, "Piezo_A": piezo_current,
        "Piezo_W": piezo_power, "Activity_Count": activity, "Battery_V": batt_v, "SOC_pct": soc, "Load_W": load_w})

sample = make_demo_data()
with st.sidebar:
    st.header("Settings")
    interval = st.selectbox("Prediction window", [15, 30, 60], index=2, format_func=lambda x: f"{x} minutes")
    load_w = st.number_input("Estimated load (W)", min_value=0.0, max_value=1000.0, value=3.5, step=0.5)
    st.markdown("**Proposed project specs**")
    st.write("Solar panel: 30 W")
    st.write("Piezo discs: 100 × 27 mm")
    st.write("Battery: 12 V, 7.5 Ah (≈90 Wh nominal)")
    st.write("Controller: ESP32")

latest = sample.iloc[-1]
pv_energy_wh = sample["PV_W"].sum() * .25
piezo_energy_wh = sample["Piezo_W"].sum() * .25
c1, c2, c3, c4 = st.columns(4)
c1.metric("PV power (latest)", f"{latest.PV_W:.2f} W")
c2.metric("Piezo power (latest)", f"{latest.Piezo_W:.3f} W")
c3.metric("Battery voltage (demo)", f"{latest.Battery_V:.2f} V")
c4.metric("Estimated SOC (demo)", f"{latest.SOC_pct:.0f}%")

st.subheader("Source power")
st.plotly_chart(px.line(sample, x="Timestamp", y=["PV_W", "Piezo_W"],
    labels={"value":"Power (W)", "variable":"Source"}, title="Solar and Piezo power — synthetic demo data"), use_container_width=True)

st.subheader("Energy contribution (sample period)")
left, right = st.columns(2)
left.metric("Solar energy", f"{pv_energy_wh:.2f} Wh")
right.metric("Piezo energy", f"{piezo_energy_wh:.3f} Wh")

future_start = sample.Timestamp.iloc[-1] + pd.Timedelta(minutes=15)
hist = sample[sample.Timestamp.dt.hour == future_start.hour]
predicted_source_power = float(hist[["PV_W", "Piezo_W"]].sum(axis=1).mean()) if not hist.empty else float(sample[["PV_W", "Piezo_W"]].sum(axis=1).mean())
source_wh = predicted_source_power * interval / 60
load_wh = load_w * interval / 60
net_wh = source_wh - load_wh
st.subheader(f"Baseline availability estimate — next {interval} minutes")
a, b, c = st.columns(3)
a.metric("Estimated source energy", f"{source_wh:.3f} Wh")
b.metric("Estimated load energy", f"{load_wh:.3f} Wh")
c.metric("Net energy estimate", f"{net_wh:+.3f} Wh")
st.caption("Baseline estimate uses average synthetic source power for the same hour in demo history. It is not a validated forecast model.")

st.subheader("Battery status trend (demo)")
st.plotly_chart(px.line(sample, x="Timestamp", y="SOC_pct", title="Illustrative SOC trend", labels={"SOC_pct":"SOC (%)"}), use_container_width=True)
st.subheader("Sample data")
st.dataframe(sample.tail(24), use_container_width=True)
st.download_button("Download demo data CSV", sample.to_csv(index=False).encode("utf-8"),
    file_name="renewable_energy_demo_data.csv", mime="text/csv")
st.markdown("---")
st.markdown("**Hardware safety:** Battery charging, source conditioning, reverse-current protection, fusing, sensor calibration, and voltage-divider design must be implemented and verified separately before connecting hardware.")
