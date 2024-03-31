import math
import os

import matplotlib.pyplot as plt
from math import cos, sin


class BikeSimulator:

    def __init__(self, mass, wheel_radius, mu_s_wheel, mu_k_skis, mu_k_wheel, max_motor_power, pedaling_power,
                 battery_voltage, battery_capacity_ah, drag_coefficient, frontal_area, air_density, rolling_resistance,
                 gradient, speed):
        self.mass = mass + 20
        self.wheel_radius = wheel_radius
        self.mu_s_wheel = mu_s_wheel
        self.mu_k_skis = mu_k_skis
        self.mu_k_wheel = mu_k_wheel
        self.max_motor_power = max_motor_power
        self.pedaling_power = pedaling_power
        self.battery_voltage = battery_voltage
        self.battery_capacity_ah = battery_capacity_ah
        self.drag_coefficient = drag_coefficient
        self.frontal_area = frontal_area
        self.air_density = air_density
        self.rolling_resistance = rolling_resistance
        self.angle = math.atan(gradient / 100.0)
        self.g = 9.81
        self.speed = speed
        self.motor_powers = []
        self.operation_times = []
        self.battery_ranges = []
        self.motor_efficiencies = []
        self.messages = []
        self.gradient = gradient
        self.gear_ratio = 4.59

    def determine_bike_state(self, speed, force, max_static_friction, max_battery_force, pedaling_force, mode, state):
        motor_force = 0
        total_force = 0
        message = ""
        if force <= 0:
            motor_force = -1 * min(abs(force), max_battery_force)
            total_force = motor_force
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
            force += kinetic_friction_wheel
            message = "Wheel will slip"

        else:
            if force <= total_force:
                if total_force <= max_static_friction:
                    message = "Wheel will start rolling without slipping" if state == 'rest' else "Bike continues rolling without slipping"

            else:
                message = "Bike is not able to move" if state == 'rest' else "Bike starts to slow down and eventually comes to a stop"

        if self.speed == speed:
            self.messages.append(message)
        return motor_force, total_force

    def simulate(self, mode, speeds):
        pedaling_power = 0
        motor_efficiency = 0.8
        electrical_power = 0
        recovered_energy_watt_hours = 0

        for speed in speeds:
            rpm = 0
            total_power = 0
            drag_force = 0
            battery_range = 0
            print("************************************************************")
            print("Gradient: " + str(self.gradient) + "%")
            if self.speed == speed:
                self.messages.append("Gradient: " + str(self.gradient) + "%")
            normal_force = self.mass * self.g * cos(self.angle)
            max_static_friction = self.mu_s_wheel * normal_force
            ski_friction = self.mu_k_skis * normal_force
            rolling_resistance_force = self.rolling_resistance * normal_force
            gravity_force = self.mass * self.g * sin(self.angle)
            force = gravity_force + rolling_resistance_force + ski_friction
            torque = force * self.wheel_radius
            motor_torque = torque / self.gear_ratio

            max_angular_speed = 2 * 3.1416 * 470 / 60
            max_torque = self.max_motor_power / max_angular_speed

            max_battery_force = (max_torque * self.gear_ratio) / self.wheel_radius

            if speed > 0:
                pedaling_force = (pedaling_power / speed) * self.gear_ratio
            else:
                pedaling_force = 0

            motor_force, total_force = self.determine_bike_state(speed, force, max_static_friction,max_battery_force,
                                                                 pedaling_force, mode,
                                                                 'rest')

            if self.speed == speed:
                self.log_initial_stats(max_static_friction, force, motor_torque, motor_force)
            self.print_initial_stats(max_static_friction, force, motor_torque, motor_force)

            if force < 0:
                print("Bike does not need any additional force to move")

            if force <= total_force:
                drag_force = 0.5 * self.drag_coefficient * self.air_density * self.frontal_area * speed ** 2
                force = self.mass * self.g * sin(self.angle) + rolling_resistance_force + ski_friction + drag_force
                motor_force, total_force = self.determine_bike_state(speed, force, max_static_friction, max_battery_force,
                                                                     pedaling_force, mode, 'motion')

                angular_speed_motor = speed / self.wheel_radius
                rpm = angular_speed_motor * 60 / (2 * 3.1416)
                motor_torque = (motor_force * self.wheel_radius) / self.gear_ratio
                mechanical_power = motor_torque * angular_speed_motor
                electrical_power = mechanical_power / motor_efficiency

                total_power = pedaling_power + mechanical_power

            if force < 0:
                regenerative_braking_efficiency = 0.8
                recoverable_energy = 0.5 * self.mass * self.speed**2 * regenerative_braking_efficiency
                recovered_energy_watt_hours = recoverable_energy * (1 / 3600)  # Convert to Wh if needed

            battery_energy = self.battery_voltage * self.battery_capacity_ah
            if electrical_power > 0:
                operation_time = (battery_energy / electrical_power)
            else:
                operation_time = float('inf')
            if speed != 0:
                if electrical_power <= 1000:
                    battery_range = operation_time * speed * 3.6

            else:
                battery_range = float('inf')
            if self.speed == speed:
                self.log_stats(force, motor_torque, motor_force, total_force, electrical_power, rpm, pedaling_power,
                               total_power,speed)
                self.log_battery_stats(operation_time, battery_range, recovered_energy_watt_hours)
                self.print_stats(normal_force, max_static_friction, drag_force, rolling_resistance_force, force,
                                 motor_torque, motor_force, total_force, electrical_power, rpm, total_power, pedaling_power,speed)
                self.print_battery_stats(operation_time, battery_range, recovered_energy_watt_hours)

            self.motor_powers.append(electrical_power)
            self.battery_ranges.append(battery_range)
            self.operation_times.append(operation_time)
        self.plot_motor_power(speeds, self.motor_powers)
        self.plot_battery_range(speeds, self.battery_ranges)
        self.plot_operation_time(speeds, self.operation_times)
        return self.messages

    def print_stats(self, normal_force, max_static_friction, drag_force, rolling_resistance_force, force, torque,
                    motor_force, total_force, electrical_power, motor_rpm, total_power, pedaling_power,speed):
        print("constant speed to maintain : " + str(speed) + "m/s")
        print("The normal force is: " + str(normal_force) + "N")
        print("The static friction force is: " + str(max_static_friction) + "N")
        print("The drag force is: " + str(drag_force) + "N")
        print("The rolling resistance force is: " + str(rolling_resistance_force) + "N")
        print("The force is: " + str(force) + "N")
        print("The torque is: " + str(torque) + "Nm")
        print("The actual motor force is : " + str(motor_force) + "N")
        print("The pedalling + motor force is :" + str(total_force) + "N")
        print("The pedaling power is: " + str(pedaling_power) + "W")
        print("The electrical motor power is: " + str(electrical_power) + "W")
        print("The motor rpm  is: " + str(motor_rpm) + "rpm")
        print("Pedaling + motor power : " + str(total_power) + "W")

    def log_stats(self, force, torque, motor_force, total_force, electric_power, motor_rpm, pedaling_power,
                  total_power, speed):
        self.messages.append("constant speed to maintain : " + str(speed) + "m/s")
        self.messages.append("The force required to continue motion is: " + str(force) + "N")
        # self.messages.append("The torque is: " + str(torque) + "Nm")
        self.messages.append("The actual motor force is: " + str(motor_force) + "N")
        self.messages.append("The pedalling + motor force is: " + str(total_force) + "N")
        self.messages.append("The pedaling power is: " + str(pedaling_power) + "W")
        self.messages.append("The electrical motor power is: " + str(electric_power) + "W")
        self.messages.append("The motor rpm  is: " + str(motor_rpm) + "rpm")
        # self.messages.append("Pedaling + motor power : " + str(total_power) + "W")

    def print_initial_stats(self, max_static_friction, force, torque, motor_force):
        print("Maximum static friction: " + str(max_static_friction) + "N")
        print("Force required to set bike in motion: " + str(force) + "N")
        print("Torque required to set bike in motion: " + str(torque) + "Nm")
        print("The motor force is: " + str(motor_force) + "N")

    def log_initial_stats(self, max_static_friction, force, torque, motor_force_):
        self.messages.append("Maximum static friction: " + str(max_static_friction) + "N")
        self.messages.append("Force required to set bike in motion: " + str(force) + "N")
        #self.messages.append("Torque required to set bike in motion: " + str(torque) + "Nm")
        self.messages.append("The motor force is: " + str(motor_force_) + "N")

    def print_battery_stats(self, operation_time, battery_range, recovered_energy_watt_hours):
        print("The operational time is: " + str(operation_time) + "hours")
        print("The battery range is: " + str(battery_range) + "km")
        print("The recovered energy is: " + str(recovered_energy_watt_hours) + "Wh")

    def log_battery_stats(self, operation_time, battery_range, recovered_energy_watt_hours):
        self.messages.append("The operational time is: " + str(operation_time) + "hours")
        self.messages.append("The battery range is: " + str(battery_range) + "km")
        self.messages.append("The recovered energy is: " + str(recovered_energy_watt_hours) + "Wh")

    def plot_motor_power(self, speeds, motor_powers):
        plt.figure(figsize=(10, 6))
        plt.plot(speeds, motor_powers, '-o', label='Motor Power')
        max_power = max(motor_powers)
        max_speed = speeds[motor_powers.index(max_power)]
        plt.plot(max_speed, max_power, 'r*', markersize=10, label=f'Max Power: {max_power}W at {max_speed}m/s')
        plt.xlabel('Speed (m/s)', fontsize=14)
        plt.ylabel('Motor Power (W)', fontsize=14)
        plt.title('Motor Power vs Speed', fontsize=16)
        plt.legend()
        plt.grid(True)
        plot_path = os.path.join('static', 'motor_power_plot.png')
        plt.savefig(plot_path)
        plt.show()
        plt.close()

    def plot_battery_range(self, speeds, battery_ranges):
        plt.figure(figsize=(10, 6))
        plt.plot(speeds, battery_ranges, '-o', label='Battery Range')
        max_range = max(battery_ranges)
        optimal_speed = speeds[battery_ranges.index(max_range)]
        plt.plot(optimal_speed, max_range, 'g^', markersize=10, label=f'Max Range: {max_range}km at {optimal_speed}m/s')
        plt.xlabel('Speed (m/s)', fontsize=14)
        plt.ylabel('Battery Range (km)', fontsize=14)
        plt.title('Battery Range vs Speed', fontsize=16)
        plt.legend()
        plt.grid(True)
        plot_path = os.path.join('static', 'battery_range_plot.png')
        plt.savefig(plot_path)
        plt.show()
        plt.close()

    def plot_operation_time(self, speeds, operation_times):
        plt.figure(figsize=(10, 6))
        plt.plot(speeds, operation_times, '-o', label='Operation Time')
        max_time = max(operation_times)
        optimal_speed = speeds[operation_times.index(max_time)]
        plt.plot(optimal_speed, max_time, 'bs', markersize=10, label=f'Max Time: {max_time}h at {optimal_speed}m/s')
        plt.xlabel('Speed (m/s)', fontsize=14)
        plt.ylabel('Operation Time (h)', fontsize=14)
        plt.title('Operation Time vs Speed', fontsize=16)
        plt.legend()
        plt.grid(True)
        plot_path = os.path.join('static', 'operation_time_plot.png')
        plt.savefig(plot_path)
        plt.show()
        plt.close()
