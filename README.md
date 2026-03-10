# Advanced ML mit SQLite-Persistenz

Wichtig: Nach einem sauberen Clone sind die Modellordner vorhanden, die meisten Modellartefakte aber noch nicht erzeugt.
Um lokal nutzbare Modelle zu erhalten, muessen Trainings- oder Finetuning-Schritte ausgefuehrt werden.

Dieses Projekt kombiniert FastAPI, SQLite, React und mehrere trainierbare scikit-learn-Modelle in einer gemeinsamen Oberflaeche.

Der Service kann:

1. einen `area`-Wert vom Benutzer empfangen
2. das trainierte Originalmodell der linearen Regression aus `trained_models/linear_regression/linear_regression_model.joblib` laden
3. den vorhergesagten Preis berechnen
4. Eingabeflaeche und vorhergesagten Preis in einer lokalen SQLite-Datenbank speichern
5. gespeicherte Vorhersagen ueber Verlauf-Endpunkte bereitstellen
6. mehrere scikit-learn-Algorithmen ueber eine Navigationsleiste umschaltbar machen
7. jeden Algorithmus mit seinem eigenen Anwendungsfall, eigenen Eingabefeldern und eigener Modelldatei trainieren
8. Trainingslaeufe und algorithmusspezifische Vorhersagen zusaetzlich in SQLite protokollieren

Wichtig fuer die lineare Regression:

- Training ueber `/ml/algorithms/linear_regression/train` erzeugt das Originalmodell `trained_models/linear_regression/linear_regression_model.joblib`
- Finetuning aus SQLite erzeugt zusaetzlich `trained_models/linear_regression/model_linear_reg_finetuned.joblib`

## Dateien

- `app.py`: FastAPI-Anwendung
- `database.py`: SQLite-Hilfsfunktionen
- `ml_algorithms/`: eigene Konfigurationsdateien pro Algorithmus fuer bessere Wartbarkeit
- `model_finetuning.py`: trainiert ein neues lineares Regressionsmodell aus gespeicherten SQLite-Zeilen mit echten Vergleichspreisen nach
- `model_artifacts.py`: persistiert und laedt Modelle ausschliesslich per `joblib`
- `model_training.py`: zentraler Service fuer Algorithmus-Registry, Validierung, Training und Vorhersage
- `requirements.txt`: Python-Abhaengigkeiten
- `predictions.db`: SQLite-Datenbankdatei, die beim Start automatisch erstellt wird
- `trained_models/`: Ausgabeverzeichnis fuer benutzerdefiniert trainierte Modelle

## Clone-Zustand des Repositories

Nach einem sauberen Clone sind die algorithmusspezifischen Modellordner bereits im Repository vorhanden, aber absichtlich noch untrainiert.

Das bedeutet:

- die Ordner unter `trained_models/` sind vorhanden
- die trainierten `.joblib`- und `.json`-Artefakte werden erst spaeter durch Training oder Finetuning erzeugt
- diese generierten Dateien sind per `.gitignore` von der Versionsverwaltung ausgeschlossen

Dadurch bleibt das Repository sauber, waehrend die benoetigte Ordnerstruktur fuer alle Algorithmen sofort nach dem Clone existiert.

## Modellartefakte nach Training

Je nach Algorithmus entstehen nach Training und Finetuning unterschiedliche Dateien unter `trained_models/`.

### Lineare Regression

- Originalmodell nach Training:
  `trained_models/linear_regression/linear_regression_model.joblib`
- Metadaten zum generischen Training:
  `trained_models/linear_regression/linear_regression_metadata.json`
- Finetuntes Modell aus SQLite:
  `trained_models/linear_regression/model_linear_reg_finetuned.joblib`
- Finetuning-Metadaten:
  `trained_models/linear_regression/model_linear_reg_finetuned_metadata.json`

### Ridge Regression

- Originalmodell nach Training:
  `trained_models/ridge_regression/ridge_regression_model.joblib`
- Trainings-Metadaten:
  `trained_models/ridge_regression/ridge_regression_metadata.json`
- Finetuntes Modell aus echten SQLite-Finetuning-Samples:
  `trained_models/ridge_regression/ridge_regression_model_finetuned.joblib`
- Finetuning-Metadaten:
  `trained_models/ridge_regression/ridge_regression_metadata_finetuned.json`

### Decision Tree Classifier

- Originalmodell nach Training:
  `trained_models/decision_tree_classifier/decision_tree_classifier_model.joblib`
