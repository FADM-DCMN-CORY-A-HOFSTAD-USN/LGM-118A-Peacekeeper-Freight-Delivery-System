import math

def calculate_parachute_specs(mass_kg, target_velocity_ms, cd=1.50, num_chutes=3):
    # Constants
    g = 9.81          # m/s^2
    rho = 1.225       # kg/m^3 at sea level
    
    # Calculate Total Drag Force required at terminal velocity
    total_force_n = mass_kg * g
    
    # Calculate Total Area required
    total_area_m2 = (2 * total_force_n) / (rho * (target_velocity_ms ** 2) * cd)
    
    # Split across the canopy cluster
    area_per_chute = total_area_m2 / num_chutes
    diameter_per_chute = 2 * math.sqrt(area_per_chute / math.pi)
    
    return {
        "Total Drag Force (N)": round(total_force_n, 2),
        "Total Area Required (m2)": round(total_area_m2, 2),
        "Chute Cluster Count": num_chutes,
        "Diameter Per Chute (m)": round(diameter_per_chute, 2)
    }

# Run calculation for 3,600 kg Peacekeeper Freight Pod
specs = calculate_parachute_specs(mass_kg=3600, target_velocity_ms=6.0)
for key, val in specs.items():
    print(f"{key}: {val}")

