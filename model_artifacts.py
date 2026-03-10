from pathlib import Path
from typing import Any

import joblib


def dump_model_artifact(model: Any, model_path: Path) -> None:
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)


def load_model_artifact(model_path: Path) -> Any:
    if not model_path.exists():
        raise FileNotFoundError(model_path)

    return joblib.load(model_path)