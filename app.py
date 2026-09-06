from flask import Flask, jsonify, request

app = Flask(__name__)

APP_VERSION = "1.0.0"


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "application": "student-ml-api",
        "version": APP_VERSION
    }), 200


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not data or "value" not in data:
        return jsonify({
            "error": "Missing required field: value"
        }), 400

    value = data["value"]

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return jsonify({
            "error": "Value must be a number"
        }), 400

    prediction = value * 2

    return jsonify({
        "input": value,
        "prediction": prediction
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)