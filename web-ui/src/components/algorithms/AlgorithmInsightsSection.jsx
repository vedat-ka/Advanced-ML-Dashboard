import SummaryItem from '../common/SummaryItem'
import { formatNumber, formatTimestamp } from '../common/formatters'

function AlgorithmInsightsSection({ selectedAlgorithm, selectedAlgorithmModel, selectedAlgorithmFinetunedModel, trainingSamples }) {
  return (
    <>
      <section className="card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Algorithmus-Daten</p>
            <h2>Modellstatus und letzte Trainingsdaten</h2>
          </div>
        </div>

        {selectedAlgorithmModel?.trained ? (
          <dl className="summary-grid">
            <SummaryItem label="Szenario" value={selectedAlgorithm?.scenario_name ?? '-'} />
            <SummaryItem label="Task-Typ" value={selectedAlgorithmModel.task_type} />
            <SummaryItem label="Modelltyp" value={selectedAlgorithmModel.model_type} />
            <SummaryItem label="Sample Count" value={formatNumber(selectedAlgorithmModel.sample_count)} />
            <SummaryItem label="Training Score" value={formatNumber(selectedAlgorithmModel.training_score)} />
            <SummaryItem label="Trainiert am" value={formatTimestamp(selectedAlgorithmModel.trained_at)} />
            <SummaryItem label="Finetuned Samples" value={formatNumber(selectedAlgorithmFinetunedModel?.sample_count)} />
            <SummaryItem label="Finetuned Score" value={formatNumber(selectedAlgorithmFinetunedModel?.training_score)} />
          </dl>
        ) : (
          <p className="muted-copy">
            Fuer diesen Algorithmus sind noch keine SQLite-Preisreports sichtbar, weil hier stattdessen algorithmusspezifische Trainingsdaten verwendet werden.
          </p>
        )}
      </section>

      <section className="card wide-card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Spezifische Trainingsdaten</p>
            <h2>Aktuelle Beispieldaten fuer {selectedAlgorithm?.label}</h2>
          </div>
        </div>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                {selectedAlgorithm?.training_fields.map((field) => (
                  <th key={field.name}>{field.label}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {(selectedAlgorithmModel?.training_samples ?? trainingSamples).map((sample, index) => (
                <tr key={`specific-sample-${index}`}>
                  {selectedAlgorithm?.training_fields.map((field) => (
                    <td key={`${field.name}-${index}`}>{String(sample[field.name] ?? '-')}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="card wide-card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Modell-Details</p>
            <h2>Hyperparameter und Modellinformationen</h2>
          </div>
        </div>

        {selectedAlgorithmModel?.trained ? (
          <div className="schema-grid">
            <article className="schema-card">
              <span className="schema-type">Hyperparameter</span>
              <pre>{JSON.stringify(selectedAlgorithmModel.hyperparameters, null, 2)}</pre>
            </article>
            <article className="schema-card">
              <span className="schema-type">Modell-Details</span>
              <pre>{JSON.stringify(selectedAlgorithmModel.model_details, null, 2)}</pre>
            </article>
          </div>
        ) : (
          <p className="muted-copy">Trainiere zuerst dieses Modell, um spezifische Modellinformationen anzuzeigen.</p>
        )}
      </section>
    </>
  )
}

export default AlgorithmInsightsSection