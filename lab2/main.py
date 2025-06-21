import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Fuzzy Logic Air Conditioning System",
    page_icon="🌡️",
    layout="wide"
)

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

def create_fuzzy_system():
    """Create the fuzzy logic control system"""
    # Define input and output variables
    error = ctrl.Antecedent(np.arange(-10, 11, 0.1), 'error')
    error_dot = ctrl.Antecedent(np.arange(-15, 16, 0.1), 'error_dot')
    cooling = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'cooling')
    
    # Define membership functions for error
    error['negative'] = fuzz.trapmf(error.universe, [-10, -10, -4, 0])
    error['zero'] = fuzz.trimf(error.universe, [-2, 0, 2])
    error['positive'] = fuzz.trapmf(error.universe, [0, 4, 10, 10])
    
    # Define membership functions for error_dot
    error_dot['negative'] = fuzz.trapmf(error_dot.universe, [-15, -15, -10, 0])
    error_dot['zero'] = fuzz.trimf(error_dot.universe, [-5, 0, 5])
    error_dot['positive'] = fuzz.trapmf(error_dot.universe, [0, 10, 15, 15])
    
    # Define membership functions for cooling output
    cooling['off'] = fuzz.trapmf(cooling.universe, [0, 0, 0.3, 0.5])
    cooling['on'] = fuzz.trapmf(cooling.universe, [0.5, 0.7, 1, 1])
    
    # Define fuzzy rules
    rule1 = ctrl.Rule(error['negative'], cooling['on'])  # Too hot -> cooling on
    rule2 = ctrl.Rule(error['zero'], cooling['off'])     # Perfect -> cooling off
    rule3 = ctrl.Rule(error['positive'], cooling['off']) # Too cold -> cooling off
    rule4 = ctrl.Rule(error_dot['positive'], cooling['on'])  # Getting hotter -> cooling on
    rule5 = ctrl.Rule(error_dot['negative'], cooling['off']) # Getting colder -> cooling off
    
    # Create control system
    cooling_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
    cooling_sim = ctrl.ControlSystemSimulation(cooling_ctrl)
    
    return cooling_sim, error, error_dot, cooling

def calculate_error_dot(current_error):
    """Calculate error dot (rate of change)"""
    if len(st.session_state.history) == 0:
        return 0.0
    
    previous_error = st.session_state.history[-1]['error']
    return previous_error - current_error

def add_reading(target_temp, room_temp):
    """Add a new temperature reading to history"""
    error = target_temp - room_temp
    error_dot = calculate_error_dot(error)
    
    reading = {
        'timestamp': datetime.now(),
        'target_temp': target_temp,
        'room_temp': room_temp,
        'error': error,
        'error_dot': error_dot
    }
    
    st.session_state.history.append(reading)
    return error, error_dot

def plot_membership_functions(fuzzy_var, current_value, title):
    """Plot membership functions for a fuzzy variable"""
    fig = go.Figure()
    
    colors = {'negative': '#e74c3c', 'zero': '#27ae60', 'positive': '#3498db',
              'off': '#3498db', 'on': '#e74c3c'}
    
    for label in fuzzy_var.terms:
        mf = fuzzy_var[label].mf
        fig.add_trace(go.Scatter(
            x=fuzzy_var.universe,
            y=mf,
            mode='lines',
            name=label.title(),
            line=dict(color=colors.get(label, '#2c3e50'), width=3)
        ))
    
    # Add current value line
    fig.add_vline(
        x=current_value,
        line_dash="dash",
        line_color="#f39c12",
        line_width=4,
        annotation_text="Current Value"
    )
    
    fig.update_layout(
        title=title,
        xaxis_title=fuzzy_var.label.title(),
        yaxis_title="Membership Degree",
        yaxis=dict(range=[0, 1.1]),
        height=400,
        template="plotly_white"
    )
    
    return fig

def plot_output(cooling_var, cooling_output):
    """Plot the fuzzy output and defuzzification"""
    fig = go.Figure()
    
    # Plot membership functions
    for label in cooling_var.terms:
        mf = cooling_var[label].mf
        fig.add_trace(go.Scatter(
            x=cooling_var.universe,
            y=mf,
            mode='lines',
            name=f'Cooling {label.upper()}',
            line=dict(width=2)
        ))
    
    # Add defuzzified output line
    fig.add_vline(
        x=cooling_output,
        line_dash="dash",
        line_color="#8e44ad",
        line_width=4,
        annotation_text=f"Output: {cooling_output:.3f}"
    )
    
    fig.update_layout(
        title="Fuzzy Output and Defuzzification",
        xaxis_title="Cooling Output",
        yaxis_title="Membership Degree",
        yaxis=dict(range=[0, 1.1]),
        height=400,
        template="plotly_white"
    )
    
    return fig

