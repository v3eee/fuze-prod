import streamlit as st
from oven import FuzzyMicrowaveOven

# Configure Streamlit page
st.set_page_config(
    page_title="🔥 Fuzzy Microwave Oven",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF6B35;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .sub-header {
        color: #2E86AB;
        font-size: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .result-box {
        background-color: #F8F9FA;
        border-left: 5px solid #28A745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .info-box {
        background-color: #E3F2FD;
        border-left: 5px solid #2196F3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .stSlider > div > div > div > div {
        background: linear-gradient(to right, #FF6B35, #F7931E);
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🔥 Fuzzy Logic Microwave Oven 🔥</h1>', unsafe_allow_html=True)

# Description
st.markdown("""
<div class="info-box">
<h3>🎯 Smart Cooking Time Predictor</h3>
This intelligent microwave system uses fuzzy logic to determine the optimal cooking time based on your food's temperature and weight. 
Simply adjust the sliders below and let the AI do the calculations!
</div>
""", unsafe_allow_html=True)

# Initialize the fuzzy oven system
@st.cache_resource
def get_oven():
    return FuzzyMicrowaveOven()

try:
    oven = get_oven()
    
    # Create two columns for inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="sub-header">🌡️ Food Temperature</h3>', unsafe_allow_html=True)
        
        # Temperature input with presets
        temp_preset = st.selectbox(
            "Quick Temperature Presets:",
            ["Custom", "Frozen (-18°C)", "Refrigerated (4°C)", "Room Temperature (22°C)", "Warm (45°C)", "Hot (70°C)"]
        )
        
        if temp_preset == "Frozen (-18°C)":
            temp_value = -18
        elif temp_preset == "Refrigerated (4°C)":
            temp_value = 4
        elif temp_preset == "Room Temperature (22°C)":
            temp_value = 22
        elif temp_preset == "Warm (45°C)":
            temp_value = 45
        elif temp_preset == "Hot (70°C)":
            temp_value = 70
        else:
            temp_value = 22
        
        temperature = st.slider(
            "Temperature (°C)",
            min_value=-18,
            max_value=70,
            value=temp_value,
            step=1,
            help="Range: -18°C (frozen) to 70°C (hot)"
        )
        
        # Temperature indicator
        if temperature <= 0:
            temp_status = "🧊 Frozen"
            temp_color = "#87CEEB"
        elif temperature <= 25:
            temp_status = "❄️ Cold/Normal"
            temp_color = "#90EE90"
        elif temperature <= 50:
            temp_status = "🌡️ Warm"
            temp_color = "#FFD700"
        else:
            temp_status = "🔥 Hot"
            temp_color = "#FF6347"
        
        st.markdown(f'<p style="color: {temp_color}; font-weight: bold; font-size: 1.2rem;">{temp_status}</p>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h3 class="sub-header">⚖️ Food Weight</h3>', unsafe_allow_html=True)
        
        # Weight input with presets
        weight_preset = st.selectbox(
            "Quick Weight Presets:",
            ["Custom", "Snack (100g)", "Single Serving (250g)", "Small Meal (500g)", "Family Meal (1000g)", "Large Portion (1500g)"]
        )
        
        if weight_preset == "Snack (100g)":
            weight_value = 100
        elif weight_preset == "Single Serving (250g)":
            weight_value = 250
        elif weight_preset == "Small Meal (500g)":
            weight_value = 500
        elif weight_preset == "Family Meal (1000g)":
            weight_value = 1000
        elif weight_preset == "Large Portion (1500g)":
            weight_value = 1500
        else:
            weight_value = 500
        
        weight = st.slider(
            "Weight (grams)",
            min_value=0,
            max_value=1500,
            value=weight_value,
            step=10,
            help="Range: 0g to 1500g"
        )
        
        # Weight indicator
        if weight <= 400:
            weight_status = "🪶 Light"
            weight_color = "#98FB98"
        elif weight <= 700:
            weight_status = "⚖️ Medium"
            weight_color = "#FFD700"
        else:
            weight_status = "🏋️ Heavy"
            weight_color = "#FF6347"
        
        st.markdown(f'<p style="color: {weight_color}; font-weight: bold; font-size: 1.2rem;">{weight_status}</p>', unsafe_allow_html=True)
    
    # Calculate cooking time
    st.markdown("---")
    
    # Calculate button
    if st.button("🚀 Calculate Optimal Cooking Time", type="primary", use_container_width=True):
        try:
            cooking_time = oven.calculate_cooking_time(temperature, weight)
            
            # Display result in a beautiful box
            st.markdown(f"""
            <div class="result-box">
                <h2 style="color: #28A745; text-align: center;">⏰ Recommended Cooking Time</h2>
                <h1 style="text-align: center; color: #FF6B35; font-size: 4rem;">{cooking_time:.1f} minutes</h1>
                <p style="text-align: center; font-size: 1.2rem; color: #6C757D;">
                    Perfect timing for your {weight}g food at {temperature}°C
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show fuzzy logic interpretation
            st.markdown('<h3 class="sub-header">🧠 Fuzzy Logic Analysis</h3>', unsafe_allow_html=True)
            
            # Determine which fuzzy sets are active
            temp_fuzzy = []
            if temperature <= 0:
                temp_fuzzy.append("Frozen")
            elif -5 <= temperature <= 30:
                temp_fuzzy.append("Normal")
            if 24 <= temperature <= 70:
                temp_fuzzy.append("Hot")
            
            weight_fuzzy = []
            if weight <= 400:
                weight_fuzzy.append("Light")
            if 300 <= weight <= 700:
                weight_fuzzy.append("Medium")
            if weight >= 600:
                weight_fuzzy.append("Heavy")
            
            time_fuzzy = ""
            if cooking_time <= 10:
                time_fuzzy = "Very Short"
            elif cooking_time <= 20:
                time_fuzzy = "Short"
            elif cooking_time <= 40:
                time_fuzzy = "Normal"
            elif cooking_time <= 50:
                time_fuzzy = "Long"
            else:
                time_fuzzy = "Very Long"
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info(f"**Temperature:** {', '.join(temp_fuzzy)}")
            with col2:
                st.info(f"**Weight:** {', '.join(weight_fuzzy)}")
            with col3:
                st.success(f"**Result:** {time_fuzzy}")
            
            # Add some cooking tips
            st.markdown('<h3 class="sub-header">💡 Smart Cooking Tips</h3>', unsafe_allow_html=True)
            
            tips = []
            if temperature <= 0:
                tips.append("🧊 Frozen food detected - extra time needed for defrosting")
            if weight > 1000:
                tips.append("🍽️ Large portion - consider stirring halfway through")
            if cooking_time > 40:
                tips.append("⏰ Long cooking time - check food periodically")
            if temperature > 50:
                tips.append("🔥 Food is already hot - just reheating needed")
            
            if tips:
                for tip in tips:
                    st.write(f"• {tip}")
            else:
                st.write("• 👍 Optimal conditions detected - standard cooking recommended")
            
            # Success animation
            st.balloons()
            
        except ValueError as e:
            st.error(f"❌ Input Error: {e}")
        except Exception as e:
            st.error(f"❌ Calculation Error: {e}")
    
    # Sidebar with additional information
    with st.sidebar:
        st.markdown("### 📊 System Information")
        
        st.markdown("**Fuzzy Variables:**")
        st.write("🌡️ **Temperature:**")
        st.write("- Frozen: -18°C to 0°C")
        st.write("- Normal: -5°C to 30°C")
        st.write("- Hot: 24°C to 70°C")
        
        st.write("⚖️ **Weight:**")
        st.write("- Light: 0g to 400g")
        st.write("- Medium: 300g to 700g")
        st.write("- Heavy: 600g to 1500g")
        
        st.write("⏰ **Cooking Time:**")
        st.write("- Very Short: 0-10 min")
        st.write("- Short: 5-20 min")
        st.write("- Normal: 10-40 min")
        st.write("- Long: 20-50 min")
        st.write("- Very Long: 40-60 min")
        
        st.markdown("---")
        st.markdown("### 🔧 Fuzzy Rules Examples")
        st.write("• Frozen food → Very Long time")
        st.write("• Hot + Light → Very Short time")
        st.write("• Normal + Medium → Normal time")
        st.write("• Normal + Heavy → Long time")
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.write("This system uses fuzzy logic to simulate intelligent microwave cooking decisions, considering food temperature and weight to optimize cooking time.")

except ImportError:
    st.error("❌ **Error**: Could not import the fuzzy microwave oven system.")
    st.write("Please ensure that:")
    st.write("1. The `oven.py` file exists in the same directory")
    st.write("2. Required packages are installed: `numpy`, `scikit-fuzzy`, `matplotlib`")
    st.write("3. Run: `pip install numpy scikit-fuzzy matplotlib streamlit`")

except Exception as e:
    st.error(f"❌ **Unexpected Error**: {e}")
    st.write("Please check your installation and try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6C757D; padding: 2rem;">
    <p>🔥 Fuzzy Logic Microwave Oven System | Made with ❤️ using Streamlit</p>
    <p><em>Intelligent cooking through fuzzy mathematics</em></p>
</div>
""", unsafe_allow_html=True)

