import streamlit as st
import pandas as pd

# ================= PAGE =================
st.set_page_config(page_title="Concrete Mix Design Pro", layout="wide")

st.title("🏗️ Concrete Mix Design Pro Tool")
st.markdown("### 📘 IS Method | Sustainable Design | Cost & CO₂ Analysis")

# ================= LAYOUT =================
col1, col2 = st.columns(2)

# ================= INPUT =================
with col1:
    st.subheader("🧊 Concrete Requirement")

    num_cubes = st.number_input("No. of Cubes (150mm)", 1, 100, 1)
    wastage = st.slider("Wastage (%)", 0, 20, 10)

    cube_volume = 0.003375
    volume = num_cubes * cube_volume
    volume = volume * (1 + wastage / 100)

    st.info(f"Total Volume: {volume:.5f} m³")

    st.subheader("⚙️ Mix Inputs")

    grade = st.selectbox("Grade", ["M20", "M25", "M30", "M35", "M40"])

    material = st.selectbox("Cement Replacement",
                            ["None", "Fly Ash", "GGBS", "Silica Fume", "Rice Husk Ash"])

    percent = st.slider("Replacement (%)", 0, 60, 0)

    admixture_percent = st.slider("Admixture (%)", 0.0, 5.0, 0.0)

with col2:
    st.subheader("💰 Cost Inputs")

    cement_cost = st.number_input("Cement (₹/bag)", value=400.0)
    sand_cost = st.number_input("Sand (₹/m³)", value=1500.0)
    agg_cost = st.number_input("Aggregate (₹/m³)", value=1200.0)
    admixture_cost = st.number_input("Admixture (₹/kg)", value=50.0)

# ================= DATA =================
fck_values = {"M20": 20, "M25": 25, "M30": 30, "M35": 35, "M40": 40}
wc_ratio = {"M20": 0.5, "M25": 0.45, "M30": 0.4, "M35": 0.38, "M40": 0.36}

S = 5
water_content = 186

cement_co2 = 0.9
alt_co2 = 0.1

# ================= CALCULATION =================
if st.button("🚀 Calculate Mix Design"):

    fck = fck_values[grade]
    target = fck + 1.65 * S
    wc = wc_ratio[grade]

    cement = water_content / wc

    replaced = (percent / 100) * cement
    remaining = cement - replaced

    cement_vol = cement / 1440
    water_vol = water_content / 1000

    agg_vol = 1 - (cement_vol + water_vol)

    fa_vol = agg_vol * 0.4
    ca_vol = agg_vol * 0.6

    sand_m3 = fa_vol * volume
    agg_m3 = ca_vol * volume

    sand_kg = sand_m3 * 1600
    agg_kg = agg_m3 * 1450

    cement_total = cement * volume
    remaining_total = remaining * volume
    replaced_total = replaced * volume

    water_total = water_content * volume

    cement_kg = remaining_total
    bags = cement_kg / 50

    admixture = (admixture_percent / 100) * cement_total

    # ================= MIX TYPE =================
    if grade == "M20":
        mix_type = "Nominal Mix (IS 456)"
    else:
        mix_type = "Design Mix (IS 10262)"

    # ================= MIX RATIO =================
    sand_ratio = sand_kg / cement_total
    agg_ratio = agg_kg / cement_total
    mix_ratio = f"1 : {sand_ratio:.2f} : {agg_ratio:.2f}"

    # ================= COST =================
    cement_price = bags * cement_cost
    sand_price = sand_m3 * sand_cost
    agg_price = agg_m3 * agg_cost
    admixture_price = admixture * admixture_cost

    total_cost = cement_price + sand_price + agg_price + admixture_price

    # ================= CO2 =================
    co2_without = cement_total * cement_co2
    co2_with = (remaining_total * cement_co2) + (replaced_total * alt_co2)
    saved = co2_without - co2_with

    # ================= OUTPUT =================
    st.markdown("---")
    st.subheader("📊 Results")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Target Strength (MPa)", f"{target:.2f}")
    c2.metric("Mix Ratio", mix_ratio)
    c3.metric("Total Cost (₹)", f"{total_cost:.2f}")
    c4.metric("Mix Type", mix_type)

    st.markdown("### 🧱 Material Breakdown")

    data = {
        "Material": ["Cement", material, "Sand", "Aggregate", "Water", "Admixture"],
        "Quantity": [
            f"{cement_kg:.2f} kg",
            f"{replaced_total:.2f} kg" if material != "None" else "-",
            f"{sand_kg:.2f} kg",
            f"{agg_kg:.2f} kg",
            f"{water_total:.2f} L",
            f"{admixture:.2f} kg"
        ],
        "Cost (₹)": [
            f"{cement_price:.2f}",
            "-",
            f"{sand_price:.2f}",
            f"{agg_price:.2f}",
            "0",
            f"{admixture_price:.2f}"
        ]
    }

    st.table(pd.DataFrame(data))

    st.markdown("### 🌱 CO₂ Analysis")

    st.write(f"Without Replacement: {co2_without:.2f} kg CO₂")
    st.write(f"With Replacement: {co2_with:.2f} kg CO₂")
    st.success(f"CO₂ Saved: {saved:.2f} kg")

# ================= FOOTER =================
st.markdown("---")
st.write("👨‍💻 Developed by Surenthar B ")