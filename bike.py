import os

import matplotlib.pyplot as plt
from math import radians, cos, sin, degrees


class BikeSimulator:
    messages = []

    def __init__(self, mass, wheel_radius, mu_s_wheel, mu_k_skis, mu_k_wheel, max_motor_power, pedaling_force,
                 battery_voltage, battery_capacity_ah, drag_coefficient, frontal_area, air_density, rolling_resistance,
                 angle_degrees, speed):
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
        self.speed = speed
        self.motor_powers = []
        self.operation_times = []
        self.battery_ranges = []

    def determine_bike_state(self, speed, force, max_static_friction, max_battery_force, pedaling_force, mode, state):
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

        # If total applied force exceeds static friction, slipping occurs
        if total_force > max_static_friction:
            # Transition to kinetic friction for wheel
            kinetic_friction_wheel = self.mu_k_wheel * self.mass * self.g
            # Assuming kinetic friction opposes motion, it should be subtracted from the total force
            total_force -= kinetic_friction_wheel

        if force <= total_force:
            if total_force <= max_static_friction:
                message = "Wheel will start rolling without slipping" if state == 'rest' else "Bike continues to move without slipping"
            else:
                message = "Wheel will slip"
        else:
            message = "Bike is not able to move" if state == 'rest' else "Bike starts to slow down and eventually comes to a stop"

        if self.speed == speed:
            self.messages.append(message)
        return motor_force, total_force

    def simulate(self, mode, speeds):
        operation_time = 0
        battery_range = 0
        for speed in speeds:
            print("************************************************************")
            print("Analysis at speed : " + str(speed) + "m/s")
            print("The angle is: " + str(degrees(self.angle)) + "degrees")
            if self.speed == speed:
                self.messages.append("************************************************************")
                self.messages.append("Analysis at speed : " + str(speed) + "m/s")
                self.messages.append("The angle is: " + str(degrees(self.angle)) + "degrees")
            normal_force = self.mass * self.g * cos(self.angle)
            max_static_friction = self.mu_s_wheel * normal_force
            ski_friction = self.mu_k_skis * normal_force
            rolling_resistance_force = self.rolling_resistance * normal_force
            force = self.mass * self.g * sin(self.angle) + rolling_resistance_force + ski_friction
            torque = force * self.wheel_radius
            if speed != 0:
                max_battery_force = self.max_motor_power / speed
            else:
                max_battery_force = float('inf')

            motor_force_init, total_force_init = self.determine_bike_state(speed, force, max_static_friction,
                                                                           max_battery_force,
                                                                           self.pedaling_force, mode,
                                                                           'rest')
            actual_motor_power = motor_force_init * speed

            if self.speed == speed:
                self.log_initial_stats(max_static_friction, force, torque)
            self.print_initial_stats(max_static_friction, force, torque)

            if force <= total_force_init:
                drag_force = 0.5 * self.drag_coefficient * self.air_density * self.frontal_area * speed ** 2
                force = self.mass * self.g * sin(self.angle) + rolling_resistance_force + ski_friction + drag_force
                torque = force * self.wheel_radius
                motor_force, total_force = self.determine_bike_state(speed, force, max_static_friction,
                                                                     max_battery_force,
                                                                     self.pedaling_force, mode, 'motion')
                actual_motor_power = motor_force * speed
                batter_energy = self.battery_voltage * self.battery_capacity_ah
                if actual_motor_power != 0:
                    operation_time = (batter_energy / actual_motor_power)
                else:
                    actual_motor_power = float('inf')
                battery_range = operation_time * speed * 3.6
                # motor_efficiency = actual_motor_power / self.max_motor_power
                if self.speed == speed:
                    self.log_stats(force, torque, motor_force, total_force, actual_motor_power, speed)
                    self.log_battery_stats(operation_time, battery_range)
                self.print_stats(normal_force, max_static_friction, drag_force, rolling_resistance_force, force,
                                 torque, motor_force, total_force, actual_motor_power, speed)
                self.print_battery_stats(operation_time, battery_range)

            self.motor_powers.append(actual_motor_power)
            self.battery_ranges.append(battery_range)
            self.operation_times.append(operation_time)
        self.plot_motor_power(speeds, self.motor_powers)
        self.plot_battery_range(speeds, self.battery_ranges)
        self.plot_operation_time(speeds, self.operation_times)
        return self.messages

    def print_stats(self, normal_force, max_static_friction, drag_force, rolling_resistance_force, force, torque,
                    motor_force, total_force, actual_motor_power, speed):
        motor_rpm = (actual_motor_power / (torque if torque != 0 else 1)) * (60 / (2 * 3.14))
        total_power = total_force * speed

        print("The normal force is: " + str(normal_force) + "N")
        print("The static friction force is: " + str(max_static_friction) + "N")
        print("The drag force is: " + str(drag_force) + "N")
        print("The rolling resistance force is: " + str(rolling_resistance_force) + "N")
        print("The force is: " + str(force) + "N")
        print("The torque is: " + str(torque) + "Nm")
        print("The actual motor force is : " + str(motor_force) + "N")
        print("The pedalling + motor force is :" + str(total_force) + "N")
        print("The motor power is: " + str(actual_motor_power) + "W")
        print("The motor rpm  is: " + str(motor_rpm) + "rpm")
        print("Pedaling + motor power : " + str(total_power) + "W")

    def log_stats(self, force, torque, motor_force, total_force, actual_motor_power, speed):
        motor_rpm = (actual_motor_power / (torque if torque != 0 else 1)) * (60 / (2 * 3.14))
        total_power = total_force * speed

        self.messages.append("The force is: " + str(force) + "N")
        self.messages.append("The torque is: " + str(torque) + "Nm")
        self.messages.append("The actual motor force is: " + str(motor_force) + "N")
        self.messages.append("The pedalling + motor force is: " + str(total_force) + "N")
        self.messages.append("The motor power is: " + str(actual_motor_power) + "W")
        self.messages.append("Pedaling + motor power : " + str(total_power) + "W")
        self.messages.append("The motor rpm  is: " + str(motor_rpm) + "rpm")

    def print_initial_stats(self, max_static_friction, force, torque):
        print("Maximum static friction: " + str(max_static_friction) + "N")
        print("Force required to set bike in motion: " + str(force) + "N")
        print("Torque required to set bike in motion: " + str(torque) + "Nm")

    def log_initial_stats(self, max_static_friction, force, torque):
        self.messages.append("Maximum static friction: " + str(max_static_friction) + "N")
        self.messages.append("Force required to set bike in motion: " + str(force) + "N")
        self.messages.append("Torque required to set bike in motion: " + str(torque) + "Nm")

    def print_battery_stats(self, operation_time, battery_range):
        print("The operational time is: " + str(operation_time) + "hours")
        print("The battery range is: " + str(battery_range) + "km")

    def log_battery_stats(self, operation_time, battery_range):
        self.messages.append("The operational time is: " + str(operation_time) + "hours")
        self.messages.append("The battery range is: " + str(battery_range) + "km")

    def plot_motor_power(self, speeds, motor_powers):
        plt.plot(speeds, motor_powers)
        plt.xlabel('Speed (m/s)')
        plt.ylabel('Motor Power (W)')
        plt.title('Motor Power vs Speed')
        # Save the plot to a file
        plot_path = os.path.join('static', 'motor_power_plot.png')
        plt.savefig(plot_path)
        plt.show()
        plt.close()

    def plot_battery_range(self, speeds, battery_ranges):
        plt.plot(speeds, battery_ranges)
        plt.xlabel('Speed (m/s)')
        plt.ylabel('Battery Range (km)')
        plt.title('Battery Range vs Speed')

        # Save the plot to a file
        plot_path = os.path.join('static', 'battery_range_plot.png')
        plt.savefig(plot_path)
        plt.show()
        plt.close()

    def plot_operation_time(self, speeds, operation_times):
        plt.plot(speeds, operation_times)
        plt.xlabel('Speed (m/s)')
        plt.ylabel('Operation Time (hours)')
        plt.title('Operation Time vs Speed')

        # Save the plot to a file
        plot_path = os.path.join('static', 'operation_time_plot.png')
        plt.savefig(plot_path)
        plt.show()
        plt.close()
