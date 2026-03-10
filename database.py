from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "predictions.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area REAL NOT NULL,
                predicted_price REAL NOT NULL,
                actual_price REAL,
                model_source TEXT NOT NULL DEFAULT 'original',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        columns = {
            row["name"]: row
            for row in connection.execute("PRAGMA table_info(predictions)").fetchall()
        }

        if "model_source" not in columns:
            connection.execute(
                """
                ALTER TABLE predictions
                ADD COLUMN model_source TEXT NOT NULL DEFAULT 'original'
                """
            )
            connection.execute(
                """
                UPDATE predictions
                SET model_source = 'original'
                WHERE model_source IS NULL OR model_source = ''
                """
            )

        if "actual_price" not in columns:
            connection.execute(
                """
                ALTER TABLE predictions
                ADD COLUMN actual_price REAL
                """
            )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS custom_model_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                algorithm_key TEXT NOT NULL,
                algorithm_label TEXT NOT NULL,
                model_variant TEXT NOT NULL DEFAULT 'original',
                model_type TEXT NOT NULL,
                task_type TEXT NOT NULL,
                model_file TEXT NOT NULL,
                metadata_file TEXT NOT NULL,
                sample_count INTEGER NOT NULL,
                training_score REAL,
                hyperparameters_json TEXT NOT NULL,
                training_samples_json TEXT NOT NULL,
                note TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        run_columns = {
            row["name"]: row
            for row in connection.execute("PRAGMA table_info(custom_model_runs)").fetchall()
        }

        if "model_variant" not in run_columns:
            connection.execute(
                """
                ALTER TABLE custom_model_runs
                ADD COLUMN model_variant TEXT NOT NULL DEFAULT 'original'
                """
            )
            connection.execute(
                """
                UPDATE custom_model_runs
                SET model_variant = 'original'
                WHERE model_variant IS NULL OR model_variant = ''
                """
            )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS custom_model_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                algorithm_key TEXT NOT NULL,
                algorithm_label TEXT NOT NULL,
                model_variant TEXT NOT NULL DEFAULT 'original',
                model_file TEXT NOT NULL,
                input_payload_json TEXT NOT NULL,
                prediction_output_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        prediction_columns = {
            row["name"]: row
            for row in connection.execute("PRAGMA table_info(custom_model_predictions)").fetchall()
        }

        if "model_variant" not in prediction_columns:
            connection.execute(
                """
                ALTER TABLE custom_model_predictions
                ADD COLUMN model_variant TEXT NOT NULL DEFAULT 'original'
                """
            )
            connection.execute(
                """
                UPDATE custom_model_predictions
                SET model_variant = 'original'
                WHERE model_variant IS NULL OR model_variant = ''
                """
            )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS custom_finetuning_samples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                algorithm_key TEXT NOT NULL,
                algorithm_label TEXT NOT NULL,
                sample_json TEXT NOT NULL,
                note TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_prediction(
    area: float,
    predicted_price: float,
    model_source: str = "original",
) -> dict[str, int | float | str]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO predictions (area, predicted_price, model_source)
            VALUES (?, ?, ?)
            """,
            (area, predicted_price, model_source),
        )
        row = connection.execute(
            """
            SELECT id, area, predicted_price, actual_price, model_source, created_at
            FROM predictions
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()

    return dict(row)


def list_predictions(limit: int = 100) -> list[dict[str, int | float | str]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, area, predicted_price, actual_price, model_source, created_at
            FROM predictions
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def get_prediction(prediction_id: int) -> dict[str, int | float | str] | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, area, predicted_price, actual_price, model_source, created_at
            FROM predictions
            WHERE id = ?
            """,
            (prediction_id,),
        ).fetchone()

    return dict(row) if row is not None else None


def get_prediction_summary() -> dict[str, int | float | str | None]:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total_predictions,
                COALESCE(SUM(CASE WHEN model_source = 'original' THEN 1 ELSE 0 END), 0) AS original_prediction_count,
                COALESCE(SUM(CASE WHEN model_source = 'finetuned' THEN 1 ELSE 0 END), 0) AS finetuned_prediction_count,
                COALESCE(SUM(CASE WHEN actual_price IS NOT NULL THEN 1 ELSE 0 END), 0) AS actual_price_count,
                MIN(area) AS min_area,
                MAX(area) AS max_area,
                AVG(area) AS avg_area,
                MIN(predicted_price) AS min_predicted_price,
                MAX(predicted_price) AS max_predicted_price,
                AVG(predicted_price) AS avg_predicted_price,
                MIN(actual_price) AS min_actual_price,
                MAX(actual_price) AS max_actual_price,
                AVG(actual_price) AS avg_actual_price,
                AVG(CASE WHEN actual_price IS NOT NULL THEN ABS(predicted_price - actual_price) END) AS avg_absolute_error,
                MIN(created_at) AS first_prediction_at,
                MAX(created_at) AS last_prediction_at
            FROM predictions
            """
        ).fetchone()

    return dict(row)


