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


def calculate_kinetic_friction_force(mass, g, theta_degrees, mu_k):
    """
    Calculate the kinetic friction force opposing the skis' motion on snow.
    """
    normal_force = calculate_normal_force(mass, g, theta_degrees)
    f_k = mu_k * normal_force
    return f_k


def calculate_load_force(mass, g, theta_degrees, mu_k, mu_s, min_rolling_resistance=0.01):
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
