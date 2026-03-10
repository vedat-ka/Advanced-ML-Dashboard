"""Trainings-, Finetuning- und Vorhersage-Workflow fuer die konfigurierbaren ML-Algorithmen."""

from datetime import datetime
from pathlib import Path
from typing import Any
import json

from database import (
    delete_custom_finetuning_sample,
    list_custom_model_runs,
    list_custom_finetuning_samples,
    save_custom_model_prediction,
    save_custom_finetuning_sample,
    save_custom_model_run,
)
from ml_algorithms import get_algorithm_config, list_algorithm_configs
from model_artifacts import dump_model_artifact, load_model_artifact


def _serialize_value(value: Any) -> Any:
    """Wandelt Modell- und NumPy-Werte in JSON-kompatible Python-Typen um.

    Args:
        value: Beliebiger Wert aus Modellattributen, Metadaten oder Vorhersagen.

    Returns:
        Ein serialisierbarer Python-Wert wie dict, list, str, int, float oder None.
    """
    if hasattr(value, "tolist"):
        return value.tolist()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (int, float, str, bool)) or value is None:
        return value
    if isinstance(value, dict):
        return {key: _serialize_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_serialize_value(item) for item in value]
    return str(value)


def list_available_algorithms() -> list[dict[str, Any]]:
    """Liefert die UI-/API-Beschreibung aller registrierten Algorithmen.

    Returns:
        Eine Liste von Konfigurations-Dictionaries mit Labeln, Feldern, Defaults und Metadaten
        fuer die Anzeige und Nutzung in API und Frontend.
    """
    items: list[dict[str, Any]] = []

    for config in list_algorithm_configs():
        items.append(
            {
                "algorithm_key": config["algorithm_key"],
                "label": config["label"],
                "model_type": config["model_type"],
                "task_type": config["task_type"],
                "scenario_name": config["scenario_name"],
                "summary": config["summary"],
                "best_for": config["best_for"],
                "scenario_examples": config["scenario_examples"],
                "prediction_examples": config.get("prediction_examples", []),
                "min_samples": config["min_samples"],
                "training_fields": config["training_fields"],
                "prediction_fields": config["prediction_fields"],
                "hyperparameters": config["hyperparameters"],
                "default_training_samples": config["default_training_samples"],
                "default_prediction_input": config["default_prediction_input"],
            }
        )

    return items


