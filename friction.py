from forces import *


def calculate_static_friction_coefficient(r, k, mass, g, theta_degrees, tire_material_coefficient,terrain_coefficient):
    """
    Calculate the static friction coefficient needed to prevent the wheel from slipping.
    """
    if theta_degrees == 0:
        return 1.0  # Return 1.0 for flat surface

    theta_radians = math.radians(theta_degrees)
    normal_force = calculate_normal_force(mass, g, theta_degrees)
    frictional_force_required = abs((k ** 2) * mass * g * math.sin(theta_radians) / (r ** 2 + k ** 2))
    mu_s = (frictional_force_required / normal_force)
    return mu_s

