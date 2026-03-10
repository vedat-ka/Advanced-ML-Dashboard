from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any
import json

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from database import (
    DATABASE_PATH,
    get_database_schema,
    get_prediction,
    get_prediction_summary,
    initialize_database,
    list_predictions,
    save_prediction,
    update_prediction_actual_price,
)
from model_finetuning import (
    FINETUNED_MODEL_METADATA_PATH,
    FINETUNED_MODEL_PATH,
    finetune_model_from_database,
)
from model_artifacts import load_model_artifact
from model_training import (
    compare_algorithm_predictions,
    create_default_prediction_input,
    create_empty_training_sample,
    finetune_algorithm_model_from_database,
    list_available_algorithms,
    list_algorithm_finetuning_samples,
    load_algorithm_metadata,
    predict_with_algorithm,
    remove_algorithm_finetuning_sample,
    save_algorithm_finetuning_sample,
    train_algorithm_model,
)
from ml_algorithms import get_algorithm_config


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "trained_models" / "linear_regression" / "linear_regression_model.joblib"
FILE_CACHE: dict[Path, dict[str, Any]] = {}


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Advanced-ML-API fuer Preisvorhersagen",
    description="Sagt Preise anhand der Flaeche vorher und speichert jede Vorhersage in einer lokalen SQLite-Datenbank.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionRequest(BaseModel):
    area: float = Field(..., gt=0, description="Flaeche in Quadratmetern")


class PredictionRecord(BaseModel):
    id: int
    area: float
    predicted_price: float
    actual_price: float | None = None
    model_source: str
    created_at: str


class PredictionHistoryResponse(BaseModel):
    count: int
    items: list[PredictionRecord]


class PredictionSummaryResponse(BaseModel):
    total_predictions: int
    original_prediction_count: int
    finetuned_prediction_count: int
    actual_price_count: int
    min_area: float | None
    max_area: float | None
    avg_area: float | None
    min_predicted_price: float | None
    max_predicted_price: float | None
    avg_predicted_price: float | None
    min_actual_price: float | None
    max_actual_price: float | None
    avg_actual_price: float | None
    avg_absolute_error: float | None
    first_prediction_at: str | None
    last_prediction_at: str | None
    items: list[PredictionRecord]


class DatabaseSchemaItem(BaseModel):
    name: str
    type: str
    sql: str


class DatabaseSchemaResponse(BaseModel):
    database_file: str
    item_count: int
    items: list[DatabaseSchemaItem]


class FinetuningResponse(BaseModel):
    message: str
    model_file: str
    sample_count: int
    coefficient: float
    intercept: float
    training_score: float


class ActualPriceUpdateRequest(BaseModel):
    actual_price: float | None = Field(
        default=None,
        gt=0,
        description="Echter Vergleichspreis. Null entfernt einen bisher gespeicherten Wert.",
    )


class FinetunedPredictionResponse(BaseModel):
    id: int
    area: float
    model_source: str
    finetuned_model_file: str
    predicted_price: float
    created_at: str
    finetuning_sample_count: int | None = None
    finetuning_note: str | None = None


class ModelComparisonResponse(BaseModel):
    area: float
    original_model_file: str
    finetuned_model_file: str
    original_predicted_price: float
    finetuned_predicted_price: float
    prediction_difference: float
    finetuning_sample_count: int | None = None
    finetuning_note: str | None = None


class TrainingFieldDefinition(BaseModel):
    name: str
    label: str
    input_type: str
    value_type: str
    role: str | None = None
    description: str
    min_value: float | None = None
    step: float | None = None
    options: list[str] | None = None


class HyperparameterDefinition(BaseModel):
    name: str
    label: str
    parameter_type: str
    description: str
    default: Any | None = None
    minimum: float | None = None
    maximum: float | None = None
    step: float | None = None
    options: list[str] | None = None
    nullable: bool = False


class AlgorithmDefinition(BaseModel):
    algorithm_key: str
    label: str
    model_type: str
    task_type: str
    scenario_name: str
    summary: str
    best_for: str
    scenario_examples: list[str]
    prediction_examples: list[dict[str, Any]] = Field(default_factory=list)
    min_samples: int
    training_fields: list[TrainingFieldDefinition]
    prediction_fields: list[TrainingFieldDefinition]
    hyperparameters: list[HyperparameterDefinition]
    default_training_samples: list[dict[str, Any]]
    default_prediction_input: dict[str, Any]


