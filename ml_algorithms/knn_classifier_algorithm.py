from pathlib import Path

from sklearn.neighbors import KNeighborsClassifier


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "trained_models" / "knn_classifier"


CONFIG = {
    "algorithm_key": "knn_classifier",
    "label": "KNN Classifier",
    "model_type": "KNeighborsClassifier",
    "task_type": "classification",
    "scenario_name": "Lernstatus von Teilnehmenden einschaetzen",
    "summary": "Nachbarschaftsbasierte Klassifikation fuer Faelle, in denen aehnliche Beispiele aehnliche Ergebnisse liefern.",
    "best_for": "Gut fuer Lernstands-, Segmentierungs- oder Empfehlungsfaelle mit lokal aehnlichen Mustern.",
    "scenario_examples": [
        "Wenig Lernstunden, geringe Anwesenheit und kaum Uebungstests fuehren zu kritisch.",
        "Mittlere Lernzeit und solide Anwesenheit fuehren zu stabil.",
        "Viele Lernstunden, hohe Anwesenheit und viele Tests fuehren zu sehr_gut.",
    ],
    "prediction_examples": [
        {
            "label": "Kritisch",
            "description": "Wenig Lernzeit und kaum Uebung.",
            "input": {"study_hours": 3, "attendance_rate": 0.58, "practice_tests": 1},
        },
        {
            "label": "Grenzfall Stabil",
            "description": "Solide Anwesenheit mit mittlerer Lernleistung.",
            "input": {"study_hours": 10, "attendance_rate": 0.82, "practice_tests": 7},
        },
        {
            "label": "Sehr gut",
            "description": "Viel Lernzeit, hohe Anwesenheit und viele Tests.",
            "input": {"study_hours": 18, "attendance_rate": 0.95, "practice_tests": 18},
        },
    ],
    "min_samples": 3,
    "training_fields": [
        {
            "name": "study_hours",
            "label": "Lernstunden pro Woche",
            "input_type": "number",
            "value_type": "float",
            "role": "feature",
            "description": "Zeitaufwand pro Woche fuer das Lernen.",
            "min_value": 0,
            "step": 0.5,
        },
        {
            "name": "attendance_rate",
            "label": "Anwesenheitsquote",
            "input_type": "number",
            "value_type": "float",
            "role": "feature",
            "description": "Anteil besuchter Termine, z. B. zwischen 0 und 1.",
            "min_value": 0,
            "step": 0.01,
        },
        {
            "name": "practice_tests",
            "label": "Anzahl Uebungstests",
            "input_type": "number",
            "value_type": "int",
            "role": "feature",
            "description": "Wie viele Uebungstests absolviert wurden.",
            "min_value": 0,
            "step": 1,
        },
        {
            "name": "learning_status",
            "label": "Lernstatus",
            "input_type": "select",
            "value_type": "str",
            "role": "target",
            "description": "Zu lernende Ergebnisklasse.",
            "options": ["kritisch", "stabil", "sehr_gut"],
        },
    ],
    "prediction_fields": [
        {
            "name": "study_hours",
            "label": "Lernstunden pro Woche",
            "input_type": "number",
            "value_type": "float",
            "description": "Zeitaufwand pro Woche fuer das Lernen.",
            "min_value": 0,
            "step": 0.5,
        },
        {
            "name": "attendance_rate",
            "label": "Anwesenheitsquote",
            "input_type": "number",
            "value_type": "float",
            "description": "Anteil besuchter Termine, z. B. zwischen 0 und 1.",
            "min_value": 0,
            "step": 0.01,
        },
        {
            "name": "practice_tests",
            "label": "Anzahl Uebungstests",
            "input_type": "number",
            "value_type": "int",
            "description": "Wie viele Uebungstests absolviert wurden.",
            "min_value": 0,
            "step": 1,
        },
    ],
    "hyperparameters": [
        {
            "name": "n_neighbors",
            "label": "Anzahl Nachbarn",
            "parameter_type": "int",
            "description": "Wie viele aehnliche Beispiele in die Entscheidung einfliessen.",
            "default": 3,
            "minimum": 1,
            "step": 1,
        },
        {
            "name": "weights",
            "label": "Gewichtung",
            "parameter_type": "select",
            "description": "Legt fest, ob alle Nachbarn gleich oder nach Distanz gewichtet werden. Fuer kleine Datensaetze ist Distanzgewichtung stabiler.",
            "default": "distance",
            "options": ["uniform", "distance"],
        },
    ],
    "default_training_samples": [
        {"study_hours": 2, "attendance_rate": 0.55, "practice_tests": 1, "learning_status": "kritisch"},
        {"study_hours": 4, "attendance_rate": 0.62, "practice_tests": 2, "learning_status": "kritisch"},
        {"study_hours": 8, "attendance_rate": 0.8, "practice_tests": 6, "learning_status": "stabil"},
        {"study_hours": 11, "attendance_rate": 0.84, "practice_tests": 8, "learning_status": "stabil"},
        {"study_hours": 16, "attendance_rate": 0.91, "practice_tests": 15, "learning_status": "sehr_gut"},
        {"study_hours": 18, "attendance_rate": 0.95, "practice_tests": 18, "learning_status": "sehr_gut"},
    ],
    "default_prediction_input": {"study_hours": 18, "attendance_rate": 0.95, "practice_tests": 18},
    "model_path": MODEL_DIR / "knn_classifier_model.joblib",
    "metadata_path": MODEL_DIR / "knn_classifier_metadata.json",
    "factory": lambda params: KNeighborsClassifier(
        n_neighbors=params["n_neighbors"],
        weights=params["weights"],
    ),
}