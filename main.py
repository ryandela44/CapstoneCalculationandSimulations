from acceleration import *
from battery import *
from power import *
from speed import *
from torque import *
from plots import *
from friction import *

if __name__ == '__main__':
    g = 9.81  # Gravity in m/s^2
    mass_total = 100  # Total mass of the bike and rider in kg
    mass_wheel = 1.4  # Mass of the wheel in kg
    r = 0.6604  # Radius of the wheel in meters
    k = 0.15  # Radius of gyration in meters
    mu_k = 0.05  # Kinetic friction coefficient for skis on snow
    terrain_coefficient = 0.2
    # wet 0.4 , #dry 0.7
    tire_material_coefficient = 0.4
    # Initialize lists to store data
    incline_angles_list = range(-3, 4)  # Incline angles
    modes = ['Motor Only', 'Pedaling Only', 'Combined']
    # Initialize lists to store data
    # incline_angles_list = range(-10, 11)
    max_speed_motor_only = []
    max_speed_pedaling_only = []
    max_speed_combined = []
    operational_time_without_pedaling = []
    operational_time_with_pedaling = []
    range_without_pedaling = []
    range_with_pedaling = []
    energy_efficiency = []
    total_torque_without_pedaling = []
    total_torque_with_pedaling = []
    total_power_without_pedaling = []
    total_power_with_pedaling = []
    braking_distances = []
    # Initialize lists to store data
    max_speed_motor_only_1 = []
    max_speed_pedaling_only_1 = []
    max_speed_combined_1 = []

    time = 10

    # Loop through incline angles and modes
    for incline_angle in incline_angles_list:
        for mode in modes:
            if mode == 'Motor Only':
                power_val = 1000
                pedaling_power_val = 0
                initial_speed = 0  # Starting from rest
                final_speed = 10  # Example final speed
            elif mode == 'Pedaling Only':
                power_val = 0
                pedaling_power_val = 150
                initial_speed = 0  # Starting from rest
                final_speed = 10  # Example final speed
            else:  # Combined mode
                power_val = 1000
                pedaling_power_val = 150
                initial_speed = 0  # Starting from rest
                final_speed = 10  # Example final speed

                # Calculate acceleration
            acceleration_val = calculate_acceleration(initial_speed, final_speed, time)
            # Append acceleration values to corresponding lists based on mode
            if mode == 'Motor Only':
                max_speed_motor_only_1.append(acceleration_val)
            elif mode == 'Pedaling Only':
                max_speed_pedaling_only_1.append(acceleration_val)
            else:  # Combined mode
                max_speed_combined_1.append(acceleration_val)

            # Calculate various parameters
            mu_s_total_val = calculate_static_friction_coefficient(r, k, mass_total, g, incline_angle,
                                                                   tire_material_coefficient, terrain_coefficient)
            mu_s_wheel_val = calculate_static_friction_coefficient(r, k, mass_wheel, g, incline_angle,
                                                                   tire_material_coefficient, terrain_coefficient)
            kinetic_friction_force_val = calculate_kinetic_friction_force(mass_total, g, incline_angle, mu_k)
            normal_force_val = calculate_normal_force(mass_total, g, incline_angle)
            static_friction_force_val = calculate_frictional_force(mu_s_total_val, normal_force_val)
            load_force_val = calculate_load_force(mass_total, g, incline_angle, mu_k, mu_s_total_val)
            required_torque_val = calculate_required_torque(load_force_val, r)

            battery_voltage_val = 48
            battery_capacity_ah_val = 13
            energy_capacity_wh_val = battery_voltage_val * battery_capacity_ah_val
            average_speed_val = 10
            actual_power_required_val = calculate_actual_power_required(load_force_val, average_speed_val)
            max_speed_val = calculate_max_speed(power_val, load_force_val, r)
            operational_time_h_val = calculate_operational_time(energy_capacity_wh_val, actual_power_required_val)
            range_km_val = calculate_range_km(operational_time_h_val, average_speed_val)
            torque_from_pedaling_val = calculate_pedaling_contribution(pedaling_power_val, r, average_speed_val)
            total_torque_with_pedaling_val = required_torque_val + torque_from_pedaling_val
            total_power_with_pedaling_val = actual_power_required_val + pedaling_power_val
            operational_time_with_pedaling_val = calculate_operational_time(energy_capacity_wh_val,
                                                                            total_power_with_pedaling_val)
            range_with_pedaling_val = calculate_range_km(operational_time_with_pedaling_val, average_speed_val)
            distance_traveled_km_val = range_with_pedaling_val
            total_energy_consumed_wh_val = energy_capacity_wh_val
            energy_efficiency_val = calculate_energy_efficiency(mass_total, g, incline_angle, distance_traveled_km_val,
                                                                total_energy_consumed_wh_val)

            # Append values to corresponding lists
            if mode == 'Motor Only':
                max_speed_motor_only.append(max_speed_val)
                operational_time_without_pedaling.append(operational_time_h_val)
                range_without_pedaling.append(range_km_val)
                total_torque_without_pedaling.append(required_torque_val)
                total_power_without_pedaling.append(actual_power_required_val)
            elif mode == 'Pedaling Only':
                max_speed_pedaling_only.append(max_speed_val)
                operational_time_with_pedaling.append(operational_time_with_pedaling_val)
                range_with_pedaling.append(range_with_pedaling_val)
                total_torque_with_pedaling.append(total_torque_with_pedaling_val)
                total_power_with_pedaling.append(total_power_with_pedaling_val)
            else:  # Combined mode
                max_speed_combined.append(max_speed_val)
                energy_efficiency.append(energy_efficiency_val)

            # Print scenario details
            print(f"Scenario: {mode}")
            print(f"Incline angle: {incline_angle}")
            print(f"Static Friction Coefficient for the bike system: {mu_s_total_val}")
            print(f"Static Friction Coefficient for just the wheel: {mu_s_wheel_val}")
            print(f"Static Friction Force : {static_friction_force_val} N")
            print(f"Kinetic Friction Force for the skis: {kinetic_friction_force_val} N")
            print(f"Total Load Force to be overcome: {load_force_val} N")
            print(f"Required Torque to overcome the load: {required_torque_val} Nm")
            print(f"Additional Torque from Pedaling: {torque_from_pedaling_val:.2f} Nm")
            print(f"Total Torque with Pedaling: {total_torque_with_pedaling_val:.2f} Nm")
            print(f"Total Power with Pedaling: {total_power_with_pedaling_val} W")
            print(f"Actual Power Required at {average_speed_val} m/s: {actual_power_required_val} W")
            print(f"Maximum Speed achievable: {max_speed_val} m/s")
            print(f"Energy Capacity of the battery: {energy_capacity_wh_val} Wh")
            print(f"Operational Time without pedaling: {operational_time_h_val:.2f} hours")
            print(f"Estimated Range without pedaling: {range_km_val:.2f} km")
            print(f"Operational Time with pedaling: {operational_time_with_pedaling_val:.2f} hours")
            print(f"Estimated Range with pedaling: {range_with_pedaling_val:.2f} km")
            print(f"Energy Efficiency: {energy_efficiency_val:.2f}%")
            print("-" * 30)

    setup_plot()
    plot_speed_vs_angle(incline_angles_list, max_speed_motor_only, max_speed_pedaling_only, max_speed_combined)
    plot_operational_time_vs_angle(incline_angles_list, operational_time_without_pedaling,
                                   operational_time_with_pedaling)
    plot_estimated_range_vs_angle(incline_angles_list, range_without_pedaling, range_with_pedaling)
    plot_efficieny_vs_incline_angle(incline_angles_list, energy_efficiency)
    plot_torque_vs_incline_angle(incline_angles_list, total_torque_without_pedaling, total_torque_with_pedaling)
    plot_power_vs_incline_angle(incline_angles_list, total_power_without_pedaling, total_torque_with_pedaling)
    plot_speed_vs_time(time, max_speed_motor_only_1, max_speed_pedaling_only_1, max_speed_combined_1)
