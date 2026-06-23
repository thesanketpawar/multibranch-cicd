from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# Attach Prometheus exporter
metrics = PrometheusMetrics(app)

# Default metrics: request count, latency, etc.
# You can also add custom metrics

@app.route('/')
def home():
    return "Hello, Flask App with Prometheus!"

@app.route('/api/data')
def get_data():
    return jsonify({"message": "This is sample data", "status": "success"})

# Custom metric example
@app.route('/api/custom')
@metrics.do_not_track()  # exclude from default metrics
def custom_endpoint():
    return jsonify({"custom": "This endpoint is not tracked by default metrics"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
