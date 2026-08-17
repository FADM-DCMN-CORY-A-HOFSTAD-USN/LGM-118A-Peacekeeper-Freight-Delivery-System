import math

class CargoPodFlightComputer:
    def __init__(self):
        # System status flags
        self.rcs_active = True
        self.drogue_deployed = False
        self.main_deployed = False
        self.landed = False
        
        # Safe structural limits for parachute deployment
        self.MAX_DROGUE_PRESSURE = 45000  # Pascals
        self.MAX_MAIN_VELOCITY = 85.0     # m/s (~Mach 0.25)
        self.TOUCHDOWN_VELOCITY = 6.0     # m/s

    def calculate_dynamic_pressure(self, air_density, velocity):
        """Calculates dynamic pressure (q = 0.5 * rho * v^2) to ensure structural safety."""
        return 0.5 * air_density * (velocity ** 2)

    def process_telemetry(self, altitude, velocity, air_density):
        """Main flight software loop executed every clock cycle during descent."""
        if self.landed:
            return "Mission Complete: Cargo secured on surface."

        # Compute real-time physics metrics
        dynamic_pressure = self.calculate_dynamic_pressure(air_density, velocity)

        # State 1: High-Altitude Re-entry Aerobraking
        if altitude > 20000:
            return f"Status: Re-entry aerobraking. RCS aligning heatshield. Velocity: {velocity:.1f} m/s"

        # State 2: Drogue Chute Deployment Trigger
        if altitude <= 20000 and not self.drogue_deployed:
            if dynamic_pressure < self.MAX_DROGUE_PRESSURE:
                self.drogue_deployed = True
                self.rcs_active = False  # Deactivate RCS to avoid burning the parachute lines
                return "EVENT: Dynamic pressure safe. Mortar firing DROGUE parachute."
            else:
                return "Status: Waiting for dynamic pressure to drop below structural threshold."

        # State 3: Main Chute Deployment Trigger
        if self.drogue_deployed and not self.main_deployed:
            if altitude <= 3000 and velocity < self.MAX_MAIN_VELOCITY:
                self.main_deployed = True
                return "EVENT: Low altitude and velocity achieved. Deploying MAIN cargo parachutes."
            else:
                return f"Status: Stabilized by drogue. Descending to main deploy altitude. Velocity: {velocity:.1f} m/s"

        # State 4: Final Descent to Touchdown
        if self.main_deployed:
            if altitude <= 0 or velocity <= self.TOUCHDOWN_VELOCITY:
                self.landed = True
                return "EVENT: Touchdown detected. Cutting parachute risers immediately to prevent dragging."
            return f"Status: Final descent under main canopy. Velocity: {velocity:.1f} m/s"

# --- Simulation Execution Example ---
computer = CargoPodFlightComputer()

# Mock flight data slice: Approaching drogue deployment altitude at high speed
print(computer.process_telemetry(altitude=22000, velocity=1200.0, air_density=0.04))
print(computer.process_telemetry(altitude=18000, velocity=250.0, air_density=0.09))   # Pressure too high!
print(computer.process_telemetry(altitude=15000, velocity=90.0, air_density=0.15))    # Safe to deploy drogue
print(computer.process_telemetry(altitude=2500, velocity=45.0, air_density=1.1))      # Safe to deploy main

