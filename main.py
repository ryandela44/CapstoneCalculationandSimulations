import math


def calculate_gravitational_force_parallel(mass, g, theta_degrees):
    """
    Calculate the component of gravitational force parallel to the slope.
    """
    theta_radians = math.radians(theta_degrees)
    return mass * g * math.sin(theta_radians)


def calculate_normal_force(mass, g, theta_degrees):
    """
    Calculate the normal force exerted on the bike by the slope.
    """
    theta_radians = math.radians(theta_degrees)
    return mass * g * math.cos(theta_radians)


def calculate_frictional_force(mu, normal_force):
    """
    Calculate the frictional force based on the coefficient of friction and normal force.
    """
    return mu * normal_force


def calculate_static_friction_coefficient(r, k, mass, g, theta_degrees):
    """
    Calculate the static friction coefficient for the wheel on the ground.
    """
    theta_radians = math.radians(theta_degrees)
    normal_force = calculate_normal_force(mass, g, theta_degrees)
    frictional_force_required = (k ** 2) * mass * g * math.sin(theta_radians) / (r ** 2 + k ** 2)
    mu_s = frictional_force_required / normal_force
    return mu_s


def calculate_kinetic_friction_force(mass, g, theta_degrees, mu_k):
    """
    Calculate the kinetic friction force for the skis on snow.
    """
    normal_force = calculate_normal_force(mass, g, theta_degrees)
    f_k = mu_k * normal_force
    return f_k


def calculate_required_torque(load_force, radius_of_wheel):
    """
    Calculate the torque required to overcome the total load force on an incline.

    :param load_force: Total load force that needs to be overcome (in Newtons)
    :param radius_of_wheel: Radius of the wheel (in meters)
    :return: Required torque (in Newton-meters)
    """
    return load_force * radius_of_wheel


def calculate_load_force(mass, g, theta_degrees, mu_k, mu_s, r, k):
    """
    Calculate the total load force that needs to be overcome by the motor on an incline.
    """
    normal_force = calculate_normal_force(mass, g, theta_degrees)
    kinetic_friction_force = calculate_kinetic_friction_force(mass, g, theta_degrees, mu_k)
    static_friction_force = calculate_frictional_force(mu_s, normal_force)
    gravitational_force_parallel = calculate_gravitational_force_parallel(mass, g, theta_degrees)

    total_load_force = gravitational_force_parallel + kinetic_friction_force - static_friction_force
    return total_load_force


if __name__ == '__main__':
    g = 9.81  # Gravity in m/s^2
    mass_total = 100  # Total mass of the bike and rider in kg, example value
    theta_degrees = 3  # Incline angle in degrees
    r = 0.6604  # Radius of the wheel in meters
    k = 0.15  # Radius of gyration in meters
    mu_s_calculated = calculate_static_friction_coefficient(r, k, mass_total, g,
                                                            theta_degrees)  # Static friction coefficient
    mu_k = 0.05  # Kinetic friction coefficient for skis on snow (example value)
    kinetic_friction_force = calculate_kinetic_friction_force(mass_total, g, theta_degrees,
                                                              mu_k)  # Kinetic friction force

    # Calculate the total load force that needs to be overcome by the motor
    load_force = calculate_load_force(mass_total, g, theta_degrees, mu_k, mu_s_calculated, r, k)

    # Calculate the required torque
    required_torque = calculate_required_torque(load_force, r)

    print(f"Static Friction Coefficient for the wheel (mu_s): {mu_s_calculated}")
    print(f"Kinetic Friction Force for the skis (f_k): {kinetic_friction_force}")
    print(f"Total Load Force to be overcome by the motor (load_force): {load_force} N")
    print(f"Required Torque to overcome the total load force: {required_torque} Nm")
