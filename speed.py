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