- Trainings-Metadaten:
  `trained_models/decision_tree_classifier/decision_tree_classifier_metadata.json`
- Finetuntes Modell aus echten SQLite-Finetuning-Samples:
  `trained_models/decision_tree_classifier/decision_tree_classifier_model_finetuned.joblib`
- Finetuning-Metadaten:
  `trained_models/decision_tree_classifier/decision_tree_classifier_metadata_finetuned.json`

### Random Forest Classifier

- Originalmodell nach Training:
  `trained_models/random_forest_classifier/random_forest_classifier_model.joblib`
- Trainings-Metadaten:
  `trained_models/random_forest_classifier/random_forest_classifier_metadata.json`
- Finetuntes Modell aus echten SQLite-Finetuning-Samples:
  `trained_models/random_forest_classifier/random_forest_classifier_model_finetuned.joblib`
- Finetuning-Metadaten:
  `trained_models/random_forest_classifier/random_forest_classifier_metadata_finetuned.json`

### KNN Classifier

- Originalmodell nach Training:
  `trained_models/knn_classifier/knn_classifier_model.joblib`
- Trainings-Metadaten:
  `trained_models/knn_classifier/knn_classifier_metadata.json`
- Finetuntes Modell aus echten SQLite-Finetuning-Samples:
  `trained_models/knn_classifier/knn_classifier_model_finetuned.joblib`
- Finetuning-Metadaten:
  `trained_models/knn_classifier/knn_classifier_metadata_finetuned.json`

### Spam Detection

- Originalmodell nach Training:
  `trained_models/spam_detection_classifier/spam_detection_classifier_model.joblib`
- Trainings-Metadaten:
  `trained_models/spam_detection_classifier/spam_detection_classifier_metadata.json`
- Finetuntes Modell aus echten SQLite-Finetuning-Samples:
  `trained_models/spam_detection_classifier/spam_detection_classifier_model_finetuned.joblib`
- Finetuning-Metadaten:
  `trained_models/spam_detection_classifier/spam_detection_classifier_metadata_finetuned.json`

## Datenbankstruktur

Die SQLite-Datenbank enthaelt mehrere Tabellen:

### `predictions`

- `id`: eindeutiger Primaerschluessel
- `area`: Eingabeflaeche des Benutzers
- `predicted_price`: vom ML-Modell berechneter Preis
- `actual_price`: optionaler echter Vergleichspreis fuer validiertes Finetuning
- `model_source`: zeigt an, ob die Zeile vom `original`- oder `finetuned`-Modell stammt
- `created_at`: automatischer Zeitstempel der gespeicherten Vorhersage

### `custom_model_runs`

- speichert Trainingslaeufe fuer die algorithmusspezifischen Modelle
- enthaelt Algorithmusname, Modellvariante wie `original` oder `finetuned`, Modelltyp, Aufgabe, Hyperparameter, Trainingsdaten und Score

### `custom_model_predictions`

- speichert generische Vorhersagen der algorithmusspezifischen Modelle
- enthaelt Eingabepayload, Modellvariante und Vorhersageergebnis als JSON

### `custom_finetuning_samples`

- speichert echte, manuell validierte Finetuning-Datensaetze pro Algorithmus
- enthaelt die komplette Sample-Payload als JSON und optional eine Notiz zur Herkunft oder Qualitaet des Datensatzes

## Installation

Wechsle in den Projektordner und erstelle dort eine lokale virtuelle Umgebung:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Installiere anschliessend die Abhaengigkeiten mit dem Python-Interpreter der virtuellen Umgebung:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`python -m pip` ist unter Windows robuster, weil `pip` nicht in jedem Terminal direkt im `PATH` liegt.

Wenn du das gesamte Workspace-Root in VS Code geoeffnet hast, ist `${workspaceFolder}/.venv` der bevorzugte Interpreter fuer Editor, Pylance und Startkonfiguration.

## Modelle nach Clean Checkout neu erzeugen

Nach einem sauberen Clone koennen alle aktuellen Modellartefakte mit einem Befehl neu aufgebaut werden:

```powershell
python bootstrap_models.py
```

Das Skript:

- entfernt alte `.pkl`-, `.joblib`- und zugehoerige Metadateien unter `trained_models/`
- leert die SQLite-Tabellen fuer algorithmusspezifische Trainingslaeufe und Vorhersagen
- leert zusaetzlich die Tabellen `predictions` und `custom_finetuning_samples` fuer einen echten Neuaufbau
- trainiert alle Originalmodelle aus den Standard-Trainingsdaten neu
- erzeugt bewusst keine finetunten Modelle automatisch

