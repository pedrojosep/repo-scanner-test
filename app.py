from flask import Flask, request, jsonify
import utils

app = Flask(__name__)


@app.route("/submit_data", methods=["POST"])
def submit_data():
    user_data = request.json

    if any(k not in user_data for k in ("name", "email", "phone")):
        return jsonify({"message": "Missing data fields"}), 400

    if utils.process(user_data):
        return jsonify({"message": "Data proccesed successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
