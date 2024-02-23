import math

import numpy as np
from matplotlib import pyplot as plt


def calculate_gravitational_force_parallel(mass, g, theta_degrees):
    """
    Calculate the gravitational force component parallel to the slope.
    """
    theta_radians = math.radians(theta_degrees)
    return mass * g * math.sin(theta_radians)


def calculate_normal_force(mass, g, theta_degrees):
    """
    Calculate the normal force exerted by the slope on the bike.
    """
    theta_radians = math.radians(theta_degrees)
    return mass * g * math.cos(theta_radians)


def calculate_frictional_force(mu, normal_force):
    """
    Calculate the frictional force for a given coefficient of friction and normal force.
    """
    return mu * normal_force


def calculate_static_friction_coefficient(r, k, mass, g, theta_degrees):
    """
    Calculate the static friction coefficient needed to prevent the wheel from slipping.
    """
    if theta_degrees == 0:
        return 1.0  # Return 1.0 for flat surface

    theta_radians = math.radians(theta_degrees)
    normal_force = calculate_normal_force(mass, g, theta_degrees)
    frictional_force_required = abs((k ** 2) * mass * g * math.sin(theta_radians) / (r ** 2 + k ** 2))
    mu_s = frictional_force_required / normal_force
    return mu_s


def calculate_kinetic_friction_force(mass, g, theta_degrees, mu_k):
    """
    Calculate the kinetic friction force opposing the skis' motion on snow.
    """
    normal_force = calculate_normal_force(mass, g, theta_degrees)
    f_k = mu_k * normal_force
    return f_k


def calculate_required_torque(load_force, radius_of_wheel):
    """
    Calculate the torque required to overcome the load force, facilitating uphill movement.
    """
    return load_force * radius_of_wheel


def calculate_load_force(mass, g, theta_degrees, mu_k, mu_s, r, k, min_rolling_resistance=0.01):
    """
    Calculate the total load force that the motor must overcome to move the bike uphill.
    """
    normal_force = calculate_normal_force(mass, g, theta_degrees)
    kinetic_friction_force = calculate_kinetic_friction_force(mass, g, theta_degrees, mu_k)
    static_friction_force = calculate_frictional_force(mu_s, normal_force)
    gravitational_force_parallel = calculate_gravitational_force_parallel(mass, g, theta_degrees)

    # Adding minimum rolling resistance
    rolling_resistance = min_rolling_resistance * normal_force

    total_load_force = gravitational_force_parallel + kinetic_friction_force - static_friction_force + rolling_resistance

    # Ensure the total load force is non-negative
    total_load_force = max(total_load_force, 0)

    return total_load_force


def calculate_actual_power_required(load_force, speed):
    """
    Calculate the actual power required based on the load force and the speed of the bike.

    :param load_force: Load force in Newtons
    :param speed: Speed of the bike in meters per second
    :return: Required power in Watts
    """
    return load_force * speed


def calculate_max_speed(power, load_force, radius_of_wheel, realistic_max_speed=20):
    """
    Calculate the maximum speed of the bike based on the power, load force, and wheel radius.

    :param power: Power of the motor in Watts
    :param load_force: Load force in Newtons
    :param radius_of_wheel: Radius of the wheel in meters
    :param realistic_max_speed: Realistic maximum speed achievable in meters per second (default: 20 m/s)
    :return: Maximum speed in meters per second
    """
    # Avoid division by zero
    if load_force == 0:
        return realistic_max_speed

    # Calculate the torque from the power and load force
    torque = power / (load_force / radius_of_wheel)
    # Calculate the angular velocity
    angular_velocity = torque / radius_of_wheel
    # Convert angular velocity to linear velocity (speed)
    max_speed = angular_velocity * radius_of_wheel

    # Cap the maximum speed at a realistic value
    max_speed = min(max_speed, realistic_max_speed)

    return max_speed


def calculate_operational_time(energy_capacity_wh, power_consumption_w):
    """
    Calculate the operational time based on the battery's energy capacity and power consumption.

    :param energy_capacity_wh: Total energy capacity of the battery in Watt-hours
    :param power_consumption_w: Power consumption in Watts
    :return: Operational time in hours
    """
    if power_consumption_w == 0:
        return 0  # Return zero operational time when power consumption is zero
    else:
        return energy_capacity_wh / power_consumption_w


