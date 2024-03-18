import flask
from flask import request

app = flask.Flask(__name__)


@app.route('/simulate', methods=['POST'])
def simulate():
    # Extract form data
    mass = float(request.form['mass'])
    terrain = request.form['terrain']
    pedaling_force = float(request.form['pedaling_force'])
    angle = float(request.form['angle'])
    mode = request.form['mode']

    # Assuming you have a function called `run_simulation` that takes these parameters and returns some results
    # For example, let's just return a string (you would replace this with your actual simulation and plotting logic)
    simulation_result = f"Simulation results for {mass}kg on {terrain}, pedaling force {pedaling_force}N, slope {angle} degrees, mode {mode}"

    # Return results (for now, just displaying the result string; you would want to show plots or detailed results here)
    return simulation_result

    @app.route('/')
    def index():
        return flask.render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
