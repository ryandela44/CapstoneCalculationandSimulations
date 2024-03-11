import math


def calculate_actual_power_required(load_force, speed):
    """
    Calculate the actual power required based on the load force and the speed of the bike.

    :param load_force: Load force in Newtons
    :param speed: Speed of the bike in meters per second
    :return: Required power in Watts
    """
    return load_force * speed


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