def calculate_range_km(operational_time_h, speed_m_per_s):
    """
    Calculate the range in kilometers based on the operational time and speed.

    :param operational_time_h: Operational time in hours
    :param speed_m_per_s: Speed in meters per second
    :return: Range in kilometers
    """
    if operational_time_h == 0:
        return 0  # Return zero range when operational time is zero
    else:
        speed_km_per_h = speed_m_per_s * 3.6  # Convert m/s to km/h
        return speed_km_per_h * operational_time_h


def calculate_pedaling_contribution(pedaling_power, radius_of_wheel, speed):
    """
    Calculate the additional torque from pedaling based on the pedaling power.
    This function assumes the pedaling power contributes directly to the bike's motion
    by increasing the total torque applied to the wheel. The angular velocity is derived
    from the linear speed and wheel radius, allowing for the conversion of pedaling power
    (in Watts) to mechanical torque (in Newton-meters).

    :param pedaling_power: Power generated by the user through pedaling in Watts.
                           This is an estimated average value that a user can sustain.
    :param radius_of_wheel: Radius of the wheel in meters, affecting the conversion
                            from angular to linear motion.
    :param speed: The linear speed of the bike in meters per second, used to calculate
                  the wheel's angular velocity.
    :return: Additional torque from pedaling in Newton-meters, contributing to the
             total torque required to overcome the load force and move the bike.
    """
    # Calculate the angular velocity from the linear speed
    angular_velocity = speed / radius_of_wheel
    # Calculate the torque contribution from pedaling
    torque_from_pedaling = pedaling_power / angular_velocity
    return torque_from_pedaling


def calculate_energy_efficiency(mass, g, theta_degrees, distance_km, energy_consumed_wh):
    """
    Calculate the energy efficiency of the bike system.

    :param mass: Total mass of the bike and rider in kg.
    :param g: Acceleration due to gravity in m/s^2.
    :param theta_degrees: Incline angle in degrees.
    :param distance_km: Distance traveled in kilometers.
    :param energy_consumed_wh: Total electrical energy consumed in Watt-hours.
    :return: Energy efficiency as a percentage.
    """
    theta_radians = math.radians(theta_degrees)
    height_gain_m = distance_km * 1000 * math.sin(theta_radians)  # Convert km to m and calculate height gain
    useful_work_j = mass * g * height_gain_m  # Calculate useful work in Joules
    electrical_energy_consumed_j = energy_consumed_wh * 3600  # Convert Wh to Joules
    efficiency = (useful_work_j / electrical_energy_consumed_j) * 100  # Efficiency as a percentage

    # Ensure non-negative efficiency
    efficiency = max(0, efficiency)

    return efficiency


def calculate_stopping_distance(speed, deceleration):
    """
    Calculate the stopping distance based on the initial speed and deceleration.

    :param speed: Initial speed in meters per second.
    :param deceleration: Deceleration in meters per second squared.
    :return: Stopping distance in meters.
    """
    if deceleration != 0:
        return (speed ** 2) / (2 * deceleration)
    else:
        return float('inf')  # Return infinity for cases where deceleration is zero


def calculate_braking_deceleration(braking_force, mass, slope_angle_degrees, mu_k):
    """
    Calculate the total deceleration due to braking force, considering slopes and friction.

    :param braking_force: Braking force in Newtons.
    :param mass: Mass of the bike and rider in kilograms.
    :param slope_angle_degrees: Angle of the slope in degrees.
    :param mu_k: Kinetic friction coefficient.
    :return: Total deceleration in meters per second squared.
    """
    # Calculate the gravitational force component parallel to the slope
    g_parallel = calculate_gravitational_force_parallel(mass, g, slope_angle_degrees)

    # Calculate the frictional force opposing the motion
    frictional_force = calculate_frictional_force(mu_k, calculate_normal_force(mass, g, slope_angle_degrees))

    # Calculate the net force considering braking, gravity, and friction
    net_force = -braking_force + g_parallel - frictional_force

    # Ensure the net force is non-negative (prevents negative deceleration)
    net_force = max(net_force, 0)
    # Calculate the total deceleration
    deceleration = net_force / mass

    return deceleration


