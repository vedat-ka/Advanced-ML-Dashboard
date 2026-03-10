from pathlib import Path

from database import reset_all_runtime_data
from ml_algorithms import list_algorithm_configs
from model_training import train_algorithm_model


BASE_DIR = Path(__file__).resolve().parent
TRAINED_MODELS_DIR = BASE_DIR / "trained_models"
GENERATED_SUFFIXES = {".pkl", ".joblib", ".json"}


def iter_generated_artifacts() -> list[Path]:
    artifacts: list[Path] = []
    for path in TRAINED_MODELS_DIR.rglob("*"):
        if not path.is_file() or path.suffix not in GENERATED_SUFFIXES:
            continue
        artifacts.append(path)
    return artifacts


def remove_generated_artifacts() -> list[Path]:
    removed: list[Path] = []
    for artifact in iter_generated_artifacts():
        artifact.unlink(missing_ok=True)
        removed.append(artifact)
    return removed


def train_original_models() -> list[str]:
    trained_keys: list[str] = []
    for config in list_algorithm_configs():
        train_algorithm_model(
            algorithm_key=config["algorithm_key"],
            samples=list(config["default_training_samples"]),
            hyperparameters={},
            model_variant="original",
            note="Dieses Modell wurde per bootstrap_models.py aus den Standard-Trainingsdaten neu erzeugt.",
            persist_run=False,
        )
        trained_keys.append(str(config["algorithm_key"]))
    return trained_keys


def main() -> None:
    removed = remove_generated_artifacts()
    reset_all_runtime_data()
    originals = train_original_models()

    print(f"Removed artifacts: {len(removed)}")
    print(f"Original models trained: {', '.join(originals)}")
    print("Finetuned models trained: none")
    print("SQLite runtime data reset: predictions, custom_model_runs, custom_model_predictions, custom_finetuning_samples")


if __name__ == "__main__":
    main()