def get_database_schema() -> list[dict[str, str]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT name, type, sql
            FROM sqlite_master
            WHERE type IN ('table', 'index')
              AND name NOT LIKE 'sqlite_%'
            ORDER BY type, name
            """
        ).fetchall()

    return [dict(row) for row in rows]


def update_prediction_actual_price(
    prediction_id: int,
    actual_price: float | None,
) -> dict[str, int | float | str] | None:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE predictions
            SET actual_price = ?
            WHERE id = ?
            """,
            (actual_price, prediction_id),
        )

        if cursor.rowcount == 0:
            return None

        row = connection.execute(
            """
            SELECT id, area, predicted_price, actual_price, model_source, created_at
            FROM predictions
            WHERE id = ?
            """,
            (prediction_id,),
        ).fetchone()

    return dict(row) if row is not None else None


def save_custom_model_run(
    algorithm_key: str,
    algorithm_label: str,
    model_variant: str,
    model_type: str,
    task_type: str,
    model_file: str,
    metadata_file: str,
    sample_count: int,
    training_score: float | None,
    hyperparameters_json: str,
    training_samples_json: str,
    note: str,
) -> dict[str, int | float | str | None]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO custom_model_runs (
                algorithm_key,
                algorithm_label,
                model_variant,
                model_type,
                task_type,
                model_file,
                metadata_file,
                sample_count,
                training_score,
                hyperparameters_json,
                training_samples_json,
                note
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                algorithm_key,
                algorithm_label,
                model_variant,
                model_type,
                task_type,
                model_file,
                metadata_file,
                sample_count,
                training_score,
                hyperparameters_json,
                training_samples_json,
                note,
            ),
        )
        row = connection.execute(
            """
            SELECT *
            FROM custom_model_runs
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()

    return dict(row)


def get_latest_custom_model_run(
    algorithm_key: str,
    model_variant: str = "original",
) -> dict[str, int | float | str | None] | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT *
            FROM custom_model_runs
            WHERE algorithm_key = ?
              AND model_variant = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (algorithm_key, model_variant),
        ).fetchone()

    return dict(row) if row is not None else None


def list_custom_model_runs(
    algorithm_key: str,
    model_variant: str = "original",
    limit: int | None = None,
) -> list[dict[str, int | float | str | None]]:
    query = """
        SELECT *
        FROM custom_model_runs
        WHERE algorithm_key = ?
          AND model_variant = ?
        ORDER BY id DESC
    """
    params: list[int | str] = [algorithm_key, model_variant]

    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)

    with get_connection() as connection:
        rows = connection.execute(query, tuple(params)).fetchall()

    return [dict(row) for row in rows]


def save_custom_model_prediction(
    algorithm_key: str,
    algorithm_label: str,
    model_variant: str,
    model_file: str,
    input_payload_json: str,
    prediction_output_json: str,
) -> dict[str, int | float | str | None]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO custom_model_predictions (
                algorithm_key,
                algorithm_label,
                model_variant,
                model_file,
                input_payload_json,
                prediction_output_json
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                algorithm_key,
                algorithm_label,
                model_variant,
                model_file,
                input_payload_json,
                prediction_output_json,
            ),
        )
        row = connection.execute(
            """
            SELECT *
            FROM custom_model_predictions
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()

    return dict(row)


def save_custom_finetuning_sample(
    algorithm_key: str,
    algorithm_label: str,
    sample_json: str,
    note: str = "",
) -> dict[str, int | float | str | None]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO custom_finetuning_samples (
                algorithm_key,
                algorithm_label,
                sample_json,
                note
            )
            VALUES (?, ?, ?, ?)
            """,
            (algorithm_key, algorithm_label, sample_json, note),
        )
        row = connection.execute(
            """
            SELECT *
            FROM custom_finetuning_samples
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()

    return dict(row)


def list_custom_finetuning_samples(
    algorithm_key: str,
    limit: int | None = None,
) -> list[dict[str, int | float | str | None]]:
    query = """
        SELECT *
        FROM custom_finetuning_samples
        WHERE algorithm_key = ?
        ORDER BY id DESC
    """
    params: list[int | str] = [algorithm_key]

    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)

    with get_connection() as connection:
        rows = connection.execute(query, tuple(params)).fetchall()

    return [dict(row) for row in rows]


def delete_custom_finetuning_sample(sample_id: int) -> bool:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            DELETE FROM custom_finetuning_samples
            WHERE id = ?
            """,
            (sample_id,),
        )

    return cursor.rowcount > 0


def reset_all_runtime_data() -> None:
    initialize_database()
    with get_connection() as connection:
        connection.execute("DELETE FROM predictions")
        connection.execute("DELETE FROM custom_model_runs")
        connection.execute("DELETE FROM custom_model_predictions")
        connection.execute("DELETE FROM custom_finetuning_samples")