## API starten

```powershell
python -m uvicorn app:app --reload
```

Danach oeffnen:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## React-Weboberflaeche

Im Ordner `web-ui` befindet sich ein React-Dashboard.

Es bietet eine Browser-Oberflaeche fuer:

- Vorhersagen mit dem Originalmodell
- Vorhersagen mit dem finetunten Modell
- eine obere Navigationsleiste zum Umschalten zwischen Algorithmen
- Training eines eigenen Modells mit algorithmusspezifischen Feldern
- Eingabe eigener Trainingsdaten passend zum jeweiligen Anwendungsfall des Algorithmus
- separate Vorhersageformulare passend zum ausgewaehlten Modell
- Modellvergleich
- Start des Finetunings
- Vorhersageverlauf
- Reporting-Zusammenfassung
- Inspektion des SQLite-Schemas

### React-UI starten

Oeffne ein zweites Terminal und fuehre aus:

```powershell
cd web-ui
npm install
npm run dev
```

Danach oeffnen:

- `http://127.0.0.1:5173`

Wichtig:

- der FastAPI-Server muss weiter unter `http://127.0.0.1:8000` laufen
- das Backend erlaubt bereits lokale Browser-Anfragen von Port `5173`
- falls du eine andere API-URL verwenden willst, lege in `web-ui` eine `.env`-Datei an und setze `VITE_API_BASE_URL=http://127.0.0.1:8000`

### React-UI bauen

```powershell
cd web-ui
npm run build
```

Der Produktions-Build wird nach `web-ui/dist` geschrieben.

## Verfuegbare scikit-learn-Modelle

Die Algorithmen sind jetzt nicht mehr nur Varianten derselben `area -> price`-Logik. Jeder Algorithmus hat seinen eigenen fachlichen Zweck:

- `LinearRegression`: Preisvorhersage aus `area` und `price`
- `Ridge`: Gehalts- oder Verguetungsprognose aus Berufserfahrung, Zertifikaten und Performance
- `DecisionTreeClassifier`: Genehmigungs- oder Freigabeentscheidung aus Einkommen, Schuldenquote und Kredithistorie
- `RandomForestClassifier`: Risiko- oder Fraud-Klassifikation aus Transaktions- und Kontodaten
- `KNeighborsClassifier`: Lernstands- oder Segmentklassifikation aus Lernstunden, Anwesenheit und Uebungstests
- `Spam Detection`: Mail- oder Nachrichtentexte als `spam` oder `kein_spam` klassifizieren

Fuer alle diese Modelle gilt:

- `POST /ml/algorithms/{algorithm_key}/train` erzeugt das Originalmodell plus Metadaten
- `POST /ml/algorithms/{algorithm_key}/finetuning-samples` speichert echte Finetuning-Daten in SQLite
- `POST /ml/algorithms/{algorithm_key}/finetune` erzeugt aus diesen echten Finetuning-Daten eine zweite finetunte Modellvariante plus Metadaten
- `POST /ml/algorithms/{algorithm_key}/predict` verwendet das Originalmodell
- `POST /ml/algorithms/{algorithm_key}/predict-finetuned` verwendet das finetunte Modell
- `POST /ml/algorithms/{algorithm_key}/compare-models` vergleicht beide Modellvarianten

Die Auswahl wird ueber die API und die React-Oberflaeche dynamisch bereitgestellt. Dadurch zeigt die UI je nach Algorithmus automatisch:

- den besten Einsatzzweck
- passende Trainingsfelder
- passende Vorhersagefelder
- passende Hyperparameter
- das zuletzt trainierte Modell genau dieses Algorithmus

### `GET /ml/algorithms`

Liefert den verfügbaren Algorithmus-Katalog mit:

- Anzeigename
- Modelltyp
- Task-Typ wie Regression oder Klassifikation
- Kurzbeschreibung
- Einsatzempfehlung
- Mindestanzahl an Trainingsbeispielen
- Trainingsfeldern
- Vorhersagefeldern
- Hyperparametern fuer die UI

### `GET /ml/algorithms/{algorithm_key}/model`

Liefert die Metadaten des zuletzt trainierten Modells genau fuer den gewaehlten Algorithmus.

Jeder Algorithmus hat eigene Dateien im Ordner `trained_models/...`.
Auch die lineare Regression verwendet ihr Originalmodell erst nach einem ausgefuehrten Training.

### `POST /ml/algorithms/{algorithm_key}/train`