def main():
    st.title("🌡️ Fuzzy Logic Air Conditioning System")
    st.markdown("---")
    
    # Create fuzzy system
    cooling_sim, error_var, error_dot_var, cooling_var = create_fuzzy_system()
    
    # Sidebar controls
    st.sidebar.header("Temperature Controls")
    
    target_temp = st.sidebar.slider(
        "Target Temperature (°F)",
        min_value=60.0,
        max_value=90.0,
        value=72.0,
        step=0.5
    )
    
    room_temp = st.sidebar.slider(
        "Current Room Temperature (°F)",
        min_value=60.0,
        max_value=90.0,
        value=75.0,
        step=0.5
    )
    
    if st.sidebar.button("Add Temperature Reading", type="primary"):
        error, error_dot = add_reading(target_temp, room_temp)
        st.sidebar.success(f"Reading added! Error: {error:.1f}°F, Rate: {error_dot:.1f}°F/min")
    
    # Calculate current values
    current_error = target_temp - room_temp
    current_error_dot = calculate_error_dot(current_error)
    
    # Run fuzzy logic simulation
    try:
        cooling_sim.input['error'] = current_error
        cooling_sim.input['error_dot'] = current_error_dot
        cooling_sim.compute()
        cooling_output = cooling_sim.output['cooling']
    except:
        cooling_output = 0.0
    
    # Display current status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Target Temperature", f"{target_temp:.1f}°F")
    
    with col2:
        st.metric("Room Temperature", f"{room_temp:.1f}°F")
    
    with col3:
        delta_color = "inverse" if current_error > 0 else "normal"
        st.metric("Temperature Error", f"{current_error:.1f}°F", delta=f"{current_error:.1f}°F")
    
    with col4:
        cooling_status = "ON" if cooling_output > 0.5 else "OFF"
        st.metric("Cooling Status", cooling_status, f"{cooling_output:.1%}")
    
    st.markdown("---")
    
    # Create visualization tabs
    tab1, tab2, tab3 = st.tabs(["📊 Membership Functions", "🎛️ System Output", "📈 History"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            error_fig = plot_membership_functions(
                error_var, current_error, 
                "Temperature Error Membership Functions"
            )
            st.plotly_chart(error_fig, use_container_width=True)
        
        with col2:
            error_dot_fig = plot_membership_functions(
                error_dot_var, current_error_dot,
                "Error Rate Membership Functions"
            )
            st.plotly_chart(error_dot_fig, use_container_width=True)
    
    with tab2:
        output_fig = plot_output(cooling_var, cooling_output)
        st.plotly_chart(output_fig, use_container_width=True)
        
        # System interpretation
        st.subheader("System Interpretation")
        if cooling_output > 0.7:
            st.success("🔴 **Cooling System: ON** - Room is too warm, actively cooling")
        elif cooling_output < 0.3:
            st.info("🔵 **Cooling System: OFF** - Temperature is acceptable or room is too cold")
        else:
            st.warning("🟡 **Cooling System: MODERATE** - Partial cooling needed")
    
    with tab3:
        if st.session_state.history:
            # Convert history to DataFrame
            df = pd.DataFrame(st.session_state.history)
            df['time'] = df['timestamp'].dt.strftime('%H:%M:%S')
            
            # Display table
            st.subheader("Temperature History")
            display_df = df[['time', 'target_temp', 'room_temp', 'error', 'error_dot']].copy()
            display_df.columns = ['Time', 'Target (°F)', 'Room (°F)', 'Error (°F)', 'Rate (°F/min)']
            st.dataframe(display_df, use_container_width=True)
            
            # Plot history
            if len(df) > 1:
                fig = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=('Temperature History', 'Error History'),
                    vertical_spacing=0.1
                )
                
                # Temperature plot
                fig.add_trace(
                    go.Scatter(x=df.index, y=df['target_temp'], name='Target', line=dict(color='green')),
                    row=1, col=1
                )
                fig.add_trace(
                    go.Scatter(x=df.index, y=df['room_temp'], name='Room', line=dict(color='red')),
                    row=1, col=1
                )
                
                # Error plot
                fig.add_trace(
                    go.Scatter(x=df.index, y=df['error'], name='Error', line=dict(color='blue')),
                    row=2, col=1
                )
                fig.add_trace(
                    go.Scatter(x=df.index, y=df['error_dot'], name='Error Rate', line=dict(color='orange')),
                    row=2, col=1
                )
                
                fig.update_layout(height=600, template="plotly_white")
                fig.update_xaxes(title_text="Reading Number", row=2, col=1)
                fig.update_yaxes(title_text="Temperature (°F)", row=1, col=1)
                fig.update_yaxes(title_text="Error/Rate", row=2, col=1)
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Clear history button
            if st.button("Clear History", type="secondary"):
                st.session_state.history = []
                st.rerun()
        else:
            st.info("No temperature readings yet. Add some readings using the sidebar controls!")

if __name__ == "__main__":
    main()