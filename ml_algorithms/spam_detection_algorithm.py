from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "trained_models" / "spam_detection_classifier"


CONFIG = {
    "algorithm_key": "spam_detection_classifier",
    "label": "Spam Detection",
    "model_type": "TfidfVectorizer + MultinomialNB",
    "task_type": "text-classification",
    "scenario_name": "E-Mails als Spam oder Kein Spam klassifizieren",
    "summary": "Textklassifikation fuer kurze und mittlere Mailtexte mit einem leichten Naive-Bayes-Ansatz.",
    "best_for": "Gut fuer einfache Spam-Erkennung, Werbe-Mails, Gewinnspieltexte und verdaechtige Call-to-Action-Nachrichten.",
    "scenario_examples": [
        "Gewinnversprechen, viele Ausrufezeichen und dringende Aufforderungen fuehren oft zu Spam.",
        "Normale Projektabsprachen oder neutrale Team-Mails fuehren meist zu kein_spam.",
        "Ungewoehnliche Zahlungslinks und Zeitdruck sind starke Spam-Signale.",
    ],
    "prediction_examples": [
        {
            "label": "Normale Team-Mail",
            "description": "Sachliche Abstimmung ohne Druck oder Lockangebote.",
            "input": {
                "email_text": "Hallo Team, bitte schaut bis morgen in die aktualisierte Agenda und gebt kurzes Feedback zum Termin."
            },
        },
        {
            "label": "Grenzfall Verifikation",
            "description": "Dringender Sicherheitsbezug mit Link und Zeitdruck.",
            "input": {
                "email_text": "Ihr Konto muss heute bestaetigt werden. Bitte pruefen Sie die Angaben ueber den folgenden Link."
            },
        },
        {
            "label": "Klarer Spam-Fall",
            "description": "Lockangebot und sofortige Handlungsaufforderung.",
            "input": {
                "email_text": "Glueckwunsch! Sie haben 1000 Euro gewonnen. Klicken Sie jetzt sofort auf den Link und bestaetigen Sie Ihre Daten."
            },
        },
    ],
    "min_samples": 4,
    "feature_layout": "single_text",
    "training_fields": [
        {
            "name": "email_text",
            "label": "Mail-Text",
            "input_type": "textarea",
            "value_type": "str",
            "role": "feature",
            "description": "Vollstaendiger Betreff oder Mail-Inhalt, der klassifiziert werden soll.",
        },
        {
            "name": "spam_label",
            "label": "Zielklasse",
            "input_type": "select",
            "value_type": "str",
            "role": "target",
            "description": "Zu lernende Spam-Klasse.",
            "options": ["spam", "kein_spam"],
        },
    ],
    "prediction_fields": [
        {
            "name": "email_text",
            "label": "Mail zum Pruefen",
            "input_type": "textarea",
            "value_type": "str",
            "description": "Text der E-Mail oder Nachricht, die auf Spam geprueft werden soll.",
        }
    ],
    "hyperparameters": [
        {
            "name": "alpha",
            "label": "Alpha-Glattung",
            "parameter_type": "float",
            "description": "Glattung fuer den Naive-Bayes-Klassifikator. Hoeher bedeutet staerkere Regularisierung.",
            "default": 1.0,
            "minimum": 0.0001,
            "step": 0.1,
        },
        {
            "name": "ngram_max",
            "label": "Max. N-Gramm-Laenge",
            "parameter_type": "int",
            "description": "1 fuer einzelne Woerter, 2 fuer Woerter und Zweierkombinationen.",
            "default": 2,
            "minimum": 1,
            "maximum": 3,
            "step": 1,
        },
    ],
    "default_training_samples": [
        {
            "email_text": "Glueckwunsch! Sie haben einen Einkaufsgutschein gewonnen. Klicken Sie sofort auf den Link und bestaetigen Sie Ihre Daten.",
            "spam_label": "spam",
        },
        {
            "email_text": "Hallo Team, im Anhang findet ihr die aktualisierte Agenda fuer das Meeting morgen um 10 Uhr.",
            "spam_label": "kein_spam",
        },
        {
            "email_text": "Dringend: Ihr Konto wird heute gesperrt. Verifizieren Sie jetzt Ihr Passwort ueber diesen Link.",
            "spam_label": "spam",
        },
        {
            "email_text": "Kannst du bitte die finale Praesentation fuer den Kunden bis 15 Uhr freigeben? Danke.",
            "spam_label": "kein_spam",
        },
        {
            "email_text": "Exklusives Angebot nur heute: 90 Prozent Rabatt, jetzt kaufen und sofort profitieren.",
            "spam_label": "spam",
        },
        {
            "email_text": "Die Rechnung fuer Februar wurde freigegeben und im Projektordner abgelegt.",
            "spam_label": "kein_spam",
        },
    ],
    "default_prediction_input": {
        "email_text": "Achtung! Ihr Paket kann nicht zugestellt werden. Zahlen Sie jetzt 2 Euro ueber den folgenden Link."
    },
    "model_path": MODEL_DIR / "spam_detection_classifier_model.joblib",
    "metadata_path": MODEL_DIR / "spam_detection_classifier_metadata.json",
    "factory": lambda params: Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, params["ngram_max"]))),
            ("classifier", MultinomialNB(alpha=params["alpha"])),
        ]
    ),
}