class AlgorithmCatalogResponse(BaseModel):
    count: int
    items: list[AlgorithmDefinition]


class CustomModelTrainingRequest(BaseModel):
    training_samples: list[dict[str, Any]]
    hyperparameters: dict[str, Any] = Field(default_factory=dict)


class CustomModelTrainingResponse(BaseModel):
    message: str
    trained: bool = True
    algorithm_key: str
    algorithm_label: str
    model_variant: str = "original"
    model_type: str
    task_type: str
    model_file: str | None = None
    metadata_file: str | None = None
    sample_count: int = 0
    training_score: float | None = None
    hyperparameters: dict[str, Any] = Field(default_factory=dict)
    model_details: dict[str, Any] = Field(default_factory=dict)
    best_for: str
    note: str


class CustomModelMetadataResponse(CustomModelTrainingResponse):
    trained_at: str | None = None
    training_samples: list[dict[str, Any]] = Field(default_factory=list)


class CustomPredictionRequest(BaseModel):
    prediction_input: dict[str, Any]


class CustomPredictionResponse(BaseModel):
    algorithm_key: str
    algorithm_label: str
    model_variant: str = "original"
    model_type: str
    task_type: str
    model_file: str
    prediction_input: dict[str, Any]
    prediction_output: Any


class CustomModelComparisonResponse(BaseModel):
    algorithm_key: str
    algorithm_label: str
    task_type: str
    prediction_input: dict[str, Any]
    original_model_file: str
    finetuned_model_file: str
    original_prediction_output: Any
    finetuned_prediction_output: Any
    prediction_difference: float | None = None
    outputs_match: bool
    finetuning_sample_count: int | None = None
    finetuning_note: str | None = None


class FinetuningSampleRequest(BaseModel):
    sample: dict[str, Any]
    note: str = ""


class FinetuningSampleRecord(BaseModel):
    id: int
    algorithm_key: str
    algorithm_label: str
    sample: dict[str, Any]
    note: str
    created_at: str


class FinetuningSampleResponse(BaseModel):
    count: int
    items: list[FinetuningSampleRecord]


class DeleteFinetuningSampleResponse(BaseModel):
    deleted: bool
    sample_id: int


def load_cached_value(path: Path, loader):
    stat_result = path.stat()
    cached_entry = FILE_CACHE.get(path)

    if cached_entry and cached_entry["mtime_ns"] == stat_result.st_mtime_ns:
        return cached_entry["value"]

    value = loader(path)
    FILE_CACHE[path] = {
        "mtime_ns": stat_result.st_mtime_ns,
        "value": value,
    }
    return value


def load_model():
    try:
        return load_cached_value(MODEL_PATH, load_model_artifact)
    except FileNotFoundError as error:
        raise RuntimeError(
            f"Modelldatei nicht gefunden: {MODEL_PATH}. Trainiere zuerst die lineare Regression ueber /ml/algorithms/linear_regression/train."
        ) from error
    except (ModuleNotFoundError, ImportError, AttributeError) as error:
        raise RuntimeError(
            "Beim Laden des Modells ist die Umgebung nicht kompatibel mit dem gespeicherten Artefakt. Pruefe scikit-learn-Version und trainiere das Modell bei Bedarf neu."
        ) from error


def get_artifact_display_name(path: Path) -> str:
    return path.name


def load_finetuned_model():
    try:
        return load_cached_value(FINETUNED_MODEL_PATH, load_model_artifact)
    except FileNotFoundError as error:
        raise RuntimeError(
            f"Finetunte Modelldatei nicht gefunden: {FINETUNED_MODEL_PATH}. Fuehre zuerst /finetune-model aus."
        ) from error
    except (ModuleNotFoundError, ImportError, AttributeError) as error:
        raise RuntimeError(
            "Beim Laden des finetunten Modells ist die Umgebung nicht kompatibel mit dem gespeicherten Artefakt. Pruefe scikit-learn-Version und trainiere das Modell bei Bedarf neu."
        ) from error


def load_finetuned_model_metadata():
    if not FINETUNED_MODEL_METADATA_PATH.exists():
        return None

    return load_cached_value(
        FINETUNED_MODEL_METADATA_PATH,
        lambda metadata_path: json.loads(metadata_path.read_text(encoding="utf-8")),
    )


