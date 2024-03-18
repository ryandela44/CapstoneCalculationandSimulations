from flask import Flask, request, render_template_string, url_for
from bike import BikeSimulator

app = Flask(__name__)


@app.route('/')
def index():
    return render_template_string(open('index.html').read())


@app.route('/simulate', methods=['POST'])
def simulate():
    # Extract form data
    mass = float(request.form['mass'])
    terrain = request.form['terrain']
    pedaling_force = float(request.form['pedaling_force'])
    angle = float(request.form['angle'])
    mode = request.form['mode']

    # Determine friction coefficients based on terrain
    mu_s_wheel, mu_k_skis, mu_k_wheel = determine_terrain_friction(terrain)

    # Create BikeSimulator instance
    simulator = BikeSimulator(
        mass=mass,
        wheel_radius=0.6604,  # Example value, adjust as needed
        mu_s_wheel=mu_s_wheel,
        mu_k_skis=mu_k_skis,
        mu_k_wheel=mu_k_wheel,
        max_motor_power=1000,  # Example value, adjust as needed
        pedaling_force=pedaling_force,
        battery_voltage=48,  # Example value, adjust as needed
        battery_capacity_ah=13,  # Example value, adjust as needed
        drag_coefficient=0.5,  # Example value, adjust as needed
        frontal_area=0.5,  # Example value, adjust as needed
        air_density=1.225,  # Example value, adjust as needed
        rolling_resistance=0.01,  # Example value, adjust as needed
        angle_degrees=angle
    )

    # Run the simulation (adjust the 'speeds' range as needed)
    simulator.simulate(mode, range(0, 11))

    # Assuming you've saved your plots as described in step 1
    motor_power_plot = url_for('static', filename='motor_power_plot.png')
    battery_range_plot = url_for('static', filename='battery_range_plot.png')
    operation_time_plot = url_for('static', filename='operation_time_plot.png')

    # Generate URLs for the plots
    motor_power_plot = url_for('static', filename='motor_power_plot.png')
    battery_range_plot = url_for('static', filename='battery_range_plot.png')
    operation_time_plot = url_for('static', filename='operation_time_plot.png')

    # Pass the URLs to the template string
    html = render_template_string("""
                <h1>Simulation Results</h1>
                <img src="{{ motor_power_plot }}" alt="Motor Power Plot">
                <img src="{{ battery_range_plot }}" alt="Battery Range Plot">
                <img src="{{ operation_time_plot }}" alt="Operation Time Plot">
                <a href="/">Run Another Simulation</a>
            """, motor_power_plot=motor_power_plot, battery_range_plot=battery_range_plot,
                                  operation_time_plot=operation_time_plot)

    return html


def determine_terrain_friction(terrain):
    # Adjust these values based on the terrain
    if terrain == 'snow':
        mu_s_wheel = 0.2
        mu_k_skis = 0.05
        mu_k_wheel = 0.3
    elif terrain == 'ice':
        mu_s_wheel = 0.1
        mu_k_skis = 0.03
        mu_k_wheel = 0.2
    else:  # default values or you can add more terrains
        mu_s_wheel = 0.2
        mu_k_skis = 0.03
        mu_k_wheel = 0.25
    return mu_s_wheel, mu_k_skis, mu_k_wheel


if __name__ == '__main__':
    app.run(debug=True)
