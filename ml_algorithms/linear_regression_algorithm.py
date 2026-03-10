from pathlib import Path

from sklearn.linear_model import LinearRegression


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "trained_models" / "linear_regression"


CONFIG = {
    "algorithm_key": "linear_regression",
    "label": "Lineare Regression",
    "model_type": "LinearRegression",
    "task_type": "regression",
    "scenario_name": "Immobilienpreis aus Quadratmetern",
    "summary": "Ein lineares Regressionsmodell fuer direkte Zusammenhaenge zwischen Flaeche und Preis.",
    "best_for": "Ideal fuer Preisvorhersagen, wenn sich der Zielwert mit steigender Flaeche relativ linear entwickelt.",
    "scenario_examples": [
        "Wohnflaeche 45 qm fuehrt auf einen Preis von 540.",
        "Wohnflaeche 60 qm fuehrt auf einen Preis von 710.",
        "Wohnflaeche 78 qm fuehrt auf einen Preis von 890.",
    ],
    "prediction_examples": [
        {
            "label": "Kompakte Wohnung",
            "description": "Kleiner bis mittlerer Preisbereich fuer 45 qm.",
            "input": {"area": 45},
        },
        {
            "label": "Grenzfall Mitte",
            "description": "Typischer Mittelwert im Bereich 60 qm.",
            "input": {"area": 60},
        },
        {
            "label": "Grosse Flaeche",
            "description": "Hoeherer Preisbereich fuer 78 qm.",
            "input": {"area": 78},
        },
    ],
    "min_samples": 2,
    "training_fields": [
        {
            "name": "area",
            "label": "Flaeche in qm",
            "input_type": "number",
            "value_type": "float",
            "role": "feature",
            "description": "Wohn- oder Nutzflaeche in Quadratmetern.",
            "min_value": 0.1,
            "step": 0.1,
        },
        {
            "name": "target_price",
            "label": "Preis",
            "input_type": "number",
            "value_type": "float",
            "role": "target",
            "description": "Zu lernender Preiswert fuer die eingegebene Flaeche.",
            "min_value": 0.1,
            "step": 0.1,
        },
    ],
    "prediction_fields": [
        {
            "name": "area",
            "label": "Flaeche in qm",
            "input_type": "number",
            "value_type": "float",
            "description": "Flaeche, fuer die ein Preis vorhergesagt werden soll.",
            "min_value": 0.1,
            "step": 0.1,
        }
    ],
    "hyperparameters": [
        {
            "name": "fit_intercept",
            "label": "Intercept berechnen",
            "parameter_type": "bool",
            "description": "Legt fest, ob ein Achsenabschnitt mitgelernt werden soll.",
            "default": True,
        }
    ],
    "default_training_samples": [
        {"area": 45, "target_price": 540},
        {"area": 60, "target_price": 710},
        {"area": 78, "target_price": 890},
    ],
    "default_prediction_input": {"area": 72},
    "model_path": MODEL_DIR / "linear_regression_model.joblib",
    "metadata_path": MODEL_DIR / "linear_regression_metadata.json",
    "factory": lambda params: LinearRegression(fit_intercept=params["fit_intercept"]),
}