def predict_area_price(area: float) -> float:
    try:
        model = load_model()
        prediction = model.predict([[area]])
        return float(prediction[0])
    except RuntimeError:
        raise
    except Exception as error:
        raise RuntimeError(f"Vorhersage fehlgeschlagen: {error}") from error


def predict_finetuned_area_price(area: float) -> float:
    try:
        model = load_finetuned_model()
        prediction = model.predict([[area]])
        return float(prediction[0])
    except RuntimeError:
        raise
    except Exception as error:
        raise RuntimeError(f"Vorhersage fehlgeschlagen: {error}") from error


def create_prediction_record(area: float) -> PredictionRecord:
    predicted_price = predict_area_price(area)
    saved_record = save_prediction(area, predicted_price, model_source="original")
    return PredictionRecord(**saved_record)


def create_finetuned_prediction_record(area: float) -> PredictionRecord:
    predicted_price = predict_finetuned_area_price(area)
    saved_record = save_prediction(area, predicted_price, model_source="finetuned")
    return PredictionRecord(**saved_record)


@app.get("/")
async def root():
    return {
        "message": "Advanced-ML-Service mit SQLite-Persistenz laeuft.",
        "model_file": get_artifact_display_name(MODEL_PATH),
        "database_file": DATABASE_PATH.name,
        "prediction_endpoints": ["/predict", "/predictarea/{area}", "/predict-finetuned"],
        "history_endpoints": [
            "/predictions",
            "/predictions/{prediction_id}",
            "/predictions/{prediction_id}/actual-price",
        ],
        "reporting_endpoints": ["/reporting/summary", "/database/schema"],
        "model_endpoints": ["/finetune-model", "/predict-finetuned", "/compare-models"],
        "training_endpoints": [
            "/ml/algorithms",
            "/ml/algorithms/{algorithm_key}/train",
            "/ml/algorithms/{algorithm_key}/model",
            "/ml/algorithms/{algorithm_key}/finetuned-model",
            "/ml/algorithms/{algorithm_key}/finetuning-samples",
            "/ml/algorithms/{algorithm_key}/finetune",
            "/ml/algorithms/{algorithm_key}/predict",
            "/ml/algorithms/{algorithm_key}/predict-finetuned",
            "/ml/algorithms/{algorithm_key}/compare-models",
        ],
    }


@app.get("/ml/algorithms", response_model=AlgorithmCatalogResponse)
async def get_ml_algorithms():
    items = [AlgorithmDefinition(**item) for item in list_available_algorithms()]
    return AlgorithmCatalogResponse(count=len(items), items=items)


@app.get("/ml/algorithms/{algorithm_key}/model", response_model=CustomModelMetadataResponse)
async def get_custom_model_metadata(algorithm_key: str):
    config = get_algorithm_config(algorithm_key)
    metadata = load_algorithm_metadata(algorithm_key)
    if metadata is None:
        return CustomModelMetadataResponse(
            message="Fuer diesen Algorithmus wurde noch kein Modell trainiert.",
            trained=False,
            algorithm_key=algorithm_key,
            algorithm_label=config["label"],
            model_variant="original",
            model_type=config["model_type"],
            task_type=config["task_type"],
            best_for=config["best_for"],
            note="Trainiere zuerst diesen Algorithmus, damit ein eigenes Modell und Metadaten erzeugt werden.",
        )

    return CustomModelMetadataResponse(
        message="Algorithmus-Modell geladen.",
        trained=True,
        algorithm_key=metadata["algorithm_key"],
        algorithm_label=metadata["algorithm_label"],
        model_variant=str(metadata.get("model_variant", "original")),
        model_type=metadata["model_type"],
        task_type=metadata["task_type"],
        model_file=metadata["model_file"],
        metadata_file=metadata["metadata_file"],
        sample_count=int(metadata["sample_count"]),
        training_score=float(metadata["training_score"]),
        hyperparameters=dict(metadata["hyperparameters"]),
        model_details=dict(metadata["model_details"]),
        best_for=str(metadata["best_for"]),
        note=str(metadata["note"]),
        trained_at=str(metadata["trained_at"]),
        training_samples=list(metadata["training_samples"]),
    )