Trainiert genau den gewaehlten Algorithmus mit:

- manuell eingegebenen Trainingsdaten
- algorithmusspezifischen Hyperparametern

Beispiel-Request:

```json
{
  "training_samples": [
    {"monthly_income": 3800, "debt_ratio": 0.18, "credit_history_years": 6, "approval_class": "genehmigt"},
    {"monthly_income": 2100, "debt_ratio": 0.44, "credit_history_years": 2, "approval_class": "pruefen"},
    {"monthly_income": 1600, "debt_ratio": 0.67, "credit_history_years": 1, "approval_class": "abgelehnt"}
  ],
  "hyperparameters": {
    "max_depth": 4,
    "min_samples_split": 2
  }
}
```

Beispielpfad:

```text
POST /ml/algorithms/decision_tree_classifier/train
```

### `POST /ml/algorithms/{algorithm_key}/predict`

Verwendet das zuletzt trainierte Modell genau dieses Algorithmus fuer eine Vorhersage.

Die Eingabeform ist ebenfalls algorithmusspezifisch.

Beispiel:

```json
{
  "prediction_input": {
    "monthly_income": 2500,
    "debt_ratio": 0.35,
    "credit_history_years": 3
  }
}
```

### `GET /ml/algorithms/{algorithm_key}/finetuned-model`

Liefert die Metadaten des zuletzt finetunten Modells fuer den gewaehlten Algorithmus.

### `GET /ml/algorithms/{algorithm_key}/finetuning-samples`

Liefert die in SQLite gespeicherten realen Finetuning-Samples fuer den gewaehlten Algorithmus.

### `POST /ml/algorithms/{algorithm_key}/finetuning-samples`

Speichert einen echten, manuell validierten Datensatz fuer spaeteres Finetuning.

### `DELETE /ml/algorithms/{algorithm_key}/finetuning-samples/{sample_id}`

Entfernt einen gespeicherten Finetuning-Datensatz wieder aus SQLite.

### `POST /ml/algorithms/{algorithm_key}/finetune`

Trainiert fuer jeden Algorithmus eine zweite Modellvariante aus bereits in SQLite gespeicherten Original-Trainingslaeufen.

Optionaler Query-Parameter:

- `limit`: maximale Anzahl an gespeicherten realen Finetuning-Samples, die fuer das Finetuning verwendet werden

Beispielpfad:

```text
POST /ml/algorithms/spam_detection_classifier/finetune?limit=10
```

Dabei werden erzeugt:

- eine finetunte Modelldatei im jeweiligen `trained_models/<algorithmus>/..._finetuned.joblib`
- eine finetunte Metadatendatei im jeweiligen `trained_models/<algorithmus>/..._finetuned.json`
- ein weiterer SQLite-Eintrag in `custom_model_runs` mit `model_variant = "finetuned"`
- die Trainingsbasis stammt aus `custom_finetuning_samples`, nicht aus alten Original-Trainingsruns

### `POST /ml/algorithms/{algorithm_key}/predict-finetuned`

Verwendet die finetunte Modellvariante genau dieses Algorithmus fuer eine Vorhersage und speichert die Ein- und Ausgabe in SQLite.

### `POST /ml/algorithms/{algorithm_key}/compare-models`

Vergleicht Original- und Finetuned-Modell fuer dieselbe Eingabe.

Die Antwort enthaelt:

- Modell-Datei des Originalmodells
- Modell-Datei des finetunten Modells
- Original-Ausgabe
- Finetuned-Ausgabe
- numerische Differenz bei Regressionsmodellen oder `null` bei Klassenlabels
- Kennzeichen, ob beide Ausgaben gleich sind
- Finetuning-Samplecount und Finetuning-Hinweis

Dieser Vergleich speichert bewusst keine zusaetzlichen Vorhersageeintraege, damit der Workflow dem bisherigen Vergleich der linearen Regression entspricht.

### `POST /predict`

Sende einen JSON-Body:

```json
{
  "area": 52
}
```

Die API berechnet den Preis und speichert das Ergebnis in SQLite.

Beispielantwort:

```json
{
  "id": 1,
  "area": 52.0,
  "predicted_price": 620.0,
  "model_source": "original",
  "created_at": "2026-03-09 10:15:30"
}
```

### `GET /predictarea/{area}`

Alternativer Endpunkt ueber Pfadparameter.

Beispiel:

```text
http://127.0.0.1:8000/predictarea/52
```

Auch dieser Endpunkt speichert die Vorhersage in der Datenbank.

