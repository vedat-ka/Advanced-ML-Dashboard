from pathlib import Path

from sklearn.tree import DecisionTreeClassifier


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "trained_models" / "decision_tree_classifier"


CONFIG = {
    "algorithm_key": "decision_tree_classifier",
    "label": "Decision Tree Classifier",
    "model_type": "DecisionTreeClassifier",
    "task_type": "classification",
    "scenario_name": "Kreditantrag genehmigen oder ablehnen",
    "summary": "Ein Entscheidungsbaum fuer klar erklaerbare Ja-Nein- und Klassenentscheidungen.",
    "best_for": "Gut fuer Freigabe-, Risiko- oder Genehmigungsentscheidungen mit leicht nachvollziehbaren Regeln.",
    "scenario_examples": [
        "Hohes Einkommen, geringe Schuldenquote und lange Kredithistorie fuehren zu genehmigt.",
        "Mittleres Einkommen und mittlere Schuldenquote fuehren zu pruefen.",
        "Niedriges Einkommen, hohe Schuldenquote und kurze Historie fuehren zu abgelehnt.",
    ],
    "prediction_examples": [
        {
            "label": "Genehmigt",
            "description": "Hohes Einkommen, geringe Last, lange Historie.",
            "input": {"monthly_income": 3800, "debt_ratio": 0.18, "credit_history_years": 6},
        },
        {
            "label": "Grenzfall Pruefen",
            "description": "Mittlere Bonitaet mit offenem Entscheidungsraum.",
            "input": {"monthly_income": 2500, "debt_ratio": 0.35, "credit_history_years": 3},
        },
        {
            "label": "Abgelehnt",
            "description": "Niedriges Einkommen und hohe Schuldenquote.",
            "input": {"monthly_income": 1600, "debt_ratio": 0.67, "credit_history_years": 1},
        },
    ],
    "min_samples": 3,
    "training_fields": [
        {
            "name": "monthly_income",
            "label": "Monatliches Einkommen",
            "input_type": "number",
            "value_type": "float",
            "role": "feature",
            "description": "Nettoeinkommen pro Monat.",
            "min_value": 0,
            "step": 100,
        },
        {
            "name": "debt_ratio",
            "label": "Schuldenquote",
            "input_type": "number",
            "value_type": "float",
            "role": "feature",
            "description": "Anteil bestehender Verpflichtungen, z. B. zwischen 0 und 1.",
            "min_value": 0,
            "step": 0.01,
        },
        {
            "name": "credit_history_years",
            "label": "Kredithistorie in Jahren",
            "input_type": "number",
            "value_type": "float",
            "role": "feature",
            "description": "Laenge der vorhandenen Kredithistorie.",
            "min_value": 0,
            "step": 0.5,
        },
        {
            "name": "approval_class",
            "label": "Zielklasse",
            "input_type": "select",
            "value_type": "str",
            "role": "target",
            "description": "Zu lernende Entscheidungsklasse.",
            "options": ["genehmigt", "pruefen", "abgelehnt"],
        },
    ],
    "prediction_fields": [
        {
            "name": "monthly_income",
            "label": "Monatliches Einkommen",
            "input_type": "number",
            "value_type": "float",
            "description": "Nettoeinkommen pro Monat.",
            "min_value": 0,
            "step": 100,
        },
        {
            "name": "debt_ratio",
            "label": "Schuldenquote",
            "input_type": "number",
            "value_type": "float",
            "description": "Anteil bestehender Verpflichtungen, z. B. zwischen 0 und 1.",
            "min_value": 0,
            "step": 0.01,
        },
        {
            "name": "credit_history_years",
            "label": "Kredithistorie in Jahren",
            "input_type": "number",
            "value_type": "float",
            "description": "Laenge der vorhandenen Kredithistorie.",
            "min_value": 0,
            "step": 0.5,
        },
    ],
    "hyperparameters": [
        {
            "name": "max_depth",
            "label": "Maximale Tiefe",
            "parameter_type": "int",
            "description": "Begrenzt die Tiefe des Baums. Leer bedeutet keine feste Grenze.",
            "default": None,
            "minimum": 1,
            "step": 1,
            "nullable": True,
        },
        {
            "name": "min_samples_split",
            "label": "Min. Samples pro Split",
            "parameter_type": "int",
            "description": "Minimale Anzahl an Trainingsbeispielen fuer eine Verzweigung.",
            "default": 2,
            "minimum": 2,
            "step": 1,
        },
    ],
    "default_training_samples": [
        {"monthly_income": 3800, "debt_ratio": 0.18, "credit_history_years": 6, "approval_class": "genehmigt"},
        {"monthly_income": 2100, "debt_ratio": 0.44, "credit_history_years": 2, "approval_class": "pruefen"},
        {"monthly_income": 1600, "debt_ratio": 0.67, "credit_history_years": 1, "approval_class": "abgelehnt"},
    ],
    "default_prediction_input": {"monthly_income": 2500, "debt_ratio": 0.35, "credit_history_years": 3},
    "model_path": MODEL_DIR / "decision_tree_classifier_model.joblib",
    "metadata_path": MODEL_DIR / "decision_tree_classifier_metadata.json",
    "factory": lambda params: DecisionTreeClassifier(
        max_depth=params["max_depth"],
        min_samples_split=params["min_samples_split"],
        random_state=42,
    ),
}