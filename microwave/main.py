import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import streamlit as st

# --- 1. Define Fuzzy Variables (Antecedents and Consequents) ---

# Input Antecedents
# Food Type: A conceptual scale representing cookedness
food_type = ctrl.Antecedent(np.arange(0, 11, 1), 'food_type')
# Quantity of Food: A conceptual scale representing amount
quantity = ctrl.Antecedent(np.arange(0, 11, 1), 'quantity')

# Output Consequent
# Cooking Time: In minutes, from 0 to 60
cooking_time = ctrl.Consequent(np.arange(0, 61, 1), 'cooking_time')

# --- 2. Define Membership Functions for each variable ---

# Membership functions for Food Type
food_type['raw'] = fuzz.trimf(food_type.universe, [0, 0, 3])
food_type['half_cooked'] = fuzz.trimf(food_type.universe, [2, 5, 8])
food_type['fully_cooked'] = fuzz.trimf(food_type.universe, [7, 10, 10])

# Membership functions for Quantity of Food
quantity['little'] = fuzz.trimf(quantity.universe, [0, 0, 3])
quantity['medium'] = fuzz.trimf(quantity.universe, [2, 5, 8])
quantity['large'] = fuzz.trimf(quantity.universe, [7, 10, 10])

# Membership functions for Cooking Time
cooking_time['VS'] = fuzz.trimf(cooking_time.universe, [0, 0, 15])
cooking_time['S'] = fuzz.trimf(cooking_time.universe, [10, 20, 30])
cooking_time['MT'] = fuzz.trimf(cooking_time.universe, [25, 35, 45])
cooking_time['Lo'] = fuzz.trimf(cooking_time.universe, [40, 50, 60])
cooking_time['VL'] = fuzz.trimf(cooking_time.universe, [55, 60, 60])

# You can optionally visualize these MFs (uncomment to see them)
# food_type.view()
# quantity.view()
# cooking_time.view()

# --- 3. Define Fuzzy Rules ---

# Main rules as specified
rule1 = ctrl.Rule(food_type['raw'] & quantity['large'], cooking_time['VL'])
rule2 = ctrl.Rule(food_type['half_cooked'] & quantity['medium'], cooking_time['MT'])
rule3 = ctrl.Rule(food_type['fully_cooked'] & quantity['little'], cooking_time['VS'])

# Additional rules for other combinations
rule4 = ctrl.Rule(food_type['raw'] & quantity['medium'], cooking_time['Lo'])
rule5 = ctrl.Rule(food_type['raw'] & quantity['little'], cooking_time['MT'])
rule6 = ctrl.Rule(food_type['half_cooked'] & quantity['large'], cooking_time['Lo'])
rule7 = ctrl.Rule(food_type['half_cooked'] & quantity['little'], cooking_time['S'])
rule8 = ctrl.Rule(food_type['fully_cooked'] & quantity['large'], cooking_time['MT'])
rule9 = ctrl.Rule(food_type['fully_cooked'] & quantity['medium'], cooking_time['S'])

# --- 4. Create the Control System ---

cooking_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
cooking_simulation = ctrl.ControlSystemSimulation(cooking_ctrl)

def get_linguistic_term(time_value):
    if time_value <= 15:
        return "VS (Very Short)"
    elif time_value <= 30:
        return "S (Short)"
    elif time_value <= 45:
        return "MT (Medium)"
    elif time_value <= 55:
        return "Lo (Long)"
    else:
        return "VL (Very Long)"

# --- Streamlit UI ---
st.set_page_config(page_title="Smart Microwave Fuzzy Logic", layout="centered")

st.title("Smart Microwave Cooking Time Predictor 🍜")
st.markdown("""
Welcome to the Smart Microwave! Use the sliders below to specify your food and quantity,
and let our fuzzy logic system recommend the optimal cooking time.
""")

# Input selection for Food Type
st.subheader("1. Select Type of Food")
food_type_options = {
    "Raw (R)": 0,
    "Half-cooked (H)": 5,
    "Fully cooked (F)": 10
}
selected_food_type_label = st.selectbox(
    "Choose the state of your food:",
    list(food_type_options.keys())
)
selected_food_type_value = food_type_options[selected_food_type_label]

# Input selection for Quantity of Food
st.subheader("2. Select Quantity of Food")
quantity_options = {
    "Little (Li)": 0,
    "Medium (Md)": 5,
    "Large (Lg)": 10
}
selected_quantity_label = st.selectbox(
    "Choose the quantity:",
    list(quantity_options.keys())
)
selected_quantity_value = quantity_options[selected_quantity_label]

st.markdown("---")

# Calculate and display result
if st.button("Calculate Cooking Time"):
    try:
        # Pass crisp inputs to the simulation
        cooking_simulation.input['food_type'] = selected_food_type_value
        cooking_simulation.input['quantity'] = selected_quantity_value

        # Compute the fuzzy result
        cooking_simulation.compute()

        # Get the defuzzified output
        recommended_time = cooking_simulation.output['cooking_time']
        
        # Convert to linguistic term
        linguistic_term = get_linguistic_term(recommended_time)

        st.subheader("Recommended Cooking Time:")
        st.success(f"*{linguistic_term}*")
        st.info(f"Numerical Value: {recommended_time:.2f} minutes")
        st.balloons()

    except Exception as e:
        st.error(f"An error occurred during calculation: {e}")
        st.warning("Please ensure valid inputs are selected.")

st.markdown("""
---
This app demonstrates a basic fuzzy logic system. The cooking times are illustrative.
""")