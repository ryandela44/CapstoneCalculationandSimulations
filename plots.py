# Start by setting a larger figure size to accommodate all subplots clearly
from matplotlib import pyplot as plt


def setup_plot():
    # Start by setting a larger figure size to accommodate all subplots clearly
    plt.figure(figsize=(18, 12))


def plot_speed_vs_angle(incline_angles_list, max_speed_motor_only, max_speed_pedaling_only, max_speed_combined):
    # Maximum Speed vs. Incline Angle
    plt.subplot(2, 3, 1)
    plt.plot(incline_angles_list, max_speed_motor_only, 'b-o', label='Motor Only')
    plt.plot(incline_angles_list, max_speed_pedaling_only, 'r--x', label='Pedaling Only')
    plt.plot(incline_angles_list, max_speed_combined, 'g-.^', label='Combined')
    plt.xlabel('Incline Angle (Degrees)', fontsize=12)
    plt.ylabel('Maximum Speed (m/s)', fontsize=12)
    plt.title('Maximum Speed vs. Incline Angle', fontsize=14)
    plt.legend(fontsize=10, loc='upper right')
    plt.grid(alpha=0.3)


def plot_operational_time_vs_angle(incline_angles_list, operational_time_without_pedaling,
                                   operational_time_with_pedaling):
    # Operational Time vs. Incline Angle
    plt.subplot(2, 3, 2)
    plt.plot(incline_angles_list, operational_time_without_pedaling, 'c-o', label='Without Pedaling')
    plt.plot(incline_angles_list, operational_time_with_pedaling, 'm--x', label='With Pedaling')
    plt.xlabel('Incline Angle (Degrees)', fontsize=12)
    plt.ylabel('Operational Time (Hours)', fontsize=12)
    plt.title('Operational Time vs. Incline Angle', fontsize=14)
    plt.legend(fontsize=10, loc='upper right')
    plt.grid(alpha=0.3)


def plot_estimated_range_vs_angle(incline_angles_list, range_without_pedaling, range_with_pedaling):
    # Estimated Range vs. Incline Angle
    plt.subplot(2, 3, 3)
    plt.plot(incline_angles_list, range_without_pedaling, 'y-o', label='Without Pedaling')
    plt.plot(incline_angles_list, range_with_pedaling, 'k--x', label='With Pedaling')
    plt.xlabel('Incline Angle (Degrees)', fontsize=12)
    plt.ylabel('Estimated Range (km)', fontsize=12)
    plt.title('Estimated Range vs. Incline Angle', fontsize=14)
    plt.legend(fontsize=10, loc='upper right')
    plt.grid(alpha=0.3)


def plot_efficieny_vs_incline_angle(incline_angles_list, energy_efficiency):
    # Energy Efficiency vs. Incline Angle
    plt.subplot(2, 3, 4)
    plt.plot(incline_angles_list, energy_efficiency, 'b-o', label='Energy Efficiency')
    plt.xlabel('Incline Angle (Degrees)', fontsize=12)
    plt.ylabel('Energy Efficiency (%)', fontsize=12)
    plt.title('Energy Efficiency vs. Incline Angle', fontsize=14)
    plt.legend(fontsize=10, loc='upper right')
    plt.grid(alpha=0.3)


def plot_torque_vs_incline_angle(incline_angles_list, total_torque_without_pedaling, total_torque_with_pedaling):
    # Total Torque vs. Incline Angle
    plt.subplot(2, 3, 5)
    plt.plot(incline_angles_list, total_torque_without_pedaling, 'g-o', label='Without Pedaling')
    plt.plot(incline_angles_list, total_torque_with_pedaling, 'r--x', label='With Pedaling')
    plt.xlabel('Incline Angle (Degrees)', fontsize=12)
    plt.ylabel('Total Torque (Nm)', fontsize=12)
    plt.title('Total Torque vs. Incline Angle', fontsize=14)
    plt.legend(fontsize=10, loc='upper right')
    plt.grid(alpha=0.3)


def plot_power_vs_incline_angle(incline_angles_list, total_power_without_pedaling, total_power_with_pedaling):
    # Total Power vs. Incline Angle
    plt.subplot(2, 3, 6)
    plt.plot(incline_angles_list, total_power_without_pedaling, 'm-o', label='Without Pedaling')
    plt.plot(incline_angles_list, total_power_with_pedaling, 'c--x', label='With Pedaling')
    plt.xlabel('Incline Angle (Degrees)', fontsize=12)
    plt.ylabel('Total Power (W)', fontsize=12)
    plt.title('Total Power vs. Incline Angle', fontsize=14)
    plt.legend(fontsize=10, loc='upper right')
    plt.grid(alpha=0.3)

    plt.tight_layout()  # Adjust the layout to ensure no subplot is squeezed
    plt.show()


def plot_speed_vs_time(time, max_speed_motor_only_1, max_speed_pedaling_only_1, max_speed_combined_1):
    # Plot speed vs. time for different scenarios
    plt.figure(figsize=(8, 6))
    plt.plot([0, time], [0, max_speed_motor_only_1[0]], 'b-o', label='Motor Only')
    plt.plot([0, time], [0, max_speed_pedaling_only_1[0]], 'r--x', label='Pedaling Only')
    plt.plot([0, time], [0, max_speed_combined_1[0]], 'g-.^', label='Combined')
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Speed (m/s)', fontsize=12)
    plt.title('Speed vs. Time', fontsize=14)
    plt.legend(fontsize=10, loc='upper left')
    plt.grid(alpha=0.3)
    plt.show()