if __name__ == '__main__':
    g = 9.81  # Gravity in m/s^2
    mass_total = 100  # Total mass of the bike and rider in kg
    mass_wheel = 1.4  # Mass of the wheel in kg
    r = 0.6604  # Radius of the wheel in meters
    k = 0.15  # Radius of gyration in meters
    mu_k = 0.05  # Kinetic friction coefficient for skis on snow
    # Assume braking force for illustration (you can adjust this based on actual braking systems)
    braking_force = 500  # Newtons
    # Initialize lists to store data
    incline_angles_list = np.arange(-10, 11, 1)  # Incline angles from -10 to 10 degrees
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

    # Loop through incline angles and modes
    for incline_angle in incline_angles_list:
        for mode in modes:
            if mode == 'Motor Only':
                power_val = 1000
                pedaling_power_val = 0
            elif mode == 'Pedaling Only':
                power_val = 0
                pedaling_power_val = 150
            else:  # Combined mode
                power_val = 1000
                pedaling_power_val = 150

            # Calculate various parameters
            mu_s_total_val = calculate_static_friction_coefficient(r, k, mass_total, g, incline_angle)
            mu_s_wheel_val = calculate_static_friction_coefficient(r, k, mass_wheel, g, incline_angle)
            kinetic_friction_force_val = calculate_kinetic_friction_force(mass_total, g, incline_angle, mu_k)
            load_force_val = calculate_load_force(mass_total, g, incline_angle, mu_k, mu_s_total_val, r, k)
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
            print(f"Static Friction Coefficient for the bike system: {mu_s_total_val}")
            print(f"Static Friction Coefficient for just the wheel: {mu_s_wheel_val}")
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

    # Plotting the data
    plt.figure(figsize=(12, 8))

    # Plot Maximum Speed vs. Incline Angle
    plt.subplot(2, 3, 1)
    plt.plot(incline_angles_list, max_speed_motor_only, label='Motor Only')
    plt.plot(incline_angles_list, max_speed_pedaling_only, label='Pedaling Only')
    plt.plot(incline_angles_list, max_speed_combined, label='Combined')
    plt.xlabel('Incline Angle (degrees)')
    plt.ylabel('Maximum Speed (m/s)')
    plt.title('Maximum Speed vs. Incline Angle')
    plt.legend()

    # Plot Operational Time vs. Incline Angle
    plt.subplot(2, 3, 2)
    plt.plot(incline_angles_list, operational_time_without_pedaling, label='Without Pedaling')
    plt.plot(incline_angles_list, operational_time_with_pedaling, label='With Pedaling')
    plt.xlabel('Incline Angle (degrees)')
    plt.ylabel('Operational Time (hours)')
    plt.title('Operational Time vs. Incline Angle')
    plt.legend()

    # Plot Estimated Range vs. Incline Angle
    plt.subplot(2, 3, 3)
    plt.plot(incline_angles_list, range_without_pedaling, label='Without Pedaling')
    plt.plot(incline_angles_list, range_with_pedaling, label='With Pedaling')
    plt.xlabel('Incline Angle (degrees)')
    plt.ylabel('Estimated Range (km)')
    plt.title('Estimated Range vs. Incline Angle')
    plt.legend()

    # Plot Energy Efficiency vs. Incline Angle
    plt.subplot(2, 3, 4)
    plt.plot(incline_angles_list, energy_efficiency)
    plt.xlabel('Incline Angle (degrees)')
    plt.ylabel('Energy Efficiency (%)')
    plt.title('Energy Efficiency vs. Incline Angle')

    # Plot Total Torque vs. Incline Angle
    plt.subplot(2, 3, 5)
    plt.plot(incline_angles_list, total_torque_without_pedaling, label='Without Pedaling')
    plt.plot(incline_angles_list, total_torque_with_pedaling, label='With Pedaling')
    plt.xlabel('Incline Angle (degrees)')
    plt.ylabel('Total Torque (Nm)')
    plt.title('Total Torque vs. Incline Angle')
    plt.legend()

    # Plot Total Power vs. Incline Angle
    plt.subplot(2, 3, 6)
    plt.plot(incline_angles_list, total_power_without_pedaling, label='Without Pedaling')
    plt.plot(incline_angles_list, total_power_with_pedaling, label='With Pedaling')
    plt.xlabel('Incline Angle (degrees)')
    plt.ylabel('Total Power (W)')
    plt.title('Total Power vs. Incline Angle')
    plt.legend()

    plt.tight_layout()
    plt.show()
