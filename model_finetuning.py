from pathlib import Path
import json

from sklearn.linear_model import LinearRegression

from database import get_connection, initialize_database
from model_artifacts import dump_model_artifact


BASE_DIR = Path(__file__).resolve().parent
LINEAR_REGRESSION_MODEL_DIR = BASE_DIR / "trained_models" / "linear_regression"
FINETUNED_MODEL_PATH = LINEAR_REGRESSION_MODEL_DIR / "model_linear_reg_finetuned.joblib"
FINETUNED_MODEL_METADATA_PATH = LINEAR_REGRESSION_MODEL_DIR / "model_linear_reg_finetuned_metadata.json"
MIN_FINETUNING_SAMPLES = 5


def fetch_finetuning_samples(limit: int | None = None) -> list[dict[str, float | int | str]]:
    """Read saved prediction rows with validated market prices from SQLite."""
    initialize_database()

    query = """
        SELECT id, area, predicted_price, actual_price, model_source, created_at
        FROM predictions
        WHERE actual_price IS NOT NULL
        ORDER BY id ASC
    """
    params: tuple[int, ...] = ()

    if limit is not None:
        query += " LIMIT ?"
        params = (limit,)

    with get_connection() as connection:
        rows = connection.execute(query, params).fetchall()

    return [dict(row) for row in rows]


def build_training_data(
    samples: list[dict[str, float | int | str]],
) -> tuple[list[list[float]], list[float]]:
    features = [[float(sample["area"])] for sample in samples]
    targets = [float(sample["actual_price"]) for sample in samples]
    return features, targets


def finetune_model_from_database(
    limit: int | None = None,
    model_path: Path = FINETUNED_MODEL_PATH,
    metadata_path: Path = FINETUNED_MODEL_METADATA_PATH,
) -> dict[str, float | int | str]:
    samples = fetch_finetuning_samples(limit=limit)
    if len(samples) < MIN_FINETUNING_SAMPLES:
        raise ValueError(
            f"Mindestens {MIN_FINETUNING_SAMPLES} gespeicherte Zeilen mit actual_price werden fuer ein stabiles Linear-Regression-Finetuning benoetigt."
        )

    features, targets = build_training_data(samples)

    model = LinearRegression()
    model.fit(features, targets)

    training_score = float(model.score(features, targets))
    note = (
        "This finetuned model was retrained from SQLite rows using area as input and actual_price as target. "
        "Only rows with a validated comparison price were used."
    )

    dump_model_artifact(model, model_path)

    metadata = {
        "model_file": model_path.name,
        "model_type": model.__class__.__name__,
        "source_database": "predictions.db",
        "sample_count": len(samples),
        "target_field": "actual_price",
        "minimum_required_samples": MIN_FINETUNING_SAMPLES,
        "coefficient": float(model.coef_[0]),
        "intercept": float(model.intercept_),
        "training_score": training_score,
        "source_samples": samples,
        "note": note,
    }

    with metadata_path.open("w", encoding="utf-8") as metadata_file:
        json.dump(metadata, metadata_file, indent=2)

    return {
        "model_file": model_path.name,
        "sample_count": len(samples),
        "coefficient": float(model.coef_[0]),
        "intercept": float(model.intercept_),
        "training_score": training_score,
    }


if __name__ == "__main__":
    result = finetune_model_from_database()
    print(f"Created finetuned model: {result['model_file']}")
    print(f"Samples: {result['sample_count']}")
    print(f"Coefficient: {result['coefficient']}")
    print(f"Intercept: {result['intercept']}")
    print(f"Training score: {result['training_score']}")