### `GET /predictions`

Gibt den gespeicherten Vorhersageverlauf zurueck.

Optionaler Query-Parameter:

- `limit`: Anzahl der Zeilen, Standardwert `20`

### `GET /predictions/{prediction_id}`

Gibt eine einzelne gespeicherte Vorhersage anhand ihrer Datenbank-ID zurueck.

### `GET /reporting/summary`

Liefert einen kompakten Bericht ueber gespeicherte Vorhersagen, zum Beispiel:

- Gesamtanzahl der Vorhersagen
- Anzahl der Vorhersagen aus dem Originalmodell
- Anzahl der Vorhersagen aus dem finetunten Modell
- minimale, maximale und durchschnittliche Flaeche
- minimaler, maximaler und durchschnittlicher vorhergesagter Preis
- erster und letzter gespeicherter Zeitstempel
- gespeicherte Vorhersagezeilen mit `id`, `area`, `predicted_price`, `model_source` und `created_at`

Dieser Endpunkt ist nuetzlich fuer schnelle Auswertungen und Monitoring.

Optionaler Query-Parameter:

- `limit`: Anzahl gespeicherter Zeilen in der `items`-Liste, Standardwert `100`

### `GET /database/schema`

Exportiert das aktuelle SQLite-Schema aus der lokalen Datenbank.

Dieser Endpunkt ist nuetzlich, wenn du die Datenbankstruktur direkt in Swagger inklusive des SQL-Statements zur Tabellenerstellung pruefen willst.

### `POST /finetune-model`

Startet den Finetuning-Workflow direkt aus der API, indem gespeicherte Zeilen mit `actual_price` aus SQLite gelesen, ein neues lineares Regressionsmodell trainiert und als finetunte `joblib`-Datei gespeichert werden.

Optionaler Query-Parameter:

- `limit`: maximale Anzahl an SQLite-Zeilen fuer das Finetuning

Beispiel:

```text
POST /finetune-model?limit=50
```

### `POST /compare-models`

Vergleicht Vorhersagen des Originalmodells und des finetunten Modells fuer dieselbe Eingabeflaeche.

Request-Body:

```json
{
  "area": 120
}
```

Die Antwort enthaelt:

- Vorhersage des Originalmodells
- Vorhersage des finetunten Modells
- numerische Differenz zwischen beiden Vorhersagen
- Anzahl der Trainingsbeispiele und Hinweis aus den Finetuning-Metadaten

### `POST /predict-finetuned`

Verwendet das finetunte Modell direkt fuer eine Vorhersage.

Request-Body:

```json
{
  "area": 120
}
```

Die Antwort enthaelt die finetunte Vorhersage, den Dateinamen des finetunten Modells und die Finetuning-Metadaten.

Dieser Endpunkt speichert das Ergebnis in SQLite mit `model_source = "finetuned"`.
Der gespeicherte Verlauf zeigt dadurch eindeutig, ob eine Zeile vom Originalmodell oder vom finetunten Modell erzeugt wurde.

Die API prueft den Zeitstempel der Modelldatei bei jedem Zugriff und laedt geaenderte Artefakte automatisch neu. Dadurch bleiben auch mehrere Worker nach Training oder Finetuning synchron, ohne ein manuelles `cache_clear()`.

## Zusatzmodul fuer Modell-Finetuning

Die Datei `model_finetuning.py` kann aus der SQLite-Tabelle ein neues lineares Regressionsmodell erzeugen.

Verwendet werden:

- Eingabefeature: `area`
- Zielwert: `actual_price`

Starten mit:

```bash
python model_finetuning.py
```

Das Modul speichert:

- `trained_models/linear_regression/model_linear_reg_finetuned.joblib`
- `trained_models/linear_regression/model_linear_reg_finetuned_metadata.json`

Wichtig:

Das Finetuning verwendet nur Zeilen, in denen `actual_price` gesetzt ist.
Damit wird gegen reale Vergleichspreise trainiert statt gegen alte Modelloutputs.
Fuer mehr Stabilitaet sind mindestens fuenf validierte Zeilen erforderlich.

Wenn auch finetunte Vorhersagen in SQLite gespeichert werden, ist das fuer dieses Finetuning unkritisch, weil nur `actual_price` als Zielwert zaehlt.

## Workflow