def _coerce_bool(value: Any, field_name: str) -> bool:
    """Normalisiert boolesche Eingaben aus Formularen und JSON-Payloads.

    Args:
        value: Rohwert aus Formular, Query oder JSON.
        field_name: Fachlicher Feldname fuer valide Fehlermeldungen.

    Returns:
        Den normalisierten booleschen Wert.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes", "ja"}:
            return True
        if normalized in {"false", "0", "no", "nein"}:
            return False
    raise ValueError(f"Ungueltiger boolescher Wert fuer {field_name}: {value}")


def _coerce_number(value: Any, field_name: str, parameter_type: str) -> int | float:
    """Erzwingt numerische Eingaben und meldet ungueltige Werte mit Feldbezug.

    Args:
        value: Rohwert aus Request oder Formular.
        field_name: Name des Feldes fuer Fehlermeldungen.
        parameter_type: Erwarteter Zieltyp, aktuell "int" oder "float".

    Returns:
        Den numerisch konvertierten Wert als int oder float.
    """
    if value in (None, ""):
        raise ValueError(f"Der Wert fuer {field_name} darf nicht leer sein.")

    try:
        if parameter_type == "int":
            return int(value)
        return float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"Ungueltiger numerischer Wert fuer {field_name}: {value}") from error


def _coerce_field_value(value: Any, field_spec: dict[str, Any]) -> Any:
    """Validiert einen einzelnen Feldwert anhand der Algorithmus-Felddefinition.

    Args:
        value: Rohwert fuer ein Trainings-, Vorhersage- oder Hyperparameterfeld.
        field_spec: Felddefinition aus der Algorithmus-Konfiguration.

    Returns:
        Den normalisierten und validierten Feldwert im erwarteten Python-Typ.
    """
    value_type = field_spec.get("value_type", "str")
    field_name = field_spec["name"]

    if value_type == "bool":
        coerced = _coerce_bool(value, field_name)
    elif value_type in {"int", "float"}:
        coerced = _coerce_number(value, field_name, value_type)
    else:
        if value in (None, ""):
            raise ValueError(f"Der Wert fuer {field_name} darf nicht leer sein.")
        coerced = str(value)

    options = field_spec.get("options")
    if options and coerced not in options:
        raise ValueError(
            f"Ungueltige Auswahl fuer {field_name}: {coerced}. Erlaubt sind: {', '.join(options)}"
        )

    minimum = field_spec.get("min_value")
    if minimum is not None and isinstance(coerced, (int, float)) and coerced < minimum:
        raise ValueError(f"Der Wert fuer {field_name} muss groesser oder gleich {minimum} sein.")

    return coerced


def create_empty_training_sample(algorithm_key: str) -> dict[str, Any]:
    """Erzeugt eine leere Trainingszeile passend zur Felddefinition des Algorithmus.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.

    Returns:
        Ein Dictionary mit allen Trainingsfeldern des Algorithmus und leeren String-Werten.
    """
    config = get_algorithm_config(algorithm_key)
    return {field["name"]: "" for field in config["training_fields"]}


def create_default_prediction_input(algorithm_key: str) -> dict[str, Any]:
    """Liefert die Default-Eingabe fuer Vorhersagen im ausgewaehlten Szenario.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.

    Returns:
        Ein Dictionary mit der vorkonfigurierten Standard-Eingabe fuer Vorhersagen.
    """
    config = get_algorithm_config(algorithm_key)
    return dict(config["default_prediction_input"])


def create_default_finetuning_sample(algorithm_key: str) -> dict[str, Any]:
    """Liefert ein Startbeispiel fuer die Erfassung realer Finetuning-Samples.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.

    Returns:
        Das erste Default-Trainingssample des Algorithmus als Vorlage fuer Finetuning-Daten.
    """
    config = get_algorithm_config(algorithm_key)
    first_sample = config["default_training_samples"][0] if config["default_training_samples"] else {}
    return dict(first_sample)


def get_algorithm_artifact_paths(algorithm_key: str, model_variant: str = "original") -> tuple[Path, Path]:
    """Berechnet Modell- und Metadatenpfad fuer Original- oder Finetuned-Artefakte.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.
        model_variant: Entweder "original" oder "finetuned".

    Returns:
        Ein Tupel aus Modellpfad und Metadatenpfad.
    """
    config = get_algorithm_config(algorithm_key)
    base_model_path: Path = config["model_path"]
    base_metadata_path: Path = config["metadata_path"]

    if model_variant == "original":
        return base_model_path, base_metadata_path

    if model_variant == "finetuned":
        return (
            base_model_path.with_name(f"{base_model_path.stem}_finetuned{base_model_path.suffix}"),
            base_metadata_path.with_name(f"{base_metadata_path.stem}_finetuned{base_metadata_path.suffix}"),
        )

    raise ValueError(f"Unbekannte Modellvariante: {model_variant}")


def normalize_hyperparameters(
    algorithm_key: str,
    hyperparameters: dict[str, Any] | None,
    sample_count: int,
) -> dict[str, Any]:
    """Validiert Hyperparameter gegen Typen, Grenzen und stichprobenspezifische Regeln.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.
        hyperparameters: Frei uebergebene Hyperparameter oder None fuer Defaults.
        sample_count: Anzahl der Trainingsbeispiele, relevant fuer Regeln wie `n_neighbors`.

    Returns:
        Ein Dictionary mit normalisierten Hyperparametern im erwarteten Typformat.
    """
    config = get_algorithm_config(algorithm_key)
    incoming = hyperparameters or {}
    normalized: dict[str, Any] = {}

    for spec in config["hyperparameters"]:
        name = spec["name"]
        raw_value = incoming.get(name, spec.get("default"))

        if raw_value in (None, "") and spec.get("nullable"):
            normalized[name] = None
            continue

        parameter_type = spec["parameter_type"]
        if parameter_type == "bool":
            value = _coerce_bool(raw_value, name)
        elif parameter_type in {"int", "float"}:
            value = _coerce_number(raw_value, name, parameter_type)
        elif parameter_type == "select":
            options = spec.get("options", [])
            if raw_value not in options:
                raise ValueError(
                    f"Ungueltige Auswahl fuer {name}: {raw_value}. Erlaubt sind: {', '.join(options)}"
                )
            value = raw_value
        else:
            value = raw_value

        minimum = spec.get("minimum")
        if minimum is not None and value is not None and value < minimum:
            raise ValueError(f"Der Parameter {name} muss groesser oder gleich {minimum} sein.")

        maximum = spec.get("maximum")
        if maximum is not None and value is not None and value > maximum:
            raise ValueError(f"Der Parameter {name} darf nicht groesser als {maximum} sein.")

        normalized[name] = value

    if "n_neighbors" in normalized and normalized["n_neighbors"] > sample_count:
        raise ValueError(
            "Die Anzahl der Nachbarn darf nicht groesser als die Anzahl der Trainingsbeispiele sein."
        )

    return normalized


def normalize_training_samples(
    algorithm_key: str,
    samples: list[dict[str, Any]],
    require_minimum_samples: bool = True,
) -> list[dict[str, Any]]:
    """Validiert und normalisiert frei eingegebene Trainings- oder Finetuning-Datensaetze.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.
        samples: Liste frei eingegebener Datensaetze.
        require_minimum_samples: Erzwingt bei True die Mindestanzahl laut Algorithmus-Konfiguration.

    Returns:
        Eine Liste validierter Samples mit korrekt typisierten Feldwerten.
    """
    config = get_algorithm_config(algorithm_key)
    if require_minimum_samples and len(samples) < config["min_samples"]:
        raise ValueError(
            f"Fuer {config['label']} werden mindestens {config['min_samples']} Trainingsbeispiele benoetigt."
        )

    normalized_samples: list[dict[str, Any]] = []
    for index, sample in enumerate(samples, start=1):
        normalized_sample: dict[str, Any] = {}
        for field in config["training_fields"]:
            field_name = field["name"]
            if field_name not in sample:
                raise ValueError(f"Trainingsbeispiel {index} enthaelt kein Feld {field_name}.")
            normalized_sample[field_name] = _coerce_field_value(sample[field_name], field)
        normalized_samples.append(normalized_sample)

    return normalized_samples


def normalize_prediction_input(algorithm_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Bringt eine Vorhersage-Payload in das vom Algorithmus erwartete Format.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.
        payload: Eingabedaten fuer eine Vorhersage.

    Returns:
        Ein validiertes Dictionary mit normalisierten Vorhersagefeldern.
    """
    config = get_algorithm_config(algorithm_key)
    normalized_payload: dict[str, Any] = {}

    for field in config["prediction_fields"]:
        field_name = field["name"]
        if field_name not in payload:
            raise ValueError(f"Das Vorhersagefeld {field_name} fehlt.")
        normalized_payload[field_name] = _coerce_field_value(payload[field_name], field)

    return normalized_payload


