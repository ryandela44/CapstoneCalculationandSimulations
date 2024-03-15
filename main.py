import math


class ElectricSkiBike:
    def __init__(self, mass, wheel_radius, mu_s_wheel, mu_k_skis, mu_k_wheel, power_val, pedaling_power_val,
                 battery_voltage, battery_capacity_ah):
        self.mass = mass
        self.wheel_radius = wheel_radius
        self.mu_s_wheel = mu_s_wheel
        self.mu_k_skis = mu_k_skis
        self.mu_k_wheel = mu_k_wheel
        self.power_val = power_val
        self.pedaling_power_val = pedaling_power_val
        self.battery = Battery(battery_voltage, battery_capacity_ah)

    def get_effective_power(self, mode):
        if mode == "Motor Only":
            return self.power_val
        elif mode == "Pedaling Only":
            return self.pedaling_power_val
        elif mode == "Combined":
            return self.power_val + self.pedaling_power_val
        else:
            return 0

    def get_gear_ratio(self, mode):
        if mode == "Pedaling Only":
            return 3
        elif mode == "Combined":
            return 2.5
        else:
            return 1

    def simulate(self, incline_angles_list):
        for incline_angle in incline_angles_list:
            environment = Environment(incline_angle)
            for mode in ["Motor Only", "Pedaling Only", "Combined"]:
                self.run_scenario(mode, environment)

    def run_scenario(self, mode, environment):
        effective_power = self.get_effective_power(mode)
        gear_ratio = self.get_gear_ratio(mode)
        normal_force = environment.calculate_normal_force(self.mass)
        static_friction_force_wheel, kinetic_friction_force = environment.calculate_friction_forces(normal_force,
                                                                                                    self.mu_s_wheel,
                                                                                                    self.mu_k_skis,
                                                                                                    self.mu_k_wheel)
        condition, initial_torque = environment.check_starting_condition(effective_power, gear_ratio, self.wheel_radius,
                                                                         static_friction_force_wheel)

        print(f"\nScenario: {mode}, Incline angle: {environment.incline_angle} degrees")
        if condition == 'insufficient':
            print(f"Insufficient torque ({initial_torque:.2f} Nm): The bike does not move.")
        elif condition == 'sufficient':
            print(f"Sufficient torque ({initial_torque:.2f} Nm): The bike will roll without sliding at the start.")
        else:
            print(f"Excessive torque ({initial_torque:.2f} Nm): The bike may slide at the start.")

        if condition != 'insufficient':
            load_force = kinetic_friction_force
            required_torque = environment.calculate_required_torque(load_force, self.wheel_radius)
            average_speed = environment.calculate_max_speed(effective_power, load_force, self.wheel_radius)
            actual_power_required = environment.calculate_actual_power_required(load_force, average_speed)
            operational_time_h = self.battery.calculate_operational_time(actual_power_required)
            range_km = environment.calculate_range_km(operational_time_h, average_speed)

            self.print_simulation_details(effective_power, static_friction_force_wheel, kinetic_friction_force,
                                          required_torque, average_speed, operational_time_h, range_km)

    def print_simulation_details(self, effective_power, static_friction_force_wheel, kinetic_friction_force,
                                 required_torque, average_speed, operational_time_h, range_km):
        print(f"Effective Power: {effective_power} W")
        print(f"Static Friction Force at the wheel: {static_friction_force_wheel:.2f} N")
        print(f"Kinetic Friction Force overall: {kinetic_friction_force:.2f} N")
        print(f"Required Torque for continuous motion: {required_torque:.2f} Nm")
        print(f"Average Speed: {average_speed:.2f} m/s")
        print(f"Operational Time: {operational_time_h:.2f} hours")
        print(f"Estimated Range: {range_km:.2f} km\n")


class Battery:
    def __init__(self, voltage, capacity_ah):
        self.energy_capacity_wh = voltage * capacity_ah

    def calculate_operational_time(self, power_consumption_w):
        if power_consumption_w == 0:
            return 0
        else:
            return self.energy_capacity_wh / power_consumption_w


class Environment:
    g = 9.81  # Gravity in m/s^2

    def __init__(self, incline_angle):
        self.incline_angle = incline_angle

    def calculate_normal_force(self, mass):
        theta_radians = math.radians(self.incline_angle)
        return mass * self.g * math.cos(theta_radians)

    def calculate_friction_forces(self, normal_force, mu_s_wheel, mu_k_skis, mu_k_wheel):
        static_friction_force_wheel = mu_s_wheel * normal_force
        kinetic_friction_force = (mu_k_skis * normal_force * 0.9) + (mu_k_wheel * normal_force * 0.1)
        return static_friction_force_wheel, kinetic_friction_force

    def check_starting_condition(self, effective_power, gear_ratio, radius_wheel, static_friction_force_wheel):
        nominal_speed_rpm = 100
        initial_torque = (effective_power * gear_ratio) / (2 * math.pi * (nominal_speed_rpm / 60))
        torque_needed_to_overcome_static_friction = static_friction_force_wheel * radius_wheel
        minimum_torque_to_move = torque_needed_to_overcome_static_friction * 0.8

        if initial_torque < minimum_torque_to_move:
            return 'insufficient', initial_torque
        elif initial_torque <= torque_needed_to_overcome_static_friction:
            return 'sufficient', initial_torque
        else:
            return 'excessive', initial_torque

    def calculate_required_torque(self, load_force, radius_of_wheel):
        return load_force * radius_of_wheel

    def calculate_max_speed(self, power, load_force, radius_of_wheel, realistic_max_speed=20):
        if load_force == 0:
            return realistic_max_speed
        torque = power / (load_force / radius_of_wheel)
        angular_velocity = torque / radius_of_wheel
        max_speed = angular_velocity * radius_of_wheel
        return min(max_speed, realistic_max_speed)

    def calculate_actual_power_required(self, load_force, speed):
        return load_force * speed

    def calculate_range_km(self, operational_time_h, speed_m_per_s):
        if operational_time_h == 0:
            return 0
        else:
            speed_km_per_h = speed_m_per_s * 3.6
            return speed_km_per_h * operational_time_h


if __name__ == '__main__':
    bike = ElectricSkiBike(
        mass=100,
        wheel_radius=0.6604,
        mu_s_wheel=0.3,
        mu_k_skis=0.03,
        mu_k_wheel=0.25,
        power_val=1000,
        pedaling_power_val=150,
        battery_voltage=48,
        battery_capacity_ah=13
    )
    incline_angles_list = range(-3, 4)
    bike.simulate(incline_angles_list)
