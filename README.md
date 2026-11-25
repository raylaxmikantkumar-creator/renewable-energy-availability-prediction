# Renewable Energy Availability Prediction

Streamlit dashboard concept for a **hybrid Solar + Piezoelectric Energy Generation and Storage System**. It visualizes source power, battery status, sample energy totals, and a simple baseline estimate of near-term energy availability.

> **Demo warning:** The app currently generates synthetic sample readings. No hardware measurements or validated prediction accuracy are claimed. Replace the sample data generator with calibrated ESP32 measurements before real-world monitoring or forecasting.

## Proposed specifications
- Solar PV panel: 30 W
- Piezo discs: 100 × 27 mm
- Piezo conditioning: bridge rectifier and smoothing capacitor (initial simulation value: 1000 µF)
- Battery: 12 V, 7.5 Ah (approximately 90 Wh nominal)
- Controller: ESP32
- Monitoring: source/battery voltage, current, power, energy, SOC and activity input
- Prediction: historical average baseline; validate with held-out measurements (MAE/RMSE recommended)

## Features
- PV and piezo power plot
- Latest demo PV/piezo power, battery voltage, estimated SOC
- Sample source energy contribution
- Select prediction window: 15, 30 or 60 minutes
- Configure load estimate and view source/load/net energy estimate
- Illustrative battery SOC plot
- Sample data table and CSV export

## Run locally
1. Install Python 3.9+ (Python 3.10+ recommended).
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch:
   ```bash
   streamlit run app.py
   ```
   Streamlit typically opens at `http://localhost:8501`.

## Repository layout
```text
renewable-energy-availability-prediction/
├── app.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Prediction method (demo)
Synthetic 15-minute readings are generated for demonstration. The baseline estimate averages source power for the same hour in the sample history, then calculates energy for the selected future window. This is **not** a trained or validated ML model.

For actual prediction work:
1. Collect timestamped, calibrated PV/piezo voltage and current.
2. Record irradiance (measured or clearly identified proxy), activity/footstep data, battery SOC and load.
3. Define target: source energy, stored energy, or load-deliverable energy.
4. Split chronological records into training and test periods.
5. Compare baseline and candidate regression models; report MAE/RMSE on held-out data.

## Safety
Do not connect PV, piezo, or battery voltages directly to ESP32 pins. Use suitable sensing and signal conditioning. Choose charge control, battery protection, converters, rectifiers, wiring, and fuses for the actual chemistry and source conditions. Do not parallel/connect PV and piezo sources directly without conditioning and reverse-current protection. Follow component datasheets and qualified supervision.

## Report alignment
The demo aligns with the proposed report architecture: hybrid PV/piezo sources, battery storage, ESP32 monitoring, IoT dashboard concept, energy calculations, and a future energy-availability estimation layer. Hardware implementation and prediction validation remain future work unless measured/reproducible simulated data are added.

## License
Choose and add a license before publishing publicly. MIT is one common permissive option; make the choice intentionally.