def _build_training_data(
    algorithm_key: str,
    samples: list[dict[str, Any]],
) -> tuple[list[list[Any]], list[Any]]:
    """Leitet Feature-Matrix und Zielwerte aus normalisierten Trainingssamples ab.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.
        samples: Bereits validierte Trainingssamples.

    Returns:
        Ein Tupel aus Features und Zielwerten fuer das Training.
    """
    config = get_algorithm_config(algorithm_key)
    feature_fields = [field["name"] for field in config["training_fields"] if field["role"] == "feature"]
    target_fields = [field["name"] for field in config["training_fields"] if field["role"] == "target"]

    if len(target_fields) != 1:
        raise ValueError(f"Algorithmus {algorithm_key} muss genau ein Ziel-Feld definieren.")

    target_field_name = target_fields[0]
    if config.get("feature_layout") == "single_text":
        if len(feature_fields) != 1:
            raise ValueError(f"Algorithmus {algorithm_key} muss fuer single_text genau ein Feature-Feld definieren.")
        feature_field_name = feature_fields[0]
        features = [str(sample[feature_field_name]) for sample in samples]
    else:
        features = [[sample[field_name] for field_name in feature_fields] for sample in samples]
    targets = [sample[target_field_name] for sample in samples]
    return features, targets


def _build_prediction_features(algorithm_key: str, payload: dict[str, Any]) -> list[list[Any]]:
    """Erzeugt das Modell-Input-Array fuer eine einzelne Vorhersageanfrage.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.
        payload: Bereits validierte Vorhersageeingabe.

    Returns:
        Eine Feature-Struktur im Format, das `model.predict(...)` erwartet.
    """
    config = get_algorithm_config(algorithm_key)
    feature_fields = [field["name"] for field in config["prediction_fields"]]
    if config.get("feature_layout") == "single_text":
        if len(feature_fields) != 1:
            raise ValueError(f"Algorithmus {algorithm_key} muss fuer single_text genau ein Vorhersagefeld definieren.")
        return [str(payload[feature_fields[0]])]
    return [[payload[field_name] for field_name in feature_fields]]


