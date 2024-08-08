import streamlit as st
import math

# Function to calculate log odds and probability of HFpEF based on regression equations
def calculate_log_odds_and_probability(age, bmi, af_history, htn_drug, diabetes, ntprobnp):
    results = {}
    log_odds = {}
    
    # ABA Models
    log_odds["ABA Model"] = -7.788751 + 0.062564 * age + 0.135149 * bmi + 2.040806 * af_history
    log_odds["ABA + >1 HTN drug"] = -7.436121 + 0.057758 * age + 1.957936 * af_history + 0.121762 * bmi + 0.666309 * htn_drug
    log_odds["ABA + diabetes"] = -7.619470 + 0.060999 * age + 2.047362 * af_history + 0.130498 * bmi + 0.361005 * diabetes
    log_odds["ABA + NTproBNP"] = -7.999067 + 0.052368 * age + 0.150643 * bmi + 1.505152 * af_history + 0.001010 * ntprobnp
    
    # Other Models
    log_odds["Age"] = -3.997742 + 0.073396 * age
    log_odds["BMI"] = -3.168224 + 0.124006 * bmi
    log_odds["Age + BMI"] = -8.334640 + 0.079543 * age + 0.128005 * bmi
    log_odds["Age + AF"] = -3.345276 + 0.058542 * age + 1.914686 * af_history
    log_odds["AF + BMI"] = -3.963373 + 0.136347 * bmi + 2.704942 * af_history

    for key, value in log_odds.items():
        probability = 1 / (1 + math.exp(-value))
        results[key] = {"log_odds": value, "probability": probability}
    return results

# Streamlit app
st.title("HFpEF Risk Calculator")

# Add disclaimer in an expander
with st.expander("Disclaimer"):
    st.write("""
    **Educational Use Only**
    This calculator is intended for educational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment. All results should be validated clinically by a qualified healthcare provider.
    """)

age = st.number_input("Age (years)", min_value=0, max_value=120, value=60)
bmi = st.number_input("BMI (kg/m²)", min_value=10.0, max_value=50.0, value=25.0)

afib = st.checkbox("Atrial Fibrillation History (AF)")
af_history = 1 if afib else 0

htn = st.checkbox("More than 1 Hypertension Medication")
htn_drug = 1 if htn else 0

dm = st.checkbox("Diabetes")
diabetes = 1 if dm else 0

ntprobnp = st.number_input("NT-proBNP (pg/mL)", min_value=0.0, max_value=10000.0, value=100.0)

if st.button("Calculate Risk"):
    results = calculate_log_odds_and_probability(age, bmi, af_history, htn_drug, diabetes, ntprobnp)
    st.subheader("Log Odds and Probability of HFpEF")
    
    # Display ABA Models first
    aba_models = ["ABA Model", "ABA + >1 HTN drug", "ABA + diabetes", "ABA + NTproBNP"]
    for key in aba_models:
        st.markdown(f"### {key}")
        st.write(f"**Log Odds:** {results[key]['log_odds']:.4f}")
        st.write(f"**Probability:** {results[key]['probability']*100:.2f}%")
        st.divider()
    
    # Display other models
    for key, value in results.items():
        if key not in aba_models:
            st.markdown(f"### {key}")
            st.write(f"**Log Odds:** {value['log_odds']:.4f}")
            st.write(f"**Probability:** {value['probability']*100:.2f}%")

