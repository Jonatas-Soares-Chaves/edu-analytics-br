from flask import Flask, jsonify
from src.database import consultar_dados

app = Flask(__name__)

@app.route("/dados", methods=["GET"])
def dados():
    df = consultar_dados()
    return df.to_json(orient="records")

@app.route("/kpis", methods=["GET"])
def kpis():
    df = consultar_dados()

    return jsonify({
        "media": df["indicador"].mean(),
        "max": df["indicador"].max(),
        "min": df["indicador"].min()
    })

if __name__ == "__main__":
    app.run(debug=True)