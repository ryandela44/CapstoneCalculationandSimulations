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
    gradient = float(request.form['gradient'])
    mode = request.form['mode']
    speed = int(request.form['speed'])

    # Determine friction coefficients based on terrain
    mu_s_wheel, mu_k_skis, mu_k_wheel, rolling_resistance = determine_terrain_friction(terrain)

    # Create BikeSimulator instance
    simulator = BikeSimulator(
        mass=mass,
        wheel_radius=0.6604,
        mu_s_wheel=mu_s_wheel,
        mu_k_skis=mu_k_skis,
        mu_k_wheel=mu_k_wheel,
        max_motor_power=1000,
        pedaling_force=pedaling_force,
        battery_voltage=48,
        battery_capacity_ah=13,
        drag_coefficient=0.5,
        frontal_area=0.5,
        air_density=1.225,
        rolling_resistance=rolling_resistance,
        gradient=gradient,
        speed=speed
    )

    # Run the simulation (adjust the 'speeds' range as needed)
    messages = simulator.simulate(mode, range(0, 11))

    # Generate URLs for the plots
    motor_power_plot = url_for('static', filename='motor_power_plot.png')
    battery_range_plot = url_for('static', filename='battery_range_plot.png')
    operation_time_plot = url_for('static', filename='operation_time_plot.png')

    # Return HTML with stats messages and image tags
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Simulation Results</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        .card {
            background-color: #f7f7f7;
            padding: 1rem;
            margin-bottom: 0.5rem;
            border-radius: 0.5rem;
            border-left: 5px solid;
        }
        .rolling { background-color: #48bb78; } /* Green */
        .slipping { background-color: #f6ad55; } /* Orange */
        .stopping { background-color: #f56565; } /* Red */
        .normal { border-color: #ffffff; } /* White */
    </style>
</head>
<body class="bg-gray-100 min-h-screen flex flex-col justify-center items-center">
    <div class="bg-white p-6 rounded-lg shadow-lg max-w-4xl w-full space-y-4">
        <h1 class="text-xl md:text-2xl font-bold text-gray-800 text-center">Simulation Results</h1>
        <div class="space-y-2">
            {% for message in stats_messages %}
                {% if "rolling" in message %}
                <div class="card rolling">
                {% elif "slip" in message %}
                <div class="card slipping">
                {% elif "stopping" in message %}
                <div class="card slipping">
                {% elif "not able" in message %}
                <div class="card stopping">
                {% else %}
                <div class="card normal">
                {% endif %}
                    <p class="text-sm md:text-base text-gray-700">{{ message }}</p>
                </div>
            {% endfor %}
        </div>
        <div class="flex flex-wrap justify-center gap-4">
            <img src="{{ motor_power_plot }}" alt="Motor Power Plot" class="max-w-xs rounded-lg shadow-md">
            <img src="{{ battery_range_plot }}" alt="Battery Range Plot" class="max-w-xs rounded-lg shadow-md">
            <img src="{{ operation_time_plot }}" alt="Operation Time Plot" class="max-w-xs rounded-lg shadow-md">
        </div>
        <div class="text-center mt-4">
            <a href="/" class="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50">
                Run Another Simulation
            </a>
        </div>
    </div>
</body>
</html>

        """, stats_messages=messages, motor_power_plot=motor_power_plot, battery_range_plot=battery_range_plot,
                                  operation_time_plot=operation_time_plot)


def determine_terrain_friction(terrain):
    # Adjust these values based on the terrain
    if terrain == 'snow':
        mu_s_wheel = 0.2
        mu_k_skis = 0.05
        mu_k_wheel = 0.3
        rolling_resistance = 0.05
    elif terrain == 'ice':
        mu_s_wheel = 0.1
        mu_k_skis = 0.03
        mu_k_wheel = 0.2
        rolling_resistance = 0.09
    else:  # default values or you can add more terrains
        mu_s_wheel = 0.2
        mu_k_skis = 0.03
        mu_k_wheel = 0.25
    return mu_s_wheel, mu_k_skis, mu_k_wheel, rolling_resistance


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
