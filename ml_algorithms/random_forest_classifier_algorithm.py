from pathlib import Path

from sklearn.ensemble import RandomForestClassifier


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "trained_models" / "random_forest_classifier"


CONFIG = {
    "algorithm_key": "random_forest_classifier",
    "label": "Random Forest Classifier",
    "model_type": "RandomForestClassifier",
    "task_type": "classification",
    "scenario_name": "Betrugs- und Risikoscreening fuer Transaktionen",
    "summary": "Ensemble-Klassifikation fuer robustere Entscheidungen bei komplexeren Mustern.",
    "best_for": "Sehr gut fuer Risikoerkennung, Fraud-Screening und Klassifikation mit mehreren Einflussgroessen.",
    "scenario_examples": [
        "Kleiner Betrag, altes Konto und keine Chargebacks fuehren zu niedrigem Risiko.",
        "Mittlerer Betrag und einzelne Auffaelligkeiten fuehren zu mittlerem Risiko.",
        "Hoher Betrag, junges Konto und mehrere Chargebacks fuehren zu hohem Risiko.",
    ],
    "prediction_examples": [
        {
            "label": "Niedriges Risiko",
            "description": "Kleiner Betrag, altes Konto, keine Rueckbuchungen.",
            "input": {"transaction_amount": 35, "account_age_days": 840, "chargeback_count": 0},
        },
        {
            "label": "Grenzfall Mittel",
            "description": "Mittlerer Betrag mit einem moderaten Warnsignal.",
            "input": {"transaction_amount": 540, "account_age_days": 60, "chargeback_count": 1},
        },
        {
            "label": "Hohes Risiko",
            "description": "Hoher Betrag, junges Konto und mehrere Chargebacks.",
            "input": {"transaction_amount": 1600, "account_age_days": 14, "chargeback_count": 3},
        },
    ],
    "min_samples": 4,
    "training_fields": [
        {
            "name": "transaction_amount",
            "label": "Transaktionsbetrag",
            "input_type": "number",
            "value_type": "float",
            "role": "feature",
            "description": "Hoehe einer Transaktion oder Bestellung.",
            "min_value": 0,
            "step": 1,
        },
        {
            "name": "account_age_days",
            "label": "Kontenalter in Tagen",
            "input_type": "number",
            "value_type": "int",
            "role": "feature",
            "description": "Wie lange das Konto bereits existiert.",
            "min_value": 0,
            "step": 1,
        },
        {
            "name": "chargeback_count",
            "label": "Chargeback-Anzahl",
            "input_type": "number",
            "value_type": "int",
            "role": "feature",
            "description": "Anzahl bisheriger Rueckbuchungen.",
            "min_value": 0,
            "step": 1,
        },
        {
            "name": "risk_level",
            "label": "Risikostufe",
            "input_type": "select",
            "value_type": "str",
            "role": "target",
            "description": "Zu lernende Risikoklasse.",
            "options": ["niedrig", "mittel", "hoch"],
        },
    ],
    "prediction_fields": [
        {
            "name": "transaction_amount",
            "label": "Transaktionsbetrag",
            "input_type": "number",
            "value_type": "float",
            "description": "Hoehe einer Transaktion oder Bestellung.",
            "min_value": 0,
            "step": 1,
        },
        {
            "name": "account_age_days",
            "label": "Kontenalter in Tagen",
            "input_type": "number",
            "value_type": "int",
            "description": "Wie lange das Konto bereits existiert.",
            "min_value": 0,
            "step": 1,
        },
        {
            "name": "chargeback_count",
            "label": "Chargeback-Anzahl",
            "input_type": "number",
            "value_type": "int",
            "description": "Anzahl bisheriger Rueckbuchungen.",
            "min_value": 0,
            "step": 1,
        },
    ],
    "hyperparameters": [
        {
            "name": "n_estimators",
            "label": "Anzahl Baeume",
            "parameter_type": "int",
            "description": "Wie viele Entscheidungsbaeume trainiert werden.",
            "default": 100,
            "minimum": 10,
            "step": 10,
        },
        {
            "name": "max_depth",
            "label": "Maximale Tiefe",
            "parameter_type": "int",
            "description": "Begrenzt die Tiefe der Baeume. Leer bedeutet keine feste Grenze.",
            "default": None,
            "minimum": 1,
            "step": 1,
            "nullable": True,
        },
    ],
    "default_training_samples": [
        {"transaction_amount": 35, "account_age_days": 840, "chargeback_count": 0, "risk_level": "niedrig"},
        {"transaction_amount": 120, "account_age_days": 540, "chargeback_count": 0, "risk_level": "niedrig"},
        {"transaction_amount": 420, "account_age_days": 120, "chargeback_count": 1, "risk_level": "mittel"},
        {"transaction_amount": 620, "account_age_days": 75, "chargeback_count": 1, "risk_level": "mittel"},
        {"transaction_amount": 760, "account_age_days": 55, "chargeback_count": 1, "risk_level": "mittel"},
        {"transaction_amount": 1600, "account_age_days": 14, "chargeback_count": 3, "risk_level": "hoch"},
        {"transaction_amount": 980, "account_age_days": 45, "chargeback_count": 2, "risk_level": "hoch"},
    ],
    "default_prediction_input": {"transaction_amount": 540, "account_age_days": 60, "chargeback_count": 1},
    "model_path": MODEL_DIR / "random_forest_classifier_model.joblib",
    "metadata_path": MODEL_DIR / "random_forest_classifier_metadata.json",
    "factory": lambda params: RandomForestClassifier(
        n_estimators=params["n_estimators"],
        max_depth=params["max_depth"],
        random_state=42,
    ),
}