import FieldInput from '../common/FieldInput'
import ResultCard from '../common/ResultCard'
import { formatNumber, formatTimestamp } from '../common/formatters'

function AlgorithmWorkspace({
  selectedAlgorithm,
  algorithmHyperparameters,
  trainingSamples,
  algorithmPredictionInput,
  selectedAlgorithmModel,
  selectedAlgorithmFinetunedModel,
  loadingMap,
  customTrainingResult,
  customPredictResult,
  onHyperparameterChange,
  onTrainingSampleChange,
  onAddTrainingSample,
  onRemoveTrainingSample,
  onPredictionInputChange,
  onApplyPredictionExample,
  onTrain,
  onPredict,
}) {
  return (
    <section className="card wide-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Algorithmus-Workspace</p>
          <h2>Ausgewaehlten Algorithmus trainieren, verstehen und nutzen</h2>
        </div>
      </div>

      {selectedAlgorithm ? (
        <div className="training-layout">
          <div className="training-config">
            <article className="algorithm-card">
              <span className="schema-type">{selectedAlgorithm.task_type}</span>
              <h3>{selectedAlgorithm.label}</h3>
              <p className="scenario-name">Szenario: {selectedAlgorithm.scenario_name}</p>
              <p>{selectedAlgorithm.summary}</p>
              <p className="muted-copy">Am besten geeignet fuer: {selectedAlgorithm.best_for}</p>
              <div className="algorithm-meta-grid">
                <div>
                  <strong>Modelltyp</strong>
                  <p>{selectedAlgorithm.model_type}</p>
                </div>
                <div>
                  <strong>Min. Trainingsdaten</strong>
                  <p>{selectedAlgorithm.min_samples}</p>
                </div>
              </div>
              <div className="scenario-example-box">
                <strong>Beispiel-Trainingsszenarien</strong>
                <ul className="scenario-example-list">
                  {selectedAlgorithm.scenario_examples.map((example) => (
                    <li key={example}>{example}</li>
                  ))}
                </ul>
              </div>
            </article>

            {selectedAlgorithm.hyperparameters.length > 0 && (
              <div className="parameter-grid">
                {selectedAlgorithm.hyperparameters.map((parameter) => (
                  <label key={parameter.name}>
                    {parameter.label}
                    <FieldInput
                      field={parameter}
                      value={algorithmHyperparameters[parameter.name] ?? parameter.default ?? ''}
                      onChange={(value) => onHyperparameterChange(parameter.name, value)}
                      isHyperparameter
                    />
                    <span className="field-help">{parameter.description}</span>
                  </label>
                ))}
              </div>
            )}
          </div>

          <form className="tool-form training-form" onSubmit={onTrain}>
            <div className="section-heading inline-controls">
              <div>
                <h3>Trainingsdaten fuer {selectedAlgorithm.label}</h3>
                <p className="muted-copy">
                  Die Eingabefelder richten sich nach dem Einsatz dieses Algorithmus. Nur die Lineare Regression nutzt hier Quadratmeter und Preis.
                </p>
              </div>
              <button type="button" className="secondary-button" onClick={onAddTrainingSample}>
                Zeile hinzufuegen
              </button>
            </div>

            <div className="training-sample-list">
              {trainingSamples.map((sample, index) => (
                <div key={`sample-${index}`} className="training-sample-row">
                  {selectedAlgorithm.training_fields.map((field) => (
                    <label key={`${field.name}-${index}`}>
                      {field.label}
                      <FieldInput
                        field={field}
                        value={sample[field.name] ?? ''}
                        onChange={(value) => onTrainingSampleChange(index, field.name, value)}
                      />
                    </label>
                  ))}
                  <button
                    type="button"
                    className="secondary-button"
                    onClick={() => onRemoveTrainingSample(index)}
                    disabled={trainingSamples.length <= 1}
                  >
                    Entfernen
                  </button>
                </div>
              ))}
            </div>

            <button type="submit" disabled={loadingMap['custom-train']}>
              {loadingMap['custom-train'] ? 'Trainiere...' : `${selectedAlgorithm.label} trainieren`}
            </button>

            {customTrainingResult && <ResultCard title="Letztes Training" data={customTrainingResult} />}
          </form>

          <div className="training-side-panel">
            <article className="algorithm-card">
              <span className="schema-type">Aktives Modell</span>
              {selectedAlgorithmModel?.trained ? (
                <>
                  <h3>{selectedAlgorithmModel.algorithm_label}</h3>
                  <p>Modelltyp: {selectedAlgorithmModel.model_type}</p>
                  <p>Task-Typ: {selectedAlgorithmModel.task_type}</p>
                  <p>Samples: {selectedAlgorithmModel.sample_count}</p>
                  <p>Training Score: {formatNumber(selectedAlgorithmModel.training_score)}</p>
                  <p>Trainiert am: {formatTimestamp(selectedAlgorithmModel.trained_at)}</p>
                  <p className="muted-copy">{selectedAlgorithmModel.note}</p>
                </>
              ) : (
                <>
                  <h3>Noch kein Modell fuer {selectedAlgorithm.label}</h3>
                  <p className="muted-copy">
                    {selectedAlgorithmModel?.note ?? 'Trainiere zuerst genau diesen Algorithmus. Die Modell- und Metadateien werden getrennt abgelegt.'}
                  </p>
                </>
              )}
            </article>

            <article className="algorithm-card">
              <span className="schema-type">Finetuntes Modell</span>
              {selectedAlgorithmFinetunedModel?.trained ? (
                <>
                  <h3>{selectedAlgorithmFinetunedModel.algorithm_label}</h3>
                  <p>Modelltyp: {selectedAlgorithmFinetunedModel.model_type}</p>
                  <p>Task-Typ: {selectedAlgorithmFinetunedModel.task_type}</p>
                  <p>Samples: {selectedAlgorithmFinetunedModel.sample_count}</p>
                  <p>Training Score: {formatNumber(selectedAlgorithmFinetunedModel.training_score)}</p>
                  <p>Trainiert am: {formatTimestamp(selectedAlgorithmFinetunedModel.trained_at)}</p>
                  <p className="muted-copy">{selectedAlgorithmFinetunedModel.note}</p>
                </>
              ) : (
                <>
                  <h3>Noch kein finetuntes Modell fuer {selectedAlgorithm.label}</h3>
                  <p className="muted-copy">
                    {selectedAlgorithmFinetunedModel?.note ?? 'Starte das Finetuning aus SQLite, um eine zweite Modellvariante fuer den Vergleich zu erzeugen.'}
                  </p>
                </>
              )}
            </article>

            <form className="tool-form compact-form" onSubmit={onPredict}>
              <h3>Vorhersage mit {selectedAlgorithm.label}</h3>
              {selectedAlgorithm.prediction_examples?.length > 0 && (
                <div className="example-grid">
                  {selectedAlgorithm.prediction_examples.map((example) => (
                    <button
                      key={example.label}
                      type="button"
                      className="example-card"
                      onClick={() => onApplyPredictionExample(example)}
                    >
                      <strong>{example.label}</strong>
                      <span>{example.description}</span>
                    </button>
                  ))}
                </div>
              )}
              {selectedAlgorithm.prediction_fields.map((field) => (
                <label key={field.name}>
                  {field.label}
                  <FieldInput
                    field={field}
                    value={algorithmPredictionInput[field.name] ?? ''}
                    onChange={(value) => onPredictionInputChange(field.name, value)}
                  />
                </label>
              ))}
              {!selectedAlgorithmModel?.trained && (
                <p className="muted-copy">
                  Dieses Modell muss zuerst trainiert werden. Danach ist die Vorhersage sofort verfuegbar.
                </p>
              )}
              <button type="submit" disabled={loadingMap['custom-predict'] || !selectedAlgorithmModel?.trained}>
                {loadingMap['custom-predict']
                  ? 'Berechne...'
                  : selectedAlgorithmModel?.trained
                    ? 'Vorhersage ausfuehren'
                    : 'Zuerst trainieren'}
              </button>
              {customPredictResult && <ResultCard title="Letzte Algorithmus-Vorhersage" data={customPredictResult} />}
            </form>
          </div>
        </div>
      ) : (
        <p className="muted-copy">Algorithmus-Daten werden geladen.</p>
      )}
    </section>
  )
}

export default AlgorithmWorkspace