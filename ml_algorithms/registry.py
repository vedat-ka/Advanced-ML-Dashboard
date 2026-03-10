from typing import Any

from .decision_tree_classifier_algorithm import CONFIG as DECISION_TREE_CLASSIFIER_CONFIG
from .knn_classifier_algorithm import CONFIG as KNN_CLASSIFIER_CONFIG
from .linear_regression_algorithm import CONFIG as LINEAR_REGRESSION_CONFIG
from .random_forest_classifier_algorithm import CONFIG as RANDOM_FOREST_CLASSIFIER_CONFIG
from .ridge_regression_algorithm import CONFIG as RIDGE_REGRESSION_CONFIG
from .spam_detection_algorithm import CONFIG as SPAM_DETECTION_CONFIG


ALGORITHM_CONFIGS: dict[str, dict[str, Any]] = {
    LINEAR_REGRESSION_CONFIG["algorithm_key"]: LINEAR_REGRESSION_CONFIG,
    RIDGE_REGRESSION_CONFIG["algorithm_key"]: RIDGE_REGRESSION_CONFIG,
    DECISION_TREE_CLASSIFIER_CONFIG["algorithm_key"]: DECISION_TREE_CLASSIFIER_CONFIG,
    RANDOM_FOREST_CLASSIFIER_CONFIG["algorithm_key"]: RANDOM_FOREST_CLASSIFIER_CONFIG,
    KNN_CLASSIFIER_CONFIG["algorithm_key"]: KNN_CLASSIFIER_CONFIG,
    SPAM_DETECTION_CONFIG["algorithm_key"]: SPAM_DETECTION_CONFIG,
}


def get_algorithm_config(algorithm_key: str) -> dict[str, Any]:
    if algorithm_key not in ALGORITHM_CONFIGS:
        raise ValueError(f"Unbekannter Algorithmus: {algorithm_key}")

    return ALGORITHM_CONFIGS[algorithm_key]


def list_algorithm_configs() -> list[dict[str, Any]]:
    return [ALGORITHM_CONFIGS[key] for key in ALGORITHM_CONFIGS]