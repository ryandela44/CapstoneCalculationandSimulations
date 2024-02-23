import math


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
    theta_radians = math.radians(theta_degrees)
    normal_force = calculate_normal_force(mass, g, theta_degrees)
    frictional_force_required = (k ** 2) * mass * g * math.sin(theta_radians) / (r ** 2 + k ** 2)
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


def calculate_load_force(mass, g, theta_degrees, mu_k, mu_s, r, k):
    """
    Calculate the total load force that the motor must overcome to move the bike uphill.
    """
    normal_force = calculate_normal_force(mass, g, theta_degrees)
    kinetic_friction_force = calculate_kinetic_friction_force(mass, g, theta_degrees, mu_k)
    static_friction_force = calculate_frictional_force(mu_s, normal_force)
    gravitational_force_parallel = calculate_gravitational_force_parallel(mass, g, theta_degrees)

    total_load_force = gravitational_force_parallel + kinetic_friction_force - static_friction_force
    return total_load_force


def calculate_actual_power_required(load_force, speed):
    """
    Calculate the actual power required based on the load force and the speed of the bike.

    :param load_force: Load force in Newtons
    :param speed: Speed of the bike in meters per second
    :return: Required power in Watts
    """
    return load_force * speed


def calculate_max_speed(power, load_force, radius_of_wheel):
    """
    Calculate the maximum speed of the bike based on the power, load force, and wheel radius.

    :param power: Power of the motor in Watts
    :param load_force: Load force in Newtons
    :param radius_of_wheel: Radius of the wheel in meters
    :return: Maximum speed in meters per second
    """
    # Calculate the torque from the power and load force
    torque = power / (load_force / radius_of_wheel)
    # Calculate the angular velocity
    angular_velocity = torque / radius_of_wheel
    # Convert angular velocity to linear velocity (speed)
    max_speed = angular_velocity * radius_of_wheel
    return max_speed


def calculate_operational_time(energy_capacity_wh, power_consumption_w):
    """
    Calculate the operational time based on the battery's energy capacity and power consumption.

    :param energy_capacity_wh: Total energy capacity of the battery in Watt-hours
    :param power_consumption_w: Power consumption in Watts
    :return: Operational time in hours
    """
    return energy_capacity_wh / power_consumption_w


def calculate_range_km(operational_time_h, speed_m_per_s):
    """
    Calculate the range in kilometers based on the operational time and speed.

    :param operational_time_h: Operational time in hours
    :param speed_m_per_s: Speed in meters per second
    :return: Range in kilometers
    """
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
    return efficiency


if __name__ == '__main__':
    g = 9.81  # Gravity in m/s^2
    mass_total = 100  # Total mass of the bike and rider in kg
    mass_wheel = 1.4  # Mass of the wheel in kg
    theta_degrees = 3  # Incline angle in degrees
    r = 0.6604  # Radius of the wheel in meters
    k = 0.15  # Radius of gyration in meters
    mu_s_total = calculate_static_friction_coefficient(r, k, mass_total, g, theta_degrees)  # For the bike system
    mu_s_wheel = calculate_static_friction_coefficient(r, k, mass_wheel, g, theta_degrees)  # For the wheel only
    mu_k = 0.05  # Kinetic friction coefficient for skis on snow
    kinetic_friction_force = calculate_kinetic_friction_force(mass_total, g, theta_degrees, mu_k)
    load_force = calculate_load_force(mass_total, g, theta_degrees, mu_k, mu_s_total, r, k)
    required_torque = calculate_required_torque(load_force, r)

    # Given motor specifications and previously calculated values
    power = 1000  # Motor power in Watts
    battery_voltage = 48  # Battery voltage in Volts
    battery_capacity_ah = 13  # Battery capacity in Ampere-hours
    energy_capacity_wh = battery_voltage * battery_capacity_ah  # Total energy capacity in Watt-hours

    # Assume an average speed to calculate the actual power requirement (e.g., 5 m/s)
    average_speed = 10  # Adjusted to a realistic value in m/s for calculation

    # Recalculate the actual power requirement based on a realistic average speed
    actual_power_required = calculate_actual_power_required(load_force, average_speed)

    # Recalculate maximum speed achievable with the given motor power and corrected parameters
    max_speed = calculate_max_speed(power, load_force, r)

    # Calculate operational time
    operational_time_h = calculate_operational_time(energy_capacity_wh, actual_power_required)

    # Calculate range in kilometers
    range_km = calculate_range_km(operational_time_h, average_speed)

    # Assume an average pedaling power (e.g., 150W for a non-athlete over a sustained period)
    pedaling_power = 150

    # Calculate the additional torque from pedaling
    torque_from_pedaling = calculate_pedaling_contribution(pedaling_power, r, average_speed)

    # Update the total torque and power to include pedaling
    total_torque_with_pedaling = required_torque + torque_from_pedaling
    total_power_with_pedaling = actual_power_required + pedaling_power

    # Recalculate operational time and range with pedaling power included
    operational_time_with_pedaling = calculate_operational_time(energy_capacity_wh, total_power_with_pedaling)
    range_with_pedaling = calculate_range_km(operational_time_with_pedaling, average_speed)

    # Assuming an example distance traveled
    distance_traveled_km = range_with_pedaling  # Use the calculated range with pedaling for distance

    # Assuming total energy consumed is equivalent to the battery's capacity (for simplification)
    total_energy_consumed_wh = energy_capacity_wh

    # Calculate energy efficiency
    energy_efficiency = calculate_energy_efficiency(mass_total, g, theta_degrees, distance_traveled_km,
                                                    total_energy_consumed_wh)

    # Print the corrected and additional calculations
    print(f"Static Friction Coefficient for the bike system: {mu_s_total}")
    print(f"Static Friction Coefficient for just the wheel: {mu_s_wheel}")
    print(f"Kinetic Friction Force for the skis: {kinetic_friction_force} N")
    print(f"Total Load Force to be overcome: {load_force} N")
    print(f"Required Torque to overcome the load: {required_torque} Nm")
    print(f"Additional Torque from Pedaling: {torque_from_pedaling:.2f} Nm")
    print(f"Total Torque with Pedaling: {total_torque_with_pedaling:.2f} Nm")
    print(f"Total Power with Pedaling: {total_power_with_pedaling} W")
    print(f"Actual Power Required at {average_speed} m/s: {actual_power_required} W")
    print(f"Maximum Speed achievable: {max_speed} m/s")
    print(f"Energy Capacity of the battery: {energy_capacity_wh} Wh")
    print(f"Operational Time without pedaling: {operational_time_h:.2f} hours")
    print(f"Estimated Range without pedaling: {range_km:.2f} km")
    print(f"Operational Time with pedaling: {operational_time_with_pedaling:.2f} hours")
    print(f"Estimated Range with pedaling: {range_with_pedaling:.2f} km")
    print(f"Energy Efficiency: {energy_efficiency:.2f}%")
