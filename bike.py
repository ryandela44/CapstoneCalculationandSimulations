import os

import matplotlib.pyplot as plt
from math import radians, cos, sin, degrees


class BikeSimulator:
    def __init__(self, mass, wheel_radius, mu_s_wheel, mu_k_skis, mu_k_wheel, max_motor_power, pedaling_force,
                 battery_voltage, battery_capacity_ah, drag_coefficient, frontal_area, air_density, rolling_resistance,
                 angle_degrees):
        self.mass = mass
        self.wheel_radius = wheel_radius
        self.mu_s_wheel = mu_s_wheel
        self.mu_k_skis = mu_k_skis
        self.mu_k_wheel = mu_k_wheel
        self.max_motor_power = max_motor_power
        self.pedaling_force = pedaling_force
        self.battery_voltage = battery_voltage
        self.battery_capacity_ah = battery_capacity_ah
        self.drag_coefficient = drag_coefficient
        self.frontal_area = frontal_area
        self.air_density = air_density
        self.rolling_resistance = rolling_resistance
        self.angle = radians(angle_degrees)
        self.g = 9.81
        self.motor_powers = []
        self.operation_times = []
        self.battery_ranges = []

    def determine_bike_state(self, force, max_static_friction, max_battery_force, pedaling_force, mode, state):
        motor_force = 0
        total_force = 0
        if mode == 'pedal':
            total_force = pedaling_force
        elif mode == 'motor':
            motor_force = min(force, max_battery_force)
            total_force = motor_force
        elif mode == 'both':
            motor_force = max(0, force - pedaling_force)
            total_force = pedaling_force + motor_force

        if force <= total_force:
            if total_force <= max_static_friction:
                message = "Wheel will start rolling without slipping" if state == 'rest' else "Bike continues to move without slipping"
            else:
                message = "Wheel will slip"
        else:
            message = "Bike is not able to move" if state == 'rest' else "Bike starts to slow down and eventually comes to a stop"

        print(message)
        return motor_force, total_force

    def simulate(self, mode, speeds):
        operation_time = 0
        battery_range = 0
        for speed in speeds:
            print("************************************************************")
            print("The speed is: ", speed, "m/s")
            print("The angle is: ", degrees(self.angle), "degrees")
            normal_force = self.mass * self.g * cos(self.angle)
            max_static_friction = self.mu_s_wheel * normal_force
            ski_friction = self.mu_k_skis * normal_force
            drag_force = 0.5 * self.drag_coefficient * self.air_density * self.frontal_area * speed ** 2
            rolling_resistance_force = self.rolling_resistance * normal_force
            force = self.mass * self.g * sin(self.angle) + rolling_resistance_force + ski_friction
            torque = force * self.wheel_radius
            if speed != 0:
                max_battery_force = self.max_motor_power / speed
            else:
                max_battery_force = float('inf')

            motor_force_init, total_force_init = self.determine_bike_state(force, max_static_friction,
                                                                           max_battery_force, self.pedaling_force, mode,
                                                                           'rest')
            actual_motor_power = motor_force_init * speed

            self.print_stats(normal_force, max_static_friction, drag_force, rolling_resistance_force, force, torque,
                             motor_force_init, total_force_init, actual_motor_power, speed)

            if force <= total_force_init:
                force = self.mass * self.g * sin(self.angle) + rolling_resistance_force + ski_friction + drag_force
                torque = force * self.wheel_radius
                motor_force, total_force = self.determine_bike_state(force, max_static_friction, max_battery_force,
                                                                     self.pedaling_force, mode, 'motion')
                actual_motor_power = motor_force * speed
                batter_energy = self.battery_voltage * self.battery_capacity_ah
                if actual_motor_power != 0:
                    operation_time = (batter_energy / actual_motor_power)
                else:
                    actual_motor_power = float('inf')
                battery_range = operation_time * speed * 3.6

                self.print_stats(normal_force, max_static_friction, drag_force, rolling_resistance_force, force, torque,
                                 motor_force, total_force, actual_motor_power, speed)
                self.print_battery_stats(operation_time, battery_range)

            self.motor_powers.append(actual_motor_power)
            self.battery_ranges.append(battery_range)
            self.operation_times.append(operation_time)
        self.plot_motor_power(speeds, self.motor_powers)
        self.plot_battery_range(speeds, self.battery_ranges)
        self.plot_operation_time(speeds, self.operation_times)

    def print_stats(self, normal_force, max_static_friction, drag_force, rolling_resistance_force, force, torque,
                    motor_force, total_force, actual_motor_power, speed):
        motor_rpm = (actual_motor_power / (torque if torque != 0 else 1)) * (60 / (2 * 3.14))
        total_power = total_force * speed

        print("The normal force is: ", normal_force, "N")
        print("The static friction force is: ", max_static_friction, "N")
        print("The drag force is: ", drag_force, "N")
        print("The rolling resistance force is: ", rolling_resistance_force, "N")
        print("The force is: ", force, "N")
        print("The torque is: ", torque, "Nm")
        print("The actual motor force is: ", motor_force, "N")
        print("The total force is: ", total_force, "N")
        print("The motor power is: ", actual_motor_power, "W")
        print("The motor rpm  is: ", motor_rpm, "rpm")
        print("The total power is: ", total_power, "W")

    def print_battery_stats(self, operation_time, battery_range):
        print("The operational time is: ", operation_time, "hours")
        print("The battery range is: ", battery_range, "km")

    def plot_motor_power(self, speeds, motor_powers):
        plt.plot(speeds, motor_powers)
        plt.xlabel('Speed (m/s)')
        plt.ylabel('Motor Power (W)')
        plt.title('Motor Power vs Speed')
        # Save the plot to a file
        plot_path = os.path.join('static', 'motor_power_plot.png')
        plt.savefig(plot_path)
        plt.show()

    def plot_battery_range(self, speeds, battery_ranges):
        plt.plot(speeds, battery_ranges)
        plt.xlabel('Speed (m/s)')
        plt.ylabel('Battery Range (km)')
        plt.title('Battery Range vs Speed')

        # Save the plot to a file
        plot_path = os.path.join('static', 'battery_range_plot.png')
        plt.savefig(plot_path)
        plt.show()

    def plot_operation_time(self, speeds, operation_times):
        plt.plot(speeds, operation_times)
        plt.xlabel('Speed (m/s)')
        plt.ylabel('Operation Time (hours)')
        plt.title('Operation Time vs Speed')

        # Save the plot to a file
        plot_path = os.path.join('static', 'operation_time_plot.png')
        plt.savefig(plot_path)
        plt.show()