def extract_model_details(model: Any) -> dict[str, Any]:
    """Extrahiert zentrale, serialisierbare Modellattribute fuer Metadaten und UI.

    Args:
        model: Trainiertes Scikit-Learn-Modell oder kompatibles Objekt.

    Returns:
        Ein Dictionary mit serialisierten Modellattributen wie Koeffizienten oder Klassen.
    """
    details: dict[str, Any] = {
        "model_type": model.__class__.__name__,
        "n_features_in": _serialize_value(getattr(model, "n_features_in_", None)),
    }

    if hasattr(model, "coef_"):
        details["coefficient"] = _serialize_value(model.coef_)
    if hasattr(model, "intercept_"):
        details["intercept"] = _serialize_value(model.intercept_)
    if hasattr(model, "feature_importances_"):
        details["feature_importances"] = _serialize_value(model.feature_importances_)
    if hasattr(model, "classes_"):
        details["classes"] = _serialize_value(model.classes_)

    return details


def train_algorithm_model(
    algorithm_key: str,
    samples: list[dict[str, Any]],
    hyperparameters: dict[str, Any] | None = None,
    model_variant: str = "original",
    note: str | None = None,
    persist_run: bool = True,
) -> dict[str, Any]:
    """Trainiert ein Modell, speichert Artefakte/Metadaten und optional den Run in SQLite.

    Args:
        algorithm_key: Technischer Schluessel des zu trainierenden Algorithmus.
        samples: Frei eingegebene Trainingsdaten.
        hyperparameters: Optionale Hyperparameter fuer die Modellinstanz.
        model_variant: Zielvariante, typischerweise "original" oder "finetuned".
        note: Optionale Beschreibung fuer Metadaten und Run-Historie.
        persist_run: Speichert bei True den Trainingslauf zusaetzlich in SQLite.

    Returns:
        Ein Metadaten-Dictionary zum trainierten Modell inklusive Score, Samples und Dateinamen.
    """
    config = get_algorithm_config(algorithm_key)
    normalized_samples = normalize_training_samples(algorithm_key, samples)
    normalized_hyperparameters = normalize_hyperparameters(
        algorithm_key=algorithm_key,
        hyperparameters=hyperparameters,
        sample_count=len(normalized_samples),
    )

    features, targets = _build_training_data(algorithm_key, normalized_samples)
    model = config["factory"](normalized_hyperparameters)
    model.fit(features, targets)

    model_path, metadata_path = get_algorithm_artifact_paths(algorithm_key, model_variant=model_variant)
    dump_model_artifact(model, model_path)

    training_score = float(model.score(features, targets)) if len(normalized_samples) >= 2 else 1.0
    model_details = extract_model_details(model)
    trained_at = datetime.now().isoformat(timespec="seconds")
    metadata_note = note or (
        f"Dieses Modell wurde fuer den Anwendungsfall '{config['best_for']}' mit frei eingegebenen Trainingsdaten trainiert."
    )
    metadata = {
        "algorithm_key": algorithm_key,
        "algorithm_label": config["label"],
        "model_variant": model_variant,
        "model_type": config["model_type"],
        "task_type": config["task_type"],
        "model_file": model_path.name,
        "metadata_file": metadata_path.name,
        "sample_count": len(normalized_samples),
        "training_score": training_score,
        "hyperparameters": normalized_hyperparameters,
        "model_details": model_details,
        "training_samples": normalized_samples,
        "trained_at": trained_at,
        "best_for": config["best_for"],
        "note": metadata_note,
    }

    with metadata_path.open("w", encoding="utf-8") as metadata_file:
        json.dump(metadata, metadata_file, indent=2)

    if persist_run:
        save_custom_model_run(
            algorithm_key=algorithm_key,
            algorithm_label=config["label"],
            model_variant=model_variant,
            model_type=config["model_type"],
            task_type=config["task_type"],
            model_file=model_path.name,
            metadata_file=metadata_path.name,
            sample_count=len(normalized_samples),
            training_score=training_score,
            hyperparameters_json=json.dumps(normalized_hyperparameters),
            training_samples_json=json.dumps(normalized_samples),
            note=metadata_note,
        )

    return metadata


