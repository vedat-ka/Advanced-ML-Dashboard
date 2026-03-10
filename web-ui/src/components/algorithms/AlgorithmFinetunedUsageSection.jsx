import FieldInput from '../common/FieldInput'
import ResultCard from '../common/ResultCard'

function AlgorithmFinetunedUsageSection({
  selectedAlgorithm,
  algorithmPredictionInput,
  selectedAlgorithmFinetunedModel,
  loadingMap,
  customFinetunedPredictResult,
  customCompareResult,
  onPredictionInputChange,
  onApplyPredictionExample,
  onFinetunedPredict,
  onCompare,
}) {
  return (
    <section className="card wide-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Finetuntes Modell nutzen</p>
          <h2>Finetuned-Vorhersage und Vergleich fuer {selectedAlgorithm.label}</h2>
        </div>
      </div>

      <div className="forms-grid">
        <form className="tool-form" onSubmit={onFinetunedPredict}>
          <h3>Vorhersage mit finetuntem Modell</h3>
          {selectedAlgorithm.prediction_examples?.length > 0 && (
            <div className="example-grid">
              {selectedAlgorithm.prediction_examples.map((example) => (
                <button
                  key={`finetuned-${example.label}`}
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
            <label key={`finetuned-${field.name}`}>
              {field.label}
              <FieldInput
                field={field}
                value={algorithmPredictionInput[field.name] ?? ''}
                onChange={(value) => onPredictionInputChange(field.name, value)}
              />
            </label>
          ))}
          {!selectedAlgorithmFinetunedModel?.trained && (
            <p className="muted-copy">
              Speichere zuerst reale Finetuning-Samples und starte dann das Finetuning.
            </p>
          )}
          <button
            type="submit"
            disabled={loadingMap['custom-predict-finetuned'] || !selectedAlgorithmFinetunedModel?.trained}
          >
            {loadingMap['custom-predict-finetuned']
              ? 'Berechne...'
              : selectedAlgorithmFinetunedModel?.trained
                ? 'Mit finetuntem Modell vorhersagen'
                : 'Zuerst finetunen'}
          </button>
          {customFinetunedPredictResult && (
            <ResultCard title="Letzte Vorhersage finetuntes Modell" data={customFinetunedPredictResult} />
          )}
        </form>

        <form className="tool-form" onSubmit={onCompare}>
          <h3>Original vs. Finetuned vergleichen</h3>
          {selectedAlgorithm.prediction_examples?.length > 0 && (
            <div className="example-grid">
              {selectedAlgorithm.prediction_examples.map((example) => (
                <button
                  key={`compare-${example.label}`}
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
            <label key={`compare-${field.name}`}>
              {field.label}
              <FieldInput
                field={field}
                value={algorithmPredictionInput[field.name] ?? ''}
                onChange={(value) => onPredictionInputChange(field.name, value)}
              />
            </label>
          ))}
          <button type="submit" disabled={loadingMap['custom-compare'] || !selectedAlgorithmFinetunedModel?.trained}>
            {loadingMap['custom-compare']
              ? 'Vergleiche...'
              : selectedAlgorithmFinetunedModel?.trained
                ? 'Modelle vergleichen'
                : 'Zuerst finetunen'}
          </button>
          {customCompareResult && <ResultCard title="Vergleich Original vs. Finetuned" data={customCompareResult} />}
        </form>
      </div>
    </section>
  )
}

export default AlgorithmFinetunedUsageSection