@app.get("/ml/algorithms/{algorithm_key}/finetuned-model", response_model=CustomModelMetadataResponse)
async def get_custom_finetuned_model_metadata(algorithm_key: str):
    config = get_algorithm_config(algorithm_key)
    metadata = load_algorithm_metadata(algorithm_key, model_variant="finetuned")
    if metadata is None:
        return CustomModelMetadataResponse(
            message="Fuer diesen Algorithmus wurde noch kein finetuntes Modell trainiert.",
            trained=False,
            algorithm_key=algorithm_key,
            algorithm_label=config["label"],
            model_variant="finetuned",
            model_type=config["model_type"],
            task_type=config["task_type"],
            best_for=config["best_for"],
            note="Trainiere zuerst das Originalmodell und starte danach das Finetuning aus SQLite.",
        )

    return CustomModelMetadataResponse(
        message="Finetuntes Algorithmus-Modell geladen.",
        trained=True,
        algorithm_key=metadata["algorithm_key"],
        algorithm_label=metadata["algorithm_label"],
        model_variant=str(metadata.get("model_variant", "finetuned")),
        model_type=metadata["model_type"],
        task_type=metadata["task_type"],
        model_file=metadata["model_file"],
        metadata_file=metadata["metadata_file"],
        sample_count=int(metadata["sample_count"]),
        training_score=float(metadata["training_score"]),
        hyperparameters=dict(metadata["hyperparameters"]),
        model_details=dict(metadata["model_details"]),
        best_for=str(metadata["best_for"]),
        note=str(metadata["note"]),
        trained_at=str(metadata["trained_at"]),
        training_samples=list(metadata["training_samples"]),
    )


@app.get("/ml/algorithms/{algorithm_key}/finetuning-samples", response_model=FinetuningSampleResponse)
async def get_algorithm_finetuning_samples(
    algorithm_key: str,
    limit: int = Query(50, ge=1, le=500, description="Maximale Anzahl gespeicherter Finetuning-Samples"),
):
    get_algorithm_config(algorithm_key)
    items = [
        FinetuningSampleRecord(**item)
        for item in list_algorithm_finetuning_samples(algorithm_key, limit=limit)
    ]
    return FinetuningSampleResponse(count=len(items), items=items)


@app.post("/ml/algorithms/{algorithm_key}/finetuning-samples", response_model=FinetuningSampleRecord)
async def create_algorithm_finetuning_sample(algorithm_key: str, payload: FinetuningSampleRequest):
    try:
        item = save_algorithm_finetuning_sample(algorithm_key, payload.sample, note=payload.note)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return FinetuningSampleRecord(**item)