def finetune_algorithm_model_from_database(
    algorithm_key: str,
    limit: int | None = None,
) -> dict[str, Any]:
    """Trainiert eine finetunte Modellvariante aus realen SQLite-Finetuning-Samples neu.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.
        limit: Optionales Limit fuer die Anzahl geladener SQLite-Samples.

    Returns:
        Das Metadaten-Dictionary der neu trainierten finetunten Modellvariante.
    """
    config = get_algorithm_config(algorithm_key)
    rows = list_custom_finetuning_samples(algorithm_key, limit=limit)
    if not rows:
        raise ValueError(
            f"Fuer {config['label']} wurden noch keine echten Finetuning-Datensaetze in SQLite gespeichert. Erfasse zuerst reale Vergleichsdaten in der UI."
        )

    source_samples = [json.loads(str(row["sample_json"])) for row in reversed(rows)]
    latest_run = list_custom_model_runs(algorithm_key, model_variant="original", limit=1)
    latest_hyperparameters = (
        json.loads(str(latest_run[0]["hyperparameters_json"])) if latest_run else {}
    )

    finetune_note = (
        f"Dieses finetunte Modell wurde aus {len(rows)} in SQLite gespeicherten Realwelt-Beispielen "
        f"fuer den Anwendungsfall '{config['best_for']}' erneut trainiert."
    )

    result = train_algorithm_model(
        algorithm_key=algorithm_key,
        samples=source_samples,
        hyperparameters=latest_hyperparameters,
        model_variant="finetuned",
        note=finetune_note,
    )
    result["source_run_count"] = len(rows)
    return result


def load_algorithm_model(algorithm_key: str, model_variant: str = "original") -> Any:
    """Laedt das persistierte Modellartefakt einer Algorithmusvariante aus dem Dateisystem.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.
        model_variant: Zielvariante, typischerweise "original" oder "finetuned".

    Returns:
        Das deserialisierte Modellobjekt.
    """
    config = get_algorithm_config(algorithm_key)
    model_path, _ = get_algorithm_artifact_paths(algorithm_key, model_variant=model_variant)
    if not model_path.exists():
        raise RuntimeError(
            f"Modell fuer {config['label']} ({model_variant}) nicht gefunden: {model_path}. Trainiere zuerst ueber den passenden Algorithmus-Endpunkt."
        )

    return load_model_artifact(model_path)


def load_algorithm_metadata(algorithm_key: str, model_variant: str = "original") -> dict[str, Any] | None:
    """Laedt die gespeicherten Metadaten einer Modellvariante, falls vorhanden.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.
        model_variant: Zielvariante, typischerweise "original" oder "finetuned".

    Returns:
        Das Metadaten-Dictionary oder None, falls keine Datei vorhanden ist.
    """
    config = get_algorithm_config(algorithm_key)
    _, metadata_path = get_algorithm_artifact_paths(algorithm_key, model_variant=model_variant)

    if metadata_path.exists():
        with metadata_path.open("r", encoding="utf-8") as metadata_file:
            return json.load(metadata_file)

    return None


def save_algorithm_finetuning_sample(
    algorithm_key: str,
    sample: dict[str, Any],
    note: str = "",
) -> dict[str, Any]:
    """Validiert und speichert ein einzelnes reales Finetuning-Sample in SQLite.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.
        sample: Ein einzelner realer Datensatz fuer spaeteres Finetuning.
        note: Optionale fachliche Notiz zum Datensatz.

    Returns:
        Ein Dictionary mit der gespeicherten SQLite-ID, dem Sample und Zeitstempel.
    """
    config = get_algorithm_config(algorithm_key)
    normalized_sample = normalize_training_samples(
        algorithm_key,
        [sample],
        require_minimum_samples=False,
    )[0]
    row = save_custom_finetuning_sample(
        algorithm_key=algorithm_key,
        algorithm_label=config["label"],
        sample_json=json.dumps(normalized_sample),
        note=note,
    )
    return {
        "id": int(row["id"]),
        "algorithm_key": str(row["algorithm_key"]),
        "algorithm_label": str(row["algorithm_label"]),
        "sample": normalized_sample,
        "note": str(row["note"]),
        "created_at": str(row["created_at"]),
    }


