import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class FuzzyMicrowaveOven:
    def __init__(self):
        """Initialize the fuzzy logic microwave oven system"""
        self.setup_fuzzy_system()
    
    def setup_fuzzy_system(self):
        """Set up the fuzzy logic control system"""
        
        # Define input variables
        self.temperature = ctrl.Antecedent(np.arange(-18, 71, 1), 'temperature')
        self.weight = ctrl.Antecedent(np.arange(0, 1501, 1), 'weight')
        
        # Define output variable
        self.cooking_time = ctrl.Consequent(np.arange(0, 61, 1), 'cooking_time')
        
        # Define membership functions for temperature
        self.temperature['frozen'] = fuzz.trapmf(self.temperature.universe, [-18, -18, -10, 0])
        self.temperature['normal'] = fuzz.trimf(self.temperature.universe, [-5, 22, 30])
        self.temperature['hot'] = fuzz.trapmf(self.temperature.universe, [24, 50, 70, 70])
        
        # Define membership functions for weight
        self.weight['light'] = fuzz.trapmf(self.weight.universe, [0, 0, 200, 400])
        self.weight['medium'] = fuzz.trimf(self.weight.universe, [300, 500, 700])
        self.weight['heavy'] = fuzz.trapmf(self.weight.universe, [600, 1000, 1500, 1500])
        
        # Define membership functions for cooking time
        self.cooking_time['very_short'] = fuzz.trimf(self.cooking_time.universe, [0, 5, 10])
        self.cooking_time['short'] = fuzz.trimf(self.cooking_time.universe, [4, 10, 16])
        self.cooking_time['normal'] = fuzz.trimf(self.cooking_time.universe, [12, 20, 30])
        self.cooking_time['long'] = fuzz.trimf(self.cooking_time.universe, [25, 40, 55])
        self.cooking_time['very_long'] = fuzz.trapmf(self.cooking_time.universe, [40, 60, 60, 60])
        
        # Define fuzzy rules
        self.rules = [
            # Frozen food rules
            ctrl.Rule(self.temperature['frozen'], self.cooking_time['very_long']),
            
            # Normal temperature rules
            ctrl.Rule(self.temperature['normal'] & self.weight['light'], self.cooking_time['short']),
            ctrl.Rule(self.temperature['normal'] & self.weight['medium'], self.cooking_time['normal']),
            ctrl.Rule(self.temperature['normal'] & self.weight['heavy'], self.cooking_time['long']),
            
            # Hot temperature rules
            ctrl.Rule(self.temperature['hot'] & self.weight['light'], self.cooking_time['very_short']),
            ctrl.Rule(self.temperature['hot'] & self.weight['medium'], self.cooking_time['short']),
            ctrl.Rule(self.temperature['hot'] & self.weight['heavy'], self.cooking_time['normal']),
        ]
        
        # Create control system
        self.cooking_ctrl = ctrl.ControlSystem(self.rules)
        self.cooking_simulation = ctrl.ControlSystemSimulation(self.cooking_ctrl)
    
    def calculate_cooking_time(self, temp, weight):
        """
        Calculate cooking time based on food temperature and weight
        
        Args:
            temp (float): Food temperature in Celsius (-18 to 70)
            weight (float): Food weight in grams (0 to 1500)
        
        Returns:
            float: Cooking time in minutes
        """
        # Validate inputs
        if not (-18 <= temp <= 70):
            raise ValueError("Temperature must be between -18°C and 70°C")
        if not (0 <= weight <= 1500):
            raise ValueError("Weight must be between 0g and 1500g")
        
        # Set input values
        self.cooking_simulation.input['temperature'] = temp
        self.cooking_simulation.input['weight'] = weight
        
        # Compute the result
        self.cooking_simulation.compute()
        
        return round(self.cooking_simulation.output['cooking_time'], 2)
    
    def visualize_membership_functions(self):
        """Plot the membership functions for visualization"""
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(12, 10))
        
        # Temperature membership functions
        ax0.plot(self.temperature.universe, fuzz.interp_membership(self.temperature.universe, self.temperature['frozen'].mf, self.temperature.universe), 'b', linewidth=1.5, label='Frozen')
        ax0.plot(self.temperature.universe, fuzz.interp_membership(self.temperature.universe, self.temperature['normal'].mf, self.temperature.universe), 'g', linewidth=1.5, label='Normal')
        ax0.plot(self.temperature.universe, fuzz.interp_membership(self.temperature.universe, self.temperature['hot'].mf, self.temperature.universe), 'r', linewidth=1.5, label='Hot')
        ax0.set_title('Food Temperature')
        ax0.set_xlabel('Temperature (°C)')
        ax0.set_ylabel('Membership')
        ax0.legend()
        ax0.grid(True)
        
        # Weight membership functions
        ax1.plot(self.weight.universe, fuzz.interp_membership(self.weight.universe, self.weight['light'].mf, self.weight.universe), 'b', linewidth=1.5, label='Light')
        ax1.plot(self.weight.universe, fuzz.interp_membership(self.weight.universe, self.weight['medium'].mf, self.weight.universe), 'g', linewidth=1.5, label='Medium')
        ax1.plot(self.weight.universe, fuzz.interp_membership(self.weight.universe, self.weight['heavy'].mf, self.weight.universe), 'r', linewidth=1.5, label='Heavy')
        ax1.set_title('Food Weight')
        ax1.set_xlabel('Weight (grams)')
        ax1.set_ylabel('Membership')
        ax1.legend()
        ax1.grid(True)
        
        # Cooking time membership functions
        ax2.plot(self.cooking_time.universe, fuzz.interp_membership(self.cooking_time.universe, self.cooking_time['very_short'].mf, self.cooking_time.universe), 'purple', linewidth=1.5, label='Very Short')
        ax2.plot(self.cooking_time.universe, fuzz.interp_membership(self.cooking_time.universe, self.cooking_time['short'].mf, self.cooking_time.universe), 'b', linewidth=1.5, label='Short')
        ax2.plot(self.cooking_time.universe, fuzz.interp_membership(self.cooking_time.universe, self.cooking_time['normal'].mf, self.cooking_time.universe), 'g', linewidth=1.5, label='Normal')
        ax2.plot(self.cooking_time.universe, fuzz.interp_membership(self.cooking_time.universe, self.cooking_time['long'].mf, self.cooking_time.universe), 'orange', linewidth=1.5, label='Long')
        ax2.plot(self.cooking_time.universe, fuzz.interp_membership(self.cooking_time.universe, self.cooking_time['very_long'].mf, self.cooking_time.universe), 'r', linewidth=1.5, label='Very Long')
        ax2.set_title('Cooking Time')
        ax2.set_xlabel('Time (minutes)')
        ax2.set_ylabel('Membership')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.show()

def main():
    """Main function to demonstrate the fuzzy microwave system"""
    oven = FuzzyMicrowaveOven()
    
    print("🔥 Fuzzy Logic Microwave Oven System 🔥")
    print("=" * 40)
    
    while True:
        try:
            # Get user input
            print("\nEnter food properties:")
            temp = float(input("Food Temperature [-18 to 70°C]: "))
            weight = float(input("Food Weight [0 to 1500g]: "))
            
            # Calculate cooking time
            cooking_time = oven.calculate_cooking_time(temp, weight)
            
            print(f"\n🕐 Recommended Cooking Time: {cooking_time} minutes")
            
            # Ask if user wants to visualize
            show_viz = input("\nShow membership function plots? (y/n): ").lower().strip()
            if show_viz == 'y':
                oven.visualize_membership_functions()
            
            # Ask if user wants to continue
            continue_input = input("\nCalculate another cooking time? (y/n): ").lower().strip()
            if continue_input != 'y':
                break
                
        except ValueError as e:
            print(f"❌ Error: {e}")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()