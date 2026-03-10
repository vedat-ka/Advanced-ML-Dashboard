from pathlib import Path

from sklearn.linear_model import Ridge


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "trained_models" / "ridge_regression"


CONFIG = {
    "algorithm_key": "ridge_regression",
    "label": "Ridge Regression",
    "model_type": "Ridge",
    "task_type": "regression",
    "scenario_name": "Gehaltsprognose fuer Mitarbeitende",
    "summary": "Regularisierte Regression fuer stabilere Vorhersagen bei verrauschten oder schwankenden Daten.",
    "best_for": "Sinnvoll fuer Gehalts- oder Umsatzprognosen mit mehreren Einflussfaktoren, wenn Ueberanpassung reduziert werden soll.",
    "scenario_examples": [
        "2 Jahre Erfahrung, 1 Zertifikat und Performance 6.5 fuehren zu 42.000 Zielgehalt.",
        "5 Jahre Erfahrung, 2 Zertifikate und Performance 8.1 fuehren zu 56.000 Zielgehalt.",
        "8 Jahre Erfahrung, 4 Zertifikate und Performance 9.0 fuehren zu 76.000 Zielgehalt.",
    ],
    "prediction_examples": [
        {
            "label": "Junior-Profil",
            "description": "Wenig Erfahrung und wenige Zertifikate.",
            "input": {"years_experience": 2, "certification_count": 1, "performance_score": 6.5},
        },
        {
            "label": "Grenzfall Mitte",
            "description": "Mittleres Erfahrungsprofil mit guter Leistung.",
            "input": {"years_experience": 5, "certification_count": 2, "performance_score": 8.1},
        },
        {
            "label": "Senior-Profil",
            "description": "Hohe Erfahrung, mehrere Zertifikate und starke Performance.",
            "input": {"years_experience": 8, "certification_count": 4, "performance_score": 9.0},
        },
    ],
    "min_samples": 3,
    "training_fields": [
        {
            "name": "years_experience",
            "label": "Berufserfahrung in Jahren",
            "input_type": "number",
            "value_type": "float",
            "role": "feature",
            "description": "Relevante Berufserfahrung in Jahren.",
            "min_value": 0,
            "step": 0.5,
        },
        {
            "name": "certification_count",
            "label": "Anzahl Zertifikate",
            "input_type": "number",
            "value_type": "int",
            "role": "feature",
            "description": "Wie viele fachliche Zertifikate die Person besitzt.",
            "min_value": 0,
            "step": 1,
        },
        {
            "name": "performance_score",
            "label": "Performance-Score",
            "input_type": "number",
            "value_type": "float",
            "role": "feature",
            "description": "Interner Leistungswert, z. B. zwischen 1 und 10.",
            "min_value": 0,
            "step": 0.1,
        },
        {
            "name": "target_salary",
            "label": "Zielgehalt",
            "input_type": "number",
            "value_type": "float",
            "role": "target",
            "description": "Zielwert fuer das Training, etwa Jahresgehalt oder Bonus.",
            "min_value": 0,
            "step": 100,
        },
    ],
    "prediction_fields": [
        {
            "name": "years_experience",
            "label": "Berufserfahrung in Jahren",
            "input_type": "number",
            "value_type": "float",
            "description": "Relevante Berufserfahrung in Jahren.",
            "min_value": 0,
            "step": 0.5,
        },
        {
            "name": "certification_count",
            "label": "Anzahl Zertifikate",
            "input_type": "number",
            "value_type": "int",
            "description": "Wie viele fachliche Zertifikate die Person besitzt.",
            "min_value": 0,
            "step": 1,
        },
        {
            "name": "performance_score",
            "label": "Performance-Score",
            "input_type": "number",
            "value_type": "float",
            "description": "Interner Leistungswert, z. B. zwischen 1 und 10.",
            "min_value": 0,
            "step": 0.1,
        },
    ],
    "hyperparameters": [
        {
            "name": "alpha",
            "label": "Alpha",
            "parameter_type": "float",
            "description": "Staerke der Regularisierung.",
            "default": 1.0,
            "minimum": 0.0001,
            "step": 0.1,
        },
        {
            "name": "fit_intercept",
            "label": "Intercept berechnen",
            "parameter_type": "bool",
            "description": "Legt fest, ob ein Achsenabschnitt mitgelernt werden soll.",
            "default": True,
        },
    ],
    "default_training_samples": [
        {"years_experience": 2, "certification_count": 1, "performance_score": 6.5, "target_salary": 42000},
        {"years_experience": 5, "certification_count": 2, "performance_score": 8.1, "target_salary": 56000},
        {"years_experience": 8, "certification_count": 4, "performance_score": 9.0, "target_salary": 76000},
    ],
    "default_prediction_input": {"years_experience": 6, "certification_count": 3, "performance_score": 8.4},
    "model_path": MODEL_DIR / "ridge_regression_model.joblib",
    "metadata_path": MODEL_DIR / "ridge_regression_metadata.json",
    "factory": lambda params: Ridge(alpha=params["alpha"], fit_intercept=params["fit_intercept"]),
}