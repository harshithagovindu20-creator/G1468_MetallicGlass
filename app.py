

from flask import Flask, render_template, request
import joblib
import pandas as pd
from pymatgen.core import Composition
from matminer.featurizers.composition import ElementProperty

app = Flask(__name__)

# Load trained models and their exact feature names
tg_data = joblib.load("saved_models/Tg_K_model.pkl")
tx_data = joblib.load("saved_models/Tx_K_model.pkl")
tl_data = joblib.load("saved_models/Tl_K_model.pkl")

tg_model = tg_data["model"]
tx_model = tx_data["model"]
tl_model = tl_data["model"]
feature_cols = tg_data["features"]

# Generate the same Magpie features used during training
magpie = ElementProperty.from_preset("magpie")
magpie_labels = magpie.feature_labels()


@app.route("/", methods=["GET", "POST"])
def home():
    predictions = None
    error = None

    if request.method == "POST":
        try:
            zr = float(request.form["zr"])
            cu = float(request.form["cu"])
            ni = float(request.form["ni"])
            al = float(request.form["al"])

            values = [zr, cu, ni, al]

            if any(v <= 0 or v > 100 for v in values):
                raise ValueError(
                    "Each element percentage must be greater than 0 and at most 100."
                )

            if abs(sum(values) - 100) > 0.1:
                raise ValueError("The four percentages must add up to 100%.")

            formula = f"Zr{zr}Cu{cu}Ni{ni}Al{al}"
            composition = Composition(formula)

            feature_values = magpie.featurize(composition)
            all_features = pd.DataFrame(
                [feature_values], columns=magpie_labels
            )

            X = all_features.reindex(columns=feature_cols)

            if X.isnull().any().any():
                raise ValueError(
                    "Some required model features could not be generated."
                )

            predictions = {
                "Tg": round(float(tg_model.predict(X)[0]), 2),
                "Tx": round(float(tx_model.predict(X)[0]), 2),
                "Tl": round(float(tl_model.predict(X)[0]), 2),
            }

        except Exception as e:
            error = f"Could not make prediction: {e}"

    return render_template(
        "index.html",
        predictions=predictions,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
