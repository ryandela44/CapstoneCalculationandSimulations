from math import radians, cos, sin, degrees

from matplotlib import pyplot as plt


def determine_bike_state(force, max_static_friction, max_battery_force, pedaling_force, mode, state):
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
            if state == 'rest':
                print("Wheel will start rolling without slipping")
            else:
                print("Bike  continues to move without slipping")
        else:
            print("Wheel will slip")
    else:
        if state == 'rest':
            print("Bike is not able to move")
        else:
            print("Bike starts to slow down and eventually comes to a stop")
    return motor_force, total_force


def print_motor_stats(normal_force, max_static_friction, drag_force, rolling_resistance_force,
                      force, torque, motor_force, total_force, actual_motor_power, motor_rpm,
                      total_power):
    print("The normal force is: ", normal_force, "N")
    print("The static friction force is: ", max_static_friction, "N")
    print("The drag force is: ", drag_force, "N")
    print("The rolling resistance force is: ", rolling_resistance_force, "N")
    print("The force from rest  is: ", force, "N")
    print("The torque from rest is: ", torque, "Nm")
    print("The actual motor force is: ", motor_force, "N")
    print("The total force from rest is: ", total_force, "N")
    print("The motor power from rest is: ", actual_motor_power, "W")
    print("The motor rpm from rest is: ", motor_rpm, "rpm")
    print("The total power from rest is: ", total_power, "W")


def print_battery_stats(operation_time, battery_range):
    print("The operational time is: ", operation_time, "hours")
    print("The battery range is: ", battery_range, "km")


def plot_motor_power(speeds, motor_powers):
    plt.plot(speeds, motor_powers)
    plt.xlabel('Speed (m/s)')
    plt.ylabel('Motor Power (W)')
    plt.title('Motor Power vs Speed')
    plt.show()


def plot_battery_range(speeds, battery_ranges):
    plt.plot(speeds, battery_ranges)
    plt.xlabel('Speed (m/s)')
    plt.ylabel('Battery Range (km)')
    plt.title('Battery Range vs Speed')
    plt.show()


def plot_operation_time(speeds, operation_times):
    plt.plot(speeds, operation_times)
    plt.xlabel('Speed (m/s)')
    plt.ylabel('Operation Time (hours)')
    plt.title('Operation Time vs Speed')
    plt.show()


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
    speeds = range(0, 11)
    rolling_resistance = 0.01
    operation_time = 0
    battery_range = 0
    max_battery_force = 0
    angular_speed_motor_init = 0
    motor_rpm = 0
    angular_speed_motor = 0

    modes = ['pedal', 'motor', 'both']
    states = ['rest', 'motion']
    time = range(0, 11)

    angle = radians(10)

    operation_times = []
    battery_ranges = []
    motor_powers = []

    normal_force = mass * g * cos(angle)
    max_static_friction = mu_s_wheel * normal_force
    ski_friction = mu_k_skis * normal_force
    # motor_angular_max_velocity = 470 * 2 * 3.14 / 60
    # max_motor_torque = max_motor_power / motor_angular_max_velocity
    # max_battery_force = max_motor_torque / wheel_radius
    # print("The motor max torque is: ", max_motor_torque)

    mode = input("Press Enter the mode of operation... ")

    for speed in speeds:
        print("**************************************************************")
        print("The speed is: ", speed, "m/s")
        print("The angle is: ", degrees(angle), "degrees")
        # Starting from rest
        drag_force = 0.5 * drag_coefficient * air_density * frontal_area * speed ** 2
        rolling_resistance_force = rolling_resistance * normal_force
        # drag is 0 when the bike is not moving
        force_init = mass * g * sin(angle) + rolling_resistance_force + ski_friction
        torque_init = force_init * wheel_radius
        if speed != 0:
            max_battery_force = max_motor_power / speed
        acceleration_init = force_init / mass

        motor_force_init, total_force_init = determine_bike_state(force_init, max_static_friction,
                                                                  max_battery_force, pedaling_force, mode, states[0])
        motor_torque_init = motor_force_init * wheel_radius
        actual_motor_power_init = motor_force_init * speed
        if motor_torque_init != 0:
            angular_speed_motor_init = actual_motor_power_init / motor_torque_init
        motor_rpm_init = angular_speed_motor_init * 60 / (2 * 3.14)
        total_power_init = total_force_init * speed

        print_motor_stats(normal_force, max_static_friction, drag_force, rolling_resistance_force,
                          force_init, torque_init, motor_force_init, total_force_init,
                          actual_motor_power_init, motor_rpm_init, total_power_init)

        if force_init <= total_force_init:
            # bike in motion
            force = mass * g * sin(angle) + rolling_resistance_force + ski_friction + drag_force
            torque = force * wheel_radius
            motor_force, total_force = determine_bike_state(force, max_static_friction, max_battery_force,
                                                            pedaling_force, mode, states[1])

            actual_motor_power = motor_force * speed
            total_power = total_force * speed
            if motor_torque_init != 0:
                angular_speed_motor = actual_motor_power_init / motor_torque_init
            motor_rpm = angular_speed_motor * 60 / (2 * 3.14)
            batter_energy = battery_voltage * battery_capacity_ah
            # operational time in hours
            if actual_motor_power == 0:
                actual_motor_power = 0.01
            operation_time = (batter_energy / actual_motor_power)
            # battery range in km
            battery_range = operation_time * speed * 3.6
            print_motor_stats(normal_force, max_static_friction, drag_force, rolling_resistance_force,
                              force, torque, motor_force, total_force, actual_motor_power, motor_rpm,
                              total_power)
            print_battery_stats(operation_time, battery_range)

        motor_powers.append(actual_motor_power)
        operation_times.append(operation_time)
        battery_ranges.append(battery_range)
        print("**************************************************************")

    plot_motor_power(speeds, motor_powers)
    plot_battery_range(speeds, battery_ranges)
    plot_operation_time(speeds, operation_times)