@app.delete(
    "/ml/algorithms/{algorithm_key}/finetuning-samples/{sample_id}",
    response_model=DeleteFinetuningSampleResponse,
)
async def delete_algorithm_finetuning_sample(algorithm_key: str, sample_id: int):
    get_algorithm_config(algorithm_key)
    deleted = remove_algorithm_finetuning_sample(sample_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Finetuning-Sample nicht gefunden")

    return DeleteFinetuningSampleResponse(deleted=True, sample_id=sample_id)


@app.post("/ml/algorithms/{algorithm_key}/train", response_model=CustomModelTrainingResponse)
async def train_custom_ml_model(algorithm_key: str, payload: CustomModelTrainingRequest):
    try:
        result = train_algorithm_model(
            algorithm_key=algorithm_key,
            samples=payload.training_samples,
            hyperparameters=payload.hyperparameters,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Training fehlgeschlagen: {error}") from error

    return CustomModelTrainingResponse(
        message="Algorithmus-Modell wurde erfolgreich trainiert.",
        trained=True,
        algorithm_key=result["algorithm_key"],
        algorithm_label=result["algorithm_label"],
        model_variant=str(result.get("model_variant", "original")),
        model_type=result["model_type"],
        task_type=result["task_type"],
        model_file=result["model_file"],
        metadata_file=result["metadata_file"],
        sample_count=int(result["sample_count"]),
        training_score=float(result["training_score"]),
        hyperparameters=dict(result["hyperparameters"]),
        model_details=dict(result["model_details"]),
        best_for=str(result["best_for"]),
        note=str(result["note"]),
    )


@app.post("/ml/algorithms/{algorithm_key}/finetune", response_model=CustomModelTrainingResponse)
async def finetune_custom_ml_model(
    algorithm_key: str,
    limit: int | None = Query(
        None,
        ge=1,
        le=1000,
        description="Optional maximale Anzahl an SQLite-Trainingslaeufen fuer das Finetuning",
    ),
):
    try:
        result = finetune_algorithm_model_from_database(algorithm_key=algorithm_key, limit=limit)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Finetuning fehlgeschlagen: {error}") from error

    return CustomModelTrainingResponse(
        message="Finetuntes Algorithmus-Modell wurde erfolgreich aus SQLite erstellt.",
        trained=True,
        algorithm_key=result["algorithm_key"],
        algorithm_label=result["algorithm_label"],
        model_variant=str(result.get("model_variant", "finetuned")),
        model_type=result["model_type"],
        task_type=result["task_type"],
        model_file=result["model_file"],
        metadata_file=result["metadata_file"],
        sample_count=int(result["sample_count"]),
        training_score=float(result["training_score"]),
        hyperparameters=dict(result["hyperparameters"]),
        model_details=dict(result["model_details"]),
        best_for=str(result["best_for"]),
        note=str(result["note"]),
    )


@app.post("/ml/algorithms/{algorithm_key}/predict", response_model=CustomPredictionResponse)
async def predict_with_custom_ml_model(algorithm_key: str, payload: CustomPredictionRequest):
    try:
        result = predict_with_algorithm(algorithm_key, payload.prediction_input)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Vorhersage fehlgeschlagen: {error}") from error

    return CustomPredictionResponse(
        algorithm_key=result["algorithm_key"],
        algorithm_label=result["algorithm_label"],
        model_variant=str(result.get("model_variant", "original")),
        model_type=result["model_type"],
        task_type=result["task_type"],
        model_file=result["model_file"],
        prediction_input=dict(result["prediction_input"]),
        prediction_output=result["prediction_output"],
    )


@app.post("/ml/algorithms/{algorithm_key}/predict-finetuned", response_model=CustomPredictionResponse)
async def predict_with_custom_finetuned_model(algorithm_key: str, payload: CustomPredictionRequest):
    try:
        result = predict_with_algorithm(algorithm_key, payload.prediction_input, model_variant="finetuned")
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Vorhersage fehlgeschlagen: {error}") from error

    return CustomPredictionResponse(
        algorithm_key=result["algorithm_key"],
        algorithm_label=result["algorithm_label"],
        model_variant=str(result.get("model_variant", "finetuned")),
        model_type=result["model_type"],
        task_type=result["task_type"],
        model_file=result["model_file"],
        prediction_input=dict(result["prediction_input"]),
        prediction_output=result["prediction_output"],
    )


@app.post("/ml/algorithms/{algorithm_key}/compare-models", response_model=CustomModelComparisonResponse)
async def compare_custom_models(algorithm_key: str, payload: CustomPredictionRequest):
    try:
        result = compare_algorithm_predictions(algorithm_key, payload.prediction_input)
        finetuned_metadata = load_algorithm_metadata(algorithm_key, model_variant="finetuned")
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Vergleich fehlgeschlagen: {error}") from error

    sample_count = (
        int(finetuned_metadata["sample_count"])
        if finetuned_metadata and "sample_count" in finetuned_metadata
        else None
    )
    note = str(finetuned_metadata["note"]) if finetuned_metadata and "note" in finetuned_metadata else None

    return CustomModelComparisonResponse(
        algorithm_key=result["algorithm_key"],
        algorithm_label=result["algorithm_label"],
        task_type=result["task_type"],
        prediction_input=dict(result["prediction_input"]),
        original_model_file=result["original_model_file"],
        finetuned_model_file=result["finetuned_model_file"],
        original_prediction_output=result["original_prediction_output"],
        finetuned_prediction_output=result["finetuned_prediction_output"],
        prediction_difference=result["prediction_difference"],
        outputs_match=bool(result["outputs_match"]),
        finetuning_sample_count=sample_count,
        finetuning_note=note,
    )


@app.post("/predict", response_model=PredictionRecord)
async def predict_price(payload: PredictionRequest):
    try:
        return create_prediction_record(payload.area)
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.post("/finetune-model", response_model=FinetuningResponse)
async def finetune_model(
    limit: int | None = Query(
        None,
        ge=1,
        le=10000,
        description="Optional maximale Anzahl an SQLite-Zeilen fuer das Finetuning",
    )
):
    try:
        result = finetune_model_from_database(limit=limit)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Finetuning fehlgeschlagen: {error}") from error

    return FinetuningResponse(
        message="Finetuntes Modell wurde erfolgreich aus SQLite-Zeilen mit echten Vergleichspreisen erstellt.",
        model_file=str(result["model_file"]),
        sample_count=int(result["sample_count"]),
        coefficient=float(result["coefficient"]),
        intercept=float(result["intercept"]),
        training_score=float(result["training_score"]),
    )


@app.post("/compare-models", response_model=ModelComparisonResponse)
async def compare_models(payload: PredictionRequest):
    try:
        original_predicted_price = predict_area_price(payload.area)
        finetuned_predicted_price = predict_finetuned_area_price(payload.area)
        metadata = load_finetuned_model_metadata()
    except RuntimeError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    sample_count = int(metadata["sample_count"]) if metadata and "sample_count" in metadata else None
    note = metadata.get("note") if metadata else None

    return ModelComparisonResponse(
        area=payload.area,
        original_model_file=get_artifact_display_name(MODEL_PATH),
        finetuned_model_file=get_artifact_display_name(FINETUNED_MODEL_PATH),
        original_predicted_price=original_predicted_price,
        finetuned_predicted_price=finetuned_predicted_price,
        prediction_difference=finetuned_predicted_price - original_predicted_price,
        finetuning_sample_count=sample_count,
        finetuning_note=note,
    )


@app.post("/predict-finetuned", response_model=FinetunedPredictionResponse)
async def predict_with_finetuned_model(payload: PredictionRequest):
    try:
        saved_record = create_finetuned_prediction_record(payload.area)
        metadata = load_finetuned_model_metadata()
    except RuntimeError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    sample_count = int(metadata["sample_count"]) if metadata and "sample_count" in metadata else None
    note = metadata.get("note") if metadata else None

    return FinetunedPredictionResponse(
        id=saved_record.id,
        area=saved_record.area,
        model_source=saved_record.model_source,
        finetuned_model_file=get_artifact_display_name(FINETUNED_MODEL_PATH),
        predicted_price=saved_record.predicted_price,
        created_at=saved_record.created_at,
        finetuning_sample_count=sample_count,
        finetuning_note=note,
    )


@app.get("/predictarea/{area}", response_model=PredictionRecord)
async def predict_price_from_path(area: float):
    try:
        return create_prediction_record(area)
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.get("/predictions", response_model=PredictionHistoryResponse)
async def get_predictions(
    limit: int = Query(20, ge=1, le=500, description="Maximale Anzahl gespeicherter Vorhersagen")
):
    items = [PredictionRecord(**record) for record in list_predictions(limit=limit)]
    return PredictionHistoryResponse(count=len(items), items=items)


@app.get("/predictions/{prediction_id}", response_model=PredictionRecord)
async def get_prediction_by_id(prediction_id: int):
    record = get_prediction(prediction_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Vorhersage nicht gefunden")

    return PredictionRecord(**record)


@app.patch("/predictions/{prediction_id}/actual-price", response_model=PredictionRecord)
async def save_actual_price_for_prediction(prediction_id: int, payload: ActualPriceUpdateRequest):
    record = update_prediction_actual_price(prediction_id, payload.actual_price)
    if record is None:
        raise HTTPException(status_code=404, detail="Vorhersage nicht gefunden")

    return PredictionRecord(**record)


@app.get("/reporting/summary", response_model=PredictionSummaryResponse)
async def get_reporting_summary(
    limit: int = Query(100, ge=1, le=1000, description="Maximale Anzahl gespeicherter Vorhersagen in der Antwort")
):
    summary = get_prediction_summary()
    items = [PredictionRecord(**record) for record in list_predictions(limit=limit)]
    return PredictionSummaryResponse(**summary, items=items)


@app.get("/database/schema", response_model=DatabaseSchemaResponse)
async def export_database_schema():
    items = [DatabaseSchemaItem(**item) for item in get_database_schema()]
    return DatabaseSchemaResponse(
        database_file=DATABASE_PATH.name,
        item_count=len(items),
        items=items,
    )