1. FastAPI-Service starten
2. `POST /predict` oder `GET /predictarea/{area}` aufrufen
3. Die Anwendung berechnet den vorhergesagten Preis mit dem zuvor trainierten Originalmodell der linearen Regression
4. Eingabeflaeche und vorhergesagter Preis werden in `predictions.db` eingefuegt
5. optional wird spaeter fuer denselben Datensatz ein echter Vergleichspreis in `actual_price` gespeichert
6. `POST /finetune-model` trainiert ein neues Modell nur aus validierten Zeilen mit `actual_price`
5. Mit `GET /predictions` fruehere Vorhersagen pruefen
6. Mit `GET /reporting/summary` aggregierte Statistiken abrufen
7. Mit `GET /database/schema` das SQLite-Schema pruefen
8. Mit `POST /finetune-model` das Finetuning direkt aus Swagger starten
9. In der React-Navigation einen Algorithmus auswaehlen
10. Die zum Algorithmus passenden Trainingsdaten eingeben
11. Den Algorithmus ueber `/ml/algorithms/{algorithm_key}/train` trainieren
12. Das zuletzt trainierte Modell desselben Algorithmus ueber `/ml/algorithms/{algorithm_key}/model` laden
13. Optional zuerst reale Samples ueber `/ml/algorithms/{algorithm_key}/finetuning-samples` speichern und danach ueber `/ml/algorithms/{algorithm_key}/finetune` ein finetuntes Zweitmodell erzeugen
14. Das zuletzt finetunte Modell desselben Algorithmus ueber `/ml/algorithms/{algorithm_key}/finetuned-model` laden
15. Mit `/ml/algorithms/{algorithm_key}/predict` algorithmusspezifisch mit dem Originalmodell vorhersagen
16. Mit `/ml/algorithms/{algorithm_key}/predict-finetuned` mit dem finetunten Modell desselben Algorithmus vorhersagen
17. Mit `/ml/algorithms/{algorithm_key}/compare-models` Original- und finetuntes Modell vergleichen
18. Fuer die lineare Regression zusaetzlich `POST /predict-finetuned`, `POST /compare-models` und optional `python model_finetuning.py` verwenden

Dadurch entsteht ein produktionsnaeherer Workflow, weil Vorhersagen nicht mehr nur temporaer existieren, sondern spaeter erneut ausgewertet werden koennen.

## Direkter Modellzugriff in Python

Die gespeicherten Modelle sind normale scikit-learn-Objekte. Nach dem Laden in Python kann das Modell direkt abgefragt werden, ohne den FastAPI-Endpunkt zu verwenden.

Typische scikit-learn-Schnittstellen der hier verwendeten Modelle:

- `model.predict(X)`: Standardmethode fuer Regressions- und Klassifikationsvorhersagen
- `model.score(X, y)`: liefert je nach Modell den Standard-Score des Estimators
- `model.get_params()`: zeigt die aktuell gesetzten Hyperparameter
- `model.set_params(...)`: aendert Hyperparameter programmgesteuert
- `model.predict_proba(X)`: bei vielen Klassifikatoren verfuegbar, zum Beispiel Decision Tree, Random Forest oder Naive Bayes
- `model.decision_function(X)`: bei manchen Klassifikatoren verfuegbar, aber nicht bei allen in diesem Projekt
- `model.kneighbors(X)`: speziell beim `KNeighborsClassifier` verfuegbar

Beispiel fuer lineare Regression nach dem Laden:

```python
import joblib
from pathlib import Path

model_path = Path("trained_models/linear_regression/linear_regression_model.joblib")

model = joblib.load(model_path)

prediction = model.predict([[52]])
print(prediction)
print(model.get_params())
```

Beispiel fuer einen Klassifikator:

```python
import joblib
from pathlib import Path

model_path = Path("trained_models/decision_tree_classifier/decision_tree_classifier_model.joblib")

model = joblib.load(model_path)

prediction = model.predict([[2500, 0.35, 3]])
print(prediction)

if hasattr(model, "predict_proba"):
  print(model.predict_proba([[2500, 0.35, 3]]))
```

Wichtig:

- Die Eingabe fuer `predict(...)` muss zur Feature-Reihenfolge des jeweiligen Algorithmus passen.
- Bei Textmodellen wie Spam Detection wird kein Zahlenvektor per Hand uebergeben, sondern der gespeicherte Pipeline-Estimator direkt mit Text aufgerufen.

Beispiel fuer Spam Detection:

```python
import joblib
from pathlib import Path

model_path = Path("trained_models/spam_detection_classifier/spam_detection_classifier_model.joblib")

model = joblib.load(model_path)

prediction = model.predict(["Kostenlos gewinnen, jetzt klicken!"])
print(prediction)
```