def list_algorithm_finetuning_samples(
    algorithm_key: str,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """Liest gespeicherte Finetuning-Samples fuer einen Algorithmus aus SQLite aus.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.
        limit: Optionales Limit fuer die Anzahl geladener Eintraege.

    Returns:
        Eine Liste gespeicherter Finetuning-Samples inklusive Metadaten aus SQLite.
    """
    rows = list_custom_finetuning_samples(algorithm_key, limit=limit)
    return [
        {
            "id": int(row["id"]),
            "algorithm_key": str(row["algorithm_key"]),
            "algorithm_label": str(row["algorithm_label"]),
            "sample": json.loads(str(row["sample_json"])),
            "note": str(row["note"]),
            "created_at": str(row["created_at"]),
        }
        for row in rows
    ]


def remove_algorithm_finetuning_sample(sample_id: int) -> bool:
    """Entfernt ein gespeichertes Finetuning-Sample anhand seiner SQLite-ID.

    Args:
        sample_id: Primaerschluessel des gespeicherten Samples.

    Returns:
        True, wenn ein Datensatz geloescht wurde, sonst False.
    """
    return delete_custom_finetuning_sample(sample_id)


def _run_algorithm_prediction(
    algorithm_key: str,
    payload: dict[str, Any],
    model_variant: str = "original",
    persist: bool = True,
) -> dict[str, Any]:
    """Fuehrt eine Vorhersage fuer eine Modellvariante aus und speichert sie optional ab.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.
        payload: Vorhersageeingabe fuer das Modell.
        model_variant: Zielvariante, typischerweise "original" oder "finetuned".
        persist: Speichert die Vorhersage bei True in SQLite.

    Returns:
        Ein Dictionary mit Modellinfo, normalisierter Eingabe und Vorhersagewert.
    """
    config = get_algorithm_config(algorithm_key)
    normalized_payload = normalize_prediction_input(algorithm_key, payload)
    model = load_algorithm_model(algorithm_key, model_variant=model_variant)
    raw_prediction = model.predict(_build_prediction_features(algorithm_key, normalized_payload))[0]
    prediction_output = _serialize_value(raw_prediction)
    model_path, _ = get_algorithm_artifact_paths(algorithm_key, model_variant=model_variant)

    if persist:
        save_custom_model_prediction(
            algorithm_key=algorithm_key,
            algorithm_label=config["label"],
            model_variant=model_variant,
            model_file=model_path.name,
            input_payload_json=json.dumps(normalized_payload),
            prediction_output_json=json.dumps(prediction_output),
        )

    return {
        "algorithm_key": algorithm_key,
        "algorithm_label": config["label"],
        "model_variant": model_variant,
        "model_type": config["model_type"],
        "task_type": config["task_type"],
        "model_file": model_path.name,
        "prediction_input": normalized_payload,
        "prediction_output": prediction_output,
    }


def predict_with_algorithm(
    algorithm_key: str,
    payload: dict[str, Any],
    model_variant: str = "original",
) -> dict[str, Any]:
    """Oeffentliche API fuer persistierte Vorhersagen mit einem Algorithmusmodell.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.
        payload: Vorhersageeingabe.
        model_variant: Zielvariante, typischerweise "original" oder "finetuned".

    Returns:
        Ein Dictionary mit den Vorhersagedetails der gewaehlten Modellvariante.
    """
    return _run_algorithm_prediction(
        algorithm_key=algorithm_key,
        payload=payload,
        model_variant=model_variant,
        persist=True,
    )


def compare_algorithm_predictions(algorithm_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Vergleicht Original- und Finetuned-Vorhersage fuer dieselbe Eingabe.

    Args:
        algorithm_key: Technischer Schluessel des Algorithmus.
        payload: Vorhersageeingabe, die fuer beide Modellvarianten verwendet wird.

    Returns:
        Ein Dictionary mit Original-Resultat, Finetuned-Resultat und optionaler Differenz.
    """
    normalized_payload = normalize_prediction_input(algorithm_key, payload)
    original_result = _run_algorithm_prediction(
        algorithm_key,
        normalized_payload,
        model_variant="original",
        persist=False,
    )
    finetuned_result = _run_algorithm_prediction(
        algorithm_key,
        normalized_payload,
        model_variant="finetuned",
        persist=False,
    )

    original_output = original_result["prediction_output"]
    finetuned_output = finetuned_result["prediction_output"]
    prediction_difference: float | None = None
    if isinstance(original_output, (int, float)) and isinstance(finetuned_output, (int, float)):
        prediction_difference = float(finetuned_output) - float(original_output)

    return {
        "algorithm_key": original_result["algorithm_key"],
        "algorithm_label": original_result["algorithm_label"],
        "task_type": original_result["task_type"],
        "prediction_input": normalized_payload,
        "original_model_file": original_result["model_file"],
        "finetuned_model_file": finetuned_result["model_file"],
        "original_prediction_output": original_output,
        "finetuned_prediction_output": finetuned_output,
        "prediction_difference": prediction_difference,
        "outputs_match": original_output == finetuned_output,
    }