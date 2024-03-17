from math import radians, cos, sin, degrees


def determine_bike_state(force, max_static_friction, max_battery_force, pedaling_force, mode):
    motor_force = 0
    total_force = 0
    if mode == '0':
        total_force = pedaling_force
    elif mode == '1':
        if force <= max_battery_force:
            motor_force = force
            total_force = motor_force
        else:
            motor_force = max_battery_force
            total_force = motor_force
    elif mode == '2':
        motor_force = force - pedaling_force
        if motor_force < 0:
            motor_force = 0
        total_force = pedaling_force + motor_force

    if force <= total_force:
        if total_force <= max_static_friction:
            print("wheel will start rolling without slipping")
        else:
            print("wheel will slip")
    else:
        print("bike is not able to move")
    return motor_force, total_force


if __name__ == '__main__':
    # The project is an electric ski bike that has a wheel in the back and skis in the front
    # The bike has a motor that can be used to assist the rider
    # The bike has 3 modes: pedal, motor, and both

    mass = 100
    mass_wheel = 10
    wheel_radius = 0.6604
    mu_s_wheel = 0.2
    mu_k_skis = 0.03
    mu_k_wheel = 0.25
    max_motor_power = 1000

    force = 0
    torque = 0
    motor_force = 0
    motor_power = 0
    actual_motor_power = 0
    total_power = 0
    total_force = 0

    pedaling_force = 100
    battery_voltage = 48
    battery_capacity_ah = 13
    g = 9.81
    drag_coefficient = 0.5
    frontal_area = 0.5
    # air density unit is kg/m^3
    air_density = 1.225
    # speed unit is m/s
    speed = 10
    rolling_resistance = 0.01
    operation_time = 0
    battery_range = 0
    inertia = 0.5 * mass_wheel * wheel_radius ** 2
    # angular_velocity = velocity / wheel_radius
    #
    # torque = inertia * angular_velocity
    #
    # print("The inertia is: ", inertia)
    # print("The angular velocity is: ", angular_velocity)
    # print("The torque is: ", torque)

    modes = ['pedal', 'motor', 'both']
    time = range(0, 10)

    angle = radians(3)

    # Starting from rest
    normal_force = mass * g * cos(angle)
    max_static_friction = mu_s_wheel * normal_force
    ski_friction = mu_k_skis * normal_force
    drag_force = 0.5 * drag_coefficient * air_density * frontal_area * speed ** 2
    rolling_resistance_force = rolling_resistance * mass * g * cos(angle)
    # drag is 0 when the bike is not moving
    force_init = mass * g * sin(angle) + rolling_resistance_force + ski_friction
    torque_init = force_init * wheel_radius
    max_battery_force = max_motor_power / speed

    mode = input("Press Enter the mode of operation...")
    motor_force_init, total_force_init = determine_bike_state(force_init, max_static_friction,
                                                              max_battery_force, pedaling_force, mode)

    actual_motor_power_init = motor_force_init * speed
    total_power_init = total_force_init * speed

    if force_init <= total_force_init:
        # bike in motion
        force = mass * g * sin(angle) + rolling_resistance_force + ski_friction + drag_force
        torque = force * wheel_radius
        motor_force, total_force = determine_bike_state(force, max_static_friction, max_battery_force,
                                                        pedaling_force, mode)

        actual_motor_power = motor_force * speed
        total_power = total_force * speed

        batter_energy = battery_voltage * battery_capacity_ah
        # operational time in hours
        if actual_motor_power == 0:
            actual_motor_power = 0.01
        operation_time = (batter_energy / actual_motor_power)
        battery_range = operation_time * speed

    print("************************************")
    print("The angle is: ", degrees(angle))
    print("The normal force is: ", normal_force)
    print("The static friction force is: ", max_static_friction)
    print("The drag force is: ", drag_force)
    print("The rolling resistance force is: ", rolling_resistance_force)
    print("The force from rest  is: ", force_init)
    print("The torque from rest is: ", torque)
    print("The actual motor force is: ", motor_force_init)
    print("The total force from rest is: ", total_force_init)
    print("The motor power from rest is: ", actual_motor_power_init)
    print("The total power from rest is: ", total_power_init)
    if force_init <= total_force_init:
        print("Bike is in motion")
        print("The force in motion  is: ", force)
        print("The torque in motion is: ", torque)
        print("The actual motor force in motion is: ", motor_force)
        print("The total force in motion is: ", total_force)
        print("The motor power in motion is: ", actual_motor_power)
        print("The total power in motion is: ", total_power)
        print("The operational time is: ", operation_time)
        print("The battery range is: ", battery_range)
    print("************************************")
