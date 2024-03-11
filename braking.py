from forces import *


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


def calculate_braking_deceleration(braking_force, mass, slope_angle_degrees, mu_